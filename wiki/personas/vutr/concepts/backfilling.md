---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: backfilling
topics:
- airflow
---

Backfilling reprocesses historical data via the 'airflow dags backfill' command. You control its resource footprint with max_active_runs at the orchestration layer and a dedicated resource pool at the processing layer.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
