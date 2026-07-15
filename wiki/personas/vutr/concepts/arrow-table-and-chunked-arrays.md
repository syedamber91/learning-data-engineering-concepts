---
persona: vutr
kind: concept
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: arrow-table-and-chunked-arrays
topics:
- apache-arrow
---

A [[record-batch|Record Batch]] is Arrow's unit for representing tabular data — a schema plus a list of arrays, one per column — but it's deliberately not the abstraction users are meant to manage a whole dataset through. That job belongs to the **Table**: a higher-level structure that holds one or more Record Batches (or, more precisely, their underlying array chunks) and presents them as a single, complete dataset, with the constraint that every column in a Table has the same number of rows.

The mechanism that makes a Table more than "a list of Record Batches" is the **Chunked Array**. A Table's column isn't a single Array — it's a Chunked Array, which combines multiple Arrays into one unified view. This is what lets a Table grow without copying: to append new data, you instruct the Chunked Array to include a new pointer to the new array (which can come straight from an incoming Record Batch), rather than rewriting or reallocating the existing data. Vu gives the concrete use case this is built for — a system receiving a stream of Record Batches over time and needing a convenient way to combine them for processing — and credits Arrow's pointer-based design specifically for making that combination cheap, since it avoids excessive data copying.

Vu draws an explicit analogy to Parquet's own hybrid layout: a Table's data is split horizontally into portions the same way a Parquet file is split into row groups, and within each portion the columns sit close together — Record Batches mirroring row groups, Arrays mirroring column chunks. But he's careful to name the one place the analogy breaks: unlike Parquet's row groups, Arrow's Record Batches don't need to stay physically close together in memory. The Chunked Array's pointer-based indirection is exactly what removes that constraint — a Table's chunks can live wherever they were allocated, since the Chunked Array just holds pointers to them rather than requiring contiguous storage across batches.

Neither Record Batch immutability nor Table appendability are in tension: the Record Batch (and each Array within it) stays immutable, and appending to a Table never mutates an existing Array — it only adds a new pointer to the Chunked Array pointing at a new one.

*See also: [[record-batch]] · [[arrow-columnar-array-layout]] · [[apache-arrow]]*
