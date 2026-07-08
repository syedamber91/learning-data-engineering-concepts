---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: delta-encodings
topics:
- parquet
---

Parquet offers specialized delta encodings for the right data shapes: DELTA_BINARY_PACKED shines on sorted data like timestamps or auto-incrementing keys, while DELTA_BYTE_ARRAY is effective for strings sharing common prefixes. There's also BYTE_STREAM_SPLIT, which reorganizes fixed-width FLOAT/DOUBLE data into byte streams to improve subsequent compression.
