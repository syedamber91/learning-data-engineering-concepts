---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: compaction
topics:
- lsm-tree-storage-engines
---

Compaction is literally the "Merge" in Log-Structured Merge-Tree: a resource-intensive background process that periodically reads [[sstable]] files, merges their data — straightforward since the data is already sorted — and writes the result to new SSTables. It serves two purposes: reclaiming disk space by cleaning up stale data left behind by updates and deletes (including resolving [[tombstone]] markers), and improving read performance by merging the many small files a busy [[memtable]] flush cycle produces into fewer, larger ones, so readers don't have to open/read/close a pile of small files.

Vu describes two concrete strategies. **Size-Tiered** (used in Apache Cassandra) groups SSTables into tiers by similar size; once a tier accumulates enough SSTables it merges them into one and promotes the result to a higher tier. Because the trigger is file count rather than key range, SSTables within a tier can have overlapping keys, so a read may have to check several SSTables across tiers to find the latest version of a key — high read amplification, but the strategy only rewrites data when a tier is promoted, so it's write-optimized.

**Leveled** compaction instead organizes data into levels (L0, L1, L2, …) that are non-overlapping except L0, with each level's target size roughly 10x the one below it. New SSTables land in L0 (where overlap is allowed); once a level fills, at least one of its files is merged into the overlapping range of the next level up, and the process repeats as levels exceed their size limits. Because ranges don't overlap outside L0, reads need fewer checks — lower read amplification — but the trade is higher write amplification: pulling a small amount of new data into a level forces a much larger volume of existing overlapping data in that level to be rewritten, even where nothing actually changed.

Compaction's failure mode is falling behind the write rate: if it can't keep pace, unmerged SSTables pile up, disk fills because stale data isn't cleaned, and reads slow down because more files must be checked per lookup — the flip side of the throughput compaction is meant to protect.

*See also: [[sstable]] · [[memtable]] · [[tombstone]] · [[bloom-filter]] · [[write-amplification-tradeoff]] · [[b-tree]]*

## Related in the other wiki
- [[Compaction]] — the book's account of compaction as the "background heartbeat" of LSM storage, including the same write-amplification cost when it falls behind on a write-heavy workload.
- [[Log Compaction]] — DDIA generalizes SSTable merging into the log-compaction idea that also powers Kafka's compacted topics — the same superseded-record pruning this note describes for Size-Tiered and Leveled strategies, applied at a different layer.
