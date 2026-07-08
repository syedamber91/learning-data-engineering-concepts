---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pools
topics:
- airflow
---

Pools and pool_slots control concurrency on shared resources, while priority_weight controls a task's priority within a pool. This is the orchestration-layer lever for resource allocation.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
