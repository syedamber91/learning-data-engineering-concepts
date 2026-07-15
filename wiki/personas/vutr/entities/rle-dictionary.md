---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
last_updated: '2026-07-15'
qc: passed
slug: rle-dictionary
topics:
- parquet
---

RLE_DICTIONARY is one of Parquet's most-used encodings. The writer scans a column chunk to build a dictionary of every unique value, stores that dictionary once in a dedicated dictionary page (itself [[plain-encoding|PLAIN]]-encoded), and then rewrites the data page as a stream of small integer indices — each index pointing at a value's position in the dictionary. That index stream is itself highly compressible and gets a second pass of encoding via [[rle-bit-packing-hybrid]].

The catch, stated directly in the source: Parquet's writer *aggressively* applies dictionary encoding to every column type except BOOLEAN — BOOLEAN is encoded with RLE directly instead. The scheme's effectiveness collapses as cardinality rises, so writers implement a fallback: if the dictionary exceeds a size threshold (the source names ~1MB) or the number of distinct values crosses a threshold, the writer switches to a different scheme for the rest of that chunk's pages — for example, the Java Parquet implementation falls back to `DELTA_BINARY_PACKED` for INT32/INT64 columns specifically, even though the official Parquet spec describes PLAIN as the universal fallback. Because a page is the unit of encoding, once fallback triggers mid-chunk, every subsequent page in that chunk uses the fallback scheme, not just the page that tripped the threshold. Some implementations (Rust's, notably) let a caller disable dictionary encoding and specify a column's encoding explicitly instead of relying on the writer's default choice.

The practical implication, per the luminousmen/Vu collaboration piece: dictionary encoding is a strong default for low-cardinality columns (gender, country codes) but its benefit isn't automatic — you shouldn't assume it (or the RLE stage that follows it) "just works" without the data being reasonably sorted or clustered first.

*See also: [[rle-bit-packing-hybrid]] · [[plain-encoding]] · [[delta-encodings]] · [[page]]*
