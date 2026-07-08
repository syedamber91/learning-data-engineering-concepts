---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: rle-dictionary
topics:
- parquet
---

RLE_DICTIONARY is Parquet's default and most commonly used encoding: unique values go into a dedicated dictionary page (PLAIN encoded), and the data pages then store integer indices via the RLE/Bit-Packing Hybrid. Here is the catch — Parquet aggressively applies it to every column type except BOOLEAN, and if the dictionary grows past a size threshold (e.g. 1MB) the writer falls back to another encoding.
