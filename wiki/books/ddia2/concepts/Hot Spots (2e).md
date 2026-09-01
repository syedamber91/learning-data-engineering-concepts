---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, sharding, skew, load]
sources:
  - raw/ch07.md
---
# Hot Spots

One shard receiving disproportionate load — the celebrity user, the monotonically increasing timestamp key. Defeats the point of sharding, and is the main thing sharding schemes are judged on.

See [[Skewed Workloads and Relieving Hot Spots (2e)]].

## Appears In
- [[Implementing Linearizable Systems (2e)]]
- [[Joins and Grouping (2e)]]
- [[Materializing and Updating Timelines (2e)]]
- [[Preventing Lost Updates (2e)]]
- [[Relying on Synchronized Clocks (2e)]]
- [[Serializability (2e)]]
- [[Serializable Snapshot Isolation (2e)]]
- [[Sharding by Hash of Key (2e)]]
- [[Sharding of Key-Value Data (2e)]]
- [[Shuffling Data (2e)]]
- [[Skewed Workloads and Relieving Hot Spots (2e)]]
- [[Snapshot Isolation and Repeatable Read (2e)]]
- [[Trust, but Verify (2e)]]
- [[Two-Phase Locking (2e)]]
