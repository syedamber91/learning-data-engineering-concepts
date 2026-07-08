---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: star-tree-index
topics:
- apache-pinot-druid-and-real-time-olap
---

The star-tree index is Pinot's structure for holding pre-aggregated results. Together with bit-compressed forward indices, it is what gives Pinot an order-of-magnitude latency advantage over Druid.
