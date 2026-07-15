---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, consensus, distributed-systems]
sources:
  - raw/ch05.md
  - raw/ch08.md
  - raw/ch09.md
  - raw/ch12.md
---
# Consensus

Getting several nodes to agree on a value such that the decision is final even if
nodes crash or the network misbehaves. Formally equivalent to many problems that
look different: atomic commit, [[Leader Election]], total-order broadcast,
linearizable compare-and-set. FLP says it's impossible in a fully asynchronous
system, but timeouts (partial synchrony) make practical algorithms — Paxos, Raft,
Zab, VSR — work: they proceed when a [[Quorum]] agrees, using epoch numbers to
prevent stale leaders from acting.

Book home ground: [[Fault-Tolerant Consensus]] and the rest of
[[Distributed Transactions and Consensus]] in [[Ch 09 - Consistency and Consensus]];
implemented in practice by [[ZooKeeper]] and [[Etcd]].

## Referenced In
- [[Aiming for Correctness]]
- [[Atomic Commit and Two-Phase Commit (2PC)]]
- [[Byzantine Faults]]
- [[Ch 05 - Replication]]
- [[Ch 08 - The Trouble with Distributed Systems]]
- [[Ch 09 - Consistency and Consensus]]
- [[Ch 12 - The Future of Data Systems]]
- [[Combining Specialized Tools by Deriving Data]]
- [[Consistency Guarantees]]
- [[Home]]
- [[Data Integration]]
- [[Distributed Transactions and Consensus]]
- [[Enforcing Constraints]]
- [[Fault-Tolerant Consensus]]
- [[Handling Node Outages]]
- [[Implementing Linearizable Systems]]
- [[Leaderless Replication]]
- [[Limitations of Quorum Consistency]]
- [[Membership and Coordination Services]]
- [[Ordering Guarantees]]
- [[Part II - Distributed Data]]
- [[Relying on Linearizability]]
- [[Request Routing]]
- [[Synchronous Versus Asynchronous Replication]]
- [[Total Order Broadcast]]
- [[Trust, but Verify]]
