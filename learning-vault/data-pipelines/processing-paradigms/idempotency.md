---
title: "Idempotency"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [idempotency, data-pipelines, fault-tolerance, upserts, retries, exactly-once]
---

# Idempotency

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

← Prev: [[batch-vs-streaming|Batch vs Streaming]] · Next: [[dags-schedulers|DAGs & Schedulers]] →

## Recap — where we just were

In [[batch-vs-streaming|Batch vs Streaming]] you learned that pipelines either collect data in big chunks and process them on a schedule, or handle each event the instant it arrives. Either way, one uncomfortable question looms: *what happens if the pipeline crashes halfway through?* You have two choices — skip the remaining work and lose data, or re-run from the beginning and risk processing some rows twice. Idempotency is the design principle that makes the second option safe.

---

## Level 1 — The big idea

An **idempotent** operation is one where running it once produces exactly the same result as running it ten times.

The word comes from Latin *idem* (same) + *potens* (powerful). Same power, same result, no matter how many repetitions.

**Everyday analogy — a "PAID" stamp:**
When an accountant stamps an invoice "PAID", it doesn't matter if they stamp it once or accidentally five times. The invoice is still just *PAID* — not *PAID PAID PAID PAID PAID*. The stamp is idempotent.

A *non-idempotent* instruction would be "ADD $100 TO BALANCE". Run it five times by accident and you've added $500 instead of $100. That is the exact bug idempotency prevents in data pipelines.

<!-- mermaid-source:
graph LR
    A[Pipeline Step] -->|Run 1 time| B[Result: 500 rows]
    A -->|Run 5 times| B
    A -->|Run 100 times| B
-->
![[idempotency-d1.svg]]

The key insight: **safe to retry = safe to operate at scale.** Crashes, network blips, and scheduler restarts happen constantly in production. Idempotency turns "re-run after failure" from a dangerous gamble into a reliable strategy.

---

## Level 2 — How it actually works

Now that you have the intuition, let's look at the two concrete techniques that make a step idempotent.

### Technique 1 — Deterministic keys

Every event or row needs a **deterministic key**: an ID that is *computed from the event's content*, not generated randomly at write time. If the same event arrives twice, it produces the same key — and the database recognises the second arrival as a duplicate.

For example: a payment event carries a `payment_id` supplied by the payment gateway. Whether your pipeline processes that event once or three times, `payment_id` is always identical. The database sees the same key and knows it already has this row.

Without a deterministic key, each retry might call `uuid()` to generate a fresh ID, resulting in a new duplicate row every single time.

### Technique 2 — Upserts

An **upsert** (UPDATE + INSERT merged) tells the database: *"If a row with this key already exists, update it. If not, insert it."* Either way, the end state is one row with correct values — whether the step ran once or fifty times.

<!-- mermaid-source:
graph TD
    E[Event arrives - possibly a retry] --> K[Compute deterministic key]
    K --> U{Row with this key already exists?}
    U -->|Yes| UP[UPDATE - overwrite with same values]
    U -->|No| IN[INSERT new row]
    UP --> R[Final state: exactly one row with correct values]
    IN --> R
-->
![[idempotency-d2.svg]]

Together, deterministic keys + upserts produce a pipeline where *re-running always converges on the same final state*.

### The crash-and-retry scenario made concrete

Imagine a nightly batch job processing 1,000,000 rows. At row 700,001 the server loses power. Without idempotency you face a dilemma: skip the remaining 300,000 rows (missing data) or re-run from scratch (the first 700,000 rows get processed twice, inflating totals). With idempotency, re-running is safe — the first 700,000 upserts find existing rows and overwrite them with identical values; the remaining 300,000 rows are inserted fresh. The table ends in exactly the right state.

<!-- mermaid-source:
sequenceDiagram
    participant Job as Batch Job
    participant DB as Database
    Job->>DB: Upsert payment_id=001 amount=50.00
    Job->>DB: Upsert payment_id=002 amount=75.00
    Note over Job: Server crashes at row 700001
    Job->>DB: Upsert payment_id=001 amount=50.00
    Note over DB: Key exists - UPDATE with identical value
    Job->>DB: Upsert payment_id=002 amount=75.00
    Note over DB: Key exists - UPDATE with identical value
    Job->>DB: Upsert payment_id=700001 amount=99.00
    Note over DB: New key - INSERT
