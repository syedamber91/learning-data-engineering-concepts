---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: rdd
topics:
- spark
---

The RDD is Spark's foundational abstraction, defined by five properties: a list of partitions, a compute function per partition, a list of dependencies, an optional partitioner for key-value RDDs, and optional preferred locations. RDDs are immutable and lazily evaluated — transformations only build up a DAG, and it's the actions that actually trigger execution.
