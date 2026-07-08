---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: kubernetes-executor
topics:
- airflow
---

The KubernetesExecutor spins up a dynamic pod per task, so for me it gives the best resource isolation, scalability, and fault tolerance. The trade-off is cold start cost, but it also lets different tasks carry different Python dependencies.

*See also: [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]] · [[pools]]*
