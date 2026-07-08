---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: tombstone
topics:
- lsm-tree-storage-engines
---

Tombstones are markers that record a deletion in an LSM-tree; the record is not physically removed at delete time. The real removal is deferred until compaction sweeps through and drops the tombstoned data.
