---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: row-group
topics:
- parquet
---

A row group is Parquet's horizontal partition: it holds a subset of the dataset's rows, and within it each column is stored as its own [[column-chunk]]. Row groups are also the coarse unit of parallelism — different threads or tasks can each read a different row group from the same file concurrently, independent of the finer column-chunk-level parallelism inside a group.

Sizing a row group is a genuine trade-off, not a default to ignore. Larger row groups (the guideline is 128MB-1GB, tuned historically to match large disk blocks like HDFS's) cut I/O overhead, reduce the amount of per-row-group metadata the footer has to carry, and give the encoder/compressor a bigger sample of each column's values to exploit patterns in. Smaller row groups give finer-grained parallelism and finer data-skipping via [[predicate-pushdown]], at the cost of more metadata and less sequential I/O. The catch on the large side: the writer must buffer an entire row group in memory before it can flush any of it to disk — there's no partial-column-chunk flush — so a too-large row group risks memory pressure and out-of-memory failures.

That buffering constraint collides badly with wide or large-valued columns. Back-of-the-envelope: an 8-byte column packed into a 512MB row group holds roughly 64 million rows, but a column with 4KiB values (a plausible size for a vector embedding) only fits about 125,000 rows in the same 512MB. Because more rows-per-row-group is what makes a row group "big enough" to justify its metadata and sequential-I/O cost, a table with large column values ends up needing far more row groups than a table of small scalars — more metadata to manage, more non-sequential I/O, and encoding/compression working over a much thinner sample per row group. Growing the row group size to compensate just pushes the memory-pressure problem back up. The sources call this the row-group constraint, and name it explicitly as a problem for AI feature stores that pack embeddings, documents, or images into a single Parquet column.

This is one of the three axes the newer formats disagree on. [[lance-file-format|Lance]] abandons row groups outright — each column's pages are written independently at their own pace, with no forced row-group alignment across columns. [[nimble-file-format|Nimble]] keeps the row-group concept (so the same sizing tension persists), but moves the footer metadata to the file's end and to FlatBuffers rather than inline Thrift. [[vortex-file-format|Vortex]] takes no fixed position: its layout system can express a Parquet-style row-group layout, a Lance-style no-row-group layout, or (by default) its own adaptive per-column chunking that repartitions to roughly 1MB compressed chunks regardless of row-group boundaries.

*See also: [[column-chunk]] · [[page]] · [[pax-hybrid-layout]] · [[parquet-random-access-limitation]]*
