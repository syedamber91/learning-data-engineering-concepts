---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: executor-memory-model
topics:
- spark
---

A Spark executor's heap is carved into regions: 300MB is hardcoded as reserved memory, and of what remains, spark.memory.fraction (default 0.6) is the unified pool split between execution and storage. Since Spark 1.6 this pool is unified rather than statically partitioned — execution memory can reclaim storage memory when it needs it (cached blocks get evicted), which is why raising parallelism without raising memory can still starve tasks. This is also the arena where [[data-skew-oom]] plays out: a skewed partition demands more of this pool than one task can be given.
