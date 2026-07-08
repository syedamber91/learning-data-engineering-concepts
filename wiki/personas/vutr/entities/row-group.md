---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: row-group
topics:
- parquet
---

A row group is Parquet's horizontal partition of the data, and inside it the columns are split into column chunks as a vertical partition. I recommend sizing row groups between 128MB and 1GB: smaller groups give you better parallelism but more metadata overhead, while larger ones cut I/O overhead; DuckDB suggests 100K-1M rows per row group as a practical target.

*See also: [[parquet-origin]] · [[rle-dictionary]] · [[footer-filemetadata]] · [[column-by-name]] · [[page]] · [[delta-encodings]]*
