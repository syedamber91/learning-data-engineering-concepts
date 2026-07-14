---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, coordination, systems]
sources:
  - raw/ch06.md
  - raw/ch09.md
---
# ZooKeeper

The workhorse coordination service: a small, strongly consistent, replicated
key-value store with total-order broadcast (Zab), ephemeral nodes, watches, and
version numbers. Systems outsource their hardest problems to it — [[Leader Election]], partition assignment, service discovery, distributed locks with
[[Fencing Tokens]] — instead of implementing [[Consensus]] themselves.

In the book: [[Membership and Coordination Services]] (Ch 9), plus cameos in
[[Request Routing]] (Ch 6) and HBase/Kafka/Hadoop ecosystems throughout Parts II–III.

## Referenced In
- [[Ch 06 - Partitioning]]
- [[Ch 09 - Consistency and Consensus]]
- [[Consistency Guarantees]]
- [[Home]]
- [[Distributed Transactions and Consensus]]
- [[Fault-Tolerant Consensus]]
- [[Implementing Linearizable Systems]]
- [[Linearizability]]
- [[Membership and Coordination Services]]
- [[Relying on Linearizability]]
- [[Request Routing]]
- [[The Truth Is Defined by the Majority]]
- [[Total Order Broadcast]]
