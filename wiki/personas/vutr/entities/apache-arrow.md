---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-arrow
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
- apache-arrow
---

Apache Arrow is an in-memory columnar data format project that began in February 2016. Unlike Parquet or CSV, which specify how data is organized on disk, Arrow focuses on how data is organized in memory. Its arrays and Record Batches are immutable, so concurrent access is safe by design.
