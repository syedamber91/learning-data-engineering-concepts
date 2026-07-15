---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/i-made-110-in-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: parquet-row-group-parallelism
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

DuckDB has advanced support for Parquet, including the ability to query Parquet files directly rather than always loading them into DuckDB's own storage first — the docs give guidance on which situation calls for which approach.

The parallelism mechanics are specific and worth being precise about: DuckDB can only parallelize *over row groups*. Concretely, DuckDB suggests working with Parquet files with row groups of 100K–1M rows each to achieve better parallelized performance. If a Parquet file has a single giant row group, it can only be processed by a single thread, no matter how many CPU cores are available. DuckDB can also parallelize across the row groups of multiple different Parquet files, not just within one file — so the practical rule of thumb is to have at least as many total row groups across all files as there are CPU threads. For example, on a computer with 5 threads, either 5 files with 1 row group each, or 1 file with 5 row groups, will achieve complete parallelism; what matters is the total row-group count relative to available threads, not how those row groups are distributed across files.

Layout on disk compounds with this: when querying many files, performance can be improved by using a Hive-format folder structure that partitions the data along the columns used in filter conditions — for example, a bucket organized as `s3://bucket_name/country=us/date=2024-01-01`, `s3://bucket_name/country=us/date=2024-01-02`, and so on. A query that only needs `2024-01-02` data will only need to load the prefix that matches, rather than scanning the whole bucket.

*See also: [[duckdb-embedded-analytics-model]] · [[duckdb-vector-formats]]*
