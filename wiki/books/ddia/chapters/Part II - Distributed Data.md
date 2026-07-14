---
book: Designing Data-Intensive Applications
type: part-moc
tags: [ddia, distributed-systems]
sources:
  - raw/partI.md
---
# Part II – Distributed Data

Part II moves from one machine to many. Why distribute at all: scale beyond one
box, survive machine/datacenter failures, and put data close to globally spread users.
The book contrasts scaling up (shared-memory — cost grows super-linearly, single
location) and shared-disk (contention-limited) with the *shared-nothing* approach it
focuses on: independent nodes coordinating over a plain network. Shared-nothing
gives price/performance freedom and geographic spread, but pushes distributed-systems
complexity onto the application developer — sometimes a single-threaded program
beats a 100-core cluster, so distribution is a trade, not a default.

Two orthogonal distribution mechanisms anchor the part: [[Replication]] (same data
on several nodes, for redundancy and read performance) and [[Partitioning]]
(splitting data into subsets, aka [[Sharding]]) — usually combined, with several
replicas per partition.

## Chapters
- [[Ch 05 - Replication]] — leader-based, multi-leader, and leaderless designs and
  their anomalies.
- [[Ch 06 - Partitioning]] — key-range vs hash partitioning, [[Secondary Indexes]],
  rebalancing, routing.
- [[Ch 07 - Transactions]] — what [[ACID]] really promises; weak isolation to
  serializability.
- [[Ch 08 - The Trouble with Distributed Systems]] — unreliable networks, clocks,
  and process pauses.
- [[Ch 09 - Consistency and Consensus]] — [[Linearizability]], ordering,
  [[Consensus]].

## Related
- [[Home]] · prev: [[Part I - Foundations of Data Systems]] · next: [[Part III - Derived Data]]
