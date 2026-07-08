---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: spark
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

Spark is the distributed, multi-node processing framework — and my rule is don't run anything on it when you can process the data on a single machine. For a medium-sized dataset, Spark is simply overkill.

*See also: [[polars]] · [[duckdb]] · [[apache-arrow]] · [[pandas]] · [[single-node-processing]]*
