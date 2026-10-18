---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
type: topic
tags: [ddia2, oltp, index, log, append-only]
sources:
  - raw/ch04.md
---
# Storage and Indexing for OLTP
The chapter opens with the world's simplest database, two bash functions:

```bash
db_set () { echo "$1,$2" >> database; }
db_get () { grep "^$1," database | sed -e "s/^$1,//" | tail -n 1; }
```

The storage format is a text file, one comma-separated key-value pair per line. Every `db_set` **appends** to the end of the file; updating a key does not overwrite old versions, so `db_get` must take the **last** occurrence — hence the `tail -n 1`. And it works.

`db_set` has pretty good performance for something so simple, because **appending to a file is generally very efficient**. Many databases internally use a **log** — an append-only data file — in just this way. Real databases have more to deal with (concurrent writes, reclaiming disk space so the log doesn't grow forever, partially written records after a crash), but the basic principle is the same. Note the book's vocabulary: *log* here does **not** mean human-readable application logs, but the general sense of an append-only sequence of records on disk, possibly binary and internal to the database.

`db_get`, by contrast, has terrible performance at scale: every lookup scans the whole file from beginning to end. The cost is **O(n)** — double the records, double the lookup time. To find a value efficiently we need a different structure: an **index**. The general idea is to structure the data in a particular way (sorted by key, say) that makes locating what you want faster; if you want to search the same data several ways, you may need several indexes on different parts of it.

## Subtopics
- [[Log-Structured Storage (2e)]] — keep appending, and make reads fast with in-memory maps, sorted files, and background merging.
- [[B-Trees (2e)]] — the update-in-place alternative that has dominated relational databases since 1970.
- [[Comparing B-Trees and LSM-Trees (2e)]] — the honest performance comparison, on four separate axes.
- [[Multicolumn and Secondary Indexes (2e)]] — indexes on things other than the primary key.
- [[Storing Values Within the Index (2e)]] — where the row actually lives relative to the index.
- [[Keeping Everything in Memory (2e)]] — what changes when the dataset fits in RAM.

## Key Takeaways
- **An index is derived data.** It is an additional structure derived from the primary data; adding or removing one doesn't affect the database's contents, only query performance.
- **The central trade-off of storage systems:** well-chosen indexes speed up read queries, but every index consumes additional disk space and slows down writes, sometimes substantially. For writes it is hard to beat simply appending to a file, because that is the simplest possible write operation.
- Because of that trade-off, **databases don't usually index everything by default**. They require you — the application author or administrator — to select indexes manually using knowledge of your typical query patterns, so you get the greatest benefit without more write overhead than necessary.
- **Embedded storage engines** are worth knowing about: databases that expose no network API but run as libraries inside your process, reading and writing local files, called through normal function calls. RocksDB, SQLite, LMDB, DuckDB, and KùzuDB are examples. They are very common in mobile apps for local user data, and on the backend they suit data small enough for one machine without many concurrent transactions — for instance a multitenant system where each tenant is small and completely separate, which can use a separate embedded database instance per tenant.

## Since the 1st Edition
The 1st edition's [[Data Structures That Power Your Database]] opened identically with the two-line bash database and the index trade-off, and that framing is unchanged. What differs is the subtopic structure: the 1st edition had [[Hash Indexes]] and [[SSTables and LSM-Trees]] as separate subtopics, which the 2nd edition merges into [[Log-Structured Storage (2e)]]; [[Other Indexing Structures]] is split into [[Multicolumn and Secondary Indexes (2e)]], [[Storing Values Within the Index (2e)]], and [[Keeping Everything in Memory (2e)]]; and the embedded-storage-engine sidebar is new.

## Related
- chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Data Storage for Analytics (2e)]] — the other half of the chapter, for the other workload
- [[Characterizing Transaction Processing and Analytics (2e)]] — the workload distinction being served
- 1st edition: [[Data Structures That Power Your Database]] — the same topic, differently subdivided
