---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: redshift
topics:
- storage-models-nsm-dsm-pax-and-column-store
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Redshift leans on Code Specialization — it generates C++ code specific to a query — which is distinct from the vectorization used by ClickHouse and DuckDB, and it caches compiled code through Compilation-as-a-Service. It is the only OLAP system I am aware of that explicitly uses ML for operations: AutoWLM uses XGBoost to predict query execution time. It also ships AZ64 proprietary compression and AQUA, which pushes FPGAs down to the storage layer.
