---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
last_updated: '2026-07-15'
qc: passed
slug: layout-over-code
topics:
- parquet
---

The claim, stated plainly in the closing argument of the luminousmen/Vu Trinh collaboration piece: most pipelines run slow not because the code is bad, but because the files are. Wrong [[row-group]] size, poor partitioning, or missing compression can produce jobs that are roughly "5x slower," with nobody realizing why, since the slowness never shows up as a code-review-visible bug — it shows up as a physical-layout decision made once, at write time, that compounds across every later read.

The piece backs this with concrete, specific practices rather than leaving it abstract: pick a row-group size deliberately (its guidance is 128MB-512MB, balancing I/O efficiency against parallelism and skip granularity — a narrower range than the general 128MB-1GB figure elsewhere in the sources, reflecting this piece's specific "avoid small files, but don't over-buffer" framing); choose a compression codec for the actual workload (Snappy for speed, Gzip for ratio, ZSTD as the balanced default); avoid small files altogether, since every file pays fixed overhead in headers, footers, and metadata operations regardless of size — merge them via Spark or Hudi compaction; sort or cluster data before writing, since [[predicate-pushdown|predicate pushdown]] and encodings like [[rle-dictionary|RLE/dictionary]] only pay off on data that's actually ordered, not by default; and reach for a transactional table format (Iceberg, Delta Lake, Hudi) rather than hand-rolling schema evolution, ACID semantics, or time travel on top of raw Parquet files.

The unifying idea across all of these: because the [[pax-hybrid-layout|hybrid layout]] bakes physical decisions (row-group size, sort order, encoding choice) into the file at write time, getting those decisions right once is a higher-leverage lever than optimizing the query code that reads the file afterward — the layout is what the code has to work with, not the other way around.

*See also: [[predicate-pushdown]] · [[row-group]] · [[rle-dictionary]]*
