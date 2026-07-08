---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: uber-lambda-kafka
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber serves 137 million monthly active users and 25 million daily trips on one of the largest Apache Kafka deployments in the world — trillions of messages and petabytes of data per day. Its Lambda architecture pairs a stream path (Flink→Pinot→Presto) with a batch path (Spark→HDFS/Hudi/Hive→Presto), and in 2023 Uber moved all batch workloads to Spark across 20,000+ critical pipelines before starting a Google Cloud migration in 2024. The batch pain is real: because Uber can't know if a driver's earning data changed, it must assume 'data was changed in the last X days' and reprocess all X partitions.
