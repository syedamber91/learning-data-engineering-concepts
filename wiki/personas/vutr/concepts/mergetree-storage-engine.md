---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-3-hours-learning-the-overview.md
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: mergetree-storage-engine
topics:
- clickhouse-internals
---

MergeTree is the primary table-engine family in ClickHouse, and its shape follows directly from one design goal: accept a very high, bursty ingestion rate without paying an indexing tax on every row. Based on the idea of LSM-trees (though not 100% the same), a MergeTree table stores its data in horizontally divided, immutable portions called "parts." Each insertion — or each buffered batch of inserts — forms a new part rather than being merged into existing storage immediately. A dedicated background thread later merges smaller parts into larger ones, which is what keeps read operations from having to open and close an ever-growing number of small files. Within a part, data is stored in primary-key (or sort-key) order and organized column by column: MergeTree stores each column independently, so the "columnar" split here is purely vertical — a different arrangement than the row-group-then-columns approach used by Parquet, DuckDB, Snowflake, or BigQuery.

Small parts create a secondary problem: if every column of a small part is written to its own file, per-column file overhead can hurt read/write performance. MergeTree resolves this with two on-disk column formats. **Wide** format writes each column to its own file (`column_name.bin`), which is the default for larger parts. **Compact** format, used by default for parts smaller than 10 MB, stores all columns consecutively in a single file (`data.bin`) to increase spatial locality for small reads and writes.

On disk, a part corresponds to a directory whose name encodes a version and a **level**. A newly created part starts at level 0. Parts can only merge with other parts holding adjacent block numbers, and when parts of the same level merge, the resulting part's level becomes `original_level + 1` — the original parts are deleted once no query still holds a reference to them (reference count reaches zero). If an `ALTER TABLE` has modified a part, its directory name also carries a version marker.

Beneath the part/column split sits a finer unit: a part's column data is logically divided into **granules** of a configurable size (default 8192 records) — the smallest unit the scan and index-lookup operators process (see [[sparse-index-and-read-path]] for how granules are addressed). Physically, though, disk reads and writes happen at the **block** level, not the granule level: a block combines several neighboring granules, sized by a configurable byte target (default 1 MB — the exact granule count per block depends on the column's data type and distribution), and is compressed before storage (LZ4 by default, with alternatives like Gorilla or FPC available for specialized data). ClickHouse is explicit that "block" is an overloaded term: this on-disk/compression block is distinct from the in-memory block used during query processing, which is simply a set of table rows passed between operators.

Finally, MergeTree tables can be partitioned — by range, hash, round-robin, or a custom expression. When a table is partitioned, ClickHouse stores the partitioning expression's min/max value per partition, which lets a query prune whole partitions it doesn't need to scan.

*See also: [[sparse-index-and-read-path]] · [[mergetree-merge-and-mutation]] · [[clickhouse-replication-and-keeper-consensus]] · [[clickhouse]]*
