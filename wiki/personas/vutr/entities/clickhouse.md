---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: clickhouse
topics:
- storage-models-nsm-dsm-pax-and-column-store
- olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks
---

ClickHouse originated at Yandex for Yandex Metrica (2009 internally, open-sourced 2016), and its MergeTree storage engine is LSM-inspired: data is written in sorted parts and background merges consolidate them. It uses a sparse primary index with one entry per granule (8192 rows by default), the granule being the smallest unit a scan or index lookup processes, plus vectorized execution with opportunistic code compilation. Unlike the PAX layout of BigQuery/Snowflake/Parquet, ClickHouse is true DSM — each column stored separately.
