---
persona: vutr
kind: concept
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: sequential-vs-random-io
topics:
- lsm-tree-storage-engines
---

The gap between sequential and random I/O is the entire reason the LSM-tree exists as an alternative to the [[b-tree]]. A B+Tree write is random by construction: to change a 30-byte key-value pair, the engine reads the whole 4KB or 8KB page containing it, modifies those bytes in memory, and writes the *entire* page back to disk — a small logical write becoming a large physical one, wherever that page happens to sit.

The LSM-tree avoids that penalty on the hot path. Setting aside the [[write-ahead-log]] write, which both engines pay, the LSM-tree's heavy I/O is flushing the [[memtable]] to a new [[sstable]] — and because the Memtable is already sorted, that flush is a single sequential pass rather than an in-place page overwrite. Vu is explicit that this sequential-versus-random distinction is what lets the LSM-tree sustain higher write throughput than the B-Tree in most cases. Reads later have to reverse the search order (Memtable, then SSTables level by level), but the write side is where sequential I/O pays off.

*See also: [[memtable]] · [[sstable]] · [[b-tree]] · [[write-amplification-tradeoff]]*
