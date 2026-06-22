---
title: "Data Quality & Validation"
area: "Data Pipelines"
topic: "Orchestration"
tags: [data-quality, validation, orchestration, data-pipelines, pipeline-reliability, fail-fast]
---

# Data Quality & Validation

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

## In one line
Data quality checks are automated tests that inspect incoming data for completeness, correctness, and freshness before anything downstream is allowed to trust it.

## Picture this
Imagine a conveyor belt at a chocolate factory. Before the chocolates are boxed and shipped to stores, a quality-control inspector checks each tray: Are any chocolates missing? Are they the right shape? Did they arrive at the right temperature? If a whole tray fails, it gets pulled off the line right there — not discovered by an angry customer later.

Data quality validation is that inspector. The "chocolates" are rows of data. The "store" is a dashboard, a machine-learning model, or a business report. The inspector sits at the entrance to your pipeline and refuses to let bad batches through.

## How it actually works

Every time new data arrives — say, a file of today's customer orders — your pipeline runs a set of checks before doing anything else. Think of these as a short to-do list for the inspector.

**1. Null checks — "Is anything missing?"**
A null is a blank field, like an order row with no `customer_id`. If downstream code tries to join that row to a customer table, it silently fails or produces wrong results. The check asks: does this column have a value in every row where we expect one?

**2. Range and type checks — "Does the value make sense?"**
A negative `order_amount` or a `birth_year` of 1850 might be technically non-null, but they are almost certainly wrong. Range checks enforce business rules: prices must be positive, percentages must be between 0 and 100, dates can't be in the future.

**3. Uniqueness checks — "Is this a duplicate?"**
If `order_id` should be unique (one row per order), finding two rows with the same ID means either the source system double-fired an event or the pipeline ran twice. A uniqueness check catches that before it inflates revenue numbers.

**4. Freshness checks — "Is the data recent enough?"**
A dataset can pass every other check and still be useless if it is three days old when you expected it updated an hour ago. Freshness checks look at a `loaded_at` timestamp or the `MAX(event_date)` in the table and ask: did new data actually arrive? A pipeline that silently stops feeding data — but reports "success" — is one of the sneakiest failure modes in data engineering.

**5. Volume / anomaly checks — "Does the row count look sane?"**
If yesterday's batch had 80,000 rows and today's has 12, something is probably wrong upstream. A simple threshold ("row count must be within 20% of the 7-day average") catches source-system outages before they become silent data gaps.

When a check fails, the pipeline should **fail fast**: stop immediately, alert someone, and refuse to load broken data. The cost of one failed pipeline run is small. The cost of three months of dashboards built on bad data is enormous.

## Worked example

Suppose you receive a daily CSV of e-commerce orders and load it into a staging table called `stg_orders`. You run these checks before promoting the data to production:

```sql
-- 1. Null check: customer_id must never be null
SELECT COUNT(*) AS null_customer_ids
FROM stg_orders
WHERE customer_id IS NULL;
-- Expected: 0  |  Found: 47  →  FAIL

-- 2. Range check: order_amount must be positive and < $50,000
SELECT COUNT(*) AS bad_amounts
FROM stg_orders
WHERE order_amount <= 0 OR order_amount > 50000;
-- Expected: 0  |  Found: 3  →  FAIL

-- 3. Uniqueness check: order_id must be unique
SELECT COUNT(*) - COUNT(DISTINCT order_id) AS duplicates
FROM stg_orders;
-- Expected: 0  |  Found: 0  →  PASS

-- 4. Freshness check: at least one order in the last 25 hours
SELECT MAX(order_created_at) AS latest_order
FROM stg_orders;
-- Expected: within 25 hours of NOW()
-- Found: 2026-06-21 03:00 UTC  →  FAIL (data is stale)

-- 5. Volume check: today vs. 7-day average
-- 7-day avg = 62,000 rows; today = 9,800  →  FAIL (84% drop)
```

Three out of five checks fail. The pipeline halts, sends an alert to the on-call engineer, and does **not** write any data to the production `orders` table. The analyst's morning dashboard is delayed — but it shows yesterday's correct data instead of today's broken data. That is the right outcome.

## In the real world

An online retailer runs a nightly pipeline that loads orders from their transaction database into a data warehouse. The finance team's revenue dashboard reads from that warehouse every morning at 08:00.

