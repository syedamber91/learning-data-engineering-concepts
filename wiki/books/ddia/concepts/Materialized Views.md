---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, derived-data, analytics]
sources:
  - raw/ch11.md
  - raw/ch12.md
---
# Materialized Views

A query result physically stored and kept up to date, instead of recomputed per
read. Classic case: [[Aggregation - Data Cubes and Materialized Views]] in
analytics. Part III generalizes the idea: caches, search indexes, even application
state are materialized views over an event log, maintained by stream processors
([[Databases and Streams]], [[Designing Applications Around Dataflow]]).

Trade-off: faster reads for slower/more complex writes plus staleness management —
i.e., a form of [[Derived Data]] with all its consistency questions.

## Referenced In
- [[Aggregation - Data Cubes and Materialized Views]]
- [[Batch and Stream Processing]]
- [[Ch 11 - Stream Processing]]
- [[Ch 12 - The Future of Data Systems]]
- [[Column-Oriented Storage]]
- [[Composing Data Storage Technologies]]
- [[Describing Load]]
- [[Materialization of Intermediate State]]
- [[Observing Derived State]]
- [[Part III - Derived Data]]
- [[Processing Streams]]
- [[State, Streams, and Immutability]]
- [[Stream Joins]]
- [[Unbundling Databases]]
- [[Uses of Stream Processing]]
- [[Write Skew and Phantoms]]

## Related in the other wiki
- [[bigquery-internals]] — vutr's notes on Google Napa show this concept as a production serving system's central design choice: materialized views sorted, indexed, and range-partitioned by primary key, maintained through LSM-tree compaction, traded explicitly against ingestion freshness and resource cost to hit sub-millisecond query latency.
- [[sql-fundamentals-and-execution-model]] — vutr's [[materialization-strategies]] note walks through the same trade-off at the single-SQL-engine level: a table stores on every write, a materialized view stores once and executes a defining query then goes stale until refreshed (scheduled, full, or incremental), and a plain view never stores at all and re-executes on every reference — the SQL-specific instance of this concept's general "faster reads for slower/staler writes" trade-off.
