---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: databricks-photon
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Databricks' Photon engine applies vectorized execution, the same batch-per-operator-pass technique used by BigQuery and Snowflake. Architecturally Databricks sits in the shared-disk camp alongside BigQuery and Snowflake.
