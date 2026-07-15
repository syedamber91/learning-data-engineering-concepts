---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-twitter-processes-4-billion-events.md
last_updated: '2026-07-15'
qc: passed
slug: twitter-kappa-migration
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Twitter's interaction and engagement pipeline processes 400 billion events in real time and generates a petabyte of daily data. Per a 2021 Twitter engineering blog (as summarized in the notes), Twitter replaced its original Lambda architecture — Summingbird (Scalding batch + Heron stream) writing to Manhattan and Nighthawk respectively — with a single Kappa-style pipeline: on-prem preprocessing into intermediate Kafka topics, Event Processors that convert to Google Pub/Sub representation with UUID-based deduplication tagging, at-least-once publishing to Pub/Sub, Dataflow jobs for deduplication and real-time aggregation, and BigTable as the output sink.

The migration's headline results: latency stabilized at roughly 10 seconds versus 10 seconds–10 minutes under Lambda; throughput reached ~1 GB/s versus a ~100 MB/s ceiling under the old Heron-based pipeline; no event loss on restart (the old architecture lost events whenever it restarted Heron containers to recover from backpressure-induced Stream Manager failures); and more than 95% exact match against the old batch pipeline's results when both were compared via scheduled BigQuery queries, with the ~5% gap attributed to late events the old batch pipeline discarded.

*See also: [[twitter-lambda-to-kappa-pipeline]] · [[spotify-pubsub-scio]] · [[persistent-message-bus-data-transfer]]*
