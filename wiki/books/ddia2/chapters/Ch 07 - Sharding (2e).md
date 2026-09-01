---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: chapter-moc
tags: [ddia2, sharding, partitioning, hot-spots, rebalancing, secondary-indexes, moc]
sources:
  - raw/ch07.md
---
# Ch 07 – Sharding
A distributed database distributes data across nodes in two ways: **replication** (a copy of the same data on multiple nodes, Chapter 6) and **sharding** — if there is so much data or such high write throughput that a single node cannot handle it, splitting the data into smaller **shards** or **partitions** and storing different shards on different nodes.

Normally shards are defined so that **each piece of data belongs to exactly one shard**; in effect **each shard is a small database of its own**, though some systems support operations touching multiple shards. Sharding is usually **combined with replication**, so copies of each shard live on multiple nodes — a record belongs to exactly one shard but may still be stored on several nodes for fault tolerance. A node may store more than one shard: with single-leader replication, each shard's leader is assigned to one node and its followers to others, so **each node may be leader for some shards and follower for others**, while each shard still has exactly one leader.

> **The terminology is a mess, and the book says so.** A shard is called a **partition** in Kafka, a **range** in CockroachDB, a **region** in HBase and TiDB, a **vBucket** in Couchbase, a **vnode** in Riak, a **token-range** in Cassandra, and a **tablet** in Bigtable, YugabyteDB, and ScyllaDB. Some databases treat the two words as distinct: in PostgreSQL, **partitioning** splits a large table into several files on the same machine (making it very fast to delete an entire partition), while **sharding** splits a dataset across machines; in many other systems partitioning is just another word for sharding. As for where "sharding" came from: one theory traces it to the online role-playing game **Ultima Online**, where a magic crystal was shattered and each shard refracted a copy of the game world, so *shard* came to mean one of a set of parallel game servers; another says it was an acronym for *System for Highly Available Replicated Data*, a 1980s database whose details are lost to history. And **partitioning has nothing to do with network partitions (netsplits)**.

Everything about replication applies equally to replication of shards, and since the sharding scheme is mostly independent of the replication scheme, **this chapter ignores replication for simplicity**.

## Map
- [[Pros and Cons of Sharding (2e)]] — why it's a heavyweight solution you should avoid until you need it
- [[Sharding for Multitenancy (2e)]] — a shard per customer, and the seven things that buys you
- [[Sharding of Key-Value Data (2e)]] — skew, hot shards, and hot keys
  - [[Sharding by Key Range (2e)]] — contiguous ranges, range scans, and time-based hot spots
  - [[Sharding by Hash of Key (2e)]] — mod N, fixed shard counts, hash ranges, and consistent hashing
  - [[Skewed Workloads and Relieving Hot Spots (2e)]] — celebrities, key salting, and heat management
  - [[Operations - Automatic Versus Manual Rebalancing (2e)]] — why a human in the loop is sometimes right
- [[Request Routing (2e)]] — three routing architectures, and ZooKeeper as the authority
- [[Sharding and Secondary Indexes (2e)]] — the part that doesn't shard neatly
  - [[Local Secondary Indexes (2e)]] — document-partitioned; cheap writes, scatter-gather reads
  - [[Global Secondary Indexes (2e)]] — term-partitioned; cheap reads, complicated writes

## Chapter Summary
**Sharding is necessary when you have so much data that storing and processing it on a single machine is no longer feasible.** The goal is to **spread data and query load evenly, avoiding hot spots**, which requires a sharding scheme appropriate to your data and rebalancing when nodes are added or removed.

Two main approaches. **Key range sharding**: keys are sorted and a shard owns all keys from a minimum to a maximum. Sorting makes **efficient range queries possible**, but risks hot spots if the application often accesses keys close together in sorted order; shards are typically rebalanced by **splitting a range into two subranges** when one gets too big. **Hash sharding**: a hash function is applied to each key and a shard owns a range of hash values (or another consistent hashing algorithm maps hashes to shards). This **destroys key ordering, making range queries inefficient**, but may distribute load more evenly; it is common to create a **fixed number of shards in advance**, assign several to each node, and move whole shards when nodes change — though splitting is also possible.

**It's common to use the first part of the key as the partition key and sort records within a shard by the rest of the key**, so you still get efficient range queries among records sharing a partition key.

For secondary indexes there are two methods. **Local secondary indexes** live in the same shard as the primary key and value: **only one shard is updated on write, but a lookup requires reading from all shards.** **Global secondary indexes** are sharded separately by indexed value: **several index shards may need updating on write, but a postings-list read is served from a single shard** (fetching the actual records still requires reading from multiple shards).

**By design every shard operates mostly independently — that's what allows a sharded database to scale.** But operations writing to several shards are problematic: what happens if the write to one shard succeeds and another fails? That question opens the next chapter.

## Since the 1st Edition
This is the 1st edition's Chapter 6, **renamed from "Partitioning" to "Sharding"** — and the terminology box explaining that decision, along with the Ultima Online etymology, is new. The chapter is also **promoted out of the Part II grouping** since the 2nd edition has no Parts.

**Retained:** key-range and hash sharding, the mod-N problem, fixed-shard-count rebalancing, hot spots and key salting, request routing's three approaches, ZooKeeper coordination, and the local/global (document-/term-partitioned) secondary index distinction.

**Genuinely new:** [[Pros and Cons of Sharding (2e)]] as an explicit topic arguing you should avoid sharding if a single machine suffices; [[Sharding for Multitenancy (2e)]] as an entire topic (cell-based architecture, per-tenant backup, GDPR-driven per-person shards, data residency, gradual schema rollout); **consistent hashing** covered properly with rendezvous and jump consistent hashing named; the Cassandra/ScyllaDB random-boundary hash-range variant; the warehouse partition/cluster-key aside for BigQuery, Snowflake, and Delta Lake; **heat management / adaptive capacity** as automated hot-shard handling; and single-machine sharding for CPU-core parallelism and NUMA.

**Restructured:** the 1st edition's [[Rebalancing Partitions]] topic with its own subtopics is dissolved — rebalancing is now discussed inside each sharding scheme, with only the automatic-versus-manual question kept as a subtopic.

## Related
- home: [[Home (2e)]] · previous: [[Ch 06 - Replication (2e)]] · next: [[Ch 08 - Transactions (2e)]]
- [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — the scaling architecture sharding implements
- [[Distributed Transactions (2e)]] — the cross-shard write problem this chapter defers
- 1st edition: [[Ch 06 - Partitioning]] — the chapter this one revises and renames
