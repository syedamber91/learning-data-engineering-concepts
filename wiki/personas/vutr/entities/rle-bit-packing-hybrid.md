---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: rle-bit-packing-hybrid
topics:
- parquet
---

The RLE/Bit-Packing Hybrid is how Parquet stores those dictionary indices: when the same value repeats 8 or more consecutive times it uses run-length encoding, otherwise it bit-packs them. BOOLEAN columns skip dictionary encoding entirely and use the RLE scheme directly.

*See also: [[parquet-origin]] · [[rle-dictionary]] · [[footer-filemetadata]] · [[column-by-name]] · [[row-group]] · [[page]]*
