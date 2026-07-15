---
persona: vutr
kind: concept
sources:
- raw/bigquery-internals/i-spent-3-hours-trying-to-figure.md
last_updated: '2026-07-15'
qc: passed
slug: partitioning-and-clustering-bigquery
topics:
- bigquery-internals
---

BigQuery gives users two related but distinct levers for controlling how data is physically organized, both of which ride on top of the storage-set mechanism described in [[immutable-storage-sets-and-dml]]. **Partitioning** divides a large table into smaller parts so a query's filter only has to touch the partitions it needs — Vu's example: filtering a date-partitioned table for `2024-01-01` to `2024-01-15` means only files belonging to those fifteen partitions get read, everything else is skipped. Internally, BigQuery represents each partition by tagging storage sets with an associated partition ID, so the filter can be applied purely at the metadata layer without opening any physical data. Because a partition behaves like its own table internally — data from one partition is stored entirely separately from another's — operations like expiration, insertion, and deletion can all be scoped to a single partition efficiently. BigQuery caps a table at 4,000 partitions; over-partitioning (splitting a table into more physical partitions than is useful) generates proportionally more metadata, which slows the query optimizer down as it has to read through more metadata files.

**Clustering** is a separate, complementary technique: it stores data semi-sorted by a key drawn from up to four columns, so each data file ends up owning a non-overlapping range of that key space. That non-overlapping property is what makes lookups and range scans efficient — the query engine only has to open the files whose range could contain the requested key. Because new data keeps arriving and gets written into new files as usual, the sorted order degrades over time as incoming rows land in ranges that already overlap existing files. BigQuery tracks this drift via a **clustering ratio** — the fraction of data that is still completely clustered — and when that ratio falls too low, it triggers a background **re-clustering** pass that rewrites the affected data in sorted form into a new storage set. Re-clustering, like the base clustering and partitioning mechanisms, is fully automatic; users don't have to trigger or manage it themselves.

*See also: [[immutable-storage-sets-and-dml]] · [[disaggregated-shuffle-service]]*
