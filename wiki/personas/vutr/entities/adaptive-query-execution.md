---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: adaptive-query-execution
topics:
- spark
---

AQE landed in Spark 3.0 (2020) and re-optimizes a query at runtime: it coalesces shuffle partitions, switches join strategies on the fly, and handles skew joins. The trick is that a shuffle or broadcast exchange creates a query stage boundary — that pause is exactly what gives Spark the chance to re-optimize with real statistics.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[shuffle-hash-join]] · [[catalyst-optimizer]]*
