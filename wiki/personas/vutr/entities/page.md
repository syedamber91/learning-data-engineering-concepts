---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: page
topics:
- parquet
---

The page is the smallest data unit in Parquet, and it comes in three flavours: data pages, dictionary pages, and index pages. This is the layer few people look at, but it's where the actual encoding and compression happen.
