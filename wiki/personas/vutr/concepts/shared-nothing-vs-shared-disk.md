---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: shared-nothing-vs-shared-disk
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

OLAP engines split on their storage-compute coupling: shared-nothing systems include ClickHouse, DuckDB, StarRocks, Pinot, Druid, Doris, and Redshift (except RA3), while shared-disk systems include BigQuery, Snowflake, Databricks, and Redshift on RA3 only. Even Snowflake, which separates compute from storage, is internally shared-nothing in its compute layer with local disk that only holds temporary or cache data.

*See also: [[snowflake]] · [[photon]] · [[duckdb]] · [[clickhouse]] · [[redshift]] · [[bigquery]]*
