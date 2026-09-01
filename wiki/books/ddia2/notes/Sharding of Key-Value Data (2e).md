---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: topic
tags: [ddia2, skew, hot-spot, hot-key, partition-key, rebalancing]
sources:
  - raw/ch07.md
---
# Sharding of Key-Value Data
You have a large amount of data and want to shard it. **How do you decide which records to store on which nodes?**

**The goal is to spread the data and the query load evenly across nodes.** If every node takes a fair share then, in theory, 10 nodes should handle 10 times the data and 10 times the read and write throughput of one node. And when you add or remove a node you want to **rebalance** the load so it stays evenly distributed.

**If the sharding is unfair, so some shards have more data or queries than others, we call it skewed.** Skew makes sharding much less effective — in the extreme, all the load ends up on one shard, **9 out of 10 nodes are idle, and your bottleneck is the single busy node.** A shard with disproportionately high load is a **hot shard** or **hot spot**; if one key has particularly high load — a celebrity in a social network — it is a **hot key**.

To split the dataset we need **an algorithm that takes a record's partition key as input and says which shard contains it.** In a key-value store the partition key is usually the key or the first part of it; in a relational model it might be a column of a table, **not necessarily its primary key**. And **that algorithm must be amenable to rebalancing** in order to relieve hot spots.

## Subtopics
- [[Sharding by Key Range (2e)]] — contiguous key ranges, good for scans, prone to time-based hot spots.
- [[Sharding by Hash of Key (2e)]] — hash first, then range or modulo; even distribution at the cost of ordering.
- [[Skewed Workloads and Relieving Hot Spots (2e)]] — what to do when the load itself is uneven.
- [[Operations - Automatic Versus Manual Rebalancing (2e)]] — who decides when shards move.

## Key Takeaways
- **Three distinct words worth keeping straight:** *skew* is uneven distribution; a *hot shard* is the shard that suffers from it; a *hot key* is a single key hot enough to cause it. Only the third one resists every sharding scheme, because no scheme can split one key.
- The partition key **need not be the primary key**, and choosing it well is the single highest-leverage decision in a sharded design.
- Rebalancing is not an afterthought — **the algorithm must be designed for it**, which is what disqualifies the obvious mod-N approach.

## Since the 1st Edition
The 1st edition's [[Partitioning of Key-Value Data]] made the same argument with the same vocabulary (skew, hot spots). **New:** the explicit distinction of a **hot key** from a hot shard, and the note that in a relational model the partition key might be a column that is not the primary key. The subtopic structure differs — the 1st edition had rebalancing as a separate top-level topic, while the 2nd folds most of it into the two sharding schemes.

## Related
- chapter: [[Ch 07 - Sharding (2e)]]
- [[Materializing and Updating Timelines (2e)]] — the celebrity problem in its application form
- [[Pros and Cons of Sharding (2e)]] — why the partition-key choice is hard to undo
- 1st edition: [[Partitioning of Key-Value Data]] — the same topic
