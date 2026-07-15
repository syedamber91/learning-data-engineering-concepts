---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/its-time-to-replace-parquet.md
last_updated: '2026-07-15'
qc: passed
slug: parquet-origin
topics:
- parquet
---

Apache Parquet came out of a collaboration between engineers at Twitter and Cloudera in the early 2010s, who were looking for a more efficient, higher-performance columnar storage format for large-scale data processing inside the Apache Hadoop ecosystem. It wasn't a green-field design: it was built as an improvement over Trevni, a columnar storage format created by Doug Cutting (the creator of Hadoop) that later folded into Apache Avro. Parquet also deliberately incorporated concepts from Google's Dremel paper to handle complex, nested data structures — the record-shredding technique behind [[definition-repetition-levels]]. The stated goal was an open-source, columnar standard offering superior compression, richer encoding schemes, and better query performance specifically by letting engines read only the columns they need. Apache Parquet 1.0 shipped in July 2013.

Two things about this origin shape everything that follows in the format. First, it committed from day one to the [[pax-hybrid-layout|PAX hybrid layout]] — row groups partitioned horizontally, then columns within each group — rather than a pure column-per-file design, which is why "Parquet is purely columnar" is a common but imprecise description of the format. Second, because it grew out of the Hadoop/HDFS world, its physical defaults (row groups sized 128MB-1GB) were tuned to match large disk blocks and maximize sequential I/O — an assumption that a decade of hardware evolution has since put pressure on (see [[cpu-bound-lakehouse]]).

*See also: [[definition-repetition-levels]] · [[pax-hybrid-layout]] · [[row-group]] · [[apache-avro]]*
