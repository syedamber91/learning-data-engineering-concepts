---
persona: vutr
kind: entity
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
- raw/duckdb-polars-single-node-engines/why-single-node-engine-like-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: duckdb
topics:
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
- single-node-engines-duckdb-polars-vs-distributed-systems
---

DuckDB is an embedded, client-server-free analytical database — deliberately following SQLite's philosophy of simplicity, running as a SQL interface beside your application on the same machine rather than as a separate server process ([[duckdb-embedded-analytics-model]]). It runs a vectorized, push-based execution engine — a push model DuckDB adopted after its original pull-based design hit real problems like code duplication and operators that couldn't run separately from the tree plan — and its execution style is directly inspired by the 2005 MonetDB/X100 paper, the same lineage BigQuery, Databricks (Photon), and Snowflake draw on ([[vectorized-execution-engine]], [[push-based-vs-pull-based-dataflow]]). Internally it stores data in its own `Vector` in-memory format, with Flat, Constant, Dictionary, and Sequence physical representations behind one logical array type ([[duckdb-vector-formats]]).

DuckDB has advanced native support for Parquet, including direct querying without loading into its own storage, and it can only parallelize across row groups — 100K–1M rows per group is the recommended sizing for real parallelism ([[parquet-row-group-parallelism]]). It provides full ACID guarantees through a custom, bulk-optimized Multi-Version Concurrency Control implementation, despite being an embedded single-process engine rather than a client-server OLTP system ([[duckdb-acid-and-mvcc]]).

Positioned against the rest of the field, DuckDB is one of the two named engines (alongside Polars) filling the "medium data" gap that neither Pandas/NumPy (small data, GIL-limited) nor Spark/cloud warehouses (built for genuinely large data, with real setup and cost-planning overhead) covered well ([[single-node-engine-market-gap]]). It's also called out as a fascinating example of standing on the shoulders of giants — borrowing components from various open-source projects and drawing on ideas from scientific publications, in a database that can be installed and running without advanced technical knowledge, yet has real depth for anyone who wants to look into its internals.

*See also: [[polars]] · [[pandas]] · [[vectorized-execution-engine]] · [[single-node-processing]]*
