---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, replication]
sources:
  - raw/ch05.md
  - raw/ch06.md
  - raw/ch11.md
---
# Replication

Keeping copies of the same data on multiple nodes. Buys you fault tolerance (a
replica can take over), read scaling (spread reads across copies), and lower latency
(serve users from a nearby copy). The hard part is keeping copies in sync when data
changes — which is why replication strategy (single-leader, multi-leader, leaderless)
determines what anomalies your application can observe.

Book home ground: [[Ch 05 - Replication]] — [[Leaders and Followers]],
[[Multi-Leader Replication]], [[Leaderless Replication]], and the lag anomalies in
[[Problems with Replication Lag]]. Interacts with [[Partitioning]] (replicas per
partition) and underpins [[Linearizability]] questions in Ch 9.

## Referenced In
- [[Approaches for Coping with Load]]
- [[Ch 05 - Replication]]
- [[Ch 06 - Partitioning]]
- [[Ch 11 - Stream Processing]]
- [[Home]]
- [[Databases and Streams]]
- [[Hardware Faults]]
- [[Implementing Linearizable Systems]]
- [[Leaders and Followers]]
- [[Limitations of Quorum Consistency]]
- [[Messaging Systems]]
- [[Ordering Guarantees]]
- [[Other Indexing Structures]]
- [[Part II - Distributed Data]]
- [[Partitioning and Replication]]
- [[Preventing Lost Updates]]
- [[Scalability]]
- [[Setting Up New Followers]]
- [[Sort Order in Column Storage]]
- [[The Meaning of ACID]]
- [[The Slippery Concept of a Transaction]]
- [[Transmitting Event Streams]]
- [[Use Cases for Multi-Leader Replication]]
