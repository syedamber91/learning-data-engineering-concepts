---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: column-by-name
topics:
- parquet
---

Parquet reads columns by name, not by position. Each column is identified by its name in the schema, so reordering columns is a safe schema-evolution operation — a reader asking for 'price' still finds it regardless of where it now sits in the file. This name-based resolution is a quiet but important robustness property of the format.

*See also: [[parquet-origin]] · [[rle-dictionary]] · [[footer-filemetadata]] · [[row-group]] · [[page]] · [[delta-encodings]]*
