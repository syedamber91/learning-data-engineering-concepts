---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: doordash-flink-iceberg
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

DoorDash processes 30 million messages per second and peaks near 5GB of event data per second, shifting strategy from AWS and third-party services toward open-source with Kafka and Flink as the backbone. It chose Flink for real-time processing — deploying each Flink application as a separate Kubernetes pod — and picked Iceberg over Delta Lake for its more mature Flink integration.

*See also: [[linkedin-kafka-beam]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[twitter-kappa-migration]] · [[meta-velox-tectonic]] · [[spotify-pubsub-scio]]*
