---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: snowflake
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Snowflake was founded in 2012 by ex-Oracle engineers (Dageville, Cruanes) and Vectorwise co-founder Zukowski, and its processing engine was built from scratch rather than on Hadoop or PostgreSQL. Its storage format resembles PAX (built before Parquet existed), it uses push-based vectorized execution, and it routes cache via consistent hashing — lazy consistent hashing avoids reshuffling when node count changes — with file stealing for work-stealing across nodes. ACID comes from Snapshot Isolation on MVCC tracked in FoundationDB; it is not distributed across AZs by design and does not support partial retries.
