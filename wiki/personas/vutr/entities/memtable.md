---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: memtable
topics:
- lsm-tree-storage-engines
---

The Memtable is the in-memory component of an LSM-tree, and here is the thing most people get wrong (I used to be one of them): it is NOT an append-only log, it is a sorted data structure. Keeping it sorted in memory is what lets writes stay fast while the data is still ordered for later flushing to disk.

*See also: [[compaction]] · [[bigquery-vortex]] · [[bloom-filter]] · [[b-tree]] · [[write-ahead-log]] · [[tombstone]]*

## Related in the other wiki
- [[Compaction]] — the book process that consumes what the memtable produces: each flush becomes a new SSTable segment for compaction to eventually merge.
