---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, failure-modes, replication]
sources:
  - raw/ch05.md
---
# Split Brain

The failure mode where two nodes simultaneously believe they are the leader and
both accept writes — typically after a network partition triggers a bad failover.
Consequence: conflicting writes, lost or corrupted data.

In the book: raised in [[Handling Node Outages]] (Ch 5 failover risks) and
[[The Truth Is Defined by the Majority]] (Ch 8). Defenses: majority quorums for
election ([[Consensus]]), [[Fencing Tokens]] so a deposed leader's writes are
rejected, and shutting down the minority side of a partition.

## Referenced In
- [[Ch 05 - Replication]]
- [[Distributed Transactions and Consensus]]
- [[Handling Node Outages]]
- [[Implementing Linearizable Systems]]
- [[Leaders and Followers]]
- [[Network Faults in Practice]]
- [[Relying on Linearizability]]
- [[The Truth Is Defined by the Majority]]
