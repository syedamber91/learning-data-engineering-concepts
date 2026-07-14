---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: compaction
topics:
- lsm-tree-storage-engines
---

Compaction is the background process that merges SSTables and is also when actual deletion happens. The two main strategies trade off differently: Size-Tiered merges SSTables of similar size and is write-optimized, while Leveled merges into fixed-size levels and is read-optimized with less space amplification.

*See also: [[bigquery-vortex]] · [[bloom-filter]] · [[b-tree]] · [[memtable]] · [[write-ahead-log]] · [[tombstone]]*

## Related in the other wiki
- [[Compaction]] — the book's fuller account of compaction as the "background heartbeat" of LSM storage, including the write-amplification cost when it falls behind on a write-heavy workload.
- [[Log Compaction]] — DDIA generalizes this SSTable-merging process into the log-compaction idea that also powers Kafka's compacted topics for self-sufficient CDC feeds — the same superseded-record pruning at a different layer.
