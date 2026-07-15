---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-multi-region-failover-and-backfilling
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber runs an **all-active** strategy: services are backed up across geographically distributed data centers so that if one region goes down, the service keeps running from another. The foundation is a multi-region Kafka setup providing data redundancy and traffic continuation. Vu's worked example is dynamic pricing: trip events are sent to a regional Kafka cluster and also aggregated into cross-region clusters for a global view; a Flink job computes pricing per area in each region; each region runs its own update-service instance, and an all-active coordinating service designates one region's instance as primary, whose output gets written to an active/active database for fast lookup. When the primary region has an outage, the coordinating service promotes another region to primary and the calculation fails over there. The one thing that can't simply fail over is Flink's own computation state — it's too large to replicate synchronously between regions, so each region's Flink job computes its state independently rather than sharing it. The trade-off Uber accepts for this resilience is that it's compute-intensive: redundant pipelines must run in every region, not just the active one.

Separately, Uber needs to **backfill** — reprocess a stream from an earlier point in time — for three recurring reasons: a new pipeline needs to be tested against existing data, an ML model needs months of historical data to train on, or a bug in the stream-processing logic requires redoing old data. Uber's Flink-based backfilling solution supports two modes: **SQL-based**, where the same SQL query executes over both the real-time Kafka source and the offline Hive dataset, and **API-based**, which Vu calls the "Kappa+" architecture — the stream-processing logic itself is reused directly against batch data, rather than maintaining a separate reprocessing codepath.

Both mechanisms sit on top of the same building blocks — Kafka as Stream, Flink as Compute ([[uber-kafka-scale-customizations]], [[uber-flink-unified-platform]]) — and both exist because Uber's real-time requirements ([[uber-realtime-infra-requirements]]) demand availability and freshness that a single-region, forward-only pipeline can't guarantee on its own.

*See also: [[uber-realtime-infra-requirements]] · [[uber-realtime-use-case-tradeoffs]] · [[uber-flink-unified-platform]]*
