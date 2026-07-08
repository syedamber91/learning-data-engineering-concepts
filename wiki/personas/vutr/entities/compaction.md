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
