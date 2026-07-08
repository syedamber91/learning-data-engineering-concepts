---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: photon
topics:
- spark
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

Photon is a C++ vectorized query engine that plugs into Databricks Runtime as physical operators, using a columnar in-memory representation instead of Spark SQL's row-oriented layout. It applies vectorized execution — the same batch-per-operator-pass technique used by BigQuery and Snowflake — and Databricks deliberately chose the vectorized (interpreted) approach over code generation: weeks to prototype versus two months, and print-debugging native C++ was far more manageable than debugging runtime-generated code. The JNI overhead came out at just 0.06% of execution time. Architecturally Databricks sits in the shared-disk camp alongside BigQuery and Snowflake.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[shuffle-hash-join]] · [[catalyst-optimizer]]*
