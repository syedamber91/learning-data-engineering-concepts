---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: spotify-pubsub-scio
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Spotify processes 1.4+ trillion data points daily for 640+ million MAUs, and migrated off Kafka 0.8 to Google Cloud Pub/Sub after Kafka 0.8 failed its stress test — the producer had serious stability issues and couldn't self-recover when brokers were removed from a cluster. Along the way Spotify developed Scio, a Scala API for Apache Beam that it later open-sourced.

*See also: [[doordash-flink-iceberg]] · [[linkedin-kafka-beam]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[twitter-kappa-migration]] · [[meta-velox-tectonic]]*
