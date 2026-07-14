---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, replication]
sources:
  - raw/ch05.md
  - raw/ch11.md
---
# Anti-Entropy

Background process that continuously compares replicas and copies missing or newer
data between them, closing the gaps that [[Read Repair]] (read-triggered, so blind
to unread keys) leaves. Often implemented with Merkle trees to find differences
without shipping full datasets; unlike a replication log it may apply changes in no
particular order and with delay.

Book home ground: leaderless replication's catch-up duo in
[[Writing to the Database When a Node Is Down]] (Ch 5); conceptual kin to keeping
derived systems in sync in [[Keeping Systems in Sync]] (Ch 11).

## Referenced In
- [[Ch 05 - Replication]]
- [[Leaderless Replication]]
- [[Limitations of Quorum Consistency]]
- [[Writing to the Database When a Node Is Down]]
