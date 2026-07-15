---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: trigger-rules
topics:
- airflow
---

A task's `trigger_rule` decides when it fires relative to the status of its upstream (parent) tasks; the default fires a task only once every parent has succeeded. Vu's worked example sets `trigger_rule="all_done"` on a task C downstream of both A and B (`[task_A, task_B] >> task_C`), so C runs once both parents have finished — regardless of whether either succeeded or failed. This is the standard lever for cleanup, notification, or teardown logic that must run at the end of a branch no matter how that branch went, and it stands in direct contrast to the default failure-handling path, where a task whose upstream exhausted its retries is marked `upstream_failed` and skipped outright (see [[airflow-failure-handling-and-retries]]) — `all_done` is exactly the escape hatch for the cases where you don't want that skip to cascade.

*See also: [[airflow-failure-handling-and-retries]] · [[trigger-dag-run-operator]] · [[conditional-operators]]*
