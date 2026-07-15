---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: sensors
topics:
- airflow
---

A Sensor is a special kind of operator whose only job is to wait for a condition — with a configurable timeout — to become true before downstream tasks proceed. It is Airflow's answer to "actively wait for an event to happen," the polling half of event-driven scheduling (the passive half is [[assets]]). `S3KeySensor` waits for a file to land in S3, configured with a `poke_interval` (how often to check, e.g. every 60 seconds) and a `timeout` (when to give up, e.g. after 6 hours). `ExternalTaskSensor` waits for a task in a different DAG to finish. Under the hood, a sensor works by polling — e.g., periodically listing a key in S3 to check for existence — and once the condition is met, the sensor itself is marked a successful task and downstream work runs. A detail Vu calls out specifically: a sensor is still just a task, so it needs its own cron schedule like any other task in the DAG — sensing doesn't replace scheduling, it composes with it.

*See also: [[assets]] · [[airflow-scheduling-cron-vs-event-driven]]*
