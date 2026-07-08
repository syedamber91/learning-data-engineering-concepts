---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: celery-executor
topics:
- airflow
---

The CeleryExecutor distributes tasks across workers using a message broker like RabbitMQ or Redis. Its downsides are the Noisy Neighbor problem and underutilized resources when only a few tasks are running.

*See also: [[kubernetes-executor]] · [[assets]] · [[trigger-rules]] · [[local-executor]] · [[xcom]] · [[pools]]*
