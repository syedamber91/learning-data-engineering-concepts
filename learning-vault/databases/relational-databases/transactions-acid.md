---
title: "Transactions & ACID"
area: "Databases"
topic: "Relational Databases"
tags: [transactions, acid, sql, relational-databases, data-integrity, databases]
---

# Transactions & ACID

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

← Prev: [[indexing|Indexing]] · Next: [[star-schema|Star Schema]] →

## Recap — where we just were

In [[indexing|Indexing]] you discovered how a B-tree lets the database leap to a matching row in O(log n) steps instead of scanning every row — turning a 100-second query into a sub-millisecond one. Now that the database can *find* data fast, a harder question surfaces: what happens when two updates must land together, or the server crashes halfway through a change? That is the problem transactions were built to solve.

---

## Level 1 — The Big Idea

A **transaction** is a wrapper that groups two or more database changes into a single all-or-nothing unit. Either every change inside the wrapper succeeds and gets saved permanently, or — if anything goes wrong — every change is erased as if it never happened.

**Everyday analogy:** Think of tapping your card at a checkout. The cashier scans every item, your card is charged, and the store's stock count drops by one. That whole sequence is one transaction. If your card is declined after items are scanned, nothing is taken — the store doesn't keep your money *and* put items back on the shelf, nor does it take your money without handing anything over. It is all-or-nothing.

**ACID** is the four-letter acronym for the specific guarantees a transactional database makes to ensure your data stays correct:

| Letter | Word | Plain meaning |
|--------|------|---------------|
| A | Atomic | All steps happen, or none do |
| C | Consistent | Declared rules (constraints) are never broken |
| I | Isolated | Parallel transactions can't see each other's unfinished work |
| D | Durable | Once saved, data survives a power cut |

<!-- mermaid-source:
graph TD
    Start[BEGIN transaction] --> S1[Step 1 - Debit Alice]
    S1 --> S2[Step 2 - Credit Bob]
    S2 --> OK{All steps OK?}
    OK -- Yes --> Commit[COMMIT - both changes saved]
    OK -- No --> Rollback[ROLLBACK - both changes erased]
-->
![[transactions-acid-d1.svg]]

The key insight: a transaction draws a boundary around work so the database never gets stuck in a half-done state.

---

## Level 2 — How it Actually Works

Now that you have the picture, let's climb inside each letter and see the real mechanism.

### A — Atomicity: the all-or-nothing guarantee

When you issue `BEGIN`, the database starts tracking every change you make. It does this by writing to an **undo log** — a record of every "before" image of each row you touch. If you reach `COMMIT`, all changes are written to permanent storage. If anything fails before that — a network cut, a disk error, your own `ROLLBACK` command — the engine replays the undo log backwards and restores every row to its pre-`BEGIN` state.

<!-- mermaid-source:
sequenceDiagram
    participant App as Application
    participant DB as Database Engine
    participant UL as Undo Log

    App->>DB: BEGIN
    App->>DB: UPDATE accounts - debit Alice 200
    DB->>UL: Save Alice old balance 1000
    App->>DB: UPDATE accounts - credit Bob 200
    DB->>UL: Save Bob old balance 500
    App->>DB: COMMIT
    DB-->>App: OK - both changes permanent
    Note over UL: Undo log no longer needed
-->
![[transactions-acid-d2.svg]]

If a crash happens anywhere before COMMIT, the database uses the undo log on restart to revert both rows — Alice goes back to $1,000, Bob stays at $500. No half-state survives.

### C — Consistency: constraints always hold

Consistency means the database only moves from one *valid* state to another. "Valid" is defined by the rules you declared: `NOT NULL`, foreign keys, `CHECK` constraints, `UNIQUE` constraints. If an update would break a rule, the entire transaction is rejected. Note carefully: the database enforces the rules *you wrote down*. If you forgot to add `CHECK (balance >= 0)`, the database will happily allow a negative balance. Consistency guards declared rules, not your business logic.

### I — Isolation: parallel work stays private

Dozens of users may hit your database at the same moment. Without isolation, User A could read Bob's balance *while* User B is mid-update — catching a half-written value. Isolation levels control how much concurrent transactions can see of each other. From weakest to strongest:

