---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sensors
topics:
- airflow
---

Sensors like S3KeySensor wait for an external condition before letting downstream work proceed. They are Airflow's poll-based way of reacting to the outside world.
