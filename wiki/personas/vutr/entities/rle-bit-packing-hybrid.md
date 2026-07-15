---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: rle-bit-packing-hybrid
topics:
- parquet
---

The RLE/Bit-Packing Hybrid scheme reads a stream of integers and dynamically switches between two modes depending on what it finds. For a run of identical, consecutive values, it uses Run-Length Encoding: the value is stored once alongside a count of its repetitions (so `[5, 5, 5, 5, 5]` becomes "store 5, five times"). For a run of varying integers, it uses bit-packing instead: each integer is stored using only the minimum number of bits its range of values actually requires, rather than a fixed 32- or 64-bit width — if a run of numbers never exceeds 7, 3 bits is enough, and using a full integer width would be wasteful. In a stream, the writer switches to RLE once it sees the same value repeat 8 or more consecutive times; otherwise it bit-packs.

The scheme is used in three specific places in Parquet: encoding the definition- and repetition-level integer streams that carry [[definition-repetition-levels|nested/repeated structure]]; encoding the integer indices produced by [[rle-dictionary]]; and encoding BOOLEAN values directly (since BOOLEAN columns skip dictionary encoding entirely).

*See also: [[rle-dictionary]] · [[definition-repetition-levels]] · [[plain-encoding]]*
