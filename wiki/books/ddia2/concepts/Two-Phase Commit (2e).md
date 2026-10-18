---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, transactions, atomic-commit, 2pc]
sources:
  - raw/ch08.md
---
# Two-Phase Commit

The classic atomic commit protocol: a coordinator asks every participant to prepare, and only then tells everyone to commit. Correct, and famous for the in-doubt window where a coordinator crash leaves participants holding locks.

See [[Distributed Transactions (2e)]] — and [[Enforcing Constraints (2e)]] for how stream processing achieves the same correctness without it.

## Appears In
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Distributed Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Messaging Systems (2e)]]
- [[Single-Object and Multi-Object Operations (2e)]]
- [[The End-to-End Argument for Databases (2e)]]
- [[The Many Faces of Consensus (2e)]]
- [[Two-Phase Commit (2e)]]
- [[Two-Phase Locking (2e)]]
