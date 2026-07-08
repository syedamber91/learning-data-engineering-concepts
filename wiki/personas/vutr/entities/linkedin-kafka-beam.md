---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: linkedin-kafka-beam
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LinkedIn runs 3,000 data pipelines over 4 trillion events daily for 950 million users, and is the birthplace of a remarkable open-source lineage — Kafka (2011), Samza, DataHub, Voldemort, Databus, and Espresso. Adopting Apache Beam cut one pipeline's processing from 7.5 hours to 25 minutes with a 50% memory/CPU improvement, yet LinkedIn deliberately kept its Lambda architecture — unlike Twitter, which pivoted to Kappa.

*See also: [[doordash-flink-iceberg]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[twitter-kappa-migration]] · [[meta-velox-tectonic]] · [[spotify-pubsub-scio]]*
