---
persona: vutr
kind: concept
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: offline-realtime-query-merge
topics:
- apache-pinot-druid-and-real-time-olap
---

When a Pinot query needs data that spans both the offline half of a table (Hadoop-backed, serving as the global view) and the online/real-time half (Kafka-backed, serving the current view), Pinot doesn't answer it against some unified view of the data — it transparently rewrites the incoming query into two separate queries. One is scoped to the offline part, covering data before a time boundary; the other is scoped to the real-time part, covering data at or after that boundary. Each half runs independently, and Pinot merges the two result sets before returning a single answer to the caller.

The source's own worked example: a hypothetical table with two segments per day might have overlapping data for August 1st and 2nd. A query that spans that overlap gets split at the time boundary into an offline query and a real-time query rather than deduplicated after the fact — the split happens before execution, not after.

This is the concrete query-time mechanism behind Pinot's lambda-architecture design (see [[real-time-olap]] and [[apache-pinot]]): the offline/online split isn't just a decision about where data gets ingested from, it's something the query planner has to actively reconcile on every query that crosses the time boundary between the two halves.

*See also: [[apache-pinot]] · [[real-time-olap]]*
