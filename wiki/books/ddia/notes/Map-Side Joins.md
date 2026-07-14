---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: MapReduce and Distributed Filesystems
type: subtopic
tags: [ddia, joins, broadcast-hash-join, partitioned-join]
sources:
  - raw/ch10.md
---
# Map-Side Joins
> If you can guarantee something about your inputs' size, partitioning, or sort order, you can join with mappers alone — no shuffle, no sort, no reducers.

## The Idea
Reduce-side joins make no assumptions about input data, but pay for that generality with sorting, network copying, and repeated disk spills. A map-side join is a stripped-down job — mappers read blocks and write output, nothing else — that trades assumptions for speed. Three variants exist, each demanding progressively more structure from the inputs.

## How It Works
- **Broadcast hash join** — *assumption: one input is small.* Each mapper of the large input first loads the entire small input (e.g. the user database) into an in-memory hash table, then streams its block of the large input, probing the table per record. "Broadcast" because every mapper reads the whole small side; "hash" for the lookup structure. A variant keeps the small side in a read-only on-disk index whose hot pages live in the OS page cache — near-memory speed without the memory requirement.
- **Partitioned hash join** — *assumption: both inputs are partitioned identically* (same key, same hash function, same partition count). Then mapper *i* loads only partition *i* of the small side into its hash table and scans only partition *i* of the large side — e.g. both datasets bucketed by the last digit of user ID into ten partitions. Each hash table is a tenth the size. Usually realistic only when upstream [[MapReduce]] jobs produced the inputs with that exact grouping. Hive calls these bucketed map joins.
- **Map-side merge join** — *assumption: both inputs are partitioned AND sorted by the join key.* Mappers stream both files in key order and merge-match, so neither side needs to fit in memory. If inputs are already in this form, an earlier job likely made them so — but re-joining in a separate map-only job still makes sense when those sorted datasets serve other consumers too.

## Trade-offs & Pitfalls
- Output structure differs: a reduce-side join's output is partitioned and sorted by the join key, whereas a map-side join's output inherits the layout of the large input. Downstream jobs care.
- Correctness silently depends on physical layout — partition counts, key choice, hash function, sort order. Directory name and encoding aren't enough; this metadata must be tracked (HCatalog and the Hive metastore fill this role in the [[Hadoop]] ecosystem).
- Multiple entries per key in the hash table must be handled (emit all matches), though unique-key dimensions like user IDs sidestep it.

## Examples & Systems
Pig ("replicated join"), Hive ("MapJoin" / bucketed map join), Cascading, Crunch; Impala and other warehouse engines use broadcast hash joins internally; LinkedIn's PalDB-style side-data indexes for the on-disk variant.

## Related
- up: [[MapReduce and Distributed Filesystems]] · chapter: [[Ch 10 - Batch Processing]]
- [[Reduce-Side Joins and Grouping]] — the assumption-free baseline
- [[Partitioning by Hash of Key]] — the partitioning discipline both sides must share
- [[Materialization of Intermediate State]] — dataflow engines choose among these join strategies
- [[Column-Oriented Storage]] — warehouse engines pairing these joins with columnar scans
