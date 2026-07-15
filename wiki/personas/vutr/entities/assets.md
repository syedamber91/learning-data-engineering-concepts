---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: assets
topics:
- airflow
---

An Asset is a named logical object — a URI such as `s3://bucket/…` — representing a piece of data. It is Airflow's answer to "passively triggered by an event," the data-aware complement to poll-based [[sensors]]. A task declares that it produces or updates an asset via the `outlets` parameter; a separate DAG declares, via its own `schedule` parameter, that it runs whenever that asset updates. When the producing task finishes successfully, Airflow marks the asset updated and automatically triggers every DAG that depends on it. One asymmetry Vu is explicit about: only DAGs can be triggered by an asset update — a task can carry an `inlets` parameter, but that only gives it read access to information about the named assets, it cannot itself be fired by one. The `@asset` decorator is a shortcut for defining a whole DAG with a single task that updates an asset; critically, each `@asset`-decorated function *is* a DAG, not a task, and you can chain several of them (`schedule=asset_1`, then `schedule=asset_2`, …) to build a complete asset-driven pipeline. The abstraction extends past object storage and tables: an `Asset` can carry an `AssetWatcher` wrapping a trigger such as `MessageQueueTrigger`, letting a DAG's `schedule` react directly to an external event stream like a Kafka topic (`schedule=[kafka_topic_asset]`) — folding message-queue-driven triggering into the same named-asset abstraction as file or table freshness, rather than treating it as a separate mechanism. Beyond assets and sensors, Airflow also exposes direct external triggering via its REST API — e.g., an AWS Lambda function invoking a specific DAG run on demand — for cases that need more direct control than either.

*See also: [[sensors]] · [[airflow-scheduling-cron-vs-event-driven]]*
