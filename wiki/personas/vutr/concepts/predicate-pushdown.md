---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
- raw/parquet-file-format/its-time-to-replace-parquet.md
- raw/parquet-file-format/why-parquet-is-the-go-to-format-for.md
- raw/parquet-file-format/why-there-are-so-many-parquets-alternative.md
last_updated: '2026-07-15'
qc: passed
slug: predicate-pushdown
topics:
- parquet
---

Column pruning and predicate pushdown are named directly as Parquet's two most obvious analytical advantages. Column pruning is the simpler of the two: because columns are stored in separate [[column-chunk]]s, the engine reads only the columns a query names and skips the rest. Predicate pushdown goes further, pushing the query's filter down to the physical file itself using the min/max statistics every [[column-chunk]] carries in the [[footer-filemetadata|footer]]. A filter for value 5 can skip every row group and every column-chunk page whose recorded min/max range doesn't include 5 — cutting disk I/O and avoiding decompression entirely for the skipped data, rather than reading it and discarding it after the fact.

Mechanically, the read path is: load FileMetadata from the footer, iterate every row group's metadata and test the filter against each relevant column-chunk's min/max statistics, keep only the row groups that could satisfy the filter (or all of them, if no filter is given), then within each surviving row group narrow to the requested columns.

This only pays off under real conditions, not by default. The luminousmen/Vu collaboration piece is explicit that the processing engine (Spark, DuckDB, or whatever else) has to actually be configured to exploit those min/max statistics — writing queries that force full scans with overly dynamic filters defeats it. It also depends on the data being sorted or clustered on the filtered column *before* it's written: pre-sorting on columns frequently used in filters helps predicate pushdown work more effectively and makes encodings more efficient. This is also why table formats built on top of Parquet — Iceberg, Delta Lake, Hudi — centralize and extend exactly this same statistics layer rather than reinventing pruning from scratch.

*See also: [[footer-filemetadata]] · [[row-group]] · [[column-chunk]] · [[parquet-random-access-limitation]]*
