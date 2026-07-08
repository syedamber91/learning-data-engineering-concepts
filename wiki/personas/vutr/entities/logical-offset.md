---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: logical-offset
topics:
- kafka
---

A message stored in Kafka has no explicit message ID; instead each message is addressed by its logical offset. This deliberately avoids the overhead of maintaining index structures that map message IDs to actual message locations.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[acks-setting]] · [[partition]]*
