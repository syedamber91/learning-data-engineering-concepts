---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: physical-layout-partitioning-clustering-and-compaction
topics:
- data-pipeline-design-framework
---

Vu Trinh treats the usage-pattern question — how consumers actually filter and join a served table — as the decision that sets physical layout. Partitioning breaks a table into smaller pieces (say, by date); clustering co-locates similar rows (say, by user_id); both boost query performance, but only for the queries that can actually leverage the spec — filtering on the date partition, joining on the clustered column. The cost is on the write side: writing data into a predefined layout is always slower than writing it naively, because the data has to be organized as it lands. His resulting rule is that any optimization has to justify itself against at least 80% of the queries actually run against the table, or it's paying a write-side tax for nothing.

A second, less obvious cost he names is what frequent inserts do to that layout over time. OLAP systems store data as immutable files, so new data always means new files — the more frequent the inserts, the more (small) files accumulate, and reads have to open more of them to answer a query. Clustering degrades the same way: if data is sorted by user_id, an id's rows start out contiguous within a file, but as new rows for that same id keep arriving, they land in new files and the id's data ends up spread non-contiguously across several.

Compaction is the fix — consolidating many small files into fewer larger ones, restoring the intended sort order, and improving read performance. Cloud warehouses like BigQuery and Snowflake run this automatically in the background, so it's invisible; a self-managed lakehouse built on a table format like Iceberg puts the compaction job on the team operating it.

*See also: [[data-grain-and-serving-storage-shape]] · [[concurrency-and-resource-isolation-in-serving]] · [[safe-writes-and-schema-evolution-in-serving]]*
