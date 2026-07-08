---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: druid-broker
topics:
- apache-pinot-druid-and-real-time-olap
---

The Druid broker maintains an LRU cache but never caches results from real-time nodes, which forces every such query back through the real-time node and guarantees the freshness of the result. During a Zookeeper failure, Druid broker nodes fall back to their last known state.

*See also: [[pinot-pql]] · [[star-tree-index]] · [[apache-druid]] · [[pinot-broker]] · [[apache-pinot]] · [[real-time-olap]]*
