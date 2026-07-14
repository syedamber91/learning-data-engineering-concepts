---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, transactions, distributed-systems]
sources:
  - raw/ch07.md
  - raw/ch09.md
  - raw/ch12.md
---
# Two-Phase Commit

Atomic commit across multiple nodes: a coordinator asks all participants to
*prepare* (phase 1 — each promises it can commit, come what may), then broadcasts
the *commit/abort* decision (phase 2). The promise plus the coordinator's logged
decision are points of no return. Weakness: if the coordinator crashes after
prepare, participants are "in doubt" — holding locks, blocked until it recovers.

Book home ground: [[Atomic Commit and Two-Phase Commit (2PC)]] and the XA
war-stories in [[Distributed Transactions in Practice]] (Ch 9). Not the same as
[[Consensus]] (2PC requires *every* node's yes; consensus needs only a
[[Quorum]] — and fault-tolerant consensus doesn't block).

## Referenced In
- [[Aiming for Correctness]]
- [[Atomic Commit and Two-Phase Commit (2PC)]]
- [[Ch 07 - Transactions]]
- [[Ch 09 - Consistency and Consensus]]
- [[Ch 12 - The Future of Data Systems]]
- [[Composing Data Storage Technologies]]
- [[Home]]
- [[Data Integration]]
- [[Distributed Transactions and Consensus]]
- [[Distributed Transactions in Practice]]
- [[Enforcing Constraints]]
- [[Fault Tolerance]]
- [[Fault-Tolerant Consensus]]
- [[Messaging Systems]]
- [[Single-Object and Multi-Object Operations]]
- [[The End-to-End Argument for Databases]]
- [[Two-Phase Locking (2PL)]]
- [[Unbundling Databases]]
