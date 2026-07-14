---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Data Structures That Power Your Database
type: subtopic
tags: [ddia, b-tree, page-oriented, indexing, wal]
sources:
  - raw/ch03.md
---
# B-Trees
> The dominant database index since 1970: a balanced tree of fixed-size pages, updated in place, giving O(log n) lookups and range scans.

## The Idea
While log-structured engines are the newcomers, the B-tree is the index that actually powers almost every relational database (and many non-relational ones). Introduced in 1970 and dubbed "ubiquitous" within a decade, it keeps key-value pairs sorted by key — like SSTables — but with an entirely different philosophy: instead of append-only variable-size segments, treat the disk as a set of **fixed-size pages** (traditionally 4 KB) that are read and written one at a time, mirroring how disks themselves are block-structured.

## How It Works
- Pages reference each other by on-disk address, forming a tree. Lookup starts at the **root** page, which holds keys acting as range boundaries plus child references; each hop narrows the key range until a **leaf page** is reached, holding the value inline or a pointer to it.
- The **branching factor** — child references per page — is typically several hundred. Depth stays O(log n): most databases fit in 3–4 levels. A four-level tree of 4 KB pages with branching factor 500 addresses up to 256 TB.
- **Updates** overwrite the leaf page in place; references stay valid because the page address doesn't change.
- **Inserts** go into the page covering the key's range; if the page is full it **splits** into two half-full pages and the parent is updated. This keeps the tree balanced. (Deletion while preserving balance is considerably fiddlier.)

**Reliability.** Overwriting a page is a genuine hardware operation (head seek + platter rotation on magnetic disks; block erase-rewrite cycles on SSDs). A split touches multiple pages — two children plus the parent — and a crash mid-way can corrupt the index (e.g., orphan pages). The standard defense is a [[Write-Ahead Log]] (redo log): an append-only file that records every modification *before* it is applied to pages, replayed on restart to restore consistency. Concurrent access needs **latches** (lightweight locks) so threads never observe a half-updated tree — a complication log-structured engines avoid by merging in the background and swapping segments atomically.

**Optimizations accumulated over decades:**
- Copy-on-write instead of WAL + overwrite (LMDB): modified pages are written to new locations with new parent versions — also handy for concurrency, foreshadowing [[Snapshot Isolation and Repeatable Read]].
- Key abbreviation in interior pages (the essence of the B+ tree variant): boundary keys need only enough bytes to separate ranges, raising the branching factor and lowering depth.
- Attempting sequential on-disk layout of leaf pages for faster range scans — hard to maintain as the tree grows, and a place where LSM-trees (which rewrite big sorted runs anyway) have an easier time.
- Sibling pointers between leaves, so ordered scans skip the trip back through parents.
- Fractal trees, which borrow log-structured buffering ideas to cut disk seeks.

## Trade-offs & Pitfalls
- Every write is a whole-page write, even for a few changed bytes, and lands at least twice (WAL + page). Some engines write pages twice more to survive partial page writes on power failure.
- Fragmentation: split pages sit half-empty; space in pages goes unused.
- Random page writes are slower than the sequential writes LSM engines issue — see [[Comparing B-Trees and LSM-Trees]].

## Examples & Systems
Every major relational database (e.g., MySQL's InnoDB, SQL Server, PostgreSQL) indexes with B-trees; LMDB shows the copy-on-write variant; fractal trees appeared in TokuDB-style engines.

## Related
- up: [[Data Structures That Power Your Database]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[SSTables and LSM-Trees]] — the append-only rival design
- [[Comparing B-Trees and LSM-Trees]] — when each one wins
- [[Write-Ahead Log]] — crash-recovery backbone of in-place updates
- [[Other Indexing Structures]] — clustered/covering indexes built on B-trees
