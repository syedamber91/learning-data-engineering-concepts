---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Data Structures That Power Your Database
type: subtopic
tags: [ddia, hash-index, log-structured, key-value-store]
sources:
  - raw/ch03.md
---
# Hash Indexes
> The simplest viable index: an in-memory hash map pointing each key to a byte offset in an append-only log file on disk.

## The Idea
An append-only log is the fastest possible way to write data, but finding a key in it means scanning the whole file — O(n) per lookup. A hash index fixes reads without giving up append-only writes: keep a hash map in RAM that maps every key to the byte position where its latest value lives in the log. Writes append to the file and update the map; reads consult the map, seek once, and read the value.

## How It Works
- **Write path:** append the key-value record to the current log file, then point the in-memory map at the new offset. Updates and inserts are identical operations.
- **Read path:** one map lookup → one disk seek (zero if the filesystem cache already holds that block).
- **Segments + [[Compaction]]:** to stop the log growing forever, close a file once it hits a size threshold and start a new segment. Background compaction rewrites segments keeping only the newest value per key, and merges several small segments into one — all against immutable frozen files, so reads continue on old segments until an atomic switchover.
- **Lookups across segments:** each segment keeps its own hash map; check the newest segment first, then progressively older ones. Merging keeps the segment count low.
- Practical necessities: a length-prefixed binary record format (faster than CSV, no escaping), **tombstone** records to mark deletions so merges drop earlier values, per-segment hash-map snapshots on disk for fast crash restarts, checksums to detect half-written records, and a single writer thread (many concurrent readers are fine since segments are immutable).

Append-only beats update-in-place here because sequential writes are far faster than random writes (especially on spinning disks), crash recovery is simple (no half-overwritten values), and merging prevents fragmentation.

## Trade-offs & Pitfalls
- **All keys must fit in RAM.** On-disk hash maps perform poorly (random I/O, costly growth, awkward collision handling), so a huge keyspace rules this design out.
- **No range queries.** Keys hash to arbitrary locations, so scanning, say, all keys in a lexical range requires one lookup per key.
- Best fit: workloads with a modest set of keys, each updated very often (e.g., a per-video play counter).

## Examples & Systems
Bitcask, the default storage engine in Riak, is essentially this design: memory-speed reads and writes as long as the key set fits in RAM, with hash-map snapshots for quick recovery.

## Related
- up: [[Data Structures That Power Your Database]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[SSTables and LSM-Trees]] — the sorted successor that lifts both limitations
- [[B-Trees]] — the contrasting update-in-place indexing school
- [[Compaction]] — the segment-merging mechanism introduced here
