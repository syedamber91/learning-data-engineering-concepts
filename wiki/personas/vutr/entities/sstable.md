---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sstable
topics:
- lsm-tree-storage-engines
---

SSTables are the immutable, sorted files that the LSM-tree persists to disk. They rely on a sparse index — one entry per block rather than per row — so you locate a block and then scan within it rather than indexing every single record.

*See also: [[compaction]] · [[bigquery-vortex]] · [[bloom-filter]] · [[b-tree]] · [[memtable]] · [[write-ahead-log]]*
