---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: column-chunk
topics:
- parquet
---

A column chunk holds the data for a single column within one row group, and it's the level at which Parquet keeps min/max statistics in the footer. Those per-column-chunk statistics are what power predicate pushdown, letting a reader skip chunks that can't match a filter.

*See also: [[parquet-origin]] · [[rle-dictionary]] · [[footer-filemetadata]] · [[column-by-name]] · [[row-group]] · [[page]]*
