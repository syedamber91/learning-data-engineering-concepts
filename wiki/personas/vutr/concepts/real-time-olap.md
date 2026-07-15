---
persona: vutr
kind: concept
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: real-time-olap
topics:
- apache-pinot-druid-and-real-time-olap
---

Real-time OLAP names the gap both source posts open with. OLTP systems handle many concurrent transactions with fast response times but aren't built for complex analytical queries; classic OLAP systems handle complex queries over large record counts but offer neither low latency nor high queries-per-second (QPS). Real-time OLAP is what's needed when a use case demands analytical insight, low latency, AND high QPS at once — LinkedIn's example is its "Who viewed my profile" feature, which serves a huge user base at very low latency and high QPS while still being fundamentally an analytical query over event data.

LinkedIn spells out the requirements this forces on a system like Pinot: fast, interactive-level performance — batch tools like MapReduce and Spark have high throughput, but their latency and lack of online processing "limit fluent interaction"; near-linear scalability as concurrent query load grows; cost-effectiveness with an upper bound as data and query volume increase; low data-ingestion latency, meaning users can query recently-added rows without waiting on a batch job, unlike most analytics systems, which can't do single-row ingestion and rely on bulk loads; flexibility, so users aren't boxed into predefined dimensions when drilling down; fault tolerance; uninterrupted operation with no downtime for upgrades or schema changes; and a cloud-friendly architecture.

Both engines answer this with a split between a real-time/fresh path and a durable/historical path, though they draw the line differently. Pinot follows the lambda architecture directly: it ingests online data straight from Kafka and offline data from Hadoop, with the offline half serving as the global view and the online half providing the current view; a query spanning both gets transparently rewritten into two sub-queries divided at a time boundary and merged (see [[offline-realtime-query-merge]]). Druid draws the same kind of split inside its own node types rather than a separate batch system: real-time nodes serve just-ingested data from an in-memory buffer, while historical nodes serve the durable, deep-storage-backed segments once data has been finalized (see [[druid-realtime-node]] and [[druid-historical-node]]).

Underneath both splits is the same architectural bet: immutable, columnar segment storage (see [[immutable-segment]]). It's what lets Pinot route high-throughput, low-complexity queries to data held in memory while placing complex or larger-volume queries on NVMe-backed hardware, and it's what lets Druid's historical nodes guarantee read consistency without coordinating over concurrent writes.

*See also: [[apache-pinot]] · [[apache-druid]] · [[immutable-segment]] · [[offline-realtime-query-merge]] · [[druid-realtime-node]] · [[druid-historical-node]]*
