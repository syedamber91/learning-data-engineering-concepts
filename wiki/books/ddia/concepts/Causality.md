---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, ordering, distributed-systems]
sources:
  - raw/ch09.md
---
# Causality

The happens-before relation: event B is causally dependent on A if B could have
been influenced by A (saw it, answered it, built on it). Causal order is *partial* —
concurrent events are simply unordered — unlike the total order that
[[Linearizability]] imposes. Causal consistency is the strongest guarantee that
stays available during network partitions, which makes it a sweet spot many systems
aim for.

In the book: [[Ordering and Causality]] in Ch 9; violation examples include the
question-before-answer anomaly of [[Consistent Prefix Reads]] and concurrent-write
detection via [[Version Vectors]] in Ch 5. Tracked compactly by
[[Lamport Timestamps]] (consistent with causality but totally ordered).

## Referenced In
- [[Ch 09 - Consistency and Consensus]]
- [[Combining Specialized Tools by Deriving Data]]
- [[Consistency Guarantees]]
- [[Consistent Prefix Reads]]
- [[Home]]
- [[Data Integration]]
- [[Messaging Systems]]
- [[Multi-Leader Replication Topologies]]
- [[Ordering Guarantees]]
- [[Ordering and Causality]]
- [[Problems with Replication Lag]]
- [[Relying on Synchronized Clocks]]
- [[Sequence Number Ordering]]
- [[Transmitting Event Streams]]
