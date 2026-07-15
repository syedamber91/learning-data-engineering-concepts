---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
type: topic
tags: [ddia, column-store, analytics, compression, data-warehouse]
sources:
  - raw/ch03.md
---
# Column-Oriented Storage
Fact tables in a data warehouse can hold trillions of rows across petabytes, yet a typical analytic query touches only 4 or 5 of a table's 100+ columns. Row-oriented storage (the OLTP norm — all values of a row adjacent on disk, as in relational and document databases alike) is a terrible match: even with indexes on the filter columns, the engine must drag entire wide rows off disk, parse them, and throw most of each row away. The columnar idea is disarmingly simple — store all values of each *column* together, one file per column — so a query reads only the columns it names. The one structural rule that makes this work: every column file keeps rows in the *same order*, so the kth entry of every file belongs to the kth row, and rows are reassembled positionally. The idea extends beyond relational data (Parquet is a columnar format for a document model, derived from Google's Dremel), and it must not be confused with Bigtable-style "column families" in Cassandra and HBase, which store each row's columns together and are really row-oriented. Columnar layout also unlocks two follow-on wins covered in the subtopics: aggressive compression (repetitive per-column values, bitmaps, run-length encoding) and CPU-efficient *vectorized processing* that chews through compressed column chunks inside the L1 cache without per-record function calls.

## Subtopics
- [[Column Compression]] — bitmap encoding of low-cardinality columns plus run-length encoding of sparse bitmaps; bitwise AND/OR answers warehouse predicates directly, and compressed chunks feed vectorized execution.
- [[Sort Order in Column Storage]] — sorting whole rows (though stored by column) turns the first sort key into an index and a compression jackpot; C-Store/Vertica even keep the same data in several sort orders.
- [[Writing to Column-Oriented Storage]] — compressed, sorted columns can't be updated in place; LSM-style in-memory buffering with bulk merges makes writes workable.
- [[Aggregation - Data Cubes and Materialized Views]] — precomputing common aggregates as [[Materialized Views]] and OLAP cubes trades query flexibility for speed.

## Key Takeaways
- OLAP's bottleneck is disk *bandwidth* (and memory-to-CPU bandwidth), not seek time — so the goal is to read fewer bytes, which columnar layout plus compression achieves directly.
- Positional correspondence across column files is the load-bearing invariant: it enables row reassembly, bitmap conjunctions, and forbids sorting columns independently.
- Sort order, compression, and columnar layout reinforce each other: sorted low-cardinality first columns collapse under run-length encoding even at billions of rows.
- Writes are the price of read optimization; the LSM-tree pattern from earlier in the chapter rescues them.
- Columnar storage is spreading fast for ad-hoc analytics, but not every warehouse is a column store — row-oriented and aggregate-centric architectures persist.

## Related
- chapter: [[Ch 03 - Storage and Retrieval]] · part: [[Part I - Foundations of Data Systems]]
- [[Transaction Processing or Analytics]] — the workload split that motivates this storage family
- [[Data Warehousing]] — the system context these engines live in
- [[SSTables and LSM-Trees]] — the write-path machinery column stores borrow
- [[bigquery-internals]] — vutr's notes ground this note's Dremel origin claim: BigQuery's own Capacitor format and Big Metadata/CMETA system apply the same columnar bet to both data and metadata, and its definition/repetition-level encoding (adopted directly by Parquet) is the mechanism this note's "Parquet... derived from Google's Dremel" line only names in passing.
- [[apache-pinot-druid-and-real-time-olap]] — vutr's notes on Pinot and Druid apply this note's columnar rationale to a real-time-serving workload instead of a warehouse: both engines store immutable columnar segments, and Druid's real-time nodes even perform the row-to-column conversion this note describes live, on every flush from memory to disk.
- [[parquet]] — vutr's notes work through Parquet's actual on-disk mechanics (row groups, column chunks, pages, dictionary/RLE/delta encodings, and the newer Lance/Nimble/Vortex alternatives) that this note's "Parquet... derived from Google's Dremel" line only names in passing.
