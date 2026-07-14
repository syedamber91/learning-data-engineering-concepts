---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, storage-engines, streams]
sources:
  - raw/ch11.md
---
# Log Compaction

Throwing away log records that have been superseded: keep, for each key, only the
most recent value. Turns an unbounded append-only log into bounded storage while
preserving a full snapshot of latest state — so a new consumer can rebuild a
complete table by reading the compacted log from the start.

In the book: compaction of segment files in [[Hash Indexes]] and [[SSTables and LSM-Trees]] (Ch 3), and the stream-processing version in [[Change Data Capture]] /
[[Partitioned Logs]] (Ch 11), as used by [[Apache Kafka]] to make CDC feeds
self-sufficient.

## Referenced In
- [[Ch 11 - Stream Processing]]
- [[Change Data Capture]]
- [[Data Structures That Power Your Database]]
- [[Databases and Streams]]
- [[Event Sourcing]]
- [[Partitioned Logs]]
- [[State, Streams, and Immutability]]
- [[Stream Joins]]
- [[Uses of Stream Processing]]
