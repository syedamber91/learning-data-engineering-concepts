---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: vectorized-vs-code-compilation
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Two rival execution strategies show up across these engines: vectorized execution moves a batch of multiple values per operator pass (ClickHouse, Snowflake, DuckDB, BigQuery, Databricks Photon), while code compilation / JIT writes a fresh program per query and compiles it to machine code (Redshift and Spark). Redshift's Code Specialization is the compilation branch; the vectorized branch traces back to VectorWise/MonetDB/X100.

*See also: [[snowflake]] · [[photon]] · [[duckdb]] · [[clickhouse]] · [[redshift]] · [[bigquery]]*
