---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: memtable
topics:
- lsm-tree-storage-engines
---

The Memtable is the in-memory structure that absorbs every write hitting an LSM-tree, and Vu calls out a common misconception directly: it is not an append-only log, it is a *sorted* data structure. Common implementations use Skip Lists, Red-Black Trees, or AVL Trees, and the three share the properties that make the Memtable work — fast for both writes and reads, self-balancing (which underpins that speed), and automatically sorted as data is inserted.

That sortedness is the whole point. A sorted structure supports `O(log N)` binary-search lookups for something like `WHERE key = 'user_123'`; an unsorted list would force an `O(n)` scan of the entire data space. And because the Memtable is already sorted, flushing it to disk needs no separate sort step — the system writes its contents to a new [[sstable]] in a single sequential pass, which is what gives the LSM-tree its high-throughput write path (see [[sequential-vs-random-io]]).

The Memtable is explicitly a temporary buffer, not the durable copy — a machine failure loses whatever's still in memory, which is why every write also goes to the [[write-ahead-log]] first. In the write path, once a Memtable is "full" it is frozen (stops accepting writes) while a new active Memtable is created immediately, so the write path never stalls; the frozen Memtable is then flushed into a new SSTable, after which its now-redundant WAL records can be dropped. Reads always start here: the read path checks both the active and frozen Memtables in memory first, before falling through to on-disk SSTables — and stops as soon as it finds the key. Updates and deletes for keys still resident in the Memtable are handled by directly overwriting the existing key in place, which the structure's fast, self-balancing design allows; once a key's data has already moved to an on-disk SSTable, an update instead has to be written as a brand-new key-value pair with a newer timestamp, and a delete as a [[tombstone]] marker.

*See also: [[write-ahead-log]] · [[sstable]] · [[sequential-vs-random-io]] · [[compaction]] · [[b-tree]]*

## Related in the other wiki
- [[SSTables and LSM-Trees]] — DDIA's account of "sorting in memory first" as the trick that turns segment merges into cheap, mergesort-like passes matches Vu's description of the Memtable as a sorted, not append-only, write buffer.
