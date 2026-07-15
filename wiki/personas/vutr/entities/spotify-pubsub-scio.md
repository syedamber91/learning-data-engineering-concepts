---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/lets-build-a-data-platform-like-spotify.md
last_updated: '2026-07-15'
qc: passed
slug: spotify-pubsub-scio
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Google Cloud Pub/Sub is the reliable, persistent queue Spotify adopted for event delivery after Kafka 0.8 failed its stress test in 2015 — the notes describe Kafka 0.8's producer as having serious stability issues, entering an unrecoverable state if an admin removed brokers from the cluster, with Mirror Maker only mirroring cross-datacenter data on a best-effort basis. Pub/Sub, by contrast, is globally available, exposes a simple REST API, retains undelivered data for seven days, and is fully managed by Google — freeing Spotify from the operational overhead of running its own broker. Spotify validated it directly: a producer test at 2 million events/second published without service degradation and almost no server errors, and a consumer test pulling batches of 1,000 messages held median end-to-end latency around 20 seconds with no observed message loss.

Scio is the Scala API for Apache Beam that Spotify built after this migration, to run its Google Dataflow streaming jobs — Spotify later open-sourced it. Together, Pub/Sub as the queue and Scio/Dataflow as the processing layer replaced Kafka 0.7/0.8, HDFS, and MapReduce in Spotify's event delivery pipeline.

*See also: [[spotify-event-delivery-architecture-evolution]] · [[twitter-kappa-migration]]*
