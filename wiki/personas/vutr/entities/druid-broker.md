---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: druid-broker
topics:
- apache-pinot-druid-and-real-time-olap
---

Druid's broker nodes route the "right" queries to the historical and real-time nodes that actually hold the needed data. They read Zookeeper metadata to know what segments are queryable and where they live; when a query needs results from both real-time and historical nodes, the broker merges those results before returning them to the caller.

**Caching.** Brokers cache with an LRU strategy, backed by either local heap memory or an external store like Memcached. On a query, the broker maps it to a set of segments and checks whether the results already exist in cache — anything cached doesn't get reprocessed. For results that aren't cached, the broker forwards to the correct nodes: results from historical nodes get cached per segment for future reuse, but results from real-time nodes are never cached. That asymmetry is deliberate — it forces every query touching real-time data back through the real-time node every time, which is exactly what guarantees the freshness of the result.

**Zookeeper dependence and failure handling.** Because brokers depend on Zookeeper for the segment-to-node mapping that routing requires, a Zookeeper failure is a real risk to routing correctness. Brokers handle it by falling back to the cluster's latest known state — the last metadata received before Zookeeper became unavailable — and assuming the cluster hasn't changed since.

*See also: [[apache-druid]] · [[druid-historical-node]] · [[druid-realtime-node]] · [[druid-coordinator-node]] · [[pinot-broker]] · [[real-time-olap]]*
