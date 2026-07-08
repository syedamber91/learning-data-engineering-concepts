---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: assets
topics:
- airflow
---

Assets enable event-driven triggering between DAGs, so one DAG can fire when data it depends on becomes available. This is the data-aware, event-driven complement to poll-based Sensors.

*See also: [[kubernetes-executor]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]] · [[pools]]*
