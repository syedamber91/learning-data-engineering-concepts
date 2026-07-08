---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: wal
topics:
- lsm-tree-storage-engines
---

The WAL (write-ahead log) is the durability backbone of the LSM-tree, capturing writes on disk before they live only in the volatile Memtable. Without it, an in-memory sorted structure would lose data on a crash.
