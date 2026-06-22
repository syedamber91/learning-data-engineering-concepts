---
title: "Idempotency"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [idempotency, data-pipelines, reliability, upserts, exactly-once]
---

# Idempotency

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

## In one line

An idempotent operation always produces the same result, no matter how many times you run it — so running it once is identical to running it ten times.

## Picture this

Imagine you press the button to call an elevator. Pressing it once makes the elevator come. Pressing it five more times in frustration does not send five elevators — you still get exactly one. The button is **idempotent**: the outcome is the same regardless of how many times you press it.

Now contrast that with a vending machine that charges your card every time you tap it. Tap it six times and you get charged six times. That is **not** idempotent — each extra run adds a new effect.

Data pipeline steps work exactly the same way. Some steps are "vending machines" (dangerous to repeat). Idempotency is the engineering discipline of turning them into "elevator buttons" (safe to repeat).

## How it actually works

When a data pipeline runs, things go wrong. Networks drop. Servers crash. A nightly job that started at 2 a.m. might die at 2:47 a.m. and restart automatically at 3 a.m. The question is: when it restarts, does it leave the data in a consistent state, or does it create chaos?

A non-idempotent step blindly **appends** new data every time it runs. Restart it after a half-finished run and you get duplicates, doubled totals, or corrupted records.

An idempotent step instead **overwrites or merges** using a stable, deterministic key — a unique identifier that was always going to be the same for that record (for example: `order_id`, a date + store combination, or a hash of the source row). The mechanism looks like this:

1. **Compute a deterministic key** for each record. The key must not change between runs — it is derived from the data itself, not from "when the job ran."
2. **Use an upsert** (short for "update or insert"): if a row with that key already exists, update it to the new value; if it does not exist yet, insert it. Either way, after the operation the table contains exactly one row per key, with the correct values.
3. **Optionally delete-then-reload** a bounded partition (e.g., all rows for `date = 2026-06-22`) before writing, which is another pattern that guarantees a clean slate.

The result: run the step once, twice, or a hundred times — the final table looks identical every time.

## Worked example

Suppose you have a pipeline that loads daily order totals from a source system into a `daily_sales` table. Each row represents one store's total for one day.

**Non-idempotent version (dangerous):**

```sql
-- Runs every morning. If it retries, it inserts duplicate rows.
INSERT INTO daily_sales (store_id, sale_date, total_usd)
VALUES (42, '2026-06-22', 15000.00);
```

Run this twice on the same day and you get two rows for store 42 on 2026-06-22, giving a false total of $30,000.

**Idempotent version (safe):**

```sql
-- PostgreSQL upsert: insert or update if the key already exists.
INSERT INTO daily_sales (store_id, sale_date, total_usd)
VALUES (42, '2026-06-22', 15000.00)
ON CONFLICT (store_id, sale_date)
DO UPDATE SET total_usd = EXCLUDED.total_usd;
```

Here `(store_id, sale_date)` is the deterministic key. Run this ten times: store 42 on 2026-06-22 still shows exactly $15,000. The retry is completely safe.

In Python with a pipeline framework the same logic might look like:

```python
def load_daily_sales(store_id: int, sale_date: str, total_usd: float, conn):
    conn.execute("""
        INSERT INTO daily_sales (store_id, sale_date, total_usd)
        VALUES (%s, %s, %s)
        ON CONFLICT (store_id, sale_date)
        DO UPDATE SET total_usd = EXCLUDED.total_usd
    """, (store_id, sale_date, total_usd))
```

Call this function once or a thousand times — the table ends up in the same correct state.

## In the real world

Consider an e-commerce company running a nightly Airflow pipeline that aggregates the previous day's orders and writes them into a reporting database. The pipeline runs at midnight and usually finishes by 1 a.m.

One night the database connection drops at 12:47 a.m. after writing 80% of the rows. Airflow automatically retries the task at 1 a.m. Because every write step uses upserts keyed on `(order_id, partition_date)`, the retry simply overwrites the 80% already written (no harm done) and finishes the remaining 20%. By 1:20 a.m. the table is perfectly correct — no duplicates, no missing rows, no manual intervention required.