In 2023, a bug in their payment processor briefly wrote `order_amount = 0` for all orders processed between 02:00 and 04:00. Without a range check, those zero-dollar orders would have made it into the warehouse, and the CFO would have seen overnight revenue drop by 40% — triggering a company-wide panic.

With a range check (`order_amount > 0`), the pipeline caught 1,200 bad rows at 03:15, halted, and paged the data engineering team. The bug was reported to the payment vendor by 04:00. The pipeline re-ran with corrected data at 06:30, and the dashboard showed accurate numbers at 08:00. No panic, no bad decisions made on bad numbers.

## Common misconceptions

**People think: "Data from our own internal systems is always clean."**
Actually: Internal systems break, change schemas, and produce duplicates just as often as external feeds. A software deploy can silently change the format of a timestamp field overnight. Always validate, even from sources you own and trust.

**People think: "Freshness is just a nice-to-have — correctness is what matters."**
Actually: Stale data that passes every correctness check is still wrong for its purpose. If your inventory pipeline hasn't updated since yesterday, a customer placing an order today might buy stock that is already sold out. Freshness is a full dimension of quality, not a bonus feature.

**People think: "Once data passes validation at ingestion, it stays valid forever."**
Actually: Downstream transformations can introduce new nulls, duplicates, or out-of-range values. A bad JOIN can multiply rows and inflate counts. A `COALESCE` can replace a meaningful null with a misleading zero. Quality checks belong at every stage of the pipeline, not just the entrance.

## How it relates & differs

| Concept | How it RELATES | How it DIFFERS |
|---|---|---|
| [[dags-schedulers\|DAGs & Schedulers]] | Validation tasks are nodes in the DAG; the scheduler runs them in dependency order and halts every downstream task if a check node fails. | DAGs are about *orchestrating* tasks. Quality checks are the *content* of specific tasks — the DAG doesn't care what a node does, only whether it succeeds or fails. |
| [[transactions-acid\|Transactions & ACID]] | Both protect systems from bad data reaching production. ACID ensures a write is all-or-nothing at the database level. | ACID guarantees that a write either fully happens or fully doesn't — it says nothing about whether the *values* written are correct. A transaction can successfully commit 1,000 rows of nonsense. Quality checks catch the nonsense *before* the write. |
| [[idempotency\|Idempotency]] | Idempotent pipelines (safe to re-run without side effects) pair naturally with quality checks: when a check fails and the source data is fixed, you can re-run from scratch without fear of double-counting. | Idempotency is about the *behavior of re-runs*. Quality validation is about the *correctness of input data*. They are complementary tools, not the same concept. |

## Why you'd use it (and when not to)

Use data quality validation whenever incorrect or missing data would cause a downstream decision, report, or model to be wrong — which is nearly always. The cost is low (SQL queries are cheap; a five-check suite adds seconds to a pipeline) and the protection is high.

The one situation to be careful: overly strict thresholds in a **streaming** context can reject valid-but-unusual data in real time, creating customer-facing errors. In streaming pipelines, consider routing suspect records to a quarantine topic for human review rather than hard-failing the entire stream. Calibrate thresholds with historical data, and revisit them when the business changes (a flash sale will legitimately spike your row counts).

## Check yourself

**Memory hook:** *"Check before you wreck"* — validate data at entry so broken values never reach production.

**Q1: What is the difference between a null check and a range check?**
A null check asks whether a value exists at all (the field isn't blank). A range check assumes the value exists and asks whether it falls within acceptable bounds — for example, confirming that a price is greater than zero.

**Q2: Why is freshness considered a quality dimension and not just a scheduling concern?**
Because data that is technically correct but hours or days old can cause wrong decisions. Showing yesterday's stock levels to today's customers, or yesterday's revenue figures in this morning's board meeting, is a quality failure even if every value in the table is individually accurate. Freshness tells you whether the data is *current enough* to be trusted for its intended use.

**Q3: If a quality check fails, what should a well-designed pipeline do?**
Fail fast: stop immediately, refuse to write any data downstream, and alert the on-call engineer with enough detail (which check failed, how many rows were affected, what the threshold was) to diagnose the problem quickly. Never silently pass broken data through.

## Connects to

[[dags-schedulers|DAGs & Schedulers]] · [[idempotency|Idempotency]] · [[transactions-acid|Transactions & ACID]] · [[batch-vs-streaming|Batch vs Streaming]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]