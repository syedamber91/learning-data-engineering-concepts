---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: sparse-index-and-read-path
topics:
- clickhouse-internals
---

Unlike a B-Tree engine, ClickHouse does not give every record its own index entry. Instead, a table's primary index is **sparse**: a separate `primary.idx` file records the primary-key value of every N-th row, where N is the `index_granularity` (default 8192, the same size as a granule — see [[mergetree-storage-engine]]). ClickHouse's own reasoning for this: with tables expected to absorb millions of row inserts per second, updating an index entry for every single row would make high insertion rates impossible, and the write-side cost of maintaining a full index would be prohibitive. Because the index is sparse, ClickHouse keeps `primary.idx` fully in memory, and it uses binary search over the sorted index to narrow a query down to a candidate granule rather than scanning row by row.

Locating the data inside that granule needs one more piece: for every column, ClickHouse maintains a **mark file** containing one "mark" per granule — a pair of offsets. The first offset points to the start of the compressed block (in the on-disk data file) that holds the granule; the second offset points to the granule's position inside that block once it's decompressed into memory. Mark-file data is cached, so repeated lookups don't re-read it from disk.

Put together, the read path for a query filtering on the primary key looks like this: the query planner uses `primary.idx` to identify which granule(s) could contain the requested value; it then opens the mark file to read that granule's offset pair; it uses the first offset to locate and decompress the relevant block; and it uses the second offset to find the exact granule inside the decompressed block. A worked example: an 8,200,000-row table with `user_id` as the primary key and the default granularity produces 1,000 granules (the last holding 8,000 rows); a query for `user_id = 7543` uses the primary index to find that granule 1 holds the value, then follows the mark-file offsets to fetch and decompress it.

Two refinements sit on top of this base mechanism. **Table projections** let a query planner maintain an alternative copy of a table sorted by a different key — useful when filters target columns outside the main primary key — though by default projections are only lazily built for newly inserted parts, not retroactively for existing ones, unless the user fully materializes them; the optimizer chooses between the main table and a projection based on estimated I/O cost. **Skipping indices** maintain small metadata blocks at the level of consecutive granules to let a query skip rows it doesn't need without a full scan — the min-max index (storing the minimum and maximum of an index expression per index block) is the one form of skipping index the source names explicitly.

*See also: [[mergetree-storage-engine]] · [[clickhouse-insert-process-and-idempotency]]*
