---
persona: vutr
kind: concept
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: airflow-concurrency-and-resource-control
topics:
- airflow
---

Vu frames the problem plainly: if a set of ready-to-run tasks exists, running them all at once usually shortens the DAG's total duration — but how many is fine? Ten concurrent tasks on a normal daily run is nothing; a 90-day backfill turning that into 900 tasks all trying to run at once overwhelms the scheduler, exhausts worker resources, and can blow through a production database's connection limit. Concurrency control in Airflow is a set of nested knobs, from the whole environment down to a single task.

At the global level, `parallelism` (set via `AIRFLOW__CORE__PARALLELISM`) caps how many task instances can run concurrently on a single scheduler — and because an environment can run more than one scheduler, the true ceiling is `parallelism` × number of schedulers (Vu's own example: `parallelism=20` across 3 schedulers caps the whole environment at 60 concurrent task instances, across every DAG). One level down, `max_active_runs_per_dag` (global default) or its DAG-level override `max_active_runs` caps how many runs of the *same* DAG can be active simultaneously — the parameter Vu explicitly flags as the one to reconsider before kicking off a [[backfilling|backfill]]. `max_active_tasks_per_dag` / `max_active_tasks` caps how many task instances within one DAG run can execute at once, preventing a single DAG from monopolizing every available slot. At the task level, `max_active_tis_per_dag` caps concurrent instances of the *same* task across different DAG runs, and [[pools|Pools]] cap concurrency against a shared external resource regardless of which DAG or task is asking — a `production_db` pool with 5 slots never lets more than 5 queries run against that database at once, and `pool_slots` (default 1) lets one heavy task claim more than one slot in that pool.

Once a pool is full and tasks are queued, `priority_weight` (default 1, higher wins) decides which waiting task Airflow picks next — but the number itself isn't always what gets used. A `weight_rule` decides how that number is actually calculated: `downstream` (the default) makes a task's effective weight its own weight plus the weight of every task downstream of it, so tasks early in the DAG that unblock the most future work get scheduled the most aggressively — favoring overall forward progress across a run. `upstream` is the mirror image: a task's effective weight includes everything upstream of it, favoring finishing DAG runs that are already underway over starting new ones — useful when many runs are queued and you'd rather clear the backlog than spread thin. `absolute` skips graph traversal entirely: the number you set on the task is the number Airflow uses, full stop, for when you already know exactly which tasks matter most.

Vu's worked example threads all of these together: a DAG capped at `max_active_runs=2` and `max_active_tasks=8`, with an `extract_critical` task in a 5-slot `production_db` pool at `priority_weight=10` (jumping the queue whenever the pool fills), a plain `extract_normal` task in the same pool, and a `vendor_api` pool with 3 slots holding a `fetch_large` task (`pool_slots=2`, `priority_weight=5`) alongside a `fetch_small` task (1 slot) — the combined guarantee being that the production database never sees more than 5 concurrent queries, the vendor API never sees more than 3 concurrent calls, the critical extraction jumps ahead of the normal one when the pool is contended, and the heavy fetch's two slots leave room for exactly one small fetch to run alongside it.

*See also: [[pools]] · [[backfilling]] · [[orchestration-problem-space]] · [[airflow-resource-isolation-strategies]]*
