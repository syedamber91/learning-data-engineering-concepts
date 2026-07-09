---
persona: alex
kind: concept
sources:
- vutr/shuffle-hash-join
last_updated: '2026-07-09'
qc: passed
slug: shuffle-hash-join
topics:
- spark
learner: alex
source_note: shuffle-hash-join
mastery: learning
---

Alex (learner): Let me try to say it back so I know I get it. Shuffle Hash Join is a Spark way of joining two tables. It got removed in Spark 1.6 and added back in Spark 2.0. It takes the smaller table (the build side), and for each partition it builds a hash table in memory. But the whole build side of a partition has to fit in memory. If one partition is too big because of skew (uneven data), the worker runs out of memory and errors out. And unlike Sort Merge Join, it can't safely spill to disk to save itself. Did I get that right?

*Source: [[shuffle-hash-join]] (vutr)*
