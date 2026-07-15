---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: bloom-filter
topics:
- lsm-tree-storage-engines
---

A Bloom filter is a probabilistic data structure attached to each [[sstable]] individually, and it exists to fix a specific worst case in the LSM-tree read path: looking up a key that doesn't exist anywhere. Without any optimization, that lookup has to search every Memtable and then every SSTable before giving up — expensive, and exactly the case a Bloom filter targets.

Its guarantee is asymmetric: it can say "definitely not in the set" with 100% certainty (no false negatives), or it can say "possibly in the set," which may turn out to be a false positive. Applied per-SSTable, that lets the system immediately skip the entire file when the filter says the key is definitely absent — cutting real I/O for lookups of non-existent data — and only actually check the SSTable when the filter says the key might be present.

*See also: [[sstable]] · [[memtable]] · [[compaction]]*

## Related in the other wiki
- [[Bloom Filters]] — the book's concept note on the same no-false-negative membership test, including its reuse beyond storage engines in join optimization and stream processing.
