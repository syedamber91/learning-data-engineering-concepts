---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: lsm-tree-storage-engines
---

Related: [[memtable]] · [[wal]] · [[sstable]] · [[bloom-filter]] · [[compaction]] · [[tombstone]] · [[b-tree]] · [[bigquery-vortex]] · [[sequential-vs-random-io]] · [[write-amplification-tradeoff]]

## Comparisons
## LSM-tree vs B-Tree

The [[b-tree]] does in-place updates with random I/O and is excellent for reading, but pays more write amplification on random writes. The LSM-tree instead converts random writes into sequential I/O (see [[sequential-vs-random-io]]) at the cost of potentially higher read/write amplification — a deliberate [[write-amplification-tradeoff]]. Notably, Vu frames the LSM as the write-focused alternative that shows up more in the OLAP world.

## Compaction strategies

Within [[compaction]], Size-Tiered (merge SSTables of similar size) is write-optimized, while Leveled (merge into fixed-size levels) is read-optimized with less space amplification.

## Membership & indexing

[[sstable]] files carry a sparse index (one entry per block), and a [[bloom-filter]] short-circuits lookups by reliably answering 'not in set'. Deletes are handled lazily via [[tombstone]] markers, resolved only during [[compaction]].

## Open questions
- When does the higher read amplification of an LSM-tree outweigh its write advantage over a [[b-tree]] for a given workload?
- How does the [[bigquery-vortex]] WOS→ROS transition decide when a fragment is 'cold' enough to move to the Read-Optimized Store?
- What determines the choice between Size-Tiered and Leveled [[compaction]] in practice beyond the write- vs read-optimized rule of thumb?
- How aggressively should [[tombstone]] accumulation drive compaction scheduling before deleted data bloats read paths?

## Synthesis
An LSM-tree wins by keeping a sorted [[memtable]] in memory (not an append-only log), guarding it with a [[wal]], and flushing to immutable [[sstable]] files — turning random writes into sequential I/O, which is decisive given [[sequential-vs-random-io]]. Reads stay tolerable because a [[bloom-filter]] skips SSTables that definitely lack a key, while [[compaction]] merges files and resolves [[tombstone]] deletes in the background. Against a [[b-tree]], this is fundamentally a [[write-amplification-tradeoff]]: accept potentially higher read/space cost to win on writes — a pattern now surfacing in OLAP systems like [[bigquery-vortex]].
