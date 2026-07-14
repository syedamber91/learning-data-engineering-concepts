---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
type: topic
tags: [ddia, serializability, concurrency-control, locking]
sources:
  - raw/ch07.md
---
# Serializability

Serializable isolation is the strongest guarantee: even though transactions run in parallel, the committed outcome equals *some* one-at-a-time execution, so any transaction that is correct alone stays correct under concurrency — every race condition in [[Weak Isolation Levels]] is prevented wholesale. Researchers have recommended it since the 1970s, because the alternatives are grim: [[Isolation Levels]] are inconsistently implemented across databases, application code can't easily be audited for which level it tolerates, and no practical tooling detects race conditions. The reason everyone doesn't simply use it is cost, and this topic surveys the three implementation families that pay that cost differently: literal serial execution on one thread, two-phase locking (the pessimistic workhorse of three decades), and serializable snapshot isolation (the young optimistic contender). The chapter treats them on a single node; generalizing to multi-node transactions is deferred to [[Distributed Transactions and Consensus]].

## Subtopics

- [[Actual Serial Execution]] — remove concurrency entirely: one thread, in-memory data, transactions packaged as deterministic stored procedures (VoltDB/H-Store, Redis, Datomic), scaling only via single-[[Partitioning|partition]] sharding.
- [[Two-Phase Locking (2PL)]] — pessimistic shared/exclusive locks held to commit, where readers block writers and vice versa; deadlocks, unstable tail latencies, and predicate/index-range locks to shut down phantoms.
- [[Serializable Snapshot Isolation (SSI)]] — optimistic control layered on snapshot isolation: run without blocking, track stale MVCC reads and writes that invalidate prior reads, abort at commit if the premise went stale (PostgreSQL 9.1+, FoundationDB).

## Key Takeaways

- Serializability's promise is compositional correctness: the database, not the developer, rules out every possible race — including write skew and phantoms that no weaker level catches.
- Serial execution became viable around 2007 because RAM got cheap enough to hold active datasets and OLTP transactions proved short; its throughput ceiling is one CPU core per partition, and cross-partition transactions are orders of magnitude slower (VoltDB: ~1,000 cross-partition writes/sec).
- 2PL is pessimism embodied — wait whenever anything *might* conflict — which is why it protects everything but suffers lock overhead, queueing, frequent deadlock aborts, and terrible high-percentile latencies under contention.
- Phantoms require locking data that doesn't exist yet: pure predicate locks are too slow, so real systems approximate them with index-range (next-key) locks, over-locking a little in exchange for cheap checks.
- SSI bets the other way: proceed optimistically, then abort at commit if a "decision based on an outdated premise" is detected — it keeps snapshot isolation's non-blocking reads, gives predictable latency, and (unlike serial execution) scales across machines, but degrades when contention drives the abort rate up, so read-write transactions should stay short.
- Choosing among the three is a workload question: serial execution wants small, fast, in-memory, partitionable transactions; 2PL tolerates long transactions but not contention-sensitive latency; SSI wants spare capacity and low contention.

## Related

- chapter: [[Ch 07 - Transactions]]
- [[The Slippery Concept of a Transaction]] — the ACID isolation ideal that serializability finally delivers
- [[Write Skew and Phantoms]] — the anomalies that force the upgrade to serializable isolation
- [[Distributed Transactions and Consensus]] — extending these single-node techniques across nodes
- [[Linearizability]] — the recency guarantee often confused with serializability (they compose as "strict serializability")
- [[Transaction Processing or Analytics]] — why short OLTP transactions make serial execution plausible at all
