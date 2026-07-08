---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: google-napa
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Google Napa is a real-time OLAP system closer in spirit to Apache Pinot or Apache Druid, using materialized views as its main technique and implementing LSM-trees for storage. It exposes a three-way trade-off between data freshness, resource costs, and query performance.
