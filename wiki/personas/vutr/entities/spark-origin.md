---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: spark-origin
topics:
- spark
---

Spark was created at UC Berkeley's AMPLab in 2009, born to fix MapReduce's inefficiency for iterative machine-learning algorithms — the kind of workload that reuses the same dataset across many passes, where MapReduce's write-to-disk-between-stages model is punishing. That iterative-ML pressure is why in-memory reuse of the [[rdd]] sits at the heart of Spark's original design.
