---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia, two-phase-locking, deadlock, predicate-locks]
sources:
  - raw/ch07.md
---
# Two-Phase Locking (2PL)
> The classic pessimistic route to serializability: readers block writers and writers block readers, with all locks held until commit — extended by predicate/index-range locks to kill phantoms.

## The Idea
For roughly three decades 2PL was the *only* widely used serializability algorithm. It strengthens the write locks already used against dirty writes: any potential race means someone waits. Not to be confused with [[Two-Phase Commit]] (2PC), a distributed atomic-commit protocol — despite the similar name they are unrelated.

## How It Works
Each object has a lock with **shared** and **exclusive** modes:
- Reading requires the shared lock; many readers may hold it together, but not while anyone holds exclusive.
- Writing requires the exclusive lock; it excludes all other holders, shared or exclusive.
- A transaction that read then writes upgrades shared → exclusive.
- Locks are held to the end of the transaction — the two phases are *acquire* (while running) and *release* (at commit/abort). (Strictly: strong strict 2PL, SS2PL.)

So if A read an object, a writer B waits for A to finish; if A wrote it, a reader B waits too — the exact inverse of snapshot isolation's "readers never block writers." **Deadlocks** (A waits on B, B waits on A) become common; the database detects them and aborts a victim, which the application must retry.

**Predicate locks — closing the phantom hole.** Serializability demands preventing phantoms ([[Write Skew and Phantoms]]). A predicate lock attaches not to a row but to *all objects matching a search condition* — including rows that don't exist yet. Readers take a shared predicate lock on their query condition; any insert/update/delete must first check whether its old or new value matches someone's predicate lock and wait if so.

**Index-range (next-key) locks.** Matching every write against every predicate is too slow, so real systems approximate: widen the predicate to something attachable to an index entry — lock "room 123 at any time" on the room_id index, or a time range on a time index. Coarser than necessary but cheap; any conflicting write hits the same index region and blocks. With no usable index, fall back to locking the whole table.

## Trade-offs & Pitfalls
Performance is why 2PL never conquered the world: locking overhead plus drastically reduced concurrency. Unbounded queueing behind long transactions makes latency unstable and terrible at high percentiles ([[Describing Performance]]); one slow, lock-hungry transaction can stall the whole system. Frequent deadlock aborts waste completed work.

## Examples & Systems
MySQL/InnoDB and SQL Server serializable levels; DB2 repeatable read. Meeting-room booking illustrates predicate and index-range locking.

## Related
- up: [[Serializability]] · chapter: [[Ch 07 - Transactions]]
- [[Read Committed]] — the weaker, shorter-lived locking it builds on
- [[Serializable Snapshot Isolation (SSI)]] — the optimistic, non-blocking successor
- [[Snapshot Isolation and Repeatable Read]] — the opposite reader/writer blocking philosophy
