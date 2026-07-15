---
persona: vutr
kind: entity
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/partitioning-and-clustering.md
last_updated: '2026-07-15'
qc: passed
slug: snowflake-micro-partitions
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

Snowflake takes a different stance on partitioning than the BigQuery/ClickHouse/Hive-style norm described in [[partitioning-schemes-across-systems]]: instead of letting the user pick a column to partition on, Snowflake automatically splits every table into **micro-partitions**, each holding between 50 MB and 500 MB of uncompressed data. Users don't choose or manage the partition boundaries at all — Vu is explicit that "you don't need to care about the partitioning as this cloud data warehouse will automatically handle it for you."

Physically, a micro-partition is organized the same way [[pax-hybrid-layout|PAX]] organizes any hybrid row group: it contains a group of rows, and within that group, each column's data is stored together. Snowflake manages metadata per column within each micro-partition to support pruning and data management — the same min/max-style statistics that make [[oltp-vs-olap-access|Zone Map-style pruning]] work elsewhere, just automated at Snowflake's own physical granularity rather than a user-declared partition key.

*See also: [[pax-hybrid-layout]] · [[partitioning-schemes-across-systems]] · [[clustering-sort-order-and-z-ordering]]*
