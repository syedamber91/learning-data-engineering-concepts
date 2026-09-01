---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, ordering, consistency, clocks]
sources:
  - raw/ch10.md
  - raw/ch09.md
---
# Causality

The happened-before relation: if A could have influenced B, any correct ordering must place A first. Weaker than a total order — concurrent events need no agreed order at all — but strong enough for most of what applications actually need.

Captured by version vectors and Lamport timestamps; see [[ID Generators and Logical Clocks (2e)]] and [[Detecting Concurrent Writes (2e)]].

## Appears In
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Detecting Concurrent Writes (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Logical Clocks (2e)]]
- [[Messaging Systems (2e)]]
- [[Multi-Leader Replication (2e)]]
- [[Observing Derived State (2e)]]
- [[Problems with Replication Lag (2e)]]
- [[Relying on Synchronized Clocks (2e)]]
- [[Serializable Snapshot Isolation (2e)]]
