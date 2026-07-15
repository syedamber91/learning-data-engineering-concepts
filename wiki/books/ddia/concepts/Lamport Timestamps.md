---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, ordering, distributed-systems]
sources:
  - raw/ch09.md
---
# Lamport Timestamps

Logical clocks: each node keeps a counter, stamps events with (counter, node-id),
and fast-forwards its counter whenever it sees a bigger one. Result: a total order
consistent with [[Causality]] — if A happened before B, A's timestamp is smaller.
Cheaper than [[Version Vectors]] but weaker: you can't tell concurrency from
causal order by looking at two timestamps.

Book home ground: [[Sequence Number Ordering]] (Ch 9), including why timestamp
order alone can't enforce uniqueness constraints *now* — you'd have to wait to learn
of every smaller timestamp, which leads to [[Total Order Broadcast]].

## Referenced In
- [[Ch 09 - Consistency and Consensus]]
- [[Combining Specialized Tools by Deriving Data]]
- [[Monotonic Versus Time-of-Day Clocks]]
- [[Ordering Guarantees]]
- [[Relying on Synchronized Clocks]]
- [[Sequence Number Ordering]]
- [[Total Order Broadcast]]
- [[Unreliable Clocks]]
