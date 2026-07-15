---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, consistency, distributed-systems]
sources:
  - raw/ch09.md
---
# CAP Theorem

The trade often stated as "consistency, availability, partition tolerance — pick
two," more usefully read as: *when* a network partition happens, each piece of data
can be either linearizable or available-for-writes, not both. The book treats the
theorem as narrow (it addresses only linearizability and only partitions, ignoring
latency, which drives most real decisions) and prefers precise guarantee names.

In the book: [[The Cost of Linearizability]] (Ch 9) — including the observation
that many systems are neither linearizable nor perfectly available, and that
multi-leader/leaderless designs deliberately choose looser consistency
([[Multi-Leader Replication]], [[Eventual Consistency]]).

## Referenced In
- [[Ch 09 - Consistency and Consensus]]
- [[Consistency Guarantees]]
- [[Home]]
- [[Linearizability]]
- [[Ordering and Causality]]
- [[The Cost of Linearizability]]
- [[The Meaning of ACID]]
- [[The Slippery Concept of a Transaction]]
- [[Timeliness and Integrity]]
