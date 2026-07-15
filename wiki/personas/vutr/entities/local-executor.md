---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/apache-airflow-overview.md
- raw/airflow-additional/where-does-your-task-run-in-apache.md
last_updated: '2026-07-15'
qc: passed
slug: local-executor
topics:
- airflow
---

The LocalExecutor advances on the SequentialExecutor by adding parallelism while staying on a single machine — concurrency comes from multiple processes rather than multiple machines. Because real concurrent connections are required, it needs MySQL or PostgreSQL rather than SQLite. It runs in two modes: Unlimited Parallelism (`parallelism == 0`), where a new process is spawned for every submitted task and terminates on completion — a direct, on-demand approach; and Limited Parallelism (`parallelism > 0`, the more common production configuration), where a fixed number of worker processes equal to `parallelism` are pre-spawned at startup and continuously pull tasks from the queue for the executor's whole lifetime. A detail Vu flags explicitly: when an Airflow environment runs multiple Schedulers, each Scheduler runs its own LocalExecutor, so tasks end up distributed across whichever machines the Schedulers live on. Pros are simplicity plus the ability to use multiple CPU cores on the host for higher concurrency than SequentialExecutor; the con is that total task-processing capacity is bounded by the Scheduler machines' own resources — scaling up means adding more Scheduler machines, not just more workers.

*See also: [[sequential-executor]] · [[celery-executor]] · [[kubernetes-executor]] · [[airflow-resource-isolation-strategies]]*
