---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, transactions]
sources:
  - raw/ch07.md
---
# ACID

The safety promises of transactions: Atomicity (all-or-nothing on faults — really
*abortability*), Consistency (application invariants preserved — arguably the app's
job, not the DB's), Isolation (concurrent transactions can't step on each other),
Durability (committed data survives crashes). Marketing has blurred it — systems
claiming "ACID" vary wildly, especially on isolation, which is often not serializable
but a weaker level.

Book home ground: [[The Meaning of ACID]] in [[Ch 07 - Transactions]], with the
isolation spectrum in [[Weak Isolation Levels]] and [[Serializability]]. Contrast
BASE; see [[Isolation Levels]].

## Referenced In
- [[Aiming for Correctness]]
- [[Atomic Commit and Two-Phase Commit (2PC)]]
- [[Ch 07 - Transactions]]
- [[Home]]
- [[Data Warehousing]]
- [[Distributed Transactions and Consensus]]
- [[Part II - Distributed Data]]
- [[The Meaning of ACID]]
- [[The Slippery Concept of a Transaction]]
- [[Total Order Broadcast]]
- [[Transaction Processing or Analytics]]
- [[Trust, but Verify]]
