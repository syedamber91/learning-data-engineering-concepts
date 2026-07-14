---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Data Structures That Power Your Database
type: subtopic
tags: [ddia, lsm-tree, b-tree, write-amplification, benchmarking]
sources:
  - raw/ch03.md
---
# Comparing B-Trees and LSM-Trees
> Rule of thumb: LSM-trees win on writes, B-trees on reads and predictability — but only your own workload benchmark settles it.

## The Idea
Both structures index sorted key-value data, so choosing between them is a pure engineering trade-off. The headline heuristic — LSM faster to write, B-tree faster to read (LSM reads must consult the memtable plus several SSTables at various compaction stages) — hides workload-sensitive details, and published benchmarks are frequently inconclusive. Understanding the mechanisms behind each side's advantages tells you what to measure.

## How It Works
**Write amplification** is the central concept: one logical database write becoming multiple physical disk writes over the data's lifetime. B-trees pay it via the [[Write-Ahead Log]] plus the page overwrite (plus splits, plus whole-page writes for tiny changes, plus double-writes in some engines guarding against torn pages). LSM-trees pay it via repeated rewriting during [[Compaction]] and merging. It matters doubly on SSDs, whose blocks tolerate only a finite number of overwrites, and in write-heavy systems where disk write bandwidth *is* the bottleneck — the more bandwidth amplification eats, the fewer application writes per second fit.

**Why LSM-trees usually sustain higher write throughput:**
- Often lower write amplification (configuration- and workload-dependent).
- They emit compact SSTables sequentially instead of overwriting scattered pages — a large advantage on magnetic disks where sequential ≫ random writes.
- Better compression and no page fragmentation: periodic SSTable rewriting removes dead space, so on-disk footprint is smaller (especially with leveled compaction), which on SSDs also translates to more I/O headroom. (SSD firmware itself often log-structures random writes internally, softening but not eliminating the difference.)

**Why B-trees push back:**
- **Predictable latency.** Background compaction competes for finite disk resources; average impact is small, but tail latencies (see [[Describing Performance]]) at high percentiles can spike when a request waits behind an expensive compaction. B-trees behave more consistently.
- **Compaction can fall behind.** At sustained high write rates, disk bandwidth is split between initial writes (logging + memtable flushes) and compaction threads. If compaction can't keep pace, unmerged segments pile up until disk fills, and reads degrade as more files must be checked. SSTable engines typically do *not* throttle incoming writes when this happens — you need explicit monitoring.
- **One copy of each key.** A B-tree holds each key in exactly one place; an LSM engine may hold stale copies across segments. Single placement suits strong transactional semantics: range-lock–based isolation (expanded in [[Weak Isolation Levels]] and [[Serializability]]) can attach locks directly to the tree.

## Trade-offs & Pitfalls
There is no universal winner. B-trees are deeply entrenched and consistently good; log-structured indexes keep gaining ground in new datastores. Empirical testing on *your* workload is the only reliable decision procedure.

## Examples & Systems
The contrasts here map to RocksDB/LevelDB/Cassandra/HBase (LSM side) versus InnoDB, SQL Server, and other relational engines (B-tree side).

## Related
- up: [[Data Structures That Power Your Database]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[B-Trees]] — mechanism behind the update-in-place column
- [[SSTables and LSM-Trees]] — mechanism behind the log-structured column
- [[Describing Performance]] — percentile latency framing used here
- [[Compaction]] — the background process driving both LSM costs and gains

## Related in the other wiki
- [[lsm-tree-storage-engines]] — Vu's own LSM-vs-B-tree comparison (his "Comparisons" section) independently reaches the same write-vs-read trade-off this chapter formalizes via write amplification.
