---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sort-merge-join
topics:
- spark
---

Sort Merge Join is Spark's preferred join strategy and the safest one because it can spill to disk when a partition doesn't fit in memory. In the hint priority order BROADCAST > MERGE > SHUFFLE_HASH, MERGE is the middle ground you fall back to when broadcasting isn't viable.
