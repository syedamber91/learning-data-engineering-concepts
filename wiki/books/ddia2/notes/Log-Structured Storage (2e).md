---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, lsm-tree, sstable, memtable, bloom-filter, compaction, tombstone]
sources:
  - raw/ch04.md
---
# Log-Structured Storage
> Never modify a file you've written. Append, sort in memory, flush to immutable sorted files, and merge them in the background forever.

## The Idea
Keep the append-only file and just speed up reads. The first attempt: maintain an **in-memory hash map** from every key to the byte offset where its most recent value lives. Appending a key-value pair also updates the map; a lookup finds the offset, seeks, and reads — and if that part of the file is already in the filesystem cache, no disk I/O at all.

That is much faster, but has four problems: **disk space** occupied by overwritten entries is never freed, so you may run out; the hash map **isn't persisted**, so it must be rebuilt by scanning the whole log on restart, making restarts slow; the hash table **must fit in memory** (an on-disk hash map is hard to make perform well — lots of random I/O, expensive to grow when full, and fiddly collision logic); and **range queries are inefficient**, since scanning keys 10000–19999 means looking each one up individually.

## How It Works
**The SSTable file format.** In practice hash tables are not often used for database indexes; it is much more common to keep data **sorted by key**. A **Sorted String Table (SSTable)** stores key-value pairs sorted by key, with each key appearing only once. Now you don't need all keys in memory: group pairs into blocks of a few kilobytes and store only the **first key of each block** in the index — a **sparse** index, stored in a separate part of the SSTable using an immutable B-tree, a trie, or similar. If the first key of one block is `handbag` and the next block's is `handsome`, then a lookup for `handiwork` must lie between them: seek to `handbag`'s offset and scan forward. A block of a few kilobytes scans very quickly. Each block can also be **compressed**, saving disk space and I/O bandwidth at the cost of a bit more CPU.

**Constructing and merging SSTables.** SSTables read better but write worse — you can't just append, or the file stops being sorted, and rewriting the whole file per insert would be far too expensive. The **log-structured approach** is a hybrid:
1. On a write, add it to an **in-memory ordered map** — a red-black tree, skip list, or trie — where keys can be inserted in any order, looked up efficiently, and read back sorted. This is the **memtable**.
2. When the memtable exceeds a threshold (typically a few megabytes), **write it to disk in sorted order as an SSTable file** — the most recent **segment**, stored alongside older segments, each with its own index. While it is being written, the database writes to a new memtable instance; the old memtable's memory is freed on completion.
3. To read a key, look in the memtable and the most recent segment, then the next-older, and so on until found or the oldest segment is exhausted. Absent from all segments means absent from the database.
4. Periodically run **merging and compaction** in the background to combine segments and discard overwritten or deleted values.

Merging works like **mergesort**: read the input files side by side, take the lowest first key, copy it to the output, repeat — and where a key appears in more than one input, keep the more recent value. This produces a new sorted segment with one value per key using minimal memory, since SSTables are iterated one key at a time.

To avoid losing the memtable in a crash, the engine keeps a **separate log on disk** to which every write is immediately appended. It is not sorted by key, which doesn't matter — its only job is restoring the memtable after a crash — and the corresponding part can be discarded once the memtable is written out. Deleting a key means appending a **tombstone**, a special deletion record; when segments merge, the tombstone tells the process to discard previous values for that key, and once merged into the oldest segment it can itself be dropped.

This algorithm is essentially what **RocksDB, Cassandra, ScyllaDB, and HBase** use, all inspired by Google's **Bigtable** paper (which introduced the terms SSTable and memtable). It was published in **1996** as the **Log-Structured Merge-tree (LSM-tree)**, building on earlier log-structured filesystem work — hence **LSM storage engines** for engines based on merging and compacting sorted files.