**Read Uncommitted → Read Committed → Repeatable Read → Serializable**

Most databases default to **Read Committed**: you only ever see data that another transaction has already committed. The database implements this by holding a short lock on rows being written, making readers wait the milliseconds until the writer commits or rolls back.

<!-- mermaid-source:
graph LR
    TxA[Tx A - reading Bob balance] -- waits for lock --> DB[(Database)]
    TxB[Tx B - updating Bob balance uncommitted] -- holds lock --> DB
    DB -- releases lock on COMMIT --> TxA
-->
![[transactions-acid-d3.svg]]

### D — Durability: commits survive crashes

Once you receive a `COMMIT OK`, the data is safe even if the power dies one millisecond later. Databases achieve this with a **write-ahead log (WAL)**: before touching the actual data file, the engine appends the change to a sequential log on disk. Sequential writes are fast. On restart after a crash, the WAL is replayed to recover any committed changes that hadn't yet reached the main data file.

<!-- mermaid-source:
graph LR
    App[Application] -- COMMIT --> WAL[Write-Ahead Log - disk]
    WAL -- async flush --> Data[Main Data File - disk]
    WAL -- replay on crash --> Data
    App -- gets OK immediately after WAL write --> App
-->
![[transactions-acid-d4.svg]]

---

## Level 3 — See it with Real Numbers

**Scenario:** A peer-to-peer payment app. Alice has $1,000; Bob has $500. Alice sends Bob $200. That single "send" action requires exactly two SQL updates.

**Without a transaction — the danger:**

```sql
-- Step 1 executes
UPDATE accounts SET balance = balance - 200 WHERE name = 'Alice';
-- Alice: 1000 -> 800 (saved to disk)

-- Server crashes HERE before Step 2 runs

UPDATE accounts SET balance = balance + 200 WHERE name = 'Bob';
-- Bob: never updated, still 500
```

After the crash: Alice has $800, Bob has $500. $200 has vanished permanently. The data is broken.

**With a transaction — the safe version:**

```sql
BEGIN;

-- Step 1: debit Alice
UPDATE accounts SET balance = balance - 200 WHERE name = 'Alice';
-- Alice row updated in memory only (not yet committed)

-- Step 2: credit Bob
UPDATE accounts SET balance = balance + 200 WHERE name = 'Bob';
-- Bob row updated in memory only (not yet committed)

COMMIT;
-- NOW both rows are written permanently.
-- Alice = 800, Bob = 700, total = 1300 (unchanged from before: 1000+500=1500 -> 800+700=1500)
```

**Triggering a deliberate rollback** (Alice tries to overdraw):

```sql
BEGIN;

UPDATE accounts SET balance = balance - 2000 WHERE name = 'Alice';
-- Would take Alice to -1000, violating CHECK (balance >= 0)

ROLLBACK;
-- Alice's balance snaps back to 1000. Nothing was saved.
```

**Verify the plan with EXPLAIN:**

```sql
EXPLAIN (ANALYZE) UPDATE accounts SET balance = balance - 200 WHERE name = 'Alice';
-- Shows cost, rows touched, whether an index was used — useful for auditing
-- expensive transactions before they run on production data.
```

The total money in the system ($1,300) is identical before and after the successful commit. That equality is the consistency guarantee — no money created, none destroyed.

---

## Level 4 — In the Real World & Common Traps

### Real-world use case: last-seat race at a cinema booking site

A cinema has one seat left for a sold-out Saturday showing. Two users click "Buy" at the exact same millisecond. Without isolation, both users read "1 seat available," both pass the availability check, and both pay — the same seat sold twice, two angry customers, one refund nightmare.

With a properly isolated transaction, the second user's `UPDATE seats SET sold = TRUE WHERE seat_id = 42` finds the row already locked by the first transaction and waits. When the first user's transaction commits (seat now sold), the second user's transaction re-reads the row, finds `sold = TRUE`, and returns "Sorry, just sold out." One seat, one sale. That is isolation protecting real revenue and real trust.

This pattern appears identically in: hotel room booking, airline ticketing, flash-sale inventory, coupon code redemption — any system where a limited resource must be allocated exactly once under concurrent load.

### Common misconceptions

