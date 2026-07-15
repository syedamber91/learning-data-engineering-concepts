---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/apache-airflow-overview.md
- raw/airflow-additional/data-engineering-system-design-orchestration.md
- raw/airflow-additional/where-does-your-task-run-in-apache.md
last_updated: '2026-07-15'
qc: passed
slug: airflow-core-components
topics:
- airflow
---

Airflow models a workflow as a Directed Acyclic Graph (DAG): Tasks are the nodes (a query, a copy, a script, an API call), and Dependencies are the edges defining execution order. Five components implement that model. The Scheduler parses DAG files, and schedules and queues tasks based on their dependencies and schedule; the executor's own logic runs inside the Scheduler process. The Web Server serves the Airflow UI — visualizing workflows, monitoring task execution, inspecting logs, and triggering DAG runs. The Metadata Database is the central store for DAG definitions, task states, execution logs, and schedules, and is what makes workflow history trackable at all. The DAG folder holds the DAG files users define. Workers execute the tasks the executor assigns them.

Those five pieces cooperate in a fixed six-step cycle. (1) DAG defining: a user writes the DAG — its tasks, logic, start time, and schedule interval. (2) DAG parsing: the Scheduler scans the DAG folder, parses each file, and loads the definitions into the Metadata Database. (3) Scheduling: based on those definitions and their schedule intervals, the Scheduler decides which tasks are ready and queues them. (4) Task execution: the Executor fetches queued tasks and assigns them to available Workers, which execute them while task states get updated in the Metadata Database. (5) Monitoring: the Web Server queries the Metadata Database and renders DAG runs, task statuses, and logs in real time, letting users watch progress, inspect logs, or trigger manual runs from the UI. (6) Retries and state updates: on failure, the Scheduler manages retries per the task's configuration, and the Executor keeps updating task state until everything either finishes or exhausts its retries.

Deployment scales this same architecture in two shapes. On a single machine (`airflow standalone`), every component runs as a separate process (or a separate Docker/Minikube container) on one box — fine for testing and development, but insufficient for production scalability, availability, or fault tolerance. In a distributed deployment, components live independently and redundantly across separate machines (a Scheduler can even run three instances on three machines), and the most common way Vu has observed this done in practice is on Kubernetes — which is also how the managed Airflow offerings from AWS and Google Cloud run it, with DAG files stored in object storage (S3 or GCS respectively).

*See also: [[airflow-origin]] · [[orchestration-problem-space]] · [[sequential-executor]] · [[local-executor]] · [[celery-executor]] · [[kubernetes-executor]]*
