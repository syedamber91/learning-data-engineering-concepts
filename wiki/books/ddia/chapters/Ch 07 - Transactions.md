---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
type: chapter-moc
tags: [ddia, transactions, isolation, concurrency-control, moc]
sources:
  - raw/ch07.md
---
# Ch 07 – Transactions

Data systems fail in messy, overlapping ways — crashes mid-write, dropped connections, clients racing each other, readers catching half-applied updates. Transactions are the abstraction that compresses all of that into one clean question: did this group of reads and writes commit, or abort? The chapter first dismantles the marketing around [[ACID]] (atomicity is abortability, consistency belongs to the application, durability is layered risk reduction), then goes deep on the I: a catalogue of the race conditions each weak isolation level permits — dirty reads and writes, read skew, lost updates, write skew, phantoms — and finally the three ways to buy true [[Serializability]]: serial execution, two-phase locking, and serializable snapshot isolation. It applies to single-node and distributed databases alike; the distributed-only pathologies wait for [[Ch 08 - The Trouble with Distributed Systems]].

## Map
- [[The Slippery Concept of a Transaction]] — what transactions promise, and why "ACID" underdetermines it
  - [[The Meaning of ACID]] — atomicity, consistency, isolation, durability, each with fine print
  - [[Single-Object and Multi-Object Operations]] — when multi-object transactions are genuinely needed, and how to retry aborts safely
- [[Weak Isolation Levels]] — the anomaly taxonomy behind the levels databases actually run
  - [[Read Committed]] — no dirty reads, no dirty writes; the popular default
  - [[Snapshot Isolation and Repeatable Read]] — consistent snapshots via MVCC; readers and writers never block each other
  - [[Preventing Lost Updates]] — atomic operations, explicit locks, automatic detection, compare-and-set, and the replication wrinkle
  - [[Write Skew and Phantoms]] — disjoint writes from a shared premise; the doctors-on-call bug and conflicts you can't lock
- [[Serializability]] — the strongest level and its three implementation families
  - [[Actual Serial Execution]] — one thread, in-memory data, deterministic stored procedures
  - [[Two-Phase Locking (2PL)]] — pessimistic shared/exclusive locks, plus predicate and index-range locks
  - [[Serializable Snapshot Isolation (SSI)]] — optimistic detection of stale premises at commit time

## Chapter Summary
Transactions let applications ignore whole classes of hardware, software, and concurrency faults by reducing them to abort-and-retry; simple single-record apps can live without them, but anything with [[Denormalization]], [[Secondary Indexes]], or multi-object invariants gains enormously. The chapter's core is a ladder of race conditions: *dirty reads* (seeing uncommitted data) and *dirty writes* (overwriting uncommitted data), both stopped by read committed; *read skew* (inconsistent points in time within one query), stopped by snapshot isolation built on multi-version concurrency control; *lost updates* (concurrent read-modify-write cycles clobbering each other), stopped by some snapshot-isolation implementations automatically and by explicit `SELECT FOR UPDATE` elsewhere; *write skew* (a write invalidating another transaction's premise), which only serializable isolation prevents; and *phantoms* (writes changing another transaction's search results), which in read-write transactions need special treatment such as index-range locks.

Three routes deliver serializability. Literal serial execution works when transactions are short, data fits in memory, and throughput fits one CPU core (or partitions cleanly). Two-phase locking was the standard for decades but pays in contention, deadlocks, and volatile tail latencies. Serializable snapshot isolation, the newest option, runs transactions optimistically on snapshots and aborts at commit those whose premises went stale — avoiding blocking entirely. These guarantees hold regardless of data model; stretching them across many machines is the business of the next chapters.

## Related
- part: [[Part II - Distributed Data]] · home: [[Home]]
- previous: [[Ch 06 - Partitioning]] — partial failure across partitions is exactly what transactions must tame
- next: [[Ch 08 - The Trouble with Distributed Systems]] — the fault landscape when transactions span machines
- [[Ch 09 - Consistency and Consensus]] — distributed transactions, atomic commit, and [[Two-Phase Commit]]
