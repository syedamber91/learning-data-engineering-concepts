---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, storage, log-structured, compaction]
sources:
  - raw/ch04.md
---
# LSM-Trees

Log-Structured Merge trees: buffer writes in a sorted in-memory table, flush to immutable sorted files on disk, and merge those files in the background. Write-optimised, and the reason so many modern engines are append-only.

See [[Log-Structured Storage (2e)]] and [[Comparing B-Trees and LSM-Trees (2e)]].

## Appears In
- [[B-Trees (2e)]]
- [[Comparing B-Trees and LSM-Trees (2e)]]
- [[Dataflow Through Databases (2e)]]
- [[Log-Structured Storage (2e)]]
- [[Multidimensional and Full-Text Indexes (2e)]]
- [[Sorting Versus In-Memory Aggregation (2e)]]
- [[Storage and Indexing for OLTP (2e)]]

## In the vutr data-engineering wiki
- [[lsm-tree-storage-engines]] — vutr's engine-level synthesis of the same write path, with OLAP examples the book doesn't reach.
