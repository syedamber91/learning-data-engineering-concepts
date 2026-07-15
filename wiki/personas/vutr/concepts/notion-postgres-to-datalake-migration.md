---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-does-notion-handle-200-billion.md
last_updated: '2026-07-15'
qc: passed
slug: notion-postgres-to-datalake-migration
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Notion's notes trace three distinct architectures for the same underlying problem — getting analytics and ML workloads off a Postgres fleet that was never meant to serve them — and each one broke in a different, specific way as the block count grew past 20 billion toward 200 billion.

Stage one was Postgres serving everything. Before 2021, all of Notion's blocks (its universal unit — see [[notion-block-model]]) lived in a single Postgres instance handling online traffic, offline analytics, and machine learning workloads together. By 2021 that had grown past 20 billion blocks, and Notion sharded the database into 480 logical shards spread across 96 Postgres instances (5 shards per instance) — a scaling move for the operational database, not yet a fix for the analytics problem, since Postgres was still the system of record for every kind of workload.

Stage two, starting in 2021, was Fivetran plus Snowflake: 480 Fivetran connectors, one per shard, wrote hourly snapshots into raw Snowflake tables, which Notion then merged into one big table for analytics and ML. The notes are specific about why this broke down as data grew: managing 480 Fivetran connectors individually was operationally painful; Notion's workload is unusually update-heavy — users edit existing blocks far more often than they create new ones — and that update pattern slowed down and increased the cost of Snowflake ingestion, since Snowflake's ingestion model doesn't specialize for high mutation rates; and consumption itself was getting heavier as AI workloads came online.

Stage three, from 2022, is the in-house data lake Notion built specifically because the update-heavy pattern needed a storage layer designed for mutation, not just append. Postgres changes are captured by a Debezium CDC connector — one connector per Postgres host, deployed on managed Kubernetes (AWS EKS), each handling tens of MB/sec of row changes — and published to Kafka, one topic per Postgres table, with all 480 shards' connectors writing into the same per-table topic. From there, Apache Hudi Deltastreamer (a Spark-based ingestion job) consumes the Kafka messages and writes to S3. Notion chose Hudi specifically because it performs well against update-heavy workloads and integrates natively with Debezium's CDC message format — the two constraints (mutation-heavy data, log-based capture) point at the same table format. Most of the processing on top of the lake is written in PySpark, with Scala Spark reserved for the more complex jobs, and Notion uses multi-threading and parallel processing to handle all 480 shards concurrently.

The payoff the notes report is concrete on three axes: offloading ingestion and compute from Snowflake to S3/Spark saved Notion over a million dollars in 2022 alone, with larger savings in 2023 and 2024; end-to-end ingestion time from Postgres to S3/Snowflake dropped from over a day to a few minutes for small tables and a couple of hours for the largest ones; and the resulting infrastructure is what the notes credit with enabling Notion AI's 2023–2024 rollout, since that feature's analytics and ML demands were exactly what the original Postgres-does-everything design couldn't absorb.

*See also: [[notion-block-model]] · [[spotify-event-delivery-architecture-evolution]]*

## Related in the other wiki
- [[Change Data Capture]] — DDIA's concept of log-based CDC is the general mechanism Notion's Debezium-to-Kafka pipeline is a concrete production instance of.
- [[Databases and Streams]] — DDIA's chapter on turning a database's writes into a stream is exactly the shape of Notion's Postgres-to-Kafka-to-Hudi pipeline.
