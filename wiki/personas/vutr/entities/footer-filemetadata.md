---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: footer-filemetadata
topics:
- parquet
---

The footer stores the FileMetadata and is bookended by the magic number 'PAR1'. It's also where Parquet keeps the per-column-chunk min/max statistics that enable data skipping.
