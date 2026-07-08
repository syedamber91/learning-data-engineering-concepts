---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: spark
---

Related: [[rdd]] · [[catalyst-optimizer]] · [[aqe]] · [[skew-oom]]

## Comparisons
Sort Merge Join is the preferred strategy; Shuffle Hash Join needs the build side to fit in memory and OOMs on skew. Default shuffle partitions = 200 regardless of data size — see [[aqe]], [[skew-oom]].

## Open questions
- How aggressively should AQE be tuned before manual partition sizing pays off?

## Synthesis
Spark's performance story is [[rdd]] laziness compiled by the [[catalyst-optimizer]], with shuffle-to-disk (not memory) and [[skew-oom]] as the dominant real-world failure mode.
