---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-realtime-infra-requirements
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Drawing on Uber's own "Real-time Data Infrastructure at Uber" paper, Vu frames Uber's real-time stack as answering three scaling challenges — scaling data (exponentially growing volume across multiple geographic regions, without sacrificing freshness/latency/availability SLAs), scaling use cases (new requirements emerging as different parts of the org grow), and scaling users (from business users with no engineering background to advanced users building complex pipelines) — against seven concrete requirements: consistency across regions for critical applications, 99.99-percentile availability, second-level freshness for most use cases, sub-1-second p99 query latency for some use cases, scalability with ever-growing volume, low cost for operational efficiency, and flexibility to serve both programmatic and declarative (SQL-like) interfaces for a diverse user base.

To meet those requirements, Uber names seven logical building blocks that recur across its real-time stack, each with its own performance contract: **Storage** provides object/blob storage with read-after-write consistency, optimized for high write rates, and doubles as the source for backfilling/bootstrapping the stream or OLAP layers. **Stream** provides a pub-sub interface optimized for low-latency reads and writes, requiring partitioned data and at-least-once delivery semantics. **Compute** runs computation over the stream and storage layers and likewise requires at-least-once semantics between source and sink. **OLAP** provides limited SQL over data from stream or storage, optimized for analytical queries, requiring at-least-once ingestion (and exactly-once for some primary-key-based use cases). **SQL** is the query layer sitting on top of compute and OLAP — a SQL statement compiles into a compute function applicable to stream or storage, and when layered onto OLAP it extends that layer's native SQL limitations. **API** is the programmatic access path for higher-layer applications into stream or compute functions. **Metadata** is the interface managing metadata across every layer, and it specifically requires versioning and backward compatibility across versions.

This building-block framework is the scaffolding the rest of Uber's real-time stack hangs on: Kafka fills the Stream slot ([[uber-kafka-scale-customizations]]), Flink fills Compute ([[uber-flink-unified-platform]]), Pinot fills OLAP ([[uber-pinot-upsert-mechanism]]), HDFS/S3/GCS fill Storage, and Presto/FlinkSQL/CommonSQL fill the SQL slot ([[uber-presto-deployment-and-query-routing]]).

*See also: [[uber-data-platform]] · [[uber-multi-region-failover-and-backfilling]] · [[uber-realtime-use-case-tradeoffs]]*
