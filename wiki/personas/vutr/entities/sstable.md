---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: sstable
topics:
- lsm-tree-storage-engines
---

SSTables (Sorted String Tables) are the on-disk, persistent files that hold most of an LSM-tree's data, and they carry two defining properties. Immutable: once written, an SSTable file is never modified again — any update or delete is handled by writing a new record into a newer SSTable, never by editing the old one. Sorted: key-value pairs inside the file are ordered by key, a direct consequence of flushing an already-sorted [[memtable]], and this ordering is essential for reads.

A typical SSTable file has two parts: data blocks holding the actual key-value pairs, and an index block carrying a sparse index used to find the right data block for a given key. A sparse index doesn't record the location of every row the way a dense index does — instead it keeps the location of a record after every N rows (Vu's example uses 8,000), which keeps the index small enough to fit in memory. Sparse indexing only works because the data is sorted, and it still requires a binary search within the located range to pin down the exact record — it narrows the search, it doesn't eliminate it.

SSTables are created two ways: flushed directly from a frozen Memtable, or produced by merging existing SSTables during [[compaction]]. Because SSTables accumulate at multiple hierarchical levels, a read that misses in the Memtable may have to check several SSTables, at multiple levels, before finding (or failing to find) a key — which is exactly the cost a [[bloom-filter]] is built to cut down.

*See also: [[memtable]] · [[write-ahead-log]] · [[bloom-filter]] · [[compaction]] · [[sequential-vs-random-io]]*

## Related in the other wiki
- [[SSTables and LSM-Trees]] — the book's fuller walkthrough of the same sparse-index and sorted-merge mechanics this entity describes from Vu's post.
