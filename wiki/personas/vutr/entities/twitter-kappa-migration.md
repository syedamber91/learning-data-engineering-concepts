---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: twitter-kappa-migration
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Twitter handles 400 billion events and 1PB of data daily, and moved from a Lambda architecture (Scalding+Heron) to Kappa (PubSub+Dataflow+BigTable). The payoff was latency stabilized at ~10s and throughput of ~1GB/s versus the old max of ~100MB/s, while still matching 95%+ of the old batch pipeline's results — a clear win in both latency and correctness.

*See also: [[doordash-flink-iceberg]] · [[linkedin-kafka-beam]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[meta-velox-tectonic]] · [[spotify-pubsub-scio]]*
