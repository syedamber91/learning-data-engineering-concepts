---
persona: vutr
kind: concept
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/partitioning-and-clustering.md
last_updated: '2026-07-15'
qc: passed
slug: partitioning-schemes-across-systems
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

Partitioning divides a dataset into smaller portions so a query can skip the ones it doesn't need. Vu draws a first, easily-missed distinction: **vertical** partitioning is what a column store already does — [[clickhouse|ClickHouse]] splitting each column independently — while the [[pax-hybrid-layout|hybrid PAX format]] (Snowflake, BigQuery, Parquet) is *also* vertically partitioned, just not completely separated, because it groups columns together within row groups first. From that point on, when he says "partitioning" he means the **horizontal** kind: breaking a table into row-based portions at the file level (row groups) and, on top of that, at a higher table level using a column's value — a date column, for instance, breaking a table into `2025-05-01`, `2025-05-02`, and so on, so a filter on the partition key lets the optimizer prune all non-matching partitions entirely.

How that higher-level partition is actually implemented differs sharply by system:

- **BigQuery** treats a partition as a virtual table: data belonging to one partition is stored entirely separately from another's, which is what lets operations like expiration, insertion, and deletion be scoped efficiently to a single partition, each with its own metadata for pruning.
- **ClickHouse** takes the same "independent portion" stance, treating each partition as its own unit that can be written, managed, and queried independently.
- **Snowflake** does not expose a user-managed partition key at all; see [[snowflake-micro-partitions]] for its automatic 50–500MB micro-partition scheme.
- **Redshift** is the outlier in the other direction: Vu notes it does not support (user-defined) partitioning at all.
- Systems where you manage storage yourself typically fall back to a **Hive-style** scheme: each table gets a directory, and each partition a subdirectory underneath it. Newer table formats — Delta Lake, Iceberg, Hudi — still expose this same directory-per-partition shape to users, but layer much more robust metadata behind the scenes to improve pruning and performance versus raw Hive partitioning.

Apache Iceberg goes further with **hidden partitioning**, letting users change a table's partition scheme (e.g. from monthly to daily granularity) without rewriting existing data — Iceberg records every partitioning scheme a table has ever used, so older data keeps its original scheme while new data uses the updated one. See [[iceberg-hidden-partitioning-and-sort-order]] for the full mechanism (it's covered there from Iceberg-specific raw sources in more depth than these posts go into).

**Choosing a granularity is a real trade-off, not a free lunch.** Too coarse a scheme (partitioning by month when queries filter by day) forces the engine to read an entire month's partition to answer a single day's filter. Too fine a scheme creates its own tax: every partition needs its own metadata, so a highly fine-grained scheme (e.g. hourly) means a single day's filter has to consult 24 partitions' worth of metadata, and a whole month's filter touches 720 — more metadata for the query optimizer to read through, which slows planning down, on top of the per-partition management overhead. Partitioning can also introduce **data skew**, where one partition (a big sales day, say) holds far more data than its neighbors. Vu's practical conclusion: understand your organization's actual query patterns before picking a partition column and grain, and know whether your system needs you to manage this at all (Snowflake doesn't require it; BigQuery and Iceberg do, though Iceberg at least lets you evolve the scheme later without a full rewrite).

*See also: [[snowflake-micro-partitions]] · [[clustering-sort-order-and-z-ordering]] · [[pax-hybrid-layout]] · [[dsm]] · [[iceberg-hidden-partitioning-and-sort-order]] · [[partitioning-and-clustering-bigquery]] · [[olap-data-skipping-zone-maps-partitioning-clustering]]*

## Related in the other wiki
- [[Partitioning by Key Range]] — DDIA's general key-range partitioning scheme is the abstract version of the date-column/BigQuery-style partition-as-virtual-table pattern this concept grounds in vutr's specific systems.
- [[Rebalancing Partitions]] — DDIA's chapter on rebalancing cost when partition boundaries shift is the general case of the coarse-vs-fine granularity trade-off (and the data-skew risk) this concept describes for OLAP partitioning specifically.
