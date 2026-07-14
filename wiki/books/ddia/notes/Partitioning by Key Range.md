---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Partitioning of Key-Value Data
type: subtopic
tags: [ddia, partitioning, key-range, range-queries]
sources:
  - raw/ch06.md
---
# Partitioning by Key Range
> Give each partition a contiguous slice of the sorted key space — like encyclopedia volumes — so any key's location is immediately computable.

## The Idea
If keys are kept in sorted order and each partition owns everything between some minimum and maximum key, then locating a record is trivial: knowing the range boundaries tells you the partition, and knowing the partition-to-node map tells you the machine. The mental model is a shelf of encyclopedia volumes — you go straight to the right book by its spine label instead of searching all of them.

## How It Works
- **Boundaries adapt to data, not the alphabet.** Real keys are unevenly distributed, so slicing the key space into equal-width ranges would make some partitions huge and others tiny (think how few English words start with X, Y, Z versus A, B). Boundaries are therefore either set manually by an operator or picked automatically by the database.
- **Sorted keys inside each partition** (the [[SSTables and LSM-Trees]] style) make range scans cheap. The key can even act as a concatenated index (cf. [[Other Indexing Structures]]): a sensor network keyed by measurement timestamp can pull an entire month's readings with a single scan.
- **Rebalancing** for this scheme is usually *dynamic splitting*: an oversized partition divides into two subranges (detailed in [[Strategies for Rebalancing]]).

## Trade-offs & Pitfalls
- The signature failure mode: access patterns concentrated on adjacent keys create [[Hot Spots]]. Timestamp keys are the classic trap — every "now" write lands in today's partition while yesterday's partitions sit idle.
- The standard fix is reordering the key: prefix the timestamp with something high-cardinality like a sensor ID, so writes fan out across partitions first by sensor, then by time. The cost is that a multi-sensor time-range query becomes one range query per sensor instead of a single scan.
- Manually chosen boundaries can drift badly out of balance as data grows.

## Examples & Systems
Bigtable pioneered the approach; HBase (its open-source counterpart) and RethinkDB use it, as did MongoDB before version 2.4 introduced hash-based [[Sharding]].

## Related
- up: [[Partitioning of Key-Value Data]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning by Hash of Key]] — the opposite trade: even load, no ordering
- [[Skewed Workloads and Relieving Hot Spots]] — when key design alone isn't enough
- [[Strategies for Rebalancing]] — dynamic partitioning suits key ranges
- [[B-Trees]] — range-splitting mirrors B-tree top-level page splits
