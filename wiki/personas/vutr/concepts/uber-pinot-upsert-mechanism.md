---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-pinot-upsert-mechanism
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber uses Apache Pinot as its real-time OLAP layer wherever the requirement is data freshness plus low query latency. In the two years after Uber introduced Pinot, its footprint grew from a few GB to several hundred TB, and query load grew from a few hundred QPS to tens of thousands of QPS. Uber picked Pinot over the 2018 alternatives (Elasticsearch, Apache Druid) after benchmarking: for the same ingested data volume, Elasticsearch used ~4x the memory and ~8x the disk of Pinot, with 2-4x higher query latency across filter/aggregation/group-by/order-by workloads; against Druid — architecturally similar — Pinot's specialized indices (bit-compressed forward indices, star-tree, sorted, range) gave an order-of-magnitude latency advantage in some cases.

Uber's own contribution to Pinot was **upsert** support: the ability to update an existing record or insert a new one if it doesn't exist, needed for cases like correcting a ride fare or updating a delivery status after the fact. The hard part of upsert is locating the record to update. Uber's mechanism splits the input stream into multiple partitions keyed by primary key and assigns each partition to one node, so every record sharing a primary key is always processed by the same node — record identity determines placement, not arrival order. On top of that, Uber built a routing strategy that sends subqueries over segments of the same partition to that same node, keeping the upsert-relevant data and the query execution co-located.

Pinot's other gap at Uber was SQL completeness: it originally lacked subqueries and joins, so Uber integrated it with Presto to let users run standard PrestoSQL against Pinot data ([[uber-presto-deployment-and-query-routing]]). Pinot is also wired into the rest of Uber's data ecosystem — it integrates with Uber's schema service to infer a table's schema (and estimate cardinality) directly from the input Kafka topic, and it integrates with FlinkSQL as a sink, so a user's SQL transformation query can push its output straight into a Pinot table ([[uber-flink-unified-platform]]).

*See also: [[uber-data-platform]] · [[uber-flink-unified-platform]] · [[uber-presto-deployment-and-query-routing]] · [[uber-realtime-use-case-tradeoffs]]*
