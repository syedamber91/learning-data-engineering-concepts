---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: real-time-olap
topics:
- apache-pinot-druid-and-real-time-olap
---

Real-time OLAP is the workload that engines like Pinot and Druid target: keeping hot data in memory for high-QPS simple queries while leaning on NVMe for complex queries over larger data. Immutable, columnar segments are the shared backbone that makes consistent reads and efficient parallelization possible.
