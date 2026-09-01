---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding of Key-Value Data
type: subtopic
tags: [ddia2, hash-sharding, consistent-hashing, mod-n, rebalancing, murmur3]
sources:
  - raw/ch07.md
---
# Sharding by Hash of Key
> A good hash function takes skewed data and makes it uniformly distributed. Then the only question left is how you map hashes to shards — and `% N` is the wrong answer.

## The Idea
Key-range sharding is useful when you want records with **nearby but different partition keys grouped into the same shard** — timestamps, for instance. **If you don't care whether partition keys are near each other** — tenant IDs in a multitenant application — a common approach is to **hash the partition key first** and then map the hash to a shard.

A good hash function **takes skewed data and makes it uniformly distributed**: give a 32-bit hash function a new string and it returns a seemingly random number from 0 to 2³² − 1; even very similar inputs produce hashes evenly spread across the range, **while the same input always produces the same output**.

**The hash function need not be cryptographically strong** — MongoDB uses MD5, Cassandra and ScyllaDB use Murmur3. But **many built-in language hash functions are unsuitable for sharding**: in **Java's `Object.hashCode()` and Ruby's `Object#hash`, the same key may have a different hash value in different processes.**

## How It Works
**Hash modulo number of nodes — and why it fails.** The obvious approach is `hash(key) % N` for N nodes. **The problem is that if N changes, most keys have to move.** With three nodes, node 0 stores keys whose hashes are 0, 3, 6, 9…; add a fourth node and the key with hash 3 moves to node 3, hash 6 moves to node 2, hash 9 moves to node 1, and so on. **`mod N` is easy to compute but leads to very inefficient rebalancing, with a lot of unnecessary movement.** We need an approach that moves as little data as possible.

**Fixed number of shards.** One simple, widely used solution: **create many more shards than there are nodes and assign several shards to each node.** A cluster of 10 nodes might be split into **1,000 shards from the outset, 100 per node**; a key is stored in shard `hash(key) % 1,000` and the system separately tracks which shard is on which node. Adding a node means **reassigning some shards** from existing nodes until they are fairly distributed again; removing one is the reverse.

**Only entire shards move between nodes, which is cheaper than splitting shards.** The number of shards doesn't change, nor does the assignment of keys to shards — **only the assignment of shards to nodes.** Reassignment isn't immediate, since transferring data takes time, **so the old assignment is used for reads and writes while the transfer is in progress.**

It's common to choose a shard count **divisible by many factors**, so the dataset splits evenly across various numbers of nodes without requiring a power of 2. **You can also account for mismatched hardware: assign more shards to more powerful nodes** so they take a greater share of load. Used by **Citus** (a sharding layer for PostgreSQL), **Riak, Elasticsearch, and Couchbase**.

**Sharding by hash range.** If the required number of shards can't be predicted in advance, use a scheme where it **adapts to the workload**. Combine key-range sharding with a hash function so **each shard contains a range of hash values rather than a range of keys**. With a 16-bit hash returning 0 to 65,535, even very similar inputs (consecutive timestamps) hash uniformly across the range, and you assign 0–16,383 to shard 0, 16,384–32,767 to shard 1, and so on. **As with key ranges, a shard can be split when it becomes too big or too heavily loaded** — still expensive, but happening as needed, so **the number of shards adapts to data volume rather than being fixed in advance.**

**Cassandra and ScyllaDB use a variant**: the hash space is split into a number of ranges **proportional to the number of nodes** (16 per node in Cassandra by default, 256 in ScyllaDB) **with random boundaries**, so some ranges are bigger than others — **but having multiple ranges per node evens the imbalances out.** When nodes are added or removed, boundaries are adjusted and shards split or merged, **giving a new node an approximately fair share without transferring more data than necessary.**

**Consistent hashing** is a hash function mapping keys to a specified number of shards such that **the number of keys per shard is roughly equal** and **when the number of shards changes, as few keys as possible move.** (**"Consistent" here has nothing to do with replica consistency or ACID consistency** — it describes a key's tendency to stay in the same shard.) Cassandra and ScyllaDB's algorithm is similar to the original definition; other algorithms include **highest random weight, also known as rendezvous hashing**, and **jump consistent hashing**. With these, **rather than splitting existing shards into subranges for a new node, the new node is assigned individual keys previously scattered across all the other nodes** — which is preferable depends on the application.

## Trade-offs & Pitfalls
- **The fixed-shard-count approach works well only if you estimate the shard count correctly up front.** If you later need more nodes than shards, **an expensive resharding operation is required**, splitting each shard and writing it to new files with a lot of additional disk space. **Some systems don't allow resharding while concurrently writing**, making it hard to change the shard count without downtime.
- **Choosing the right number is hard when dataset size is highly variable.** Each shard holds a fixed fraction of the total, so **shard size grows with the cluster's data**. Very large shards make rebalancing and failure recovery expensive; too-small shards incur too much overhead. **The best performance comes when shard size is "just right"** — hard to hit with a fixed count and a varying dataset.
- **Hash sharding's standing cost: range queries over the partition key are not efficient**, since keys in the range are scattered across all shards. **But if the key has two or more columns and only the first is the partition key, you can still range-query efficiently over the later columns** — as long as all records in the range share a partition key, they are in the same shard.
- **Data warehouses do the same thing under different names.** BigQuery's partition key determines the partition while **cluster columns** determine sort order within it; Snowflake assigns **micro-partitions** automatically but lets users define **cluster keys**; Delta Lake supports both manual and automatic partition assignment plus cluster keys. **Clustering improves not only range scan performance but compression and filtering too.**

## Examples & Systems
MD5 (MongoDB), Murmur3 (Cassandra, ScyllaDB); Citus, Riak, Elasticsearch, Couchbase (fixed shard count); YugabyteDB, DynamoDB, MongoDB (hash-range); rendezvous and jump consistent hashing.

## Since the 1st Edition
The 1st edition's [[Partitioning by Hash of Key]] covered hashing, mod-N's failure, and the fixed-shard-count approach. **Substantially new:** hash-range sharding as a distinct scheme; the **Cassandra/ScyllaDB random-boundary variant** with its per-node range counts; **consistent hashing defined properly** with rendezvous and jump consistent hashing named and the "consistent means something else here" caveat; the **variable-dataset-size difficulty** with fixed shard counts; assigning more shards to more powerful nodes; and the **data warehouse partition/cluster-key aside**. The 1st edition also discussed consistent hashing briefly but dismissively; the 2nd gives it a fair treatment.

## Related
- up: [[Sharding of Key-Value Data (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Sharding by Key Range (2e)]] — what hashing gives up
- [[Skewed Workloads and Relieving Hot Spots (2e)]] — why uniform keys still aren't uniform load
- [[Column-Oriented Storage (2e)]] — where warehouse clustering pays off
- 1st edition: [[Partitioning by Hash of Key]] — the same subtopic
