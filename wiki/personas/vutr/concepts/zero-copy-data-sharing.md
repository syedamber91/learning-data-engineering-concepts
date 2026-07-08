---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: zero-copy-data-sharing
topics:
- apache-arrow
---

Before Arrow, each system used its own internal memory format, which wasted many CPU resources on serialization and deserialization every time data crossed a boundary. Arrow's shared columnar format enables zero-copy data sharing between systems, so data can be handed off without being re-encoded.

*See also: [[record-batch]] · [[arrow-flight]] · [[simd-memory-alignment]] · [[apache-arrow]] · [[arrow-ipc]]*
