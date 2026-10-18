---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, isolation, mvcc]
sources:
  - raw/ch08.md
---
# Snapshot Isolation

Each transaction reads from a consistent snapshot of the database as of its start, implemented with multi-version concurrency control. Readers never block writers. Permits write skew.

See [[Snapshot Isolation and Repeatable Read (2e)]] and [[Write Skew and Phantoms (2e)]].

## Appears In
- [[B-Trees (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Linearizable ID Generators (2e)]]
- [[Logical Clocks (2e)]]
- [[Preventing Lost Updates (2e)]]
- [[Read Committed (2e)]]
- [[Relying on Synchronized Clocks (2e)]]
- [[Serializability (2e)]]
- [[Serializable Snapshot Isolation (2e)]]
- [[Snapshot Isolation and Repeatable Read (2e)]]
- [[The Meaning of ACID (2e)]]
- [[Two-Phase Locking (2e)]]
- [[Weak Isolation Levels (2e)]]
- [[Write Skew and Phantoms (2e)]]
