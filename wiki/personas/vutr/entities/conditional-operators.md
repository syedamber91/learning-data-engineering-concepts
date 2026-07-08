---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: conditional-operators
topics:
- airflow
---

BranchPythonOperator and ShortCircuitOperator handle conditional logic in a DAG. BranchPythonOperator picks which downstream branch to follow based on a Python callable's return, while ShortCircuitOperator skips all downstream tasks when its condition evaluates false. Together they let a DAG make runtime routing decisions instead of running a fixed path every time.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
