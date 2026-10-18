---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding and Secondary Indexes
type: subtopic
tags: [ddia2, global-index, term-partitioned, postings-list, dynamodb]
sources:
  - raw/ch07.md
---
# Global Secondary Indexes
> One index covering every shard — itself sharded, but by the indexed value rather than by the primary key.

## The Idea
Rather than each shard having its own local index, **construct a global index covering data in all shards**. **You can't store that index on one node**, since it would become a bottleneck and defeat the purpose of sharding — so **a global index must also be sharded, but it can be sharded differently from the primary-key index.**

In the used-car example, the IDs of red cars from **all** shards appear under `color:red`, and the index is sharded so that **colours starting with a–r are in shard 0 and s–z in shard 1**; the index on make is partitioned similarly, with the boundary between f and h.

This is a **term-partitioned** index. In full-text search a **term** is a keyword you can search for; here it generalises to **any value you can search for in the secondary index**. **The global index uses the term as the partition key**, so looking for a particular term tells you which shard to query. As with primary sharding, a shard can hold **a contiguous range of terms** or terms assigned **by hash**.

## How It Works
- **A query with a single condition** — `color = red` — **needs to read from only a single shard** to fetch the postings list. That is the whole advantage.
- **But if you want records and not just IDs, you still have to read from all the shards responsible for those IDs.**

## Trade-offs & Pitfalls
- **Multiple search conditions are the weak point.** Searching for cars of a certain colour *and* a certain make, or multiple words in the same text, means **those terms will likely be assigned to different shards**. Computing the logical AND requires **finding all IDs occurring in both postings lists** — **no problem if the lists are short, but slow to send over the network for intersection if they are long.**
- **Writes are more complicated than with local indexes**, because **writing a single record might affect multiple shards of the index** — every term in the document might be on a different shard. **This makes it harder to keep the secondary index in sync with the underlying data.** One option is a **distributed transaction** to atomically update the shards storing the primary record and its secondary indexes.
- **Or accept staleness.** **DynamoDB reflects writes in global indexes asynchronously, so reads from a global index may be stale** — the same situation as replication lag.
- **The verdict:** global indexes are useful **if read throughput is higher than write throughput, and if the postings lists are not too long.**

## Examples & Systems
CockroachDB, TiDB, and YugabyteDB use global secondary indexes; **DynamoDB supports both local and global**, with asynchronous global index updates.

## Since the 1st Edition
The 1st edition's "partitioning secondary indexes by term" section, promoted to a named subtopic. The term-partitioned concept, the a–r/s–z index sharding, and the write-complexity argument carry over. **Added:** the **multi-term AND intersection cost** stated explicitly; the modern systems roster (CockroachDB, TiDB, YugabyteDB); and DynamoDB's asynchronous global index updates named as a concrete instance of index staleness.

## Related
- up: [[Sharding and Secondary Indexes (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Local Secondary Indexes (2e)]] — the opposite trade
- [[Distributed Transactions (2e)]] — one way to keep a global index in sync
- [[Full-Text Search (2e)]] — postings lists and their intersection
- 1st edition: [[Secondary Indexes]] — the closest predecessor