-->
![[idempotency-d3.svg]]

The database lands in the same clean state as if the crash never happened.

---

## Level 3 — See it with real numbers

**Scenario:** your e-commerce pipeline loads daily revenue into a `daily_revenue` table. The nightly job crashed at 2 AM and you need to re-run it safely against 500,000 rows.

**Table structure:**

| order_date | product_id | total_revenue |
|---|---|---|
| 2026-06-21 | 42 | 9 999.00 |
| 2026-06-21 | 17 | 4 500.00 |

The **composite key** `(order_date, product_id)` is deterministic — derived from the data itself.

**Without idempotency (dangerous):**

```sql
-- Non-idempotent: running twice inserts duplicate rows
INSERT INTO daily_revenue (order_date, product_id, total_revenue)
VALUES ('2026-06-21', 42, 9999.00);

-- Run again after crash → two rows for the same date + product → totals doubled
```

**With idempotency (safe to run any number of times):**

```sql
INSERT INTO daily_revenue (order_date, product_id, total_revenue)
VALUES ('2026-06-21', 42, 9999.00)
ON CONFLICT (order_date, product_id)
DO UPDATE SET total_revenue = EXCLUDED.total_revenue;
```

Run once → one row, `total_revenue = 9999.00`.
Run again after crash → same key found → row updated with `total_revenue = 9999.00` (unchanged).
Run a third time → same outcome. One row, correct value, always.

**In Python (a streaming consumer handling retries):**

```python
def process_payment_event(event, db):
    # payment_id comes from the gateway - stable, not generated here
    payment_id = event["payment_id"]

    db.execute("""
        INSERT INTO payments (payment_id, amount, status)
        VALUES (%s, %s, %s)
        ON CONFLICT (payment_id)
        DO UPDATE SET amount = EXCLUDED.amount,
                      status = EXCLUDED.status
    """, (payment_id, event["amount"], event["status"]))
    # Calling this 10 times with the same event → 1 row, same values
```

Input: `{"payment_id": "pay_001", "amount": 50.00, "status": "completed"}`
After 1 call: 1 row in `payments`.
After 10 calls: still 1 row, same values. Zero duplicates.

---

## Level 4 — In the real world & common traps

**Real-world use case — Spotify's daily royalty pipeline**

Every day, Spotify aggregates billions of play events into a `daily_plays` table used to calculate royalties for artists. If the nightly Spark job crashes at 3 AM and must restart, *every cent of royalty calculation must come out exactly the same*. Paying an artist twice because of a retry would be a legal and financial disaster.

Spotify's pipeline uses a composite deterministic key `(track_id, date)` with upserts. The job can crash and restart as many times as needed — the final table always reflects one play per event, because duplicates are silently overwritten with identical values rather than stacked on top. **Backfills** — reprocessing six months of historical data to fix a bug — also rely entirely on idempotency: engineers re-run every day's job from scratch, confident the output will be correct and duplicate-free.

**Common misconceptions**

**People think: "Just delete and re-insert to avoid duplicates."**
Actually: DELETE followed by INSERT is *two* operations. If the pipeline crashes between them, the row is gone and never re-inserted — you now have *missing* data, which is often worse than a duplicate. An upsert is a single atomic operation that cannot be half-executed.

**People think: "Idempotency means rows are never touched twice."**
Actually: idempotent steps *do* touch the same rows on retry — they just produce the same result each time. A row might be updated ten times with the same value. The *outcome* is stable, not the number of operations.

**People think: "Streaming systems handle duplicate events automatically."**
Actually: most message queues (including **Apache Kafka** in its default configuration) guarantee **at-least-once delivery** — meaning a message *may* be delivered more than once. The stream *processor* must implement idempotency itself using deterministic keys and upserts. The queue only guarantees delivery, not duplicate-safe processing.

