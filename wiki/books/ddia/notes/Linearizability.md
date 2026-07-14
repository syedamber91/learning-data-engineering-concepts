---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
type: topic
tags: [ddia, linearizability, strong-consistency, recency]
sources:
  - raw/ch09.md
---
# Linearizability
> Linearizability makes a replicated system behave as if there were exactly one copy of the data, with every operation taking effect atomically at some instant — a recency guarantee on individual objects.

Also called atomic consistency, [[Strong Consistency]], immediate consistency, or external consistency, linearizability promises that once any client has seen a written value, every subsequent read (by anyone) sees a value at least that new. The canonical intuition: two people refreshing a sports site should never see the newer score first and the older one second. Crucially, linearizability is **not** [[Serializability]] — serializability is a transaction *isolation* property over multiple objects, whereas linearizability is a *recency* property on single-object reads and writes; a system offering both is called strictly serializable. Linearizability is what locks, [[Leader Election]], and uniqueness constraints need, but it is expensive: the [[CAP Theorem]] captures its unavailability under network partitions, and even absent faults it is inherently slow on networks with variable delay.

## Subtopics
- [[What Makes a System Linearizable]] — the precise definition via register histories, atomic flip points, and compare-and-set.
- [[Relying on Linearizability]] — where recency is a hard requirement: locking, uniqueness, cross-channel dataflows.
- [[Implementing Linearizable Systems]] — which replication schemes can (and cannot) deliver it, including why quorums fall short.
- [[The Cost of Linearizability]] — CAP, the availability trade-off, and the inescapable latency penalty.

## Key Takeaways
- Linearizability = single-copy illusion + atomic operations + recency; it is a per-object total order, not a multi-object isolation level.
- Once one read returns a new value, no later read may return an older one — even across clients.
- Single-leader replication is only *potentially* linearizable; multi-leader is not; Dynamo-style quorums are not, despite w + r > n.
- Consensus algorithms ([[ZooKeeper]], [[Etcd|etcd]]) are the safe way to get linearizable storage with fault tolerance.
- The performance cost is paid all the time, not only during partitions — response time scales with network delay uncertainty (Attiya & Welch).

## Related
- chapter: [[Ch 09 - Consistency and Consensus]]
- [[Consistency Guarantees]] — where this model sits on the spectrum
- [[Ordering and Causality]] — linearizability implies causal consistency
- [[Total Order Broadcast]] — the construction equivalent to linearizable CAS
- [[Serializability]] — the frequently confused transaction-level cousin
