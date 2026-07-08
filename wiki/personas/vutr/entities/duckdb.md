---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: duckdb
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
- single-node-engines-duckdb-polars-vs-distributed-systems
---

DuckDB is an embedded OLAP database that runs beside your application without a separate DBMS server, much like SQLite does for OLTP. It uses vectorized push-based execution inspired by MonetDB/X100, and I find it exciting precisely because it stands on the shoulders of giants — borrowing components from open-source projects and ideas from scientific publications.

*See also: [[snowflake]] · [[photon]] · [[clickhouse]] · [[redshift]] · [[bigquery]] · [[google-napa]]*
