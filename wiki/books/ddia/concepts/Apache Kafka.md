---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, streams, systems]
sources:
  - raw/ch01.md
  - raw/ch11.md
  - raw/ch12.md
---
# Apache Kafka

The canonical [[Log-Based Message Broker]]: topics split into partitioned,
replicated, append-only logs; consumers track offsets; retention and
[[Log Compaction]] keep history available for replay. In the book's world it's the
connective tissue between databases ([[Change Data Capture]] feeds), stream
processors ([[Processing Streams]]), and the "unbundled database" vision of Ch 12
where the log is the system of record.

Main appearances: [[Partitioned Logs]] and [[Databases and Streams]] (Ch 11),
[[Batch and Stream Processing]] (Ch 12).

## Referenced In
- [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Change Data Capture]]
- [[Home]]
- [[Event Sourcing]]
- [[Fault Tolerance]]
- [[Leaders and Followers]]
- [[Membership and Coordination Services]]
- [[Message-Passing Dataflow]]
- [[Messaging Systems]]
- [[Partitioned Logs]]
- [[Request Routing]]
- [[State, Streams, and Immutability]]
- [[Thinking About Data Systems]]
- [[Transmitting Event Streams]]
- [[Uses of Stream Processing]]
