---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, analytics, olap, compression]
sources:
  - raw/ch04.md
---
# Column-Oriented Storage

Store each column's values contiguously rather than each row's. Analytical queries touch few columns of many rows, so this reads far less data and compresses far better.

See [[Column-Oriented Storage (2e)]] and [[Data Storage for Analytics (2e)]].

## Appears In
- [[Cloud Data Warehouses (2e)]]
- [[Column-Oriented Storage (2e)]]
- [[Data Integration (2e)]]
- [[Data Storage for Analytics (2e)]]
- [[DataFrames (2e)]]
- [[Dataflow Through Databases (2e)]]
- [[Full-Text Search (2e)]]
- [[MapReduce (2e)]]
- [[Multidimensional and Full-Text Indexes (2e)]]
- [[Query Execution - Compilation and Vectorization (2e)]]
- [[Query Languages (2e)]]
- [[Sharding by Hash of Key (2e)]]
- [[Stars and Snowflakes - Schemas for Analytics (2e)]]

## In the vutr data-engineering wiki
- [[parquet]] — the mechanics of the format this page names — row groups, column chunks, pages, and the encodings that make columnar compression pay.
