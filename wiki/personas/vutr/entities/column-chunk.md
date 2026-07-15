---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: column-chunk
topics:
- parquet
---

A column chunk is the data for one column within one [[row-group]], and within a row group the chunks are guaranteed to be stored contiguously on disk. That contiguity is the whole point: because values from the same column sit back-to-back, they tend to be far more homogeneous and repetitive than values from the same row, which is exactly what encoding schemes like [[rle-dictionary]] and compression need to be effective.

Each column chunk is itself further divided into [[page]]s, which are the actual unit of encoding and compression. The chunk's own metadata (ColumnMetadata, recorded in the [[footer-filemetadata|footer]]) tracks the encoding and compression scheme used, the compressed and uncompressed sizes, the offset of the first data page (and first dictionary page, if used), and — for measurable types — the min/max values across the chunk. That min/max is what [[predicate-pushdown]] filters against to decide whether a chunk needs to be read at all.

Parallelism can be assigned at the column-chunk level, not just the row-group level: different workers can read different chunks concurrently within the same row group, on top of different workers handling different row groups of the same file.

*See also: [[row-group]] · [[page]] · [[footer-filemetadata]] · [[predicate-pushdown]]*
