---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sequential-executor
topics:
- airflow
---

The SequentialExecutor is SQLite-compatible and meant only for dev/test. Its critical operational flaw is that it pauses the scheduler while a task runs, which prevents the scheduler from continuously monitoring or queuing new tasks — a real concern for production.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
