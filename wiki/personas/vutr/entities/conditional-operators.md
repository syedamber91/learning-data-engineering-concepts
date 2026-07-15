---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: conditional-operators
topics:
- airflow
---

Two operators give a DAG run-time branching logic — the answer to "the pipeline needs to take a different path when something happens" (a data-quality check failing after extraction, weekday-incremental vs weekend-full-refresh runs, or logic that depends on trigger configuration). `BranchPythonOperator` (`@task.branch`) returns the `task_id` — or list of `task_id`s — of whichever immediately-downstream task(s) should run, evaluated at runtime; everything else gets skipped. Vu's example: a `check_data_quality` branch task computes a null ratio and returns `["alert_and_skip"]` if it exceeds 0.05, or `["load_to_warehouse"]` otherwise. `ShortCircuitOperator` (`@task.short_circuit`) is the simpler yes/no case: it returns a plain Boolean, and a `False` skips every downstream task in one shot rather than choosing between named branches — e.g. a `has_new_data` check returning `False` (row count is zero) skips both `transform` and `load` in the same DAG. The distinction is precision: `BranchPythonOperator` picks a path among several named branches, while `ShortCircuitOperator` is a single on/off gate for everything downstream.

*See also: [[trigger-rules]] · [[trigger-dag-run-operator]] · [[airflow-failure-handling-and-retries]]*
