---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: definition-repetition-levels
topics:
- parquet
---

To encode nested data, Parquet borrows definition levels and repetition levels from Google's Dremel/BigQuery model. These levels are how a flat columnar layout can faithfully reconstruct nested and repeated structures.
