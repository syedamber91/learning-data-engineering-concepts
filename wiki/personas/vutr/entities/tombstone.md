---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: tombstone
topics:
- lsm-tree-storage-engines
---

An LSM-tree can't perform a real DELETE against data already sitting in an immutable, on-disk [[sstable]] — the engine can't go back and erase it. Instead a DELETE triggers a **logical delete**: the system writes a "delete" flag, the tombstone, which is simply a key-value pair whose value is a special marker meaning "deleted." The old record is left untouched exactly where it was; the tombstone is a new, separate write that takes precedence when the key is looked up (since reads search from most recent data to oldest). The only exception is when the target key is still resident in the active [[memtable]] — there, a delete is handled by directly overwriting the key in place rather than writing a tombstone.

The tombstone itself is not the end of the story: the actual disk-space reclamation and cleanup of the now-superseded original record only happens later, during [[compaction]], when SSTables are merged and stale data — including tombstoned entries — gets dropped.

*See also: [[sstable]] · [[memtable]] · [[compaction]]*
