---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: parquet-write-read-process
topics:
- parquet
---

The write path, laid out consistently across the sources: the writer first collects schema, null-appearance, encoding-scheme, and column-type information to populate [[footer-filemetadata|FileMetadata]]; writes the magic number at the file's start; calculates the number of [[row-group]]s from the configured max row-group size versus the data's total size, and decides which rows go into which row group. For each row group, the engine iterates through the column list and writes each [[column-chunk]] — buffering the *entire* row group in memory before any of it is flushed to disk, since a partial column chunk can't be written independently. Writing a chunk means computing rows-per-[[page]] from the max page size, computing min/max statistics for measurable types, then writing pages sequentially, each with a header recording row count and its value/definition/repetition encoding; if dictionary encoding is used, the dictionary page (with its own header) precedes the data pages. After a chunk's pages are all written, the writer records that chunk's metadata (min/max, compressed/uncompressed size, first data-page and first dictionary-page offsets) into the row group's metadata. Once every row group is written, all row-group metadata is collected into FileMetadata, written to the footer, and the file closes with a final magic number.

The read path mirrors this. The reader checks the magic number at both ends to confirm validity, reads and deserializes FileMetadata to get the schema and row-group metadata, and — if filters are given — checks every row group's column statistics against the filter to build a candidate row-group list (or includes all row groups if no filter applies, per [[predicate-pushdown]]). It defines the column list from whatever the query actually requested, then iterates the candidate row groups: for each, it reads only the needed column chunks, using ColumnMetadata to locate the first page's offset, then reads pages sequentially — tracking rows read against the chunk's total row count to know when a chunk is exhausted — decoding each page using the encoding information in its page header.

This two-level structure (row groups, then column chunks within them) is exactly what makes Parquet's parallelism story work at two granularities simultaneously: separate files can be read concurrently by different threads, and within one file, separate row groups or separate column chunks within a row group can each be assigned their own worker.

*See also: [[row-group]] · [[column-chunk]] · [[page]] · [[footer-filemetadata]]*
