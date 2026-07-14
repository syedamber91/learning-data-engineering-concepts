---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, coordination, distributed-systems]
sources:
  - raw/glossary.md
---
# Leader Election

Choosing exactly one node to play a special role (e.g. accept writes for a
partition). Sounds simple; is [[Consensus]] in disguise — all nodes must agree who
the leader is, even during network partitions, or you get [[Split Brain]] with two
nodes both accepting writes.

In the book: failover in [[Handling Node Outages]] (Ch 5), the majority-vote
framing in [[The Truth Is Defined by the Majority]] (Ch 8), protection of resources
via [[Fencing Tokens]], and proper solutions via [[Fault-Tolerant Consensus]] or a
coordination service ([[ZooKeeper]], [[Etcd]]) in
[[Membership and Coordination Services]].

## Referenced In
- [[Detecting Faults]]
- [[Distributed Transactions and Consensus]]
- [[Handling Node Outages]]
- [[Linearizability]]
- [[Membership and Coordination Services]]
- [[Process Pauses]]
- [[The Truth Is Defined by the Majority]]
