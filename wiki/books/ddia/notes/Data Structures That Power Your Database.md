---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
type: topic
tags: [ddia, storage-engines, indexes, log-structured, b-tree]
sources:
  - raw/ch03.md
---
# Data Structures That Power Your Database
The chapter opens with a database you could write in two lines of Bash: `db_set` appends `key,value` lines to a file, `db_get` greps for the last occurrence. Appends make writes nearly optimal, but every read is an O(n) scan — which motivates the *index*: an extra structure derived from the primary data that acts as a signpost to it. Indexes embody the chapter's core trade-off — a well-chosen index accelerates reads, but **every** index taxes writes, since it must be maintained on each update; that is why databases make you pick indexes by hand from knowledge of your query patterns rather than indexing everything. From this seed the topic builds up the two great schools of OLTP storage engine: the *log-structured* school (append-only files, segments, [[Compaction]] — from hash-indexed logs to SSTables and LSM-trees) and the *update-in-place* school (fixed-size pages overwritten in situ, epitomized by the B-tree), then compares them head-to-head and tours the indexing ideas beyond plain key-value lookup.

## Subtopics
- [[Hash Indexes]] — an in-memory map from key to byte offset over an append-only log; Bitcask's design, segments, compaction, tombstones.
- [[SSTables and LSM-Trees]] — sort the segments by key: mergesort-style compaction, sparse indexes, memtables, and the LSM lineage (LevelDB, RocksDB, Cassandra, HBase, Lucene).
- [[B-Trees]] — the ubiquitous page-oriented index: balanced trees of 4 KB pages, page splits, the [[Write-Ahead Log]], latches, and copy-on-write variants.
- [[Comparing B-Trees and LSM-Trees]] — write amplification, compression, compaction stalls, and why the honest answer is "benchmark your own workload."
- [[Other Indexing Structures]] — [[Secondary Indexes]], heap files versus clustered and covering indexes, multi-column and geospatial indexes, fuzzy/full-text search, and in-memory databases.

## Key Takeaways
- An index is *derived* data: adding or dropping one never changes query answers, only their speed — and its cost always lands on the write path.
- Log-structured engines turn random writes into sequential ones (append + background merge), which is the root of their high write throughput on both spinning disks and SSDs.
- Append-only immutable segments also simplify crash recovery and concurrency: no half-overwritten values, one writer, many readers.
- Update-in-place engines (B-trees) keep exactly one copy of each key in a balanced tree of pages — three or four levels reach hundreds of terabytes — and lean on a [[Write-Ahead Log]] for crash safety.
- Neither school wins outright: LSM-trees generally favor writes, B-trees reads and predictable latency; [[Bloom Filters]] and compaction tuning patch LSM weaknesses.
- Everything here optimizes for disk; once data fits in RAM, in-memory databases win mainly by shedding the *encoding* overhead of disk formats, not by avoiding disk reads.

## Related
- chapter: [[Ch 03 - Storage and Retrieval]] · part: [[Part I - Foundations of Data Systems]]
- [[Transaction Processing or Analytics]] — these indexes serve OLTP; analytics needs different machinery
- [[Column-Oriented Storage]] — the analytics-side counterpart to these OLTP structures
- [[Log Compaction]] — the keep-latest-value-per-key idea reused for logs elsewhere in the book
