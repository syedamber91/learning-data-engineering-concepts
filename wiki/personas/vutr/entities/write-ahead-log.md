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
---

The write-ahead log is the journal log-based CDC reads from — it's called the redo log in Oracle, WAL in PostgreSQL, and binlog in MySQL. Its core principle is that a data change must be recorded in the log on stable storage BEFORE it is applied to the data files.
