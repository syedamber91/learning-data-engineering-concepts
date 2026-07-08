---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: delta-lake
topics:
- iceberg
---

Delta Lake achieves Atomicity through a put-if-absent conditional write into the _delta_log directory, but that OCC path limits throughput to only several transactions per second. It introduced deletion vectors as an alternative to full copy-on-write rewrites, and its Z-ordering skips at least 43% of objects (54% on average). It is more Spark-centric than Iceberg.

*See also: [[iceberg-metadata-layer]] · [[hudi-index]] · [[apache-iceberg]] · [[conditional-writes]] · [[hudi-timeline]] · [[open-table-formats]]*
