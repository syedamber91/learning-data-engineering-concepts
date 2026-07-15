---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, ordering, replication]
sources:
  - raw/glossary.md
---
# Vector Clocks

Per-node counters attached to values so replicas can tell whether two versions
are causally ordered (one saw the other) or concurrent (neither saw the other).
Comparing element-wise: if A ≤ B everywhere, A happened before B; if each exceeds
the other somewhere, they're concurrent siblings that need conflict resolution.

In the book the closely related mechanism is called [[Version Vectors]] (per-replica
version numbers used in Dynamo-style stores, Ch 5's [[Detecting Concurrent Writes]]);
"vector clock" is the general causality-tracking construct. Both implement
[[Causality]] tracking without synchronized clocks.

## Referenced In
- [[Detecting Concurrent Writes]]
