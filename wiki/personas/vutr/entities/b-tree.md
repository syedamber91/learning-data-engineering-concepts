---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: b-tree
topics:
- lsm-tree-storage-engines
---

The B-Tree is the storage structure behind OLTP databases like MySQL and PostgreSQL, and Vu uses it as the LSM-tree's foil throughout: excellent at reads, expensive at writes. A B+Tree-based engine performs in-place updates — writing a 30-byte key-value pair still means reading the full 4KB or 8KB data page from disk into memory (unless cached), modifying just those 30 bytes in memory, and writing the *entire* page back to disk. That's high write amplification: a small logical write turns into a large physical read and write, regardless of how little actually changed.

On reads, this trade pays off. Vu's comparison is explicit: B+Trees give more predictable read latency, since a query follows a single `O(log n)` path from root to leaf — ideal for OLTP workloads where low-latency random-access reads matter most. An LSM-tree, by contrast, may be slightly slower to read because it has to check the in-memory [[memtable]] first and then potentially multiple on-disk [[sstable]] files across levels before it finds (or fails to find) the key.

Both structures share one cost: writing to a [[write-ahead-log]] before the data itself is modified, for crash durability. Where they diverge is what happens next — the B-Tree's heavy I/O is an in-place overwrite of a data page (random I/O), whereas the LSM-tree's heavy I/O is a sequential flush of an already-sorted Memtable (see [[sequential-vs-random-io]]). That single difference is why the LSM-tree can sustain higher write throughput than the B-Tree in most cases — and it's the whole engine-selection question the [[write-amplification-tradeoff]] concept is built to frame.

*See also: [[memtable]] · [[sstable]] · [[write-ahead-log]] · [[sequential-vs-random-io]] · [[write-amplification-tradeoff]]*

## Related in the other wiki
- [[B-Trees]] — the book's full mechanism (fixed-size pages, branching factor, node splits, WAL, latches, copy-on-write variants) behind the in-place, random-I/O trade-off this entity note summarizes from Vu's comparison.
- [[Comparing B-Trees and LSM-Trees]] — DDIA's own worked-out version of the same read-vs-write trade this note frames through page rewrites versus sequential Memtable flushes.
