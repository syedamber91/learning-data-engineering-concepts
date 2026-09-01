---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, leaderless, replication, availability]
sources:
  - raw/ch06.md
---
# Quorum

Requiring w writes and r reads out of n replicas, with w + r > n so the sets overlap and a read sees at least one up-to-date copy. The core of Dynamo-style leaderless replication — and weaker than it looks.

See [[Leaderless Replication (2e)]] and [[Detecting Concurrent Writes (2e)]].

## Appears In
- [[Aiming for Correctness (2e)]]
- [[Change Data Capture (2e)]]
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Implementing Linearizable Systems (2e)]]
- [[Knowledge, Truth, and Lies (2e)]]
- [[Leaderless Replication (2e)]]
- [[Linearizability (2e)]]
- [[Multi-Region Operation (2e)]]
- [[Single-Leader Replication (2e)]]
- [[Single-Leader Versus Leaderless Replication Performance (2e)]]
- [[Synchronous Versus Asynchronous Replication (2e)]]
- [[System Model and Reality (2e)]]