---

## Level 5 — Expert view

### How idempotency relates to and differs from neighbouring concepts

| Concept | What it guarantees | Where the guarantee lives |
|---|---|---|
| **Idempotency** | Re-running the same step produces the same result | In your pipeline code and write logic |
| **Exactly-once semantics** | Each event is processed exactly one time, end to end | In the messaging infrastructure itself |
| **At-least-once delivery** | Every event is delivered, but possibly multiple times | In the message queue |
| **Transactions & ACID** | A group of writes either all succeed or all fail atomically | In the database engine |

**Idempotency vs. exactly-once semantics:** they solve the same user-visible problem from different directions. **Exactly-once** tries to prevent duplicates from ever entering the system; idempotency ensures that if duplicates *do* enter, they cause no harm on the way out. In practice, idempotency is easier to implement and more portable — it works regardless of which message queue, cloud provider, or database you use. Exactly-once guarantees are expensive, fragile, and sometimes unavailable in distributed systems.

**Idempotency vs. [[transactions-acid|Transactions & ACID]]:** ACID is a complement, not a substitute. A transaction guarantees that your upsert either fully completes or fully rolls back within *one* run — it says nothing about what happens if you run the same upsert again tomorrow. You need *both*: ACID for consistency within a single execution, idempotency for safety across multiple executions.

**Idempotency and [[data-quality-validation|Data Quality & Validation]]:** validation is the verification layer on top. After a re-run, a quality check confirms that row counts and revenue totals match expectations, catching any case where idempotency broke down — for example, if a key collision caused silent data loss.

### Trade-offs and edge cases

**When idempotency is easy:** the source system provides a stable, unique ID (`payment_id`, `order_id`). Use it as the conflict key. Done.

**When idempotency is hard:** the source provides no unique ID (raw sensor readings with identical timestamps, for example). You must synthesise a key by hashing the event content — and you must be certain two genuinely *different* readings never hash to the same value. A collision causes silent data loss with no error message.

**Performance cost:** upserts are slightly slower than plain inserts because the database must check for an existing row before writing. On a 100-million-row table, this index lookup adds measurable latency. Engineers sometimes pre-sort and deduplicate events in application memory before writing, reducing the number of conflict checks the database must perform.

**Scope of the guarantee:** some pipelines are idempotent *within* a single day's data but not across days — the key is `(date, product_id)`, so re-running a different date's job is safe, but supplying the wrong date parameter could overwrite correct historical data. The scope of your deterministic key defines the scope of your safety guarantee. Know the boundary.

---

## Check yourself

**Memory hook:** *"A PAID stamp is idempotent — press it once or a hundred times, the invoice is still just PAID."*

**Q1: What two techniques combine to make a pipeline step idempotent?**
A: Deterministic keys (an ID derived from the data itself, not randomly generated at write time) and upserts (`INSERT … ON CONFLICT DO UPDATE`), so that re-running produces the same final state.

**Q2: Why is DELETE-then-INSERT not a safe substitute for an upsert?**
A: DELETE and INSERT are two separate operations. If the pipeline crashes between them, the row is permanently gone. An upsert is a single atomic operation — it either completes fully or not at all, with no gap in between.

**Q3: If your message queue guarantees at-least-once delivery, is your pipeline automatically idempotent?**
A: No. At-least-once delivery means duplicate events *will* arrive. Your pipeline must handle them with idempotent writes; the queue only promises delivery, not duplicate-safe processing.

---

## Connects to

[[batch-vs-streaming|Batch vs Streaming]] · [[transactions-acid|Transactions & ACID]] · [[data-quality-validation|Data Quality & Validation]] · [[dags-schedulers|DAGs & Schedulers]]

---

## Coming up next

[[dags-schedulers|DAGs & Schedulers]] — now that your individual pipeline steps are safe to retry, you need a system to *sequence* and *schedule* them in the right order; DAGs encode those dependencies as a directed graph, and schedulers are the engines that walk that graph and fire each step at the right time.