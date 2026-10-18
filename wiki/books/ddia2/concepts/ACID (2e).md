---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, transactions, acid, isolation]
sources:
  - raw/ch08.md
---
# ACID

Atomicity, Consistency, Isolation, Durability — the four letters a database vendor may attach to almost anything. The book's position is that **atomicity** and **isolation** are the load-bearing ones, **durability** is a spectrum rather than a promise, and **consistency** is really an application property the database cannot enforce on its own.

See [[The Meaning of ACID (2e)]] for the deconstruction, and [[Weak Isolation Levels (2e)]] for what the I actually buys you in practice.

## Appears In
- [[Aiming for Correctness (2e)]]
- [[Distributed Transactions (2e)]]
- [[Sharding by Hash of Key (2e)]]
- [[Single-Object and Multi-Object Operations (2e)]]
- [[Solutions for Replication Lag (2e)]]
- [[The Meaning of ACID (2e)]]
- [[Timeliness and Integrity (2e)]]
- [[Trust, but Verify (2e)]]
- [[Weak Isolation Levels (2e)]]
- [[What Exactly Is a Transaction (2e)]]
