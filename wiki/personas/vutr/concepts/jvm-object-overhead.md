---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: jvm-object-overhead
topics:
- spark
---

The JVM's object model is expensive: a 4-byte string occupies over 48 bytes as a JVM object once headers, padding, and references are counted. That roughly 10x blow-up is why Spark's in-memory footprint balloons far beyond the raw data size, and it's the motivation behind off-heap, columnar, code-generated execution — Project Tungsten and, further out, [[photon]]'s columnar C++ representation — that sidesteps the per-object JVM tax entirely.
