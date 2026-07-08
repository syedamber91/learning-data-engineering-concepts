---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: orchestration-problem-space
topics:
- airflow
---

Airflow, created in 2014 at Airbnb by Maxime Beauchemin (see [[airflow-origin]]), addresses eight orchestration problem categories: scheduling, dependency management, resource allocation, error handling, monitoring and alerting, dynamic workflows, data awareness, and backfilling. Framing an orchestrator this way is what lets you reason about which feature solves which category.

*See also: [[kubernetes-executor]] · [[assets]] · [[celery-executor]] · [[trigger-rules]] · [[local-executor]] · [[xcom]]*
