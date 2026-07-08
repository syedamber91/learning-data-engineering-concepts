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

Kafka uses zero-copy via sendfile() to cut context switches from four to two, so data never has to be copied into the Kafka application itself. Zero-copy doesn't mean there are no copies at all — it only guarantees no unnecessary ones — and it works because the on-disk data format is kept identical from producer to consumer, avoiding decompress/recompress.
