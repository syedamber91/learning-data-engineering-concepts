---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: pools
topics:
- airflow
---

A Pool is a named logical bucket with a fixed number of slots. You assign a task to a pool, and Airflow guarantees the total number of running tasks in that pool never exceeds its slot count — e.g., a `production_db` pool with 5 slots and 10 tasks configured against it will never run more than 5 of them concurrently, no matter how many are ready. `pool_slots` (default 1) lets a single task claim more than one slot at once, to mark it as heavier than its peers: in a 5-slot pool, a task with `pool_slots=2` leaves only 3 slots free for the remaining `pool_slots=1` tasks. Pools are Airflow's lever for protecting a shared, rate-limited resource — a production database's connection limit, a vendor API's requests-per-second cap — from being overwhelmed by parallel task execution, independent of how many tasks the DAG or the whole Airflow environment is otherwise allowed to run at once (see [[airflow-concurrency-and-resource-control]] for how pools compose with `parallelism`, `max_active_runs`, and `max_active_tasks`). When a pool is full and tasks queue up, `priority_weight` decides which one runs next as slots free up.

*See also: [[airflow-concurrency-and-resource-control]] · [[backfilling]]*
