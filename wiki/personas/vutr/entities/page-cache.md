---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: page-cache
topics:
- kafka
---

Kafka delegates storage to the OS kernel page cache, avoiding JVM object overhead and GC pain. Sequential disk access can outperform random RAM access.
