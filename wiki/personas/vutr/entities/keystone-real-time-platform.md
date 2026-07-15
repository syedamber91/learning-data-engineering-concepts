---
persona: vutr
kind: entity
sources:
- raw/netflix-data-infrastructure/netflix-data-engineer-stack.md
- raw/netflix-data-infrastructure/netflixs-trillions-scale-real-time.md
last_updated: '2026-07-15'
qc: passed
slug: keystone-real-time-platform
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Keystone is Netflix's real-time stream-processing platform for analytics use cases, and its origin story is a rescue mission. By 2015 Netflix had roughly 60 million subscribers, about 500 microservices, and more than 10PB of data generated daily; event volume had grown from 45 billion events/day in 2011 to 500 billion events/day (about 1PB of ingestion) by 2015. The existing batch pipeline — built on Chukwa, Hadoop, and Hive — could no longer handle that volume. With an estimated six-month runway and a six-person team, Netflix delivered a Keystone MVP as a streaming-first replacement, betting that fresher data would cut the developer/operations feedback loop and directly improve product features like personalization and trending.

Architecturally, Keystone abstracts away stream-destination details for producers. Rather than a service specifying where its events go, it outputs to Keystone; behind the scenes, a Kafka topic receives the data, and a Flink application routes it to whatever destination is configured — another Kafka topic, an Iceberg table, or Apache Druid. Keystone also supports using Iceberg tables as its sinks, and that same Iceberg-backed sink doubles as the backfill source when historical reprocessing is needed.

Keystone was explicitly built as the analytics-focused half of Netflix's real-time split — separated from [[mantis-observability-agent]], which handles operational use cases. That separation of concerns (analytics vs. operations, each with different priorities: correctness/predictability for the former, cost-effectiveness/latency/availability for the latter) was one of Netflix's core early strategies, alongside decoupling producers from consumers and dividing the infrastructure into Messaging, Processing, and Control Plane components. See [[netflix-streaming-platform-build-and-failure-recovery]] for the crisis-and-recovery story of Keystone's first year, and [[netflix-simplicity-vs-flexibility-evolution]] for how a dedicated Flink-based platform was later built underneath Keystone to serve custom use cases Keystone's simple abstraction couldn't cover.

*See also: [[mantis-observability-agent]] · [[maestro-workflow-orchestrator]] · [[netflix-streaming-platform-build-and-failure-recovery]] · [[netflix-simplicity-vs-flexibility-evolution]]*