**Bloom filters.** Reading a key updated long ago, or one that doesn't exist, is slow because several segments must be checked. LSM engines therefore often include a **Bloom filter** per segment: a fast, approximate check for whether a key appears in that SSTable. For every key in the SSTable, hash it to a set of numbers interpreted as indexes into a bit array and set those bits to 1 — `handbag` hashing to (2, 9, 4) sets bits 2, 9, and 4. To test a key, hash it the same way and check those bits, which CPUs do extremely quickly with bitwise operations. **If at least one bit is 0, the key definitely is not in the SSTable.** If all are 1, the key is *likely* present — but those bits may coincidentally have been set by other keys, a **false positive**. False-positive probability depends on the number of keys, bits set per key, and total bits; as a rule of thumb, **10 bits per key gives 1% false positives, and the probability falls tenfold for every 5 additional bits per key**. In an LSM engine false positives are harmless: a "not present" answer safely skips the SSTable, and a "present" answer just means consulting the sparse index and decoding a block, doing a little unnecessary work before continuing to the next-oldest segment.

**Compaction strategies.** When to compact and which SSTables to include matters, and most LSM systems let you configure it:
- **Size-tiered compaction** merges newer, smaller SSTables successively into older, larger ones — four 256 MB SSTables might become one 898 MB SSTable (not 1,024 MB, because of deletions, overwrites, and TTL expirations). Older SSTables can get very large and merging them needs a lot of temporary disk space, but it handles **very high write throughput** since most data is rewritten only a few times in large sequential merges.
- **Leveled compaction** keeps SSTable sizes fixed and groups them into increasing **levels** (L0, L1, …). L0 holds the most recently written data; all levels beyond L0 hold key-range-partitioned SSTables — L1 might have one SSTable for keys a–m and another for n–z. Each level has its own size limit, larger than the level before; when a level exceeds it, SSTables are merged from level *i* into level *i*+1 and deleted from *i*. This proceeds more incrementally and uses less disk space, and is **more efficient for reads** because fewer SSTables must be checked.

Rule of thumb: **size-tiered is better with mostly writes and few reads; leveled is better when reads dominate.** Leveled can also help if you write a small number of keys frequently and a large number rarely.

## Trade-offs & Pitfalls
- In LSM engines a segment file is written in one pass and is thereafter **immutable**. Merging runs in a background thread; reads continue to use the merge's *input* segments until it completes, at which point reads switch to the merged segment and the inputs can be deleted.
- **Segment files need not be on local disk** — they suit object storage well. SlateDB and Delta Lake take this approach.
- Immutability also **simplifies crash recovery**: a crash while writing a memtable or merging just means deleting the unfinished SSTable and starting again. The memtable's write log may contain incomplete records after a crash or a full disk; these are typically detected with **checksums**, and corrupted or incomplete entries discarded.

## Examples & Systems
RocksDB, Cassandra, ScyllaDB, HBase, Lucene; Bigtable as the origin of the SSTable/memtable vocabulary; SlateDB and Delta Lake for object-storage segments; red-black trees, skip lists, and tries as memtable structures.

## Since the 1st Edition
This note merges the 1st edition's [[Hash Indexes]] and [[SSTables and LSM-Trees]] into one. The mechanism — memtable, SSTable, mergesort compaction, tombstones, WAL for the memtable — is unchanged. **New:** **compaction strategies** (size-tiered versus leveled) as a first-class configurable decision with a workload rule of thumb; the concrete Bloom filter sizing rule (10 bits per key → 1%, tenfold per 5 more bits); object storage as a segment destination, naming SlateDB and Delta Lake; and ScyllaDB added to the engine roster. The 1st edition covered Bitcask in more detail as the hash-index exemplar; the 2nd edition compresses that history to make room for the above.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[B-Trees (2e)]] — the rival philosophy
- [[Comparing B-Trees and LSM-Trees (2e)]] — the head-to-head
- [[Full-Text Search (2e)]] — Lucene applies this same design to inverted indexes
- 1st edition: [[Hash Indexes]] and [[SSTables and LSM-Trees]] — the two notes this merges

## In the vutr data-engineering wiki
- [[lsm-tree-storage-engines]] — vutr's own synthesis of the LSM write path — sorted memtable, WAL, SSTable flush, bloom filter, compaction — mirrors this section's mechanism and extends it with OLAP-engine examples like BigQuery Vortex.
- [[sstable]] — the immutable sorted files this section flushes and merges; Vu adds the sparse-index detail.
- [[memtable]] — the in-memory structure whose flushes compaction must keep pace with — Vu is careful that it is a sorted structure, not an append-only log.
