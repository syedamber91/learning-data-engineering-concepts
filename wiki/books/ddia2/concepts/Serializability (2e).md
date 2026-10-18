---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, isolation, transactions]
sources:
  - raw/ch08.md
---
# Serializability

The isolation level that guarantees the outcome is the same as if transactions had run one at a time, in some order. Three ways to get it: actually run them serially, two-phase locking, or optimistic SSI.

See [[Serializability (2e)]], [[Two-Phase Locking (2e)]], and [[Serializable Snapshot Isolation (2e)]].

## Appears In
- [[Actual Serial Execution (2e)]]
- [[Aiming for Correctness (2e)]]
- [[Consensus in Practice (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Distributed Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]]
- [[Geographically Distributed Operation (2e)]]
- [[Language-Specific Formats (2e)]]
- [[Linearizability (2e)]]
- [[Preventing Lost Updates (2e)]]
- [[Serializability (2e)]]
- [[Serializable Snapshot Isolation (2e)]]
- [[Single-Object and Multi-Object Operations (2e)]]
- [[Snapshot Isolation and Repeatable Read (2e)]]
