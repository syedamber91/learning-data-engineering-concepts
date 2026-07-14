---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/5-insights-to-help-you-learn-any.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-7-hours-diving-deep-into.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-8-hours-relearning-the-delta.md
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-exploring-the-story.md
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
last_updated: '2026-07-15'
qc: passed
slug: copy-on-write-vs-merge-on-read
topics:
- iceberg
---

Every open table format has to answer the same question: data files on object storage are immutable, so what happens when a row changes? The two answers, shared conceptually across Iceberg, Delta Lake, and Hudi, trade off in opposite directions.

**Copy-on-write (CoW)** prioritizes read performance and simplicity. Any UPDATE or DELETE is executed as an atomic file replacement: the engine identifies every data file touched by the change, reads it, applies the change in memory, and writes an entirely new file — the old file is retained only until its retention window passes, then garbage-collected. Reads stay fast and simple (no reconciliation needed at read time, no extra files to track at a given snapshot), but writes get expensive: changing three rows in a file with a million records still means rewriting the whole file, and until the old version is garbage-collected the table effectively holds double the storage for that file.

**Merge-on-read (MoR)** prioritizes write performance instead. Rather than rewriting a data file, incoming changes are written to small, separate files, and the writer commits metadata "registering" those change files against the table's latest snapshot. The actual merge of base data and changes is deferred — either to query time (the query engine reconciles base and delta files on the fly) or to an asynchronous compaction pass that folds changes back into the base files so future readers don't pay the merge cost themselves. MoR write latency is far lower (writing a handful of small records beats rewriting a whole file), at the cost of read-path complexity that compaction timing directly controls: well-compacted tables read as fast as CoW; under-compacted tables force readers to do the merge work themselves.

Each format instantiates this trade-off differently:

- **Iceberg's** MoR uses delete files in two flavors. Positional delete files record *which row positions* to skip — cheap for the reader (skip by position, no comparison needed) but expensive for the writer, which must first read the data file to determine those positions. Equality delete files instead record *which values* were deleted — cheap to write (no read-back needed) but expensive to read, since every record in the data file must be compared against the deleted values.
- **Delta Lake** originally supported only copy-on-write. It later added **deletion vectors** (DV files) as its merge-on-read answer: a DV marks rows in a data file as logically deleted without rewriting that file, and a read that touches a data file with an associated DV must merge the two — skip any row the DV marks — while an update writes only the changed row(s) to a new file plus an updated DV. See [[delta-lake]] for the concrete worked example.
- **Hudi** is structurally MoR-oriented by design: its Base Files (columnar, read-optimized) and Log Files (row-oriented, write-optimized) split the same read/write trade-off into two file kinds inside every File Slice, with `COMMIT` writing straight to base files and `DELTA_COMMIT` writing to log files for later compaction — see [[apache-hudi]] and [[hudi-timeline]].

The performance consequences of this split show up directly in production: Walmart's own benchmark (see [[walmart-hudi-benchmark]]) found Hudi's compaction path faster than Delta's for its streaming ingestion workload, while Delta's Z-ordering (a layout optimization independent of CoW/MoR itself) let it outperform in most of its query benchmarks by roughly a 40% margin.

*See also: [[apache-iceberg]] · [[delta-lake]] · [[apache-hudi]] · [[iceberg-metadata-layer]] · [[hudi-timeline]] · [[occ-on-object-storage]] · [[walmart-hudi-benchmark]]*
