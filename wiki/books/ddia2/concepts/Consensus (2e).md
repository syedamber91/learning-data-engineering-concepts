---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, distributed, coordination, raft]
sources:
  - raw/ch10.md
---
# Consensus

Getting several nodes to agree on one value, and to stay agreed through crashes and network faults. Equivalent to total order broadcast, to linearizable compare-and-set, and to leader election — the book's point is that these are all the same problem wearing different clothes.

See [[The Many Faces of Consensus (2e)]] and [[Consensus in Practice (2e)]].

## Appears In
- [[Byzantine Faults (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Consensus (2e)]]
- [[Consensus in Practice (2e)]]
- [[Coordination Services (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Distributed Transactions (2e)]]
- [[Enforcing Constraints (2e)]]
- [[Event Sourcing and CQRS (2e)]]
- [[Handling Node Outages (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Implementing Linearizable Systems (2e)]]
- [[Knowledge, Truth, and Lies (2e)]]
