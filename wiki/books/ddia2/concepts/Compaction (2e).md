---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, storage, lsm, garbage-collection]
sources:
  - raw/ch04.md
  - raw/ch12.md
---
# Compaction

Merging accumulated log segments or SSTables, discarding overwritten and deleted entries. Reclaims space in LSM engines, and in log-based brokers it is what turns an unbounded event stream into a bounded snapshot of current state.

See [[Log-Structured Storage (2e)]] and [[Log-Based Message Brokers (2e)]].

## Appears In
- [[Avro (2e)]]
- [[Change Data Capture (2e)]]
- [[Column-Oriented Storage (2e)]]
- [[Comparing B-Trees and LSM-Trees (2e)]]
- [[Dataflow Through Databases (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Formats for Encoding Data (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Implementation of Replication Logs (2e)]]
- [[JSON, XML, and Binary Variants (2e)]]
- [[Log-Based Message Brokers (2e)]]
- [[Log-Structured Storage (2e)]]
- [[Logical Clocks (2e)]]
- [[Protocol Buffers (2e)]]
