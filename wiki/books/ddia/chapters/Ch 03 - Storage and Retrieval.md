---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
type: chapter-moc
tags: [ddia, storage-engines, indexes, olap, moc]
sources:
  - raw/ch03.md
---
# Ch 03 – Storage and Retrieval
Where [[Ch 02 - Data Models and Query Languages]] looked at data from the application developer's side, this chapter flips to the database's side: how does it physically store what you give it, and find it again when asked? You'll likely never build a storage engine, but choosing and tuning one demands a mental model of what it does under the hood. The chapter's spine is a single trade-off — indexes speed reads but tax every write — explored first through the two OLTP engine schools (log-structured engines built on append-only segments and [[Compaction]], versus update-in-place B-trees built on overwritable pages), then through the OLTP/OLAP divide, where analytics workloads escape to data warehouses and a different physical design entirely: [[Column-Oriented Storage]].

## Map
- [[Data Structures That Power Your Database]] — from a two-line Bash key-value store to the great index families
  - [[Hash Indexes]] — in-memory key→offset maps over append-only log segments; Bitcask
  - [[SSTables and LSM-Trees]] — sorted segments, memtables, mergesort-style compaction; LevelDB, RocksDB, Cassandra, HBase, Lucene
  - [[B-Trees]] — balanced trees of fixed-size pages, page splits, [[Write-Ahead Log]], copy-on-write variants
  - [[Comparing B-Trees and LSM-Trees]] — write amplification, compression, compaction stalls, transactional locking
  - [[Other Indexing Structures]] — [[Secondary Indexes]], clustered/covering indexes, multi-column and fuzzy indexes, in-memory databases
- [[Transaction Processing or Analytics]] — OLTP versus OLAP access patterns and the birth of the warehouse
  - [[Data Warehousing]] — a separate read-only analytics copy, fed by Extract–Transform–Load
  - [[Stars and Snowflakes - Schemas for Analytics]] — fact tables ringed by dimension tables; snowflaked subdimensions
- [[Column-Oriented Storage]] — store columns, not rows, when queries touch 5 of 100 columns
  - [[Column Compression]] — bitmaps, run-length encoding, and vectorized processing
  - [[Sort Order in Column Storage]] — row-wise sort orders as index and compression multiplier; multiple sort orders in Vertica
  - [[Writing to Column-Oriented Storage]] — LSM-style buffered writes merged into column files
  - [[Aggregation - Data Cubes and Materialized Views]] — precomputed aggregates and their flexibility cost

## Chapter Summary
Storage engines split along the OLTP/OLAP fault line. OLTP systems face floods of user requests, each touching a few records by key, so *disk seek time* is the bottleneck and indexes are the answer. Analytic systems see far fewer queries, but each scans millions of records, so *disk bandwidth* dominates and column-oriented layouts win by encoding data compactly and reading only the columns a query needs. On the OLTP side, two philosophies compete: the log-structured school (Bitcask, SSTables, LSM-trees, LevelDB, Cassandra, HBase, Lucene) only ever appends to files and deletes obsolete ones, systematically converting random writes into sequential writes to exploit disk performance characteristics; the update-in-place school treats disk as fixed-size overwritable pages, with the B-tree — the backbone of virtually every relational database — as its champion. The chapter closes the OLTP tour with more advanced indexing (secondary, multi-column, fuzzy, in-memory) before the warehouse detour explains *why* analytics diverges: sequential scans make indexes largely irrelevant and compact encoding paramount. Armed with these internals, a developer can match engine to workload and reason about what any tuning knob will actually do.

## Related
- part: [[Part I - Foundations of Data Systems]] · home: [[Home]]
- previous: [[Ch 02 - Data Models and Query Languages]] — data models and queries from the application's side
- next: [[Ch 04 - Encoding and Evolution]] — how the stored bytes are encoded and kept evolvable
- [[Ch 07 - Transactions]] — the transactional semantics B-tree engines are built to support
