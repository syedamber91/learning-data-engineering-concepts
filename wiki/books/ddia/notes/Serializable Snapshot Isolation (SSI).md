---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia, ssi, optimistic-concurrency, mvcc]
sources:
  - raw/ch07.md
---
# Serializable Snapshot Isolation (SSI)
> An optimistic algorithm (2008) layered on snapshot isolation: let transactions run without blocking, detect at commit time whether they acted on an outdated premise, and abort the ones that did.

## The Idea
2PL performs poorly and serial execution doesn't scale — are serializability and performance fundamentally opposed? SSI suggests not: full serializability at only a small cost over snapshot isolation. Where 2PL is *pessimistic* (anything risky ⇒ wait, like a mutex) and serial execution is pessimism taken to the extreme (one implicit global lock, compensated by ultra-fast transactions), SSI is *optimistic*: proceed anyway, check at commit, abort if isolation was violated. Optimistic concurrency control is an old, long-debated idea; SSI's novelty is building it on a consistent MVCC snapshot.

## How It Works
The write-skew pattern is a *decision on an outdated premise*: a transaction reads ("two doctors on call"), decides, writes — but by commit time the premise may be false. The database can't know how query results feed application logic, so it must assume any change to a transaction's read results may invalidate its writes. Two detection cases:

1. **Stale MVCC reads** (the conflicting write committed *before* our read but was invisible in our snapshot). Track when a transaction ignores another's uncommitted writes under MVCC visibility rules; at commit, if any ignored write has since committed, abort. Aborting only at commit — not on first detection — avoids needless aborts: the reader might be read-only (no skew risk), or the writer might itself abort.
2. **Writes affecting prior reads** (the conflicting write happens *after* our read). Analogous to index-range locks, but non-blocking: record on the index entry (or table) which transactions read that data; a writer consults these records and *notifies* the readers — a tripwire, not a block. First committer wins: in the doctors race, transaction 42 commits fine, and 43, whose premise was invalidated by 42's committed write, must abort.

Read tracking can be discarded once all concurrent transactions finish.

## Trade-offs & Pitfalls
- Tracking granularity is a dial: fine-grained ⇒ precise aborts but bookkeeping overhead; coarse ⇒ fast but spurious aborts. PostgreSQL further proves some overwritten-read executions serializable anyway to cut false aborts.
- Optimism backfires under high contention: many aborted-and-retried transactions can worsen an already saturated system. Commutative atomic ops (counter increments) reduce contention.
- Abort rate dominates performance: long read-write transactions will likely conflict, so SSI wants short ones (long *read-only* transactions are fine) — though it tolerates slowness better than 2PL or serial execution.
- Big wins: no blocking on locks ⇒ predictable latency; read-only queries run lock-free on a snapshot; not bound to one CPU core.

## Examples & Systems
PostgreSQL serializable level since 9.1 (the first single-node use); FoundationDB runs a similar algorithm distributed across machines, scaling conflict detection to high throughput across partitions. Origin: Cahill's 2008 paper and PhD thesis.

## Related
- up: [[Serializability]] · chapter: [[Ch 07 - Transactions]]
- [[Snapshot Isolation and Repeatable Read]] — the MVCC foundation SSI extends
- [[Write Skew and Phantoms]] — the anomalies SSI's premise-checking eliminates
- [[Two-Phase Locking (2PL)]] — the pessimistic counterpart and its index-range locks
- [[Distributed Transactions and Consensus]] — serializability across nodes
