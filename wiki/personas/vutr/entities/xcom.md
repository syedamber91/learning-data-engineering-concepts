---
persona: vutr
kind: entity
sources:
- raw/airflow-additional/apache-airflow-overview.md
- raw/airflow-additional/data-engineering-system-design-orchestration.md
last_updated: '2026-07-15'
qc: passed
slug: xcom
topics:
- airflow
---

XCom ("Cross-Communication") is Airflow's mechanism for tasks to exchange small amounts of data during execution — the standard answer to "task B needs to consume task A's result." One task pushes a value with `xcom_push` (or, more simply, just returns it from its execute method / task function with `do_xcom_push=True`), and another retrieves it with `xcom_pull`, e.g. `context["ti"].xcom_pull(task_ids="task_1", key="key1")`. The default XCom backend stores pushed data in the Metadata Database; for larger payloads, Airflow can be configured to use Object Storage or a custom backend instead. The mechanism is deliberately scoped to small data — it is not a substitute for a real data store, and Vu's examples use it strictly for control values (a row count, a boolean, a small dict of keys) rather than datasets.

*See also: [[trigger-dag-run-operator]] · [[conditional-operators]] · [[orchestration-problem-space]]*
