---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: trigger-dag-run-operator
topics:
- airflow
---

TriggerDagRunOperator triggers another DAG from within a DAG. It is how you compose workflows across DAG boundaries — a parent DAG can kick off a child DAG as a step, rather than cramming everything into one monolithic graph.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