**People think: "Transactions are only for banking or fintech apps."**
Actually: Any time two or more writes must land together — creating a user record *and* inserting a default settings row, placing an order *and* decrementing stock, logging an event *and* updating a counter — you need a transaction. The bank transfer is the most dramatic version of a universal pattern.

**People think: "ACID is free — just wrap everything in BEGIN/COMMIT and you're safe."**
Actually: Isolation has a real cost. Holding locks while a transaction is open blocks every other transaction trying to touch those same rows. A transaction open for 30 seconds on a hot row creates a queue of stalled queries — a condition called **lock contention** — and can make your application feel frozen. Keep transactions as short as possible: open late, commit early.

**People think: "Consistent means the data is correct."**
Actually: Consistent means the database's *declared* rules — NOT NULL, foreign keys, CHECK constraints, UNIQUE constraints — are not violated. If your business rule is "a product's stock level can never go negative" but you forgot the CHECK constraint, the database will happily write −5. Consistency enforces the rules you wrote down, not the rules you thought about.

---

## Level 5 — Expert View

### How Transactions & ACID relate to neighbouring concepts

| Concept | What it shares with Transactions | How it differs |
|---|---|---|
| [[indexing\|Indexing]] | Both are internal database mechanisms | Indexes are about *speed* — finding rows fast; transactions are about *correctness* — changing rows safely. Orthogonal: a table can have great indexes and no transaction safety, or vice versa |
| [[idempotency\|Idempotency]] | Both guard against bad states from repeated or partial operations | Idempotency is a property of the *caller* — "run me twice, same result"; a transaction is a guarantee of the *database* — "run my steps atomically once." They complement each other in pipeline design |
| [[batch-vs-streaming\|Batch vs Streaming]] | Both appear heavily in data pipelines | In batch pipelines you can wrap an entire file load in one large transaction; in streaming, micro-transactions per event are common but isolation levels are often relaxed to **Read Committed** or weaker for throughput |

### Trade-offs

**Use a transaction** any time you touch more than one row or more than one table and both changes must be inseparable.

**Be careful** with long-running transactions on frequently-updated rows. Lock contention compounds fast: 10 users each holding a lock for 2 seconds means the 11th user waits up to 20 seconds.

**Serializable isolation** makes all concurrent transactions behave as if they ran strictly one at a time. It is the safest but slowest isolation level; the database must detect and resolve conflicts called **serialization anomalies**. Most production OLTP systems use **Read Committed** and design their writes carefully to avoid the gaps.

**Distributed transactions** — spanning two separate databases or microservices — are dramatically harder. A **two-phase commit** protocol exists but is slow and failure-prone. Modern architectures often prefer eventual consistency patterns (sagas, outbox pattern) as a deliberate trade-off, accepting temporary inconsistency in exchange for availability. That trade-off is real, not free.

---

## Check Yourself

**Memory hook:** *"ACID stops the database mid-sentence."* — Atomic (complete sentence or nothing), Consistent (grammar rules hold), Isolated (no one reads your draft), Durable (once published, it stays).

**Q1: What is the difference between ROLLBACK and COMMIT?**
COMMIT permanently saves all changes made inside the transaction to disk. ROLLBACK discards every change, returning each touched row to the exact state it was in before BEGIN.

**Q2: Why does isolation matter if only one user is active?**
With a single user, isolation has no effect — there is nothing to isolate from. Isolation only matters the moment two or more transactions run concurrently and could read each other's half-written data.

**Q3: Why can a long-running transaction hurt performance even if it eventually commits successfully?**
While a transaction is open it holds locks on the rows it has modified. Other transactions needing those rows must wait. A transaction open for 30 seconds on a busy table can queue dozens of other queries, stalling the entire application — even though the data will eventually be correct.

---

## Connects to

[[indexing|Indexing]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[big-o-time-complexity|Big-O / Time Complexity]] · [[idempotency|Idempotency]] · [[batch-vs-streaming|Batch vs Streaming]] · [[data-quality-validation|Data Quality & Validation]]

---

## Coming up next

[[star-schema|Star Schema]] — now that you know how a relational database keeps individual writes safe and correct, the next lesson zooms out to the *shape* of an entire database designed for analysis: a star schema, where one central fact table radiates out to surrounding dimension tables, making complex questions across millions of rows fast and easy to ask.