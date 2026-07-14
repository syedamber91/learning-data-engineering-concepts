---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Column-Oriented Storage
type: subtopic
tags: [ddia, compression, bitmap-encoding, vectorized-processing, column-store]
sources:
  - raw/ch03.md
---
# Column Compression
> Columns full of repetitive values compress spectacularly — bitmap and run-length encoding shrink billions of rows into kilobytes and let queries run as raw bitwise math.

## The Idea
Reading only the needed columns already slashes disk I/O; compressing those columns slashes it again. Column files are ideal compression targets because values from a single column look alike — a column typically has far fewer distinct values than rows (billions of sales, only ~100,000 distinct products).

## How It Works
- **Bitmap encoding:** for a column with *n* distinct values, build *n* bitmaps — one per distinct value, one bit per row, set to 1 where the row holds that value.
- When *n* is small (a country column: ~200 values), store bitmaps directly at one bit per row. When *n* is large, most bitmaps are sparse (mostly zeros), so apply **run-length encoding** on top, yielding remarkably compact columns.
- **Queries become bit arithmetic.** `WHERE product_sk IN (30, 68, 69)` → load three bitmaps, bitwise OR. `WHERE product_sk = 31 AND store_sk = 3` → load two bitmaps, bitwise AND. This works only because every column file stores rows in the same order, so bit *k* means row *k* everywhere.
- **Vectorized processing:** compression pays off inside the CPU too. Analytical engines worry not just about disk-to-memory bandwidth but memory-to-CPU-cache bandwidth, branch mispredictions, pipeline bubbles, and SIMD utilization. A chunk of compressed column data can sit in L1 cache and be processed in a tight, function-call-free loop; compression fits more rows per cache line, and operators like the bitwise AND/OR can run on compressed chunks directly.

## Trade-offs & Pitfalls
- Different data shapes need different schemes; bitmap encoding shines specifically for the low-cardinality equality/membership predicates typical of warehouse queries.
- Compression assumes an immutable, position-aligned layout — which is exactly what makes updates hard (see [[Writing to Column-Oriented Storage]]).
- **Naming trap:** Cassandra's and HBase's "column families" (inherited from Bigtable) are *not* column-oriented — each column family stores a row's columns together with its row key and does no column compression, making the Bigtable model essentially row-oriented.

## Examples & Systems
Bitmap-indexed compressed columns are a staple of warehouse engines like Vertica and the C-Store lineage; vectorized execution originates in the MonetDB/X100 research line and appears in SQL Server's column stores. Parquet brings columnar compression to a document model.

## Related
- up: [[Column-Oriented Storage]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Sort Order in Column Storage]] — sorting creates long runs that compress even better
- [[Writing to Column-Oriented Storage]] — the write-path cost of compressed layouts
- [[Data Warehousing]] — the query patterns these encodings serve
