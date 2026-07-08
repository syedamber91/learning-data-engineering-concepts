---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: cross-az-cost
topics:
- kafka
---

When self-managing Kafka on the cloud, cross-AZ replication transfer can surprisingly account for more than 50% of the total infrastructure bill (per Confluent's observation). This economic pressure is what motivates newer diskless and leaderless designs.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]]*
