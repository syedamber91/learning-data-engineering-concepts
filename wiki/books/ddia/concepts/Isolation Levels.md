---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, transactions, concurrency]
sources:
  - raw/glossary.md
---
# Isolation Levels

How much concurrent transactions are allowed to observe of each other. The ladder
in practice: read committed (no dirty reads/writes) → snapshot isolation /
repeatable read (transaction sees a consistent point-in-time snapshot, via MVCC) →
serializable (equivalent to some serial execution). Each step blocks more anomalies:
dirty reads, read skew, lost updates, write skew and phantoms.

Book home ground: [[Weak Isolation Levels]] and its subtopics ([[Read Committed]],
[[Snapshot Isolation and Repeatable Read]], [[Preventing Lost Updates]],
[[Write Skew and Phantoms]]) plus the three serializable implementations in
[[Serializability]]. Beware: names are inconsistent across databases — "repeatable
read" means different things in different systems.

## Referenced In
- [[Aiming for Correctness]]
- [[Consistency Guarantees]]
- [[Home]]
- [[Read Committed]]
- [[Serializability]]
- [[The End-to-End Argument for Databases]]
- [[The Meaning of ACID]]
- [[Trust, but Verify]]
- [[Weak Isolation Levels]]
