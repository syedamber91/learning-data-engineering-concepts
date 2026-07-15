---
persona: vutr
kind: entity
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/what-makes-oltp-databases-so-quick.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
last_updated: '2026-07-15'
qc: passed
slug: b-plus-tree-index
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

The B+Tree is the index structure Vu names as the dominant technique for optimizing query performance in OLTP databases like PostgreSQL and MySQL — the mechanism behind the [[oltp-vs-olap-access|map-like lookup]] OLTP needs. It has been the main approach for decades, and although the classic B-Tree allows data in non-leaf pages, the near-universal B+Tree variant restricts actual data to leaf pages only, so every read/write/update operation focuses solely on the leaves.

**Why not a binary search tree.** Vu builds up to the B+Tree from first principles. A Binary Search Tree (BST) gives O(log n) search, insert, and delete when balanced, by keeping every node's left subtree smaller and right subtree larger than the node itself. But a BST is designed for memory, where following a pointer is fast because RAM does random access well. On disk, that assumption collapses: RAM access is nanoseconds, an HDD seek is milliseconds (four to five orders of magnitude slower), and even SSDs — which remove mechanical seek time — are still microseconds, much slower than RAM. Disks also transfer data in fixed-size blocks (e.g. 4–16 KB), so an efficient on-disk structure must extract maximum value from every block it reads. A balanced BST of height 20 could force up to 20 separate disk reads to find one item, since each node might live in a different, non-contiguous disk block — and each node only holds a few dozen bytes (a value plus two pointers), wasting most of a disk block's capacity per read. The goal on disk, in other words, is to minimize the number of I/O operations, not to minimize comparisons.

**Anatomy.** The B+Tree solves this by making each node (page) hold many keys and many children at once, sized to align with the disk's block size (PostgreSQL's page size is 8 KB). A root node is where every operation starts; leaf nodes store key-value pairs (index column values pointing to the actual data); internal nodes link root and leaves. Non-leaf nodes store sorted keys plus pointers, with pointer-count = key-count + 1, and each pointer covers the key range `[key_left, key_right)`. **M** is the tree's fan-out — the max children a page can point to — giving each node a max of **N = M − 1** keys, with a minimum of **N/2** keys required so no node is less than half full. A lookup (point query or range filter) starts at the root, compares the search value against the node's keys to pick a child pointer, and repeats one level at a time until it reaches the leaf holding the data.

**Overflow and underflow.** Inserting a key into a full node (N keys already) causes overflow: a new node is created, the data from position `(N/2)+1` onward moves into it, and the parent gets a new key/pointer pair. In a leaf node, the first key of the new node is *copied* up to the parent (it still needs to exist at the leaf level to serve as a data pointer); in a non-leaf node, that first key is *moved* up instead, since it exists purely to divide the two split node's keys and no data pointer depends on it. If the parent overflows too, the split can propagate recursively all the way to the root. Underflow — a node dropping below N/2 keys, typically from a deletion — is resolved the opposite way: two sibling nodes (same parent) whose combined keys fit in one node are merged, with the leaf case simply merging all key-pointer pairs and deleting the parent's separator key, and the non-leaf case first pulling the parent's separator key down into the merge before combining both siblings' keys and child pointers. Like overflow, this can cascade to the root.

**Durability.** Because some B+Tree writes touch more than one page at once (a split can write two new pages plus update a parent), B+Tree implementations universally rely on Write-Ahead Logging (WAL) — an append-only file every modification is recorded to *before* it's applied to the actual pages — so a crash mid-write can be recovered to a consistent state by replaying the log.

Vu explicitly flags the natural counterpart to this write-side cost: B+Trees are excellent for reading but require real work (splits/merges) to keep their structure valid on writes, and he names the LSM-tree as the alternative design that instead optimizes for the write side, more common in the OLAP world.

*See also: [[oltp-vs-olap-access]] · [[nsm]] · [[b-tree]]*

## Related in the other wiki
- [[B-Trees]] — DDIA's own chapter on the B-Tree mechanism (fixed-size pages, branching factor, splits, WAL, latches) is the fuller textbook treatment behind this entity's from-first-principles walkthrough.
- [[Comparing B-Trees and LSM-Trees]] — DDIA's direct comparison is the same read/write trade-off vutr gestures at when naming the LSM-tree as the write-optimized alternative to the B+Tree.
