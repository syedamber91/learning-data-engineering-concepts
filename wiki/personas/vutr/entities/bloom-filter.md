---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: bloom-filter
topics:
- lsm-tree-storage-engines
---

A Bloom Filter gives you probabilistic membership testing with no false negatives for 'not in set' queries. In an LSM-tree that means when it says a key is absent from an SSTable, you can trust it and skip reading that file entirely.

*See also: [[compaction]] · [[bigquery-vortex]] · [[b-tree]] · [[memtable]] · [[write-ahead-log]] · [[tombstone]]*
