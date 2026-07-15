---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/apache-airflow-overview.md
- raw/airflow-additional/where-does-your-task-run-in-apache.md
last_updated: '2026-07-15'
qc: passed
slug: sequential-executor
topics:
- airflow
---

The SequentialExecutor runs tasks one after another, in a single process, on the same machine as the scheduler. It is categorized (per Vu's executor deep dive) as a Local Executor, and is replaced outright by the LocalExecutor in Airflow 3. Its critical operational flaw is that it pauses the scheduler while a task is running, which stops the scheduler from continuously monitoring or queuing new work — a real concern for anything beyond dev/test. It is also the only executor able to run on SQLite as its metadata backend, a choice that lines up with its single-task nature: SQLite doesn't support multiple concurrent connections, so an executor that never runs two tasks at once is the one place that constraint doesn't bite. Its pro is pure simplicity — no external dependencies or complex configuration; its con is that it can't run tasks in parallel at all, which is why Vu frames it strictly as a development/testing tool rather than a production option.

*See also: [[local-executor]] · [[celery-executor]] · [[kubernetes-executor]] · [[airflow-resource-isolation-strategies]]*
