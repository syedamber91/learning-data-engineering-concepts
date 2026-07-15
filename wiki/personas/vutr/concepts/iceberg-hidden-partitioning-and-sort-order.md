---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-7-hours-diving-deep-into.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-doordash-evolve-realtime-processing.md
last_updated: '2026-07-15'
qc: passed
slug: iceberg-hidden-partitioning-and-sort-order
topics:
- iceberg
---

Traditional table partitioning, the kind Hive popularized, forces a specific user burden: partitioning by day usually means transforming a timestamp into a physical `partition_day` column, and users must filter on that exact derived column to get the pruning benefit. Filter on the original `created_timestamp` column instead, out of not knowing the extra column exists, and the query engine falls back to scanning the whole table.

Iceberg's **hidden partitioning** removes that burden by recording only the *transformation* in the table's metadata rather than materializing an extra physical column at all. A user filters on the natural column (`created_timestamp`); the engine reads the recorded transform from metadata and applies it automatically to prune partitions, so partition pruning stops depending on the user knowing about a column that exists purely for technical reasons. This also means Iceberg stores less physical data than a traditional scheme, since no redundant partition column has to be written and kept in sync. DoorDash's own production Iceberg migration confirms this is a real, felt benefit: it's the concrete reason "users feel less confused" once they no longer have to know which column is the internal partitioning key.

A second, related problem hidden partitioning solves is **partition evolution**. Traditional partitioning ties a table's physical file layout to subdirectories matching one partitioning scheme; changing that scheme later means rewriting the whole table. Iceberg instead keeps every historical partitioning scheme a table has ever had in its metadata. If a table was first partitioned by `month(created_timestamp)` and later switched to `day(created_timestamp)`, both schemes coexist: older data stays organized under the monthly scheme, newer data under the daily one, and a query filtering on `created_timestamp` gets *two* separate execution plans generated — one evaluating the filter against each historical scheme — so pruning still works across the boundary without ever rewriting old files.

**Sort order** is a separate, finer-grained lever on top of partitioning. Partitioning narrows which files an engine has to consider; sorting controls how data is arranged *within* those files. The worked example: a table partitioned by day holds data for four cities; without sorting, a query for one city on one day still has to open every file in that day's partition, because that city's rows are scattered across all of them. Sort the data by city first, and that city's rows consolidate into a small subset of files, so the engine can skip the rest. The cost is on the write side — sorting takes extra effort during ingestion, and maintaining a *global* sort across files (not just within each write batch) requires an ongoing compaction job to rewrite and re-sort — which is exactly why choosing a sort order deliberately matters. The recommended approach (attributed to Tabular): put the columns most likely to be filtered on first, ordered from lowest cardinality to highest, and put the highest-cardinality columns (IDs, event timestamps) last.

*See also: [[apache-iceberg]] · [[iceberg-metadata-layer]] · [[doordash-iceberg-realtime-migration]] · [[copy-on-write-vs-merge-on-read]]*
