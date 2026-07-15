---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: trigger-dag-run-operator
topics:
- airflow
---

`TriggerDagRunOperator` lets one DAG explicitly trigger a run of a different DAG — Airflow's answer to cross-pipeline dependencies, where a pipeline needs to wait for or kick off a task that lives in a different pipeline entirely. In practice it's instantiated inside a task function (`TriggerDagRunOperator(task_id=..., trigger_dag_id=..., conf={...}, dag=...)`) and wired downstream of whatever task should cause the trigger (`task_Z >> trigger_dag`). It is the imperative counterpart to [[assets|Asset]]-based DAG-to-DAG triggering: an Asset-scheduled DAG fires automatically and declaratively whenever its named asset updates, while `TriggerDagRunOperator` is an explicit, code-level call made from within a specific task — useful when the trigger condition isn't "this data changed" but "this specific upstream pipeline step just ran."

*See also: [[assets]] · [[trigger-rules]] · [[xcom]]*
