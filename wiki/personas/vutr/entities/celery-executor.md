---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/apache-airflow-overview.md
- raw/airflow-additional/data-engineering-system-design-orchestration.md
- raw/airflow-additional/where-does-your-task-run-in-apache.md
last_updated: '2026-07-15'
qc: passed
slug: celery-executor
topics:
- airflow
---

CeleryExecutor is Airflow's entry into distributed, horizontally scaled execution: it relies on Celery, a distributed task queue, and — unlike the Local executors — separates the workers that actually run tasks from the scheduler machines. The setup needs a message broker (commonly RabbitMQ or Redis), Celery workers, and a non-SQLite metadata database (MySQL/PostgreSQL). Celery workers are long-running processes that continuously pick up tasks, letting more than one task run concurrently on a given worker — but all tasks on that worker share the same Python environment, so dependency conflicts are possible. To scale, you add more machines running Celery workers; to route work, you can define multiple worker groups ("queues") and assign a task to one via its `queue` parameter — e.g. heavy tasks to high-memory workers, GPU tasks to a GPU queue, light tasks to regular workers. Pros: decoupling execution from the scheduler, and horizontal scaling by adding worker machines. Cons: more components than the Local executors means more maintenance overhead; the "Noisy Neighbor" problem, where one heavy task on a shared worker drags down everything else running there; underutilized resources, since a fixed number of workers keeps running even when few tasks are active; and the operational overhead of scaling worker machines up and down.

*See also: [[sequential-executor]] · [[local-executor]] · [[kubernetes-executor]] · [[airflow-resource-isolation-strategies]]*
