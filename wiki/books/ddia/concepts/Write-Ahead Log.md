---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, storage-engines, durability]
sources:
  - raw/ch03.md
---
# Write-Ahead Log

Append-only file where a storage engine records every modification *before*
applying it to its main data structures. After a crash, replaying the log restores a
consistent state. It's how [[B-Trees]] survive partial page writes, and the idea
radiates outward: replication logs ([[Implementation of Replication Logs]]),
[[Change Data Capture]], and [[Event Sourcing]] are all "the log is the truth" at
larger scales.

In the book: introduced with B-tree reliability in Ch 3, echoed anywhere ordered,
durable, append-only state shows up — see [[Partitioned Logs]] and
[[State, Streams, and Immutability]].

## Referenced In
- [[Atomic Commit and Two-Phase Commit (2PC)]]
- [[B-Trees]]
- [[Ch 03 - Storage and Retrieval]]
- [[Change Data Capture]]
- [[Comparing B-Trees and LSM-Trees]]
- [[Home]]
- [[Data Structures That Power Your Database]]
- [[Implementation of Replication Logs]]
- [[Leaders and Followers]]
- [[SSTables and LSM-Trees]]
- [[Setting Up New Followers]]
- [[Single-Object and Multi-Object Operations]]
- [[The Meaning of ACID]]
- [[The Output of Batch Workflows]]
- [[Total Order Broadcast]]
