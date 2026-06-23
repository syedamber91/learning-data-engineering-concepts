---
title: "Data Quality & Validation"
area: "Data Pipelines"
topic: "Orchestration"
tags: [data-quality, validation, freshness, null-checks, pipelines, orchestration]
---

# Data Quality & Validation

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

← Prev: [[dags-schedulers|DAGs & Schedulers]] · Next: [[what-dbt-is-the-t-in-elt|What dbt Is & the T in ELT]] →

## Recap — where we just were

In [[dags-schedulers|DAGs & Schedulers]] you gave your pipeline a brain: a dependency map that the scheduler reads to fire tasks in the right order, run independent steps in parallel, and retry failures automatically. Your pipeline now knows *what* to run and *when* — but it never asks the one question that matters most: *is the data it is about to process actually correct?* That is exactly the job of data quality validation.

---

## Level 1 — The big idea

**Data quality validation** means running a set of automated checks on incoming data *before* the pipeline trusts it and passes it downstream.

**Everyday analogy:** A school cafeteria receives 500 lunch boxes every morning. Before handing them out, a staff member checks: is every box labelled with a name? Is every box dated *today*, not last week? Are there any duplicate labels? If one box fails a check, it is pulled aside *before* it reaches a student — not discovered later when someone bites into a week-old sandwich.

The pipeline equivalent is a **validation gate** — a task that sits right after raw data arrives and before any expensive transformation begins:

<!-- mermaid-source:
graph LR
    A[Raw Data Arrives] --> B[Validate]
    B -->|All checks pass| C[Transform]
    C --> D[Load to Warehouse]
    B -->|Any check fails| E[Alert and Stop]
-->
![[data-quality-validation-d1.svg]]

Two things to notice immediately: validation happens *before* transformation (cheap to stop early), and on failure the pipeline *stops entirely* rather than silently continuing. That second point is called **fail fast**, and it is the single most important rule in data quality engineering.

---

## Level 2 — How it actually works

Now that you have the picture, let's look at the four kinds of checks that together catch most of what goes wrong with real data. Each one is a specific question you ask before trusting a batch.

### 1. Completeness — null checks

A **null** is a database value meaning "absent" or "unknown." If a sales record has no `order_id`, you cannot link it to anything else — it is useless, and any JOIN on that column will silently corrupt your results. A null check asks: *are required fields present in every row?*

### 2. Validity — range checks

Even when a value exists, it might be nonsense: a price of −$7, a customer age of 900, a rating of 47 out of 5. A **range check** asks: *are values within the expected bounds?* The bounds are defined by the data engineer based on what the business actually allows: "prices must be between $0.01 and $9,999."

### 3. Uniqueness — duplicate checks

Primary keys must be unique — you saw why in [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]. If two rows share the same `order_id`, every downstream JOIN on that key silently doubles counts. A **uniqueness check** counts how many IDs appear more than once; the expected answer is always zero.

### 4. Freshness — time checks

This one surprises beginners. **Freshness** asks: *is the newest record recent enough to be useful?* If your pipeline should load data every six hours but the newest row is 30 hours old, the upstream job silently failed — and your dashboard is showing yesterday's numbers while users believe they are looking at live data. Stale data is just as dangerous as wrong data because the mistake is *invisible*.

**All four checks act as parallel gates before the data is trusted:**

<!-- mermaid-source:
graph TD
    A[Incoming Batch] --> B[Null Check]
    A --> C[Range Check]
    A --> D[Uniqueness Check]
    A --> E[Freshness Check]
    B --> F{All passed?}
    C --> F
    D --> F
    E --> F
    F -->|Yes| G[Data is trusted - proceed]
    F -->|No| H[Fail fast - alert and stop]
-->
![[data-quality-validation-d2.svg]]

Notice how this connects back to [[dags-schedulers|DAGs & Schedulers]]: the validation task is just one node in your DAG. When it fails, the scheduler automatically blocks every downstream task — you do not need to write any extra logic. The DAG's dependency structure does the propagation for you.

<!-- mermaid-source:
sequenceDiagram
    participant S as Scheduler
    participant V as Validate Task
    participant T as Transform Task
    participant L as Load Task
    S->>V: Run
    V-->>S: FAILED - range check 312 bad rows
    S->>T: Blocked upstream failed
    S->>L: Blocked upstream failed
    S->>S: Fire on-call alert
-->
![[data-quality-validation-d3.svg]]

---

## Level 3 — See it with real numbers

**Scenario:** an e-commerce company loads 500,000 order rows into a staging table every night at 2 AM. Four SQL checks run before any transformation touches the data.

