---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: write-ahead-log
topics:
- change-data-capture-cdc-and-data-sourcing
- lsm-tree-storage-engines
---

The write-ahead log's core principle is that a data change must be recorded in the log on stable storage BEFORE it is applied to the data files — it's called the redo log in Oracle, WAL in PostgreSQL, and binlog in MySQL. In an LSM-tree the WAL is the durability backbone, capturing writes on disk before they live only in the volatile Memtable; without it, an in-memory sorted structure would lose data on a crash. It is also the journal that log-based CDC reads from.

*See also: [[log-based-cdc]] · [[read-replica]] · [[query-based-cdc]] · [[secrets-manager]] · [[trigger-based-cdc]] · [[silent-drift-from-hard-deletion]]*
