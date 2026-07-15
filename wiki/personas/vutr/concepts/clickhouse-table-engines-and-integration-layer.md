---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-3-hours-learning-the-overview.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-table-engines-and-integration-layer
topics:
- clickhouse-internals
---

ClickHouse's storage layer isn't a single engine — it offers a variety of table engines, split into three categories. The **MergeTree family** ([[mergetree-storage-engine]]) is the primary category, where each variant differs in how it merges rows from its input parts (e.g. `AggregatingMergeTree` aggregates rows, `ReplacingMergeTree` replaces them — see [[mergetree-merge-and-mutation]]). The **special-purpose category** covers engines built to speed up or distribute query execution; the concrete example given is "dictionaries" — in-memory key-value table engines that periodically cache the results of queries run against internal or external data sources. The **virtual table engine** category exists for data exchange with external systems: relational databases (PostgreSQL, MySQL), publish/subscribe systems (Kafka), key-value stores (Redis), table formats (Iceberg, Delta Lake, Hudi), or object storage (S3, GCP).

Sitting above the storage layer, ClickHouse's integration layer decides how external data gets in and out. There are two general approaches to feeding external data into an OLAP database — **push-based**, where a third-party component pushes data in, or **pull-based**, where the database itself connects out to remote sources. ClickHouse uses the pull-based approach. Concretely, this shows up as: 50+ integration table functions and engines for connectivity (MySQL, PostgreSQL, Kafka, Hive, S3/GCP/Azure object stores among them); support for 90+ data formats (CSV, JSON, Parquet, Avro, ORC, Arrow, Protobuf), with some analytics-oriented formats like Parquet integrated deeply enough that the query optimizer can use embedded Parquet statistics to evaluate filters directly on compressed data; and compatibility interfaces that let clients speak to ClickHouse over MySQL- or PostgreSQL-compatible wire protocols, useful when a vendor hasn't built native ClickHouse connectivity yet.

*See also: [[mergetree-storage-engine]] · [[clickhouse-vectorized-parallel-execution]] · [[clickhouse]]*
