---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: bigquery
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

BigQuery is built on Google's stack: Colossus for storage, Borg for compute, Dremel as the query engine, and a dedicated shuffle service, with the proprietary Capacitor columnar format and CMETA centralized metadata also stored column-oriented via Capacitor. For me the most exciting part is Dremel's dynamic query plans, which are adaptable at runtime because the shuffle layer makes workers stateless and a centralized scheduler observes the whole cluster. Note that BigQuery only supports hash joins, and each unit of work is atomic and idempotent.

*See also: [[snowflake]] · [[photon]] · [[duckdb]] · [[clickhouse]] · [[redshift]] · [[google-napa]]*
