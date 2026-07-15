---
persona: vutr
kind: concept
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: airflow-failure-handling-and-retries
topics:
- airflow
---

Failures are inevitable, in Vu's framing — an API server goes down, a source database is overloaded — and when a task in a pipeline fails, three things need to happen automatically: it needs to be retried with the right setup (without piling more load on an already-overloaded source), terminated if it runs too long, and reported to whoever owns the pipeline. Airflow's levers for the first two are `retries` (how many attempts), `retry_delay` (the wait between attempts), `retry_exponential_backoff` (whether that delay grows with each attempt), and `execution_timeout` (kill anything that runs longer than expected). All four are configurable at the DAG level via `default_args`, and any task can override them individually — Vu's example sets DAG-wide defaults of 2 retries and a 1-minute delay, then gives one specific task 5 retries, a 2-minute delay, and its own 1-hour timeout. `on_failure_callback` handles the third requirement, running arbitrary logic — Vu's example sends a Slack-style alert naming the failed `task_id` and the exception — the moment a task fails.

What happens after retries are exhausted is a hard rule, not a configurable one: Airflow marks every downstream task `upstream_failed` and skips it. That default is exactly what [[trigger-rules|`trigger_rule="all_done"`]] exists to override — a cleanup or notification task that must run regardless of whether its parents succeeded or failed has to opt out of the default all-must-succeed rule explicitly.

Failure detection also has a dimension retries alone don't cover: a DAG that is still technically running, not failed, but has blown its time budget. A `DeadlineAlert` — built from a `DeadlineReference` (Vu's example is `DAGRUN_QUEUED_AT`) and an `interval` — fires a callback if the DAG hasn't finished within that window of being queued; the callback itself can be an `AsyncCallback` wrapping something like a `SlackWebhookNotifier`, so an SLA miss produces the same kind of alert a hard failure would, even though nothing technically errored.

*See also: [[trigger-rules]] · [[conditional-operators]] · [[orchestration-problem-space]]*
