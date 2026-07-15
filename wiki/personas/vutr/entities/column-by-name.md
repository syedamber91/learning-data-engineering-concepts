---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/file-formats-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: column-by-name
topics:
- parquet
---

Parquet resolves columns by name rather than by position, and that one design choice is what makes several schema changes safe to apply without rewriting existing data. Adding a new column is the safest and most common change: old files simply return `null` for the new column when queried. Removing a column is nearly as safe — the client just stops selecting it; the old data stays physically present in old files but is ignored, and skipping it is cheap precisely because of the columnar layout. Reordering columns doesn't matter at all, since the reader looks columns up by name rather than by their position in the file. Renaming a column is the one case that looks safe but isn't quite what it seems: because resolution is by name, a rename is effectively the same operation as deleting the old column and adding a new one — the query engine sees two distinct columns, not one column that changed its label.

*See also: [[parquet-origin]] · [[footer-filemetadata]] · [[row-group]]*
