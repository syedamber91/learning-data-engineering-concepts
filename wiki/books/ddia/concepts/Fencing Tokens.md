---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, coordination, failure-modes]
sources:
  - raw/ch08.md
---
# Fencing Tokens

A monotonically increasing number issued with every grant of a lock or lease. Any
resource (storage service, file system) checks the token and rejects requests
carrying a smaller number than one it has already seen — so a node that held a lease,
paused (GC, network), and wrongly still believes it's the holder cannot clobber the
work of the newer holder.

In the book: Ch 8's answer to process pauses in [[Relying on Synchronized Clocks]]
and [[Process Pauses]]; [[ZooKeeper]]'s zxid/version serves as the token in practice.
A concrete instance of the end-to-end principle: the *resource* must validate, not
just the lock service.

## Referenced In
- [[Byzantine Faults]]
- [[Ch 08 - The Trouble with Distributed Systems]]
- [[Fault Tolerance]]
- [[Handling Node Outages]]
- [[Knowledge, Truth, and Lies]]
- [[Membership and Coordination Services]]
- [[Process Pauses]]
- [[Relying on Linearizability]]
- [[The End-to-End Argument for Databases]]
- [[The Truth Is Defined by the Majority]]
- [[Total Order Broadcast]]
