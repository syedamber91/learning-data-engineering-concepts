---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: zero-copy-sendfile
topics:
- kafka
---

sendfile() cuts context switches from four to two; data is not copied into the Kafka application. Zero-copy means no *unnecessary* copies, not zero copies.
