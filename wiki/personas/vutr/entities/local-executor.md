---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: local-executor
topics:
- airflow
---

The LocalExecutor runs tasks as parallel processes on a single machine, giving you concurrency beyond the sequential case. Because it needs real concurrency at the metadata layer, it requires MySQL or PostgreSQL rather than SQLite.
