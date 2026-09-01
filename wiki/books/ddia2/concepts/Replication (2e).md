---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, replication, availability]
sources:
  - raw/ch06.md
---
# Replication

Keeping a copy of the same data on several machines — for availability, for read throughput, and for latency. The three arrangements are single-leader, multi-leader, and leaderless.

See [[Single-Leader Replication (2e)]], [[Multi-Leader Replication (2e)]], and [[Leaderless Replication (2e)]].

## Appears In
- [[Actual Serial Execution (2e)]]
- [[Aiming for Correctness (2e)]]
- [[Batch Processing in Distributed Systems (2e)]]
- [[Change Data Capture (2e)]]
- [[Cloud Native System Architecture (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Composing Data Storage Technologies (2e)]]
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Coordination Services (2e)]]
- [[Data Integration (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Databases and Streams (2e)]]
- [[Dataflow Engines (2e)]]

## In the vutr data-engineering wiki
- [[leader-follower-replication]] — Kafka's leader-follower partition replication as a concrete single-leader implementation of these trade-offs.
- [[northguard-segment-level-replication]] — the same fault-tolerance goal pursued at a different granularity — segments, not whole partitions — to solve real operational problems at LinkedIn's scale.
