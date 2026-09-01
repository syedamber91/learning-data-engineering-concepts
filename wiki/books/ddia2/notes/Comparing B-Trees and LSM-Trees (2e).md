---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, write-amplification, sequential-writes, ssd, fragmentation, backpressure]
sources:
  - raw/ch04.md
---
# Comparing B-Trees and LSM-Trees
> Rule of thumb: LSM-trees for write-heavy, B-trees for reads. Then benchmark, because the rule of thumb is sensitive to details of your workload.

## The Idea
As a rule of thumb, **LSM-trees are better suited for write-heavy applications and B-trees are faster for reads**. But benchmarks are often sensitive to workload details, so you need to test with your particular workload for a valid comparison. And it is **not a strict either/or**: storage engines sometimes blend both, for example by keeping multiple B-trees and merging them LSM-style.

## How It Works
**Read performance.** In a B-tree, a lookup reads one page per level, and since levels are few, reads are generally fast with **predictable performance**. In an LSM engine reads often check several SSTables at different compaction stages, though Bloom filters reduce the disk I/O required. Both can perform well; which is faster depends on engine and workload details. **Range queries** are simple and fast on B-trees thanks to the sorted tree structure; on LSM storage they can also exploit SSTable sorting but must **scan all segments in parallel and combine results**, and **Bloom filters don't help** (you would have to hash every possible key in the range), making range queries more expensive than point queries in LSM. High write throughput can cause **latency spikes** in a log-structured engine if the memtable fills up because compaction can't keep pace; many engines including RocksDB apply **backpressure**, suspending all reads and writes until the memtable is written out. For read *throughput*, modern SSDs — especially NVMe drives on the faster PCIe bus rather than SATA — can perform many independent reads in parallel; both structures can deliver high read throughput, but engines must be carefully designed to exploit that parallelism.

**Sequential versus random writes.** With a B-tree, writing keys scattered across the key space produces scattered disk operations, since the pages to overwrite could be anywhere. A log-structured engine writes **entire segment files at a time**, much bigger than a B-tree page. The many-small-scattered pattern is **random writes**; the fewer-larger pattern is **sequential writes**. Disks generally have higher sequential than random write throughput, so a log-structured engine can generally handle higher write throughput on the same hardware. The difference is particularly large on spinning disks; on the SSDs most databases use today it is smaller but still noticeable.

*Why sequential beats random on SSDs.* On HDDs a random write must mechanically move the head and wait for the platter — several milliseconds, an eternity. SSDs have no such mechanics, yet still favour sequential writes, because **flash can be read or written one page (typically 4 KiB) at a time but erased only one block (typically 512 KiB) at a time**. Some pages in a block may hold valid data and others data no longer needed; before erasing, the controller must move the valid pages elsewhere — **garbage collection**. A sequential workload writes larger chunks, so a whole 512 KiB block likely belongs to one file, and when that file is deleted the block can be erased with no GC. A random workload leaves blocks holding a mixture of valid and invalid pages, so the collector does more work before erasing. The bandwidth GC consumes is unavailable to the application, and the extra writes **wear the flash faster** — so random writes wear out a drive quicker than sequential ones.

**Write amplification.** With any engine, one application write becomes multiple disk I/O operations. In LSM-trees a value is written to the log for durability, again when the memtable is flushed, and again in every compaction it participates in. (If values are much larger than keys, this can be reduced by storing values separately from keys and compacting only SSTables of keys and value references.) A B-tree writes every piece of data at least twice — once to the WAL and once to the tree page — and sometimes writes an entire page even when only a few bytes changed, to ensure correct recovery after a crash or power failure. Divide total bytes written to disk by the bytes you would write with a plain append-only log and no index, and you get the **write amplification** (sometimes defined in I/O operations rather than bytes). In write-heavy applications the bottleneck may be the disk write rate, and **the higher the write amplification, the fewer writes per second fit in the available bandwidth**. It is a problem for both structures; which is better depends on key and value lengths and how often you overwrite existing keys versus insert new ones. **For typical workloads LSM-trees tend to have lower write amplification**, because they don't write whole pages and can compress SSTable chunks — another reason they suit write-heavy work. Lower write amplification also **wears out SSDs less quickly**.

## Trade-offs & Pitfalls
- **Benchmark long enough.** Writing to an empty LSM-tree means no compaction is running yet, so all disk bandwidth is available for new writes. As the database grows, new writes must share bandwidth with compaction — so short experiments flatter LSM engines.
- **Disk space usage.** B-trees can become **fragmented**: deleting many keys can leave pages unused, and while later additions can reuse them, they can't easily be returned to the OS because they sit in the middle of the file. Databases therefore need a background process to move pages around, such as PostgreSQL's **vacuum**. Fragmentation is less of a problem in LSM-trees, since compaction periodically rewrites the files anyway and SSTables have no pages with unused space; blocks of key-value pairs also compress better, often giving smaller files on disk. Overwritten keys and values keep consuming space until a compaction removes them, but this overhead is quite low with **leveled** compaction; **size-tiered** uses more disk space, especially temporarily during compaction.
- **Deletion assurance is worse in LSM.** Having multiple copies on disk is a problem when you need to delete data and be confident it is gone — for data-protection compliance. In most LSM engines a deleted record may still exist in higher levels until the tombstone has propagated through all compaction levels, **which might take a long time**. Specialist designs can propagate deletions faster.
- **Snapshots are easier in LSM.** Immutable segment files make point-in-time snapshots cheap: write out the memtable, record which segment files existed, and as long as you don't delete those files you never need to copy anything. In a B-tree whose pages are overwritten, taking such a snapshot efficiently is more difficult.

## Examples & Systems
RocksDB applying backpressure on memtable pressure; PostgreSQL's vacuum for B-tree fragmentation; NVMe/PCIe SSDs versus SATA for parallel reads.

## Since the 1st Edition
The 1st edition's [[Comparing B-Trees and LSM-Trees]] covered write amplification, compaction stalls, compression, and fragmentation. **New or much expanded here:** the **SSD garbage-collection explanation** of why sequential writes still win on flash (and the resulting wear argument); range queries called out as the case where Bloom filters cannot help; backpressure named as the mechanism for memtable-full latency spikes; NVMe parallelism; the benchmarking warning about empty LSM-trees; the **deletion-assurance/data-protection** problem; and the snapshot advantage of immutable segments. The 1st edition's transactional-locking point (B-trees making it easy to attach locks to key ranges) is not carried forward here.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Log-Structured Storage (2e)]] and [[B-Trees (2e)]] — the two contenders
- [[Backpressure (2e)]] — the overload mechanism named here
- 1st edition: [[Comparing B-Trees and LSM-Trees]] — the same subtopic
