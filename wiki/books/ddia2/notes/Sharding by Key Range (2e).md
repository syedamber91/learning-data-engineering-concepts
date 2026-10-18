---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding of Key-Value Data
type: subtopic
tags: [ddia2, key-range, range-scan, pre-splitting, shard-split, hbase]
sources:
  - raw/ch07.md
---
# Sharding by Key Range
> Like the volumes of a paper encyclopedia. Range scans are easy; writing today's timestamps puts every write on one shard.

## The Idea
Assign **a contiguous range of partition keys, from a minimum to a maximum, to each shard** — like the volumes of a print encyclopedia, where an entry's partition key is its title. To look up a title you find the volume whose key range contains it.

**The ranges are not necessarily evenly spaced, because your data may not be evenly distributed.** Volume 1 might cover A and B while volume 12 covers T through Z; one volume per two letters would make some volumes much bigger than others. **To distribute data evenly, the shard boundaries need to adapt to the data.**

## How It Works
Boundaries may be **chosen manually by an administrator or automatically by the database**. Manual key-range sharding is used by **Vitess** (a sharding layer for MySQL); the automatic variant by **Bigtable and HBase**, MongoDB's range-based sharding option, **CockroachDB, RethinkDB, and FoundationDB**. **YugabyteDB offers both.**

**Within each shard, keys are stored in sorted order** — in a B-tree or SSTables. This makes **range scans easy**, and lets you **treat the key as a concatenated index** to fetch several related records in one query. For a sensor network where the key is the measurement timestamp, range scans let you easily fetch all readings from a particular month.

**Rebalancing.** On a fresh database there are no key ranges to split, so some databases — **HBase and MongoDB** — let you configure an initial set of shards on an empty database, called **pre-splitting**. That requires already having some idea of the key distribution so you can choose appropriate boundaries.

As data volume and write throughput grow, the system **grows by splitting an existing shard into two or more smaller shards**, each holding a contiguous subrange, which can then be distributed across nodes. If large amounts of data are deleted, **adjacent small shards may need merging** into one bigger one. **The process is similar to what happens at the top level of a B-tree.**

With automatic boundary management, a split is typically triggered by **the shard reaching a configured size** (HBase's default is 10 GB) or, in some systems, **write throughput persistently above a threshold** — so **a hot shard may be split even if it is not storing much data**, distributing its write load more uniformly. **The number of shards adapts to the data volume**: a small amount of data needs few shards so overheads stay small; a huge amount is limited by a configurable maximum shard size.

## Trade-offs & Pitfalls
- **The classic failure: a lot of writes to nearby keys creates a hot shard.** If the key is a timestamp, shards correspond to ranges of time — one per month — so **writing sensor measurements as they happen sends all writes to the current month's shard**, overloading it while the others sit idle.
- **The fix and its cost.** Use something other than the timestamp as the first element of the key — **prefix each timestamp with the sensor ID** so ordering is by sensor and then by time. With many sensors active at once, write load spreads out. **The downside: fetching multiple sensors' values within a time range now needs a separate range query per sensor.**
- **Splitting is expensive.** It requires all the shard's data to be rewritten into new files, similar to a compaction. **A shard needing splitting is often also one under high load, and the cost of splitting can exacerbate that load, risking it becoming overloaded.**

## Examples & Systems
Vitess (manual); Bigtable, HBase, MongoDB, CockroachDB, RethinkDB, FoundationDB (automatic); YugabyteDB (both); HBase's 10 GB default split size.

## Since the 1st Edition
The 1st edition's [[Partitioning by Key Range]] used the same encyclopedia analogy and the same sensor-timestamp hot-spot example with the same sensor-ID-prefix fix. **Added:** pre-splitting named as a technique; **splitting triggered by write throughput, not just size**, so a hot shard can be split even when small; the explicit note that **splitting is expensive and can worsen the very overload it addresses**; and an updated engine roster.

## Related
- up: [[Sharding of Key-Value Data (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Sharding by Hash of Key (2e)]] — the alternative, and what it costs
- [[Multidimensional and Full-Text Indexes (2e)]] — concatenated indexes
- 1st edition: [[Partitioning by Key Range]] — the same subtopic
