---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, sharding, rebalancing]
sources:
  - raw/ch07.md
---
# Consistent Hashing

Hash keys and nodes onto the same ring so adding or removing a node moves only a small fraction of keys. The book is careful to note that most "consistent hashing" in databases is actually fixed-shard-count rebalancing.

See [[Sharding by Hash of Key (2e)]] and [[Operations - Automatic Versus Manual Rebalancing (2e)]].

## Appears In
- [[Sharding by Hash of Key (2e)]]
- [[Skewed Workloads and Relieving Hot Spots (2e)]]
- [[The Meaning of ACID (2e)]]
