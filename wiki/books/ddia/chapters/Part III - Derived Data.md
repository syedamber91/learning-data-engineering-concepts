---
book: Designing Data-Intensive Applications
type: part-moc
tags: [ddia, derived-data]
sources:
  - raw/partI.md
---
# Part III – Derived Data

Parts I–II assumed a single database; real applications combine many datastores —
OLTP stores, caches, search indexes, analytics systems — and must move data between
them. Part III is about integrating heterogeneous systems into one coherent
architecture.

Its key distinction: **systems of record** (the authoritative, typically normalized
source of truth where new data lands first) versus **[[Derived Data]]** (anything
recomputable from a source: caches, [[Secondary Indexes]], [[Materialized Views]],
recommendation outputs). Derived data is redundant but essential for read
performance, and one source can feed many derived views. The distinction is about
*how you use* a tool, not the tool itself — and making dataflow explicit (which
system consumes whose output) is the running theme of the part.

## Chapters
- [[Ch 10 - Batch Processing]] — Unix philosophy scaled out: [[MapReduce]],
  distributed joins, dataflow engines.
- [[Ch 11 - Stream Processing]] — event streams, [[Log-Based Message Broker]]s,
  [[Change Data Capture]], stream joins and fault tolerance.
- [[Ch 12 - The Future of Data Systems]] — unbundling the database, end-to-end
  correctness, and data ethics.

## Related
- [[Home]] · prev: [[Part II - Distributed Data]]
