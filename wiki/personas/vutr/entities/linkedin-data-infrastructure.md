---
persona: vutr
kind: entity
sources:
- raw/linkedin-data-infrastructure/4-trillion-events-daily-at-linkedin.md
- raw/linkedin-data-infrastructure/datahub-the-metadata-platform-developed.md
- raw/linkedin-data-infrastructure/diving-deep-into-linkedins-data-infrastructure.md
last_updated: '2026-07-15'
qc: passed
slug: linkedin-data-infrastructure
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LinkedIn's real-time infrastructure processes about 4 trillion events daily across roughly 3,000 pipelines for over 950 million users, sitting on top of a historical stack it built mostly in-house: Kafka (built 2010, open-sourced 2011), the in-house Samza streaming engine, Voldemort (2008), Databus, and Espresso (2011) — plus DataHub, which LinkedIn did open-source (2019, evolved from WhereHows, itself open-sourced in 2016).

Rather than replace its Lambda architecture — Samza for streaming, Spark for batch — the way Twitter pivoted its own pipeline fully to Kappa, LinkedIn kept the two-engine split and optimized around it: adopting Apache Beam let a single standardization-pipeline codebase run as either a real-time job or a periodic backfill job, cutting one pipeline's resource use roughly in half (from ~5,000 GB-hours of memory and ~4,000 CPU-hours to ~2,000/~1,700) and its processing time from 7.5 hours to 25 minutes ([[unified-batch-stream-pipelines-via-beam]], [[apache-beam]], [[managed-beam-platform]]).

Beneath the pipelines sits a three-tier service architecture — data tier, service tier, display tier, with the latter two kept stateless for cheap scaling ([[linkedin-three-tier-service-architecture]]). [[voldemort]] is the low-latency key-value "live storage" tier behind products like "Who viewed my profile?"; [[databus]] is the change-data-capture backbone that keeps the Social Graph and search indexes consistent with the primary databases; [[espresso]] is the timeline-consistent document store for read-heavy features like company profiles, itself replicated over Databus. On top of all of it, [[datahub]] is LinkedIn's own metadata catalog, which took three generations — scheduled crawler, then push API, then a real-time, subscribable metadata changelog — to arrive at ([[metadata-catalog-evolution-pull-to-push-to-log]]).

*See also: [[doordash-flink-iceberg]] · [[netflix-batch-pipeline-four-steps]] · [[uber-data-platform]] · [[twitter-kappa-migration]] · [[scribe]] · [[spotify-pubsub-scio]] · [[apache-beam]] · [[managed-beam-platform]] · [[datahub]] · [[voldemort]] · [[databus]] · [[espresso]]*
