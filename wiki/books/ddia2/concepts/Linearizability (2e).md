---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, consistency, recency]
sources:
  - raw/ch10.md
---
# Linearizability

The strongest single-object consistency model: the system behaves as if there were exactly one copy of the data and every operation took effect atomically at some instant between its invocation and its response. A recency guarantee.

See [[Linearizability (2e)]] for the definition and [[The Cost of Linearizability (2e)]] for why you should want it less than you think.

## Appears In
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Coordination Services (2e)]]
- [[Distributed Transactions (2e)]]
- [[Enforcing Constraints (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Implementing Linearizable Systems (2e)]]
- [[Linearizability (2e)]]
- [[Linearizable ID Generators (2e)]]
- [[Logical Clocks (2e)]]
- [[Problems with Replication Lag (2e)]]
- [[Relying on Linearizability (2e)]]
- [[Single-Object and Multi-Object Operations (2e)]]
- [[Solutions for Replication Lag (2e)]]
