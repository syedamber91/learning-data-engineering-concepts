---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
last_updated: '2026-07-15'
qc: passed
slug: artus-columnar-format
topics:
- google-infrastructure
---

Artus is [[procella|Procella]]'s own columnar data format, built because Procella's first format, Capacitor, was tuned for the large scans typical of analysis workloads but Procella also has to serve fast point lookups and range scans (dashboards, embedded statistics). Artus uses custom encoding that lets it seek a single row without decompressing the surrounding data, which is what makes small point lookups and range scans efficient rather than just large sequential scans.

The format builds its encoding adaptively rather than picking one scheme up front: a first pass over the data collects lightweight statistics (distinct values, min, max, and similar), and that profile determines which of several encodings — dictionary encoding, run-length encoding, delta encoding, and others — gets applied to each column. For sorted columns, Artus chooses encodings that support binary search, giving O(log N) lookups. Its schema representation also departs from the nested/repeated approach used by Capacitor and Parquet: Artus treats a table's schema as a tree of fields and stores each field as its own separate column on disk, rather than the parquet-style shredding of repeated structures. Beyond the raw data, Artus stores encoding metadata, bloom filters, and min/max values alongside the column data itself, so many pruning decisions can be made without reading the actual rows, and it implements inverted indexes and a range of filtering operations directly in its API — pushing computation into the format itself rather than leaving it to a layer above, which the source credits as a source of significant performance gains. Because Artus's on-disk and in-memory representations are identical, it is also what makes Procella's data cache ([[procella-caching-and-affinity-scheduling]]) simple to populate: cached bytes need no transformation before being handed to the query executor.

*See also: [[procella]] · [[superluminal-execution-engine]] · [[procella-caching-and-affinity-scheduling]]*
