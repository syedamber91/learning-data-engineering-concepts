---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Data Structures That Power Your Database
type: subtopic
tags: [ddia, lsm-tree, sstable, log-structured, compaction]
sources:
  - raw/ch03.md
---
# SSTables and LSM-Trees
> Sort each log segment by key and you get an index that supports huge datasets, range scans, and very high write throughput — the LSM-tree.

## The Idea
Hash-indexed logs stall on two limits: every key must live in RAM, and range queries are hopeless. The fix is one format change: require each segment's key-value pairs to be **sorted by key**, with each key appearing at most once per segment. This is the Sorted String Table (SSTable). Sorting seems to conflict with sequential writes — the trick is to do the sorting in memory first.

## How It Works
Three wins from sorting:
1. **Cheap merges.** Merging segments works like the merge step of mergesort: walk the files side by side, always emit the smallest key. Works even when files dwarf RAM. If a key appears in several inputs, keep only the value from the most recent segment.
2. **Sparse index.** You no longer need every key in memory. Knowing the offsets of two nearby keys brackets where a target key must sit; one index entry per few kilobytes of file suffices, because a few KB scans fast. (Fixed-size records could use pure binary search, but real keys/values are variable-length.)
3. **Block compression.** Since reads scan a range anyway, records can be grouped into compressed blocks, with sparse-index entries pointing at block starts — saving disk space and I/O bandwidth.

The full write path:
- Incoming writes go into an in-memory balanced tree (red-black or AVL) called the **memtable**, which keeps keys sorted regardless of arrival order.
- When the memtable exceeds a threshold (a few MB), flush it to disk as a new SSTable segment; writes continue in a fresh memtable.
- Reads check memtable → newest segment → older segments.
- Background merging/compaction discards overwritten and deleted values.
- Crash safety: every write is also appended to an unsorted log on disk — a [[Write-Ahead Log]] in spirit — used solely to rebuild the memtable after a crash, and discarded when the memtable is flushed.

This cascade of merged sorted files is the **Log-Structured Merge-Tree (LSM-tree)**, from O'Neil et al., building on log-structured filesystems.

## Trade-offs & Pitfalls
- **Lookups of absent keys are slow:** you must exhaust the memtable and every segment back to the oldest before concluding a key doesn't exist. Engines counter this with [[Bloom Filters]], which cheaply prove non-membership and skip pointless disk reads.
- **[[Compaction]] strategy matters:** *size-tiered* (small new SSTables merged into big old ones — HBase) vs *leveled* (key range split into levels for more incremental compaction and less disk usage — LevelDB, RocksDB; Cassandra offers both).

## Examples & Systems
LevelDB and RocksDB are embeddable LSM libraries (LevelDB is an alternative Riak engine to Bitcask). Cassandra and HBase use similar engines, descending from Google's Bigtable paper, which coined *SSTable* and *memtable*. Lucene (behind Elasticsearch and Solr) stores its term dictionary — term → postings list — in SSTable-like sorted files merged in the background.

## Related
- up: [[Data Structures That Power Your Database]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[Hash Indexes]] — the unsorted predecessor this design supersedes
- [[B-Trees]] — the rival sorted structure using in-place page updates
- [[Comparing B-Trees and LSM-Trees]] — head-to-head performance analysis
- [[Writing to Column-Oriented Storage]] — column stores reuse the LSM write path
- [[Partitioned Logs]] — logs as a cross-system data backbone
- [[lsm-tree-storage-engines]] — vutr's own synthesis of the LSM write path (sorted memtable, WAL, SSTable flush, bloom filter, compaction) mirrors this note's mechanism, extended with Vu's OLAP-engine examples like BigQuery Vortex.
