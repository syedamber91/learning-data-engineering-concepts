---
persona: vutr
kind: entity
sources:
- raw/bigquery-internals/everything-you-need-to-know-about.md
- raw/bigquery-internals/i-spent-4-hours-learning-the-architecture.md
- raw/bigquery-internals/i-spent-8-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: capacitor-file-format
topics:
- bigquery-internals
---

Capacitor is the proprietary columnar file format Google began migrating BigQuery's storage to in 2014 — it's what a load job writes when data lands directly in BigQuery, and it's the read-optimized storage format (ROS) that Vortex's Storage Optimization Service converts write-optimized Fragments into (see [[vortex-storage-engine]]). Google's Big Metadata system also stores BigQuery's own metadata tables (CMETA) in Capacitor, reusing the same columnar machinery for metadata as for data (see [[big-metadata-cmeta]]).

Capacitor layers several concrete performance features on top of plain columnar storage. **Partition and predicate pruning** works by maintaining statistics per column that let the engine rule out entire partitions with no matching rows before touching them. **Skip-indexes** work at a finer grain: at write time, Capacitor groups column values into segments and compresses each one individually, and the column header carries an index of segment offsets, so a highly selective filter can skip straight past segments known to have no hits without ever decompressing them. **Predicate reordering** decides which filter to evaluate first using heuristics over dictionary usage, unique-value cardinality, NULL density, and expression complexity, rather than evaluating filters in the order they were written. **Row reordering** exploits the fact that row order inside a table usually carries no semantic meaning: because run-length encoding (among Capacitor's other value encodings, including dictionary encoding) is very sensitive to how rows are ordered, Capacitor is free to permute rows to make RLE more effective, improving compression.

*See also: [[vortex-storage-engine]] · [[dremel-query-engine]] · [[big-metadata-cmeta]] · [[procella]]*
