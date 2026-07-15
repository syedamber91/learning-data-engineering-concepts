---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, ordering, replication]
sources:
  - raw/ch05.md
---
# Version Vectors

The version-per-replica structure a leaderless store keeps with each key so it can
distinguish overwrites from concurrent writes. Clients read a key and get the vector
alongside values; they send it back on write, letting the server know which versions
the write supersedes and which it's concurrent with — concurrent siblings are kept
for the application to merge.

Book home ground: [[Detecting Concurrent Writes]] (Ch 5), single-replica version
numbers generalized to Riak-style dotted version vectors. The mechanism behind
sibling values, and a practical application of [[Causality]]. Cousin of
[[Vector Clocks]].

## Referenced In
- [[Ch 05 - Replication]]
- [[Consistent Prefix Reads]]
- [[Databases and Streams]]
- [[Detecting Concurrent Writes]]
- [[Keeping Systems in Sync]]
- [[Leaderless Replication]]
- [[Multi-Leader Replication]]
- [[Multi-Leader Replication Topologies]]
- [[Ordering Guarantees]]
- [[Ordering and Causality]]
- [[Relying on Synchronized Clocks]]
- [[Sequence Number Ordering]]
- [[Unreliable Clocks]]
