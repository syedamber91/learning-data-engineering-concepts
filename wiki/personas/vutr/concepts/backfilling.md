---
persona: vutr
kind: concept
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: backfilling
topics:
- airflow
---

The scenario Vu opens with: a pipeline has run daily for six months, then you discover the transformation logic has had a bug since March, quietly producing incorrect aggregates the whole time. You fix the code — but now every affected historical day needs the fix applied, which could mean 100+ runs, each still respecting the same dependency graph a normal run would.

Airflow answers this with two related but distinct mechanisms. The built-in `airflow backfill create --dag-id <id> --start-date <date> --end-date <date>` command re-runs a DAG over an explicit date range (the same action is also available from the UI). Separately, at DAG-creation time, the `catchup` parameter controls whether Airflow automatically runs every interval missed between a DAG's `start_date` and now — `catchup=True` fills up every run from `start_date` forward the moment the DAG is created or turned on. Both mechanisms lean on the same underlying safety property: each task run is scoped to its own `data_interval_start`/`data_interval_end` window (see [[airflow-scheduling-cron-vs-event-driven]]), so re-running a given day's partition — whether via `backfill` or via `catchup` — produces the same result rather than double-processing data.

Backfilling is not a purely orchestration-layer concern once it actually runs: a 90-day backfill against a DAG normally seeing 10 concurrent tasks a day can suddenly mean 900 tasks trying to run at once, which is exactly the case Vu points to as the reason `max_active_runs` (the DAG-level cap on simultaneous DAG runs) has to be considered deliberately before kicking off a backfill, rather than left at whatever default suits day-to-day operation (see [[airflow-concurrency-and-resource-control]]).

*See also: [[airflow-scheduling-cron-vs-event-driven]] · [[airflow-concurrency-and-resource-control]] · [[orchestration-problem-space]]*
