---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: shuffle-hash-join
topics:
- spark
---

Shuffle Hash Join was removed in Spark 1.6 and reintroduced in Spark 2.0. It requires the build side — the smaller table — of every partition to fit entirely in memory to build its hash table, so if a partition is large due to skew, the executor throws an OutOfMemoryError. Unlike Sort Merge Join, SHJ cannot safely spill to disk.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[catalyst-optimizer]] · [[pyspark]]*
