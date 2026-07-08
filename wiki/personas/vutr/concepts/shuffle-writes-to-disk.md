---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: shuffle-writes-to-disk
topics:
- spark
---

Despite Spark's in-memory reputation, shuffle writes go to disk, not memory — a point people routinely misunderstand. This matters for tuning: the default of 200 shuffle partitions (spark.sql.shuffle.partitions) is applied regardless of data size and must be tuned, and choosing reduceByKey over groupByKey helps because it reduces data before the shuffle rather than after.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[shuffle-hash-join]] · [[catalyst-optimizer]]*
