---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, storage-engines]
sources:
  - raw/ch03.md
---
# Compaction

Merging and rewriting storage segments to reclaim space: drop overwritten values,
remove tombstoned deletes, merge sorted runs. In LSM storage it's the background
heartbeat — memtables flush to SSTables, and size-tiered or leveled compaction
continuously merges them; done well it keeps reads fast, done poorly it starves
foreground I/O (write amplification).

Book home ground: [[Hash Indexes]] (segment merging) and [[SSTables and LSM-Trees]] + [[Comparing B-Trees and LSM-Trees]] (Ch 3). The log-retention variant
is [[Log Compaction]] (keep latest value per key).

## Referenced In
- [[Ch 03 - Storage and Retrieval]]
- [[Comparing B-Trees and LSM-Trees]]
- [[Data Structures That Power Your Database]]
- [[Hash Indexes]]
- [[SSTables and LSM-Trees]]
- [[Snapshot Isolation and Repeatable Read]]
- [[The Output of Batch Workflows]]
- [[Writing to Column-Oriented Storage]]
