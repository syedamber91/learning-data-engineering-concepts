---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: pinot-pql
topics:
- apache-pinot-druid-and-real-time-olap
---

PQL is the query language users interact with Pinot's data through — a subset of SQL, modeled around it, but deliberately narrow: it does not support joins, nested queries, DDL, or record-level operations.

The narrowness wasn't absolute from day one, and it moved in the direction of supporting more, not less. Pinot originally couldn't answer queries that only needed metadata rather than actual segment data, such as `SELECT COUNT(*)`. LinkedIn added support for this class of query by changing the planner and introducing a new metadata-based physical operator, without having to touch the underlying architecture more broadly. This reflects a more general property of Pinot's query execution: because different data encoding schemes have different physical operators, new index types and data structures for query optimization can be added by specializing physical operators rather than reworking the engine.

*See also: [[apache-pinot]] · [[star-tree-index]] · [[pinot-broker]] · [[real-time-olap]]*
