---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, locks, leases, safety]
sources:
  - raw/ch09.md
---
# Fencing Tokens

A monotonically increasing number handed out with a lock or lease, checked by the resource on every write, so a paused-then-resumed holder of an expired lease cannot corrupt anything.

See [[Distributed Locks and Leases (2e)]].

## Appears In
- [[Byzantine Faults (2e)]]
- [[Consensus in Practice (2e)]]
- [[Coordination Services (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Handling Node Outages (2e)]]
- [[Knowledge, Truth, and Lies (2e)]]
- [[Process Pauses (2e)]]
- [[Relying on Linearizability (2e)]]
- [[System Model and Reality (2e)]]
- [[The End-to-End Argument for Databases (2e)]]
- [[The Majority Rules (2e)]]
