---
persona: vutr
kind: entity
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
- raw/uber-data-infrastructure-case-studies/ubers-big-data-revolution-from-mysql.md
last_updated: '2026-07-15'
qc: passed
slug: uber-data-platform
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber serves 137 million monthly active users across 10,000 cities with 25 million trips daily, and data isn't just for reporting — it powers rider safety, ETA predictions, and fraud detection directly. To do that at "trillions of messages and petabytes of data per day" through one of the largest Kafka deployments in the world, Uber built its data architecture as a lambda split into two parallel paths from the same 10,000-foot view. The stream path has Flink consuming from Kafka, processing in real time, and sinking to Pinot for real-time analytics served through a custom SQL layer on Presto. The batch path has Spark consuming from the same Kafka topics and writing to a data lake backed by HDFS, Apache Hudi, and Apache Hive, with data transformed to the lake's predefined model before Presto serves it. The open-source stack — Kafka, HDFS, Hudi, Spark, Flink, Pinot, Presto — is the constant; what has changed is how it's operated. In 2023 Uber moved all batch workloads onto Spark across 20,000+ critical pipelines (the Sparkle framework standardized how), and in 2024 the company began migrating its batch stack — HDFS incrementally replaced by object storage — to Google Cloud Platform ([[uber-gcp-batch-migration]]).

This dual-path architecture is also the setting for [[uber-multi-region-failover-and-backfilling|Uber's all-active multi-region strategy]] and for the specific real-time [[uber-realtime-use-case-tradeoffs|use cases]] — surge pricing, the UberEats Restaurant Manager dashboard, ML prediction monitoring, ops automation — that stress-test the stream side, while the batch side is where [[uber-data-platform-evolution|the platform's four generations]] and [[uber-hudi-etl-pipeline-and-impact|Hudi's incremental ETL]] play out.

*See also: [[uber-flink-unified-platform]] · [[uber-pinot-upsert-mechanism]] · [[uber-presto-deployment-and-query-routing]] · [[uber-kafka-scale-customizations]] · [[uber-data-platform-evolution]] · [[uber-realtime-infra-requirements]]*
