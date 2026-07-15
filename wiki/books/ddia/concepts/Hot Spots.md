---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, partitioning, performance]
sources:
  - raw/ch06.md
---
# Hot Spots

Partitions receiving disproportionate load, defeating the point of distributing.
Causes: skewed key popularity (a celebrity user), poor key choice (timestamp-prefixed
keys putting all today's writes in one range partition), or unlucky hashing of one
mega-key. Remedies: better key design (compound keys), hashing
([[Partitioning by Hash of Key]]), or key-splitting tricks — appending random
suffixes to spread one hot key, at the cost of scatter-gather reads.

Book home ground: [[Skewed Workloads and Relieving Hot Spots]] (Ch 6); resurfaces
as skewed joins in batch processing ([[Reduce-Side Joins and Grouping]]).

## Referenced In
- [[Ch 06 - Partitioning]]
- [[Describing Load]]
- [[Monotonic Reads]]
- [[Partitioning by Hash of Key]]
- [[Partitioning by Key Range]]
- [[Partitioning of Key-Value Data]]
- [[Reduce-Side Joins and Grouping]]
- [[Skewed Workloads and Relieving Hot Spots]]
