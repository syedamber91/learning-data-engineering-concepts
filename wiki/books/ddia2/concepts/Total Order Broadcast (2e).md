---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, ordering, consensus, log]
sources:
  - raw/ch10.md
---
# Total Order Broadcast

Deliver every message to every node, in the same order, reliably. Equivalent to consensus, and exactly what an append-only replicated log gives you — which is why so much of the book's later machinery is built on logs.

See [[The Many Faces of Consensus (2e)]] and [[Log-Based Message Brokers (2e)]].

## Appears In
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Consensus in Practice (2e)]]
- [[Enforcing Constraints (2e)]]
- [[Linearizable ID Generators (2e)]]
- [[The Many Faces of Consensus (2e)]]