| Check | What it queries | Pass condition |
|---|---|---|
| Null check | rows where `order_id IS NULL` | count = 0 |
| Range check | rows where `revenue <= 0 OR revenue > 9999` | count = 0 |
| Uniqueness check | `order_id` values appearing more than once | 0 rows returned |
| Freshness check | newest `created_at` value | within the last 26 hours |

```sql
-- Check 1: No null order IDs
SELECT COUNT(*) AS null_count
FROM staging_orders
WHERE order_id IS NULL;
-- Pass: null_count = 0

-- Check 2: Revenue within expected bounds
SELECT COUNT(*) AS bad_revenue_count
FROM staging_orders
WHERE revenue <= 0 OR revenue > 9999;
-- Pass: bad_revenue_count = 0

-- Check 3: No duplicate order IDs
SELECT order_id, COUNT(*) AS cnt
FROM staging_orders
GROUP BY order_id
HAVING cnt > 1;
-- Pass: 0 rows returned

-- Check 4: Data is fresh
SELECT CASE
    WHEN MAX(created_at) >= NOW() - INTERVAL '26 hours'
    THEN 'PASS'
    ELSE 'FAIL'
END AS freshness_status
FROM staging_orders;
-- Pass: freshness_status = 'PASS'
```

And here is the Python task that runs these checks inside Airflow and fails fast on the first problem:

```python
from datetime import datetime, timedelta

def validate_orders(conn):
    row_checks = [
        ("Null check",
         "SELECT COUNT(*) FROM staging_orders WHERE order_id IS NULL"),
        ("Range check",
         "SELECT COUNT(*) FROM staging_orders WHERE revenue <= 0 OR revenue > 9999"),
        ("Uniqueness check",
         "SELECT COUNT(*) FROM (SELECT order_id FROM staging_orders "
         "GROUP BY order_id HAVING COUNT(*) > 1) t"),
    ]
    for name, sql in row_checks:
        count = conn.execute(sql).fetchone()[0]
        if count > 0:
            raise ValueError(f"{name} FAILED: {count} offending rows found")

    newest = conn.execute(
        "SELECT MAX(created_at) FROM staging_orders"
    ).fetchone()[0]
    if newest < datetime.utcnow() - timedelta(hours=26):
        raise ValueError(f"Freshness check FAILED: newest record is {newest}")

    print("All checks passed — 500,000 rows are trusted")
```

**What happens on night 47 when an application bug inserts `revenue = -1.00` for 312 orders?** The range check returns 312 (not zero), `validate_orders` raises a `ValueError`, the Airflow task turns red, the scheduler blocks every downstream task, and an alert fires in Slack — before a single bad number reaches the warehouse. Catching it cost one SQL query. Missing it could mean a week of corrupted revenue reports.

---

## Level 4 — In the real world & common traps

**Real-world use case — artist royalty pipelines at a music streaming company:**

A streaming service processes hundreds of millions of play events per day. Before crediting an artist's stream count — which directly determines royalty payments — the pipeline runs quality checks: is `track_id` present on every event? Is `duration_ms` a positive integer under 3,600,000 (one hour — no single play can last longer)? Has the expected volume of events arrived in the last hour? A false zero caused by a missed freshness check costs the company hours of manual investigation. A falsely inflated count caused by duplicate events costs an artist real money. Both outcomes are prevented by the same four checks you just saw.

**Common misconceptions:**

**People think: "Our data comes from our own production database — it must be correct."**
Actually: application bugs, schema migrations, failed ETL retries, manual data-entry errors, and timezone mismatches all corrupt data in internal databases constantly. The source being internal gives you no immunity. Every data team eventually uncovers a months-long bad-data streak that nobody caught because the checks were not there.

**People think: "Freshness is an ops concern, not a data quality concern."**
Actually: stale data is incorrect data — it just fails along the time dimension rather than the value dimension. If your daily sales dashboard silently shows numbers from 30 hours ago, every business decision made from it is based on false information, even if every individual row is arithmetically perfect. Freshness is a first-class quality dimension.

**People think: "Running checks on 500,000 rows will make the pipeline too slow."**
Actually: the four SQL checks above run in seconds on any modern columnar data warehouse (BigQuery, Redshift, Snowflake) because they are simple aggregations over one table with no joins. The cost of *skipping* the checks — a corrupted warehouse that takes days to diagnose and rebuild — is orders of magnitude higher than a five-second validation step.

---

## Level 5 — Expert view

