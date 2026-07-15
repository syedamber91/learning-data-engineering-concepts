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

## Related in the other wiki
- [[compaction]] — Vu's entity note on the same background merge process, naming Size-Tiered vs Leveled as the two strategies this note calls write- vs read-optimized.
- [[sstable]] — the immutable sorted files that compaction merges and rewrites; Vu's note adds the sparse-index detail this note assumes.
- [[memtable]] — the in-memory structure whose flushes are what compaction has to keep pace with; Vu's note is careful to note it's a sorted structure, not an append-only log.
- [[physical-layout-partitioning-clustering-and-compaction]] — vutr's concept names a related but distinct use of the same word: consolidating many small immutable OLAP data files (produced by frequent inserts, the same "many small sorted runs" shape this page's LSM segments have) back into fewer, well-sorted files, run automatically by BigQuery/Snowflake or self-managed on an Iceberg lakehouse — the serving-layer analog of this page's storage-engine-level merge process.
