---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: layout-over-code
topics:
- parquet
---

Much of a pipeline's speed comes from the files and their physical layout, not from the processing code. As I like to put it: most pipelines suck not because the code is bad, but because the files are — wrong [[row-group]] size, poor partitioning, or no compression can leave you with jobs that are roughly 5x slower and nobody knows why. Getting layout right (row group size, partitioning, encoding) is usually the higher-leverage lever than tuning the code.
