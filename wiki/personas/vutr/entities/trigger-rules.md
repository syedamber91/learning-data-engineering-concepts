---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: trigger-rules
topics:
- airflow
---

A task's trigger_rule decides when it runs relative to its upstream tasks. The default fires only when all upstream tasks succeed, but trigger_rule='all_done' makes a task run regardless of upstream status — success or failure. This is the standard lever for cleanup, notification, or teardown tasks that must always execute at the end of a branch.
