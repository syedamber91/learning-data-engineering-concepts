---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: lazy-evaluation
topics:
- spark
---

Spark defers work until it must run it: transformations build a logical plan (a DAG) and nothing executes until an action or output operation is called. This is why a Spark DataFrame is lazy unlike a Pandas DataFrame — each DataFrame is a plan to compute a dataset, not the computed dataset itself, which is exactly what gives Catalyst room to optimize.
