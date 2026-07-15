---
persona: vutr
kind: concept
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: airflow-scheduling-cron-vs-event-driven
topics:
- airflow
---

Scheduling answers "when should the pipeline run," and Vu splits Airflow's answer into two families. Cron scheduling is time-based and is, in his view, all many pipelines need: a daily revenue report at 6am, an hourly refresh of a user-activity table. Airflow accepts either an explicit cron expression (`schedule="0 6 * * *"`) or a preset like `"@daily"`. The detail that matters more than the cron string itself is that Airflow separates *when a task executes* from *what data interval it owns*: every task run carries `data_interval_start` and `data_interval_end`, the exact window the run is responsible for. Vu's example: a daily DAG running on April 5 at 6:00am owns the interval `2026-04-04 06:00:00` to `2026-04-05 06:00:00` — scoping a query to that window means re-running the same logical date always reprocesses the same data, which is what makes retries and backfills safe (see [[backfilling]]). Because Airflow was originally built for ETL over historical batches, the implicit assumption behind cron scheduling is that a given day's data is fully available by the time the next day's run kicks off. The older `execution_date` parameter served a similar role historically but was deprecated since Airflow 2.2 specifically because it didn't clearly define an interval; `data_interval_start`/`data_interval_end` are the modern, recommended replacement.

Cron's blind spot is exactly what event-driven triggering exists to close: cron has no information about the actual state of the data, and a source might only have data available in some narrower window (say, 3:00 to 8:00) that a fixed schedule can't target precisely. Vu names two flavors of event-driven scheduling from his own observation. Actively waiting for an event — a file landing in object storage, a dependent table updating — is handled by [[sensors]]. Being passively triggered by an event — a table insertion firing the pipeline — is handled by [[assets]]. The asset abstraction extends further than file/table freshness: an `AssetWatcher` wrapping a `MessageQueueTrigger` lets a DAG's schedule react directly to an external event stream such as a Kafka topic, and Airflow's REST API offers a still-more-direct escape hatch — an external system (Vu's example is an AWS Lambda function) invoking a specific DAG run programmatically, for cases where neither polling nor an asset declaration is the right shape.

The throughline: cron, sensors, assets, message-triggers, and API-triggers are not competing choices so much as a spectrum from "we know exactly when data is ready" (cron) to "we have to find out" (sensors) to "we get told" (assets, message triggers, API calls) — and a real pipeline typically mixes more than one, as Vu's own dbt+Snowflake example (scheduled manually, then via Orchestra's own trigger options) shows on the [[orchestra|Orchestra]] side of the comparison.

*See also: [[sensors]] · [[assets]] · [[orchestration-problem-space]] · [[backfilling]]*
