---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
type: chapter-moc
tags: [ddia2, storage-engines, lsm-tree, b-tree, column-store, indexes, moc]
sources:
  - raw/ch04.md
---
# Ch 04 – Storage and Retrieval
On the most fundamental level a database does two things: store the data you give it, and give it back when you ask. Chapter 3 covered the format in which you hand data over and the interface through which you ask for it; this chapter is the same question from **the database's point of view**. You are probably not going to implement a storage engine from scratch, but you do need to select one appropriate for your application from the many available — and to configure it to perform well on your workload, you need a rough idea of what it does under the hood. The chapter's organising split is the one Chapter 1 introduced: storage engines optimised for **transactional (OLTP)** workloads look very different from those optimised for **analytics**.

## Map
- [[Storage and Indexing for OLTP (2e)]] — the world's simplest database, and why it needs an index
  - [[Log-Structured Storage (2e)]] — hash indexes, SSTables, memtables, LSM-trees, Bloom filters, compaction strategies
  - [[B-Trees (2e)]] — fixed-size pages overwritten in place, page splits, and the write-ahead log
  - [[Comparing B-Trees and LSM-Trees (2e)]] — reads, sequential versus random writes, write amplification, disk space
  - [[Multicolumn and Secondary Indexes (2e)]] — non-unique index entries and how they are stored
  - [[Storing Values Within the Index (2e)]] — clustered indexes, heap files, and covering indexes
  - [[Keeping Everything in Memory (2e)]] — in-memory databases, and why they're actually fast
- [[Data Storage for Analytics (2e)]] — warehouse internals behind a familiar SQL interface
  - [[Cloud Data Warehouses (2e)]] — the unbundling into query engine, storage format, table format, and catalog
  - [[Column-Oriented Storage (2e)]] — storing columns together, bitmap encoding, and sort order
  - [[Query Execution - Compilation and Vectorization (2e)]] — two ways to stop being an interpreter
  - [[Materialized Views and Data Cubes (2e)]] — precomputed results and their flexibility cost
- [[Multidimensional and Full-Text Indexes (2e)]] — when one attribute at a time is not enough
  - [[Full-Text Search (2e)]] — inverted indexes, postings lists, trigrams, edit distance
  - [[Vector Embeddings (2e)]] — semantic search, and the flat/IVF/HNSW index families

## Chapter Summary
**OLTP** systems handle a high volume of requests, each reading and writing a small number of records and needing fast responses; records are typically reached via a primary key or secondary index, and those indexes are ordered key→record mappings that also support range queries. **Analytical** systems handle complex read queries scanning huge numbers of records; they use a column-oriented layout with compression to minimise bytes read from disk, and JIT compilation or vectorization to minimise CPU time.

On the OLTP side there are two schools. The **log-structured** approach appends to files and deletes obsolete ones but never updates a written file, and generally provides high write throughput — SSTables, LSM-trees, RocksDB, Cassandra, HBase, ScyllaDB, and Lucene belong here. The **update-in-place** approach treats disk as a set of fixed-size overwritable pages; B-trees are its canonical example, used in every major relational OLTP database and many non-relational ones, and as a rule of thumb give higher read throughput and lower response times.

Beyond single-attribute indexes, the chapter covers **multidimensional indexes** such as R-trees, which search by latitude and longitude simultaneously, **full-text search indexes**, which find multiple keywords in the same text, and **vector databases**, which perform semantic search on text and other media using high-dimensional vectors and similarity comparison. The chapter is explicit about its own limits: it cannot make you an expert in tuning any particular engine, but it aims to give you enough vocabulary to make sense of your database's documentation and to imagine what raising or lowering a tuning parameter will do.

## Since the 1st Edition
This is the 1st edition's Chapter 3, substantially rewritten. **Retained:** the two-line bash database, hash indexes, SSTables and LSM-trees, B-trees and page splits, the WAL, the B-tree/LSM comparison, secondary indexes, clustered and covering indexes, in-memory databases, column storage, column compression, and sort order. **Reorganised:** the 1st edition's OLTP/OLAP motivation section moved forward into [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]], and its star/snowflake schema material moved to [[Ch 03 - Data Models and Query Languages (2e)]] — so this chapter is now purely about engines rather than about why analytics differs. **Genuinely new:** [[Cloud Data Warehouses (2e)]] with the query-engine/storage-format/table-format/data-catalog unbundling, [[Query Execution - Compilation and Vectorization (2e)]], [[Multidimensional and Full-Text Indexes (2e)]] promoted from a paragraph to a whole topic, [[Full-Text Search (2e)]] as a real treatment, and [[Vector Embeddings (2e)]] — which did not exist as a database topic in 2017. Compaction strategies (size-tiered versus leveled) and the SSD garbage-collection explanation of why sequential writes beat random ones are also new.

## Related
- home: [[Home (2e)]] · previous: [[Ch 03 - Data Models and Query Languages (2e)]] · next: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Operational Versus Analytical Systems (2e)]] — the split this chapter physically implements
- [[Ch 08 - Transactions (2e)]] — durability and crash recovery, promised here
- 1st edition: [[Ch 03 - Storage and Retrieval]] — the chapter this one rewrites
