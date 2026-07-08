---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: tiered-storage-kip-405
topics:
- kafka
---

KIP-405 (Tiered Storage, proposed by Uber) splits storage into a local tier for recent data and a remote tier (HDFS/S3/GCS) for historical data. Importantly, the broker remains stateful — tiered storage does NOT make Kafka brokers stateless.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]] · [[partition]]*
