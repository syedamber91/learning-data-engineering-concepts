---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: airflow
---

Related: [[sequential-executor]] · [[local-executor]] · [[celery-executor]] · [[kubernetes-executor]] · [[sensors]] · [[assets]] · [[pools]] · [[xcom]] · [[airflow-origin]] · [[trigger-rules]] · [[trigger-dag-run-operator]] · [[conditional-operators]] · [[idempotency]] · [[backfilling]] · [[orchestration-problem-space]]

## Comparisons
The executor choice is the central trade-off. [[sequential-executor]] is dev/test only — it pauses the scheduler while a task runs, so it can't queue new work; [[local-executor]] fixes concurrency on one machine but needs MySQL/PostgreSQL. Scaling out, [[celery-executor]] distributes across workers via RabbitMQ/Redis but suffers the Noisy Neighbor problem and underutilized resources when few tasks run, whereas [[kubernetes-executor]] gives the best isolation, scalability, and fault tolerance (plus per-task Python dependencies) at the cost of pod cold starts. Since Airflow 2.10 you don't have to pick globally — you can assign different executors to different tasks in one environment. On reacting to the outside world, [[sensors]] poll for a condition while [[assets]] trigger event-driven between DAGs. On control flow within a DAG, [[conditional-operators]] (BranchPythonOperator vs ShortCircuitOperator) decide whether to route down a branch or skip downstream entirely, while [[trigger-rules]] like all_done decide when a task runs relative to upstream status; to cross DAG boundaries you reach for [[trigger-dag-run-operator]]. For moving state between tasks, [[xcom]] is for small data only, not a substitute for a real data store.

## Open questions
- At what task volume does the CeleryExecutor's Noisy Neighbor problem outweigh the KubernetesExecutor's cold-start cost in practice?
- With per-task executors available since 2.10, what decision rule should govern which tasks get which executor?
- How do you guarantee [[idempotency]] is truly end-to-end across a pipeline rather than just at the final write step?
- Where exactly does [[xcom]]'s 'small amounts of data' limit bite, and what's the right pattern once you exceed it?
- When should cross-DAG composition via [[trigger-dag-run-operator]] be preferred over collapsing the logic into one DAG with [[conditional-operators]]?

## Synthesis
Airflow's design — rooted in its 2014 Airbnb origin ([[airflow-origin]]) — is really about mapping the eight-category [[orchestration-problem-space]] onto concrete levers: executors for resource allocation, [[sensors]] and [[assets]] for data awareness, [[pools]] and priority_weight for concurrency, and [[backfilling]] for historical reprocessing. Dynamic workflows get their own toolkit: [[conditional-operators]] (BranchPythonOperator, ShortCircuitOperator) for runtime routing, [[trigger-rules]] such as all_done for status-relative execution, and [[trigger-dag-run-operator]] for composing across DAGs. The executor spectrum — from [[sequential-executor]] up to [[kubernetes-executor]] — is the axis where isolation and scalability trade against operational cost. But none of it holds up unless every task is idempotent end-to-end ([[idempotency]]), because that's what makes retries, backfills, and reruns safe.
