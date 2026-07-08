---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: b-tree
topics:
- lsm-tree-storage-engines
---

The B-Tree (introduced in the 1970s) does in-place updates with random I/O and is excellent for reading, but writing requires more work to preserve the tree's structure. The B+Tree variant keeps actual data only in leaf nodes, uses a branching factor M for max children per page, and splits nodes when they overflow — and it suffers more write amplification for random writes than an LSM-tree.

*See also: [[compaction]] · [[bigquery-vortex]] · [[bloom-filter]] · [[memtable]] · [[write-ahead-log]] · [[tombstone]]*
