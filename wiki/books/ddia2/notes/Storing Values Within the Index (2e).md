---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, clustered-index, heap-file, covering-index, innodb, postgres]
sources:
  - raw/ch04.md
---
# Storing Values Within the Index
> The key is what you search by. What sits next to it — the whole row, a pointer to it, or a few useful columns — is a separate decision with real consequences.

## The Idea
The key in an index is what queries search by. Other data may be stored alongside the keys, and there are three options.

## How It Works
- **Clustered index.** The actual data — row, document, vertex — is stored **directly within the index structure**. In MySQL's InnoDB the table's primary key is always a clustered index; in SQL Server you can specify one clustered index per table.
- **Reference to the data.** The value is either the **primary key** of the row (InnoDB does this for its secondary indexes) or a **direct reference to a location on disk**. In the latter case the place where rows are stored is a **heap file**, which stores data in no particular order — it may be append-only, or track deleted rows so they can be overwritten later. PostgreSQL uses the heap file approach.
- **Covering index** (or *index with included columns*) — the middle ground. It stores **some of a table's columns within the index**, in addition to the full row living on the heap or in the primary-key clustered index. Some queries can then be answered from the index alone, without resolving the primary key or visiting the heap file — the index is said to **cover** the query.

## Trade-offs & Pitfalls
- A covering index can make some queries faster, but **the duplication of data means the index uses more disk space and slows down writes**. This is the chapter's central index trade-off appearing again in miniature.
- **Updating a value without changing the key** is where the heap file approach gets awkward. If the new value is no larger than the old, the record can be overwritten in place. If it is larger, it probably has to move to a new heap location with enough space — and then **either all indexes must be updated to point at the new location, or a forwarding pointer must be left behind** in the old one.
- The indexes described here map only a single key to a value; querying multiple columns simultaneously is a different structure entirely.

## Examples & Systems
InnoDB (clustered primary key, secondary indexes storing the primary key); SQL Server (one clustered index per table); PostgreSQL (heap files).

## Since the 1st Edition
The 1st edition covered clustered indexes, heap files, and covering indexes inside [[Other Indexing Structures]]. The content survives largely intact as its own subtopic. **New:** the explicit discussion of what happens when an updated value grows too large for its heap slot — the forwarding-pointer versus update-all-indexes choice.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Multicolumn and Secondary Indexes (2e)]] — what these indexes are keyed on
- [[When to Use Which Model (2e)]] — the same locality question at the data-model level
- 1st edition: [[Other Indexing Structures]] — where this material used to live
