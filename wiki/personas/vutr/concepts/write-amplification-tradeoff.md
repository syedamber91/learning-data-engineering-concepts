---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: write-amplification-tradeoff
topics:
- lsm-tree-storage-engines
---

Write amplification is the lens through which you choose a storage engine: B+Trees pay more write amplification on random writes than LSM-trees, which is why the LSM design leans write-optimized. Reads and space are the counterweight — you accept potentially higher read amplification to win on the write side.

*See also: [[compaction]] · [[bigquery-vortex]] · [[bloom-filter]] · [[b-tree]] · [[memtable]] · [[write-ahead-log]]*
