---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: kraft
topics:
- kafka
---

KRaft eliminated ZooKeeper from Kafka, folding metadata management into Kafka itself. It removes the external coordination dependency the cluster previously relied on.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]]*