Now that you have seen data quality in action, it is worth placing it precisely on the map of everything you have already studied — because three neighbouring concepts are easy to confuse with it.

| | Data Quality Validation | [[transactions-acid\|Transactions & ACID]] | [[idempotency\|Idempotency]] |
|---|---|---|---|
| **What it guards** | Correctness of incoming data | Correctness of writes to the DB | Safety of re-running a task |
| **When it fires** | After ingestion, before processing | During the write itself | On every retry |
| **Who writes the rules** | Data engineers, in pipeline code | DB engine or application layer | Task authors |
| **What failure looks like** | Pipeline stops; alert fires | Write is rolled back automatically | Duplicate side-effect (if missing) |
| **Scope** | An entire arriving batch | One atomic transaction | One task execution |

**Key insight:** [[transactions-acid|Transactions & ACID]] is the database engine's promise that *writes it accepts* are internally consistent. Data quality validation is the pipeline engineer's gate that *data arriving at the system* is worth accepting in the first place. They guard different layers: ACID is inside the database; quality validation lives at the boundary where external data enters your pipeline.

**Trade-offs to know:**

*How strict to be?* Zero tolerance for any out-of-range row is the safest starting point, but it halts the pipeline over a single malformed record. Many teams relax specific thresholds once they have historical data showing what "normal noise" looks like: "allow up to 0.01 % null `product_id` values in ad-click events, because the ad-serving system occasionally omits it legitimately." The key rule: document every relaxed threshold and revisit it quarterly.

*Blocking vs. warning?* Failing fast and blocking the pipeline is the default for production data that other teams query. For exploratory or low-stakes pipelines, you may choose to *warn* — log the issue, send a Slack alert, but let the pipeline continue with clean rows only. This is a deliberate trade-off, not a shortcut.

*Checks at every stage?* Ideally you validate after extraction (first touch of raw data), after each major transformation, and before loading into any table other teams query. Over-checking wastes scheduler time; under-checking lets errors propagate. A practical starting rule: always validate after extraction and always validate before loading to a shared table.

**Scale nuance:** On five billion rows, a `GROUP BY ... HAVING COUNT(*) > 1` uniqueness check can take minutes. Teams at that scale either sample the data (check a random 10 % of rows — fast and usually sufficient) or use probabilistic data structures like **Bloom filters** or **HyperLogLog** to estimate uniqueness without a full scan, trading absolute certainty for acceptable speed. Sampling introduces a small risk of missing low-frequency duplicates; the right choice depends on how costly a missed duplicate actually is.

---

## Check yourself

**Memory hook:** *Garbage In, Garbage Out — catch it at the gate, not at the plate.*

**Q1: What does "fail fast" mean in a data pipeline, and why is it safer than letting the pipeline continue when a check fails?**
A: Fail fast means stopping the pipeline the moment any quality check fails. It is safer because bad data that continues flows into transformation steps, gets loaded into the warehouse, and gets queried by dashboards — spreading the error and making the root cause harder to trace. Stopping early contains the damage to the staging table, where it is easy to identify and fix.

**Q2: Your daily pipeline loads sales data on a 6-hour schedule. The newest record in the staging table is 36 hours old and your freshness threshold is 26 hours. What should happen, and why?**
A: The freshness check should fail and the pipeline should stop. If it continued, it would re-transform the same old data already in the warehouse and overwrite correct downstream tables with stale numbers. The alert tells the engineer to investigate why the upstream source stopped delivering — which is the real problem to fix.

**Q3: Why does a null check on `order_id` need to pass *before* you run a JOIN between the orders table and the products table?**
A: A JOIN matches rows using the key column. Rows where `order_id` is null have no key to match on — they are either silently dropped (INNER JOIN) or produce rows full of nulls (LEFT JOIN). Either outcome corrupts the joined result. Confirming every `order_id` is present guarantees every row participates correctly before the join runs.

---

## Connects to

[[dags-schedulers|DAGs & Schedulers]] · [[idempotency|Idempotency]] · [[transactions-acid|Transactions & ACID]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[batch-vs-streaming|Batch vs Streaming]]

---

## Coming up next

So far you have *moved*, *scheduled*, and *guarded* data — but you have not yet *transformed* it into the clean, analytics-ready tables that dashboards actually read. That is the job of a whole tool built around the ideas in this lesson. Up next, [[what-dbt-is-the-t-in-elt|What dbt Is & the T in ELT]] opens the dbt roadmap (see [[dbt-data-build-tool-moc|dbt (Data Build Tool)]]), where the same "fail fast on bad data" discipline you just learned becomes a first-class, version-controlled part of building every table.