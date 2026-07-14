---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, coordination, systems]
sources:
  - raw/ch09.md
---
# Etcd

A Raft-based, strongly consistent key-value store in the same role as
[[ZooKeeper]]: cluster metadata, [[Leader Election]], distributed locks, service
discovery — famously the control-plane store for Kubernetes. Linearizable writes via
[[Consensus]] (Raft), watch APIs, leases as the ephemeral-node analogue.

In the book: named alongside ZooKeeper in [[Membership and Coordination Services]]
and the linearizable-systems discussion of [[Ch 09 - Consistency and Consensus]].

## Referenced In
- [[Ch 09 - Consistency and Consensus]]
- [[Consistency Guarantees]]
- [[Distributed Transactions and Consensus]]
- [[Implementing Linearizable Systems]]
- [[Linearizability]]
- [[Membership and Coordination Services]]
- [[Relying on Linearizability]]
- [[Total Order Broadcast]]
