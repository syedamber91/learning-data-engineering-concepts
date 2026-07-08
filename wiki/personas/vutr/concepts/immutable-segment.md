---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: immutable-segment
topics:
- apache-pinot-druid-and-real-time-olap
---

Both engines lean on immutable, columnar segments as their storage unit. Immutability is what lets Druid's historical nodes guarantee consistency during reads and parallelize efficiently, and it is why Pinot's segments can be treated as fixed, read-optimized units.

*See also: [[druid-broker]] · [[pinot-pql]] · [[star-tree-index]] · [[apache-druid]] · [[pinot-broker]] · [[apache-pinot]]*
