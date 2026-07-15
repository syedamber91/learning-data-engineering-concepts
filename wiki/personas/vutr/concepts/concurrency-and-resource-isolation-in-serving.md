---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: concurrency-and-resource-isolation-in-serving
topics:
- data-pipeline-design-framework
---

Vu Trinh's starting point is that OLAP serving rarely deals with the raw concurrent-user counts an OLTP system backing a worldwide app does — a data warehouse is mostly used internally. But he argues the concurrency question still matters, because it's really a resource-contention question in disguise: one query running alone gets all of a system's resource A, but a thousand queries running at once share A — and under a naive FIFO scheduler, one giant query can take everything and leave every other query waiting. Most systems also cap the number of concurrent queries outright; exceed it and your query gets abandoned rather than queued.

His mitigations, roughly in order of first resort: most cloud warehouses handle moderate concurrency fine as long as you track your concurrency quota; reduce the workload of any single query so it finishes faster and frees its "slot" sooner, via pre-aggregation or caching (the warehouse's own cache, a materialized view, or client-side caching); isolate resources into pools so a heavy query can't starve a light one; and, for the rare case of a genuinely user-facing analytics application (his example: a LinkedIn-style profile view) rather than internal analytics, reach for a specialized engine built for that scale, like Apache Pinot or ClickHouse.

*See also: [[physical-layout-partitioning-clustering-and-compaction]] · [[batch-vs-stream-throughput-and-latency]] · [[data-grain-and-serving-storage-shape]]*
