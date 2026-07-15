---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-realtime-use-case-tradeoffs
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Four of Uber's real production use cases, each surfacing a different trade-off inside the same Kafka/Flink/Pinot/Presto stack. **Surge pricing** — a dynamic pricing mechanism balancing driver supply and rider demand — ingests streaming data from Kafka, runs a complex ML-based algorithm in Flink, and stores the result in a key-value store for fast lookup. Its explicit design choice is prioritizing data freshness and availability *over* consistency, because a late-arriving message simply doesn't contribute to the computation — so Uber configures the Kafka cluster for higher throughput rather than lossless delivery.

The **UberEats Restaurant Manager dashboard** lets restaurant owners run slice-and-dice queries over order data (customer satisfaction, popular items, service quality). Because query patterns here are fixed rather than ad hoc, flexibility isn't the priority — freshness and low query latency are. Uber uses Pinot with star-tree indexes to cut serving time, and has Flink pre-compute filtering, aggregation, and roll-ups before Pinot sees the data. The trade-off this surfaces: pre-aggregating in Flink produces optimized, "fixed-shape" data that Pinot serves fast, but that same pre-shaping is exactly what reduces query flexibility at serving time — you're trading transformation-time work for query-time speed.

**Real-time ML prediction monitoring** exists to catch drift or errors in production model output, across thousands of deployed models each with hundreds of features. The dominant requirement here is scalability against high volume and high cardinality; Uber leans on Flink's horizontal scalability to run a large streaming job that aggregates metrics and detects prediction abnormalities, with the job pre-aggregating results as Pinot tables to keep queries fast.

**UberEats Ops Automation** needed ad hoc analytical queries over real-time courier/restaurant/eater data, feeding a rule-based automation framework — notably used during COVID-19 to help the ops team operate under changing regulations. Because this decision-making is business-critical, reliability and scalability dominate: the framework runs Presto on top of Pinot-managed real-time data to pull metrics, aggregates statistics for a given location over the past few minutes, and generates alerts/notifications to couriers and restaurants. Pinot, Presto, and Flink all had to scale with data growth and stay reliable through peak hours.

Read together, these four cases show the same building blocks ([[uber-realtime-infra-requirements]]) being reconfigured differently depending on which requirement — freshness, flexibility, scalability, or reliability — the specific use case values most.

*See also: [[uber-pinot-upsert-mechanism]] · [[uber-flink-unified-platform]] · [[uber-presto-deployment-and-query-routing]] · [[uber-multi-region-failover-and-backfilling]]*
