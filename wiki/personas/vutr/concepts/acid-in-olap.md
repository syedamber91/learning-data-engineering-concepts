---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: acid-in-olap
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

ACID keeps surfacing in the OLAP world even though we assume analytics doesn't need it — Snowflake and DuckDB both implement MVCC-based transactions. If ACID were truly unnecessary here, why would open table formats like Delta Lake and Apache Iceberg be developed to make object storage more ACID?

*See also: [[snowflake]] · [[photon]] · [[duckdb]] · [[clickhouse]] · [[redshift]] · [[bigquery]]*
