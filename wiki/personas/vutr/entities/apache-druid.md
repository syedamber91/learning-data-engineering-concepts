---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-druid
topics:
- apache-pinot-druid-and-real-time-olap
---

Apache Druid uses a share-nothing architecture where real-time nodes keep an in-memory index buffer that gets converted to a column-oriented form on disk. Historical nodes then take over the immutable segments, and because they only deal with immutable data they can guarantee consistency during reads and parallelize more efficiently.