Without idempotency, the on-call engineer gets paged at 1 a.m. to manually delete the partial data and re-run the job by hand. Multiply that by dozens of pipelines and you have a fragile, sleepless data team.

## Common misconceptions

**People think "idempotent" means "runs only once."**
Actually, it means the opposite: it is *designed* to be run any number of times safely. The word describes a property of the operation, not how often it executes.

**People think retrying a failed step is always harmless.**
Actually, retrying is only harmless if the step was deliberately designed to be idempotent. A naive `INSERT` that appends rows becomes more wrong with every retry. Safety must be built in — it is not the default.

**People think idempotency is a database-only concern.**
Actually, it applies everywhere: API calls (calling a payment processor twice charges the customer twice unless the API uses an idempotency key), file writes (appending to a log vs. overwriting it), and even cache invalidation. Anywhere an action has a side effect, idempotency is relevant.

## How it relates & differs

| Concept | How it relates | How it differs |
|---|---|---|
| [[batch-vs-streaming\|Batch vs Streaming]] | Batch jobs process whole time windows and are commonly retried or backfilled; idempotency is what makes those re-runs safe | Batch vs Streaming is about *when* data is processed; idempotency is about *how* each step is designed to handle repetition |
| [[dags-schedulers\|DAGs & Schedulers]] | Schedulers like Airflow automatically retry failed tasks; idempotency is the guarantee that makes automatic retries trustworthy | DAGs & Schedulers define *what runs and when*; idempotency defines *whether running it again is safe* |
| [[data-quality-validation\|Data Quality & Validation]] | Idempotent pipelines prevent duplicates and partial writes, which are major data quality failures | Data Quality & Validation *detects* problems after the fact; idempotency *prevents* a class of problems by design |

## Why you'd use it (and when not to)

You should design for idempotency any time a pipeline step can fail and be retried — which is almost always. The cost is small (choose the right key, use upserts or partition-replace patterns) and the reliability gain is enormous: you can re-run any step, backfill historical dates, or recover from outages without manual cleanup. The main trade-off is that you need a reliable, stable key for each record; if no natural key exists you have to engineer a synthetic one (e.g., a hash of the source fields), which adds a little complexity. The only situations where idempotency is genuinely hard to achieve are truly stateful, order-dependent operations — for example, dispensing physical cash from an ATM — but in software data pipelines those cases are rare and should be flagged explicitly rather than ignored.

## Check yourself

**Memory hook:** "Idempotent = elevator button. Press it once or press it ten times — you still get one elevator."

**Q1: What is a deterministic key and why does idempotency depend on one?**
A deterministic key is a unique identifier computed from the data itself (not from the clock or a random number), so it is the same value every time the job runs for the same logical record. Idempotency depends on it because the upsert needs to know which existing row to overwrite; without a stable key you cannot safely merge, only blindly append.

**Q2: A pipeline inserts 1,000 rows, crashes, and restarts. After the restart it inserts the same 1,000 rows again. The table now has 2,000 rows. Is this step idempotent? What would fix it?**
No, it is not idempotent — a correct idempotent run would leave exactly 1,000 rows. The fix is to replace the plain `INSERT` with an upsert (`INSERT ... ON CONFLICT DO UPDATE`) keyed on a natural unique column, or to delete the partition before reloading it.

**Q3: Why is idempotency called "critical for exactly-once semantics"?**
"Exactly-once" means each logical record ends up in the output exactly one time, even if the pipeline runs more than once. Idempotency achieves this: because re-running overwrites rather than appends, the result is always as if the step ran exactly once, even if it actually ran several times.

## Connects to

[[batch-vs-streaming|Batch vs Streaming]] · [[dags-schedulers|DAGs & Schedulers]] · [[data-quality-validation|Data Quality & Validation]] · [[transactions-acid|Transactions & ACID]]