---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, failover, consensus, fencing]
sources:
  - raw/ch06.md
  - raw/ch09.md
  - raw/ch10.md
---
# Split Brain

Two nodes both believing they are the leader, both accepting writes, and diverging. The failure mode that makes automatic failover dangerous and fencing tokens necessary.

See [[Handling Node Outages (2e)]], [[The Majority Rules (2e)]], and [[Fencing Tokens (2e)]]-style protection in [[Distributed Locks and Leases (2e)]].

## Appears In
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Enforcing Constraints (2e)]]
- [[Handling Node Outages (2e)]]
- [[Implementing Linearizable Systems (2e)]]
- [[Relying on Linearizability (2e)]]
- [[Request Routing (2e)]]
- [[Single-Leader Replication (2e)]]
- [[The Majority Rules (2e)]]
