---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Data Structures That Power Your Database
type: subtopic
tags: [ddia, secondary-indexes, multi-dimensional-index, full-text-search, in-memory-databases]
sources:
  - raw/ch03.md
---
# Other Indexing Structures
> Beyond the primary key: secondary indexes, value-placement choices, multi-column and fuzzy indexes, and databases that skip the disk entirely.

## The Idea
Key-value indexes cover primary keys — the unique identifier of a row, document, or vertex. Real applications also need [[Secondary Indexes]] (non-unique keys, essential for joins), indexes over several columns at once, similarity search, and sometimes no disk at all. Each is a variation on the B-tree/LSM building blocks.

## How It Works
**Secondary indexes.** Keys aren't unique, solved either by storing a list of matching row IDs per key (like a postings list) or by appending a row ID to make each key unique. Both [[B-Trees]] and log-structured indexes work as secondary indexes.

**Where the value lives:**
- *Heap file*: the index value is a pointer; rows live in an unordered heap. Avoids duplicating rows across multiple secondary indexes. In-place updates are cheap if the new value is no larger; a grown value must move, requiring either updating all indexes or leaving a forwarding pointer.
- *Clustered index*: the row is stored inside the index itself, eliminating the extra hop. In MySQL's InnoDB the primary key is always clustered, and secondary indexes point at the primary key rather than a heap offset; SQL Server allows one clustered index per table.
- *Covering index*: middle ground — a few extra columns stored in the index so some queries are answered from the index alone. Like all [[Denormalization]], clustered/covering copies speed reads but cost write overhead, storage, and extra transactional care.

**Multi-column indexes.** A *concatenated* index glues columns into one key (lastname-then-firstname, like a phone book): great for prefix queries, useless when the leading column isn't constrained. *Multi-dimensional* indexes handle simultaneous ranges on several axes — the classic case being geospatial latitude+longitude rectangles that a single B-tree cannot serve efficiently. Options: encode 2D positions into one number with a space-filling curve and index that, or use dedicated structures like R-trees (PostGIS builds them on PostgreSQL's Generalized Search Tree). The idea generalizes past geography: (R, G, B) color search, or (date, temperature) queries as in HyperDex.

**Fuzzy and full-text indexes.** Exact-key indexes can't match misspellings. Lucene supports queries within a bounded *edit distance* (1 = one letter added/removed/replaced). Its in-memory term index is a finite state automaton over key characters (trie-like), transformable into a Levenshtein automaton for efficient approximate matching; full-text engines layer on synonyms, grammatical variants, and proximity search.

**In-memory databases.** As RAM cheapens, moderate datasets fit entirely in memory. Memcached is a pure cache; durable in-memory stores use battery-backed RAM, change logs, periodic snapshots, or [[Replication]]. Counterintuitively, their speed comes not from avoiding disk reads (the OS page cache already serves hot data from RAM) but from skipping the overhead of encoding structures for disk. They also enable data models awkward on disk, like Redis's priority queues and sets. *Anti-caching* — evicting least-recently-used records to disk at record granularity — extends the model past RAM size, though indexes must still fit in memory. Non-volatile memory (NVM) may reshape this space further.

## Trade-offs & Pitfalls
Every extra index and every copy of data (clustered, covering) accelerates some reads while taxing all writes and complicating consistency. Concatenated indexes silently fail query patterns that skip the leading column.

## Examples & Systems
InnoDB, SQL Server, PostGIS/PostgreSQL, HyperDex, Lucene, Memcached, VoltDB, MemSQL, Oracle TimesTen, RAMCloud (log-structured in memory and on disk), Redis, Couchbase (weak durability via async disk writes).

## Related
- up: [[Data Structures That Power Your Database]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Secondary Indexes]] — concept note for the non-unique index pattern
- [[Partitioning and Secondary Indexes]] — how these indexes shard across nodes
- [[SSTables and LSM-Trees]] — Lucene's term dictionary uses this layout
- [[Many-to-One and Many-to-Many Relationships]] — why joins need secondary indexes
- [[write-amplification-tradeoff]] — the clustered/covering-index trade-off here (read speed bought with write overhead and extra storage) is the same pay-now-for-read-later tax Vu frames as write amplification for B+Trees vs LSM-trees.
- [[sequential-vs-random-io]] — the in-memory databases described here are the extreme case of this concept's I/O gap: no disk seeks at all once the index and data both live in RAM.
