---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: consumer-offsets-topic
topics:
- kafka
---

The Kafka consumer does not track which messages it has consumed; instead the broker tracks the consume position, stored in the __consumer_offsets topic. This is what lets the broker, not the client, own the message-consume position.
