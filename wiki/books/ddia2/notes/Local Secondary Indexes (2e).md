---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding and Secondary Indexes
type: subtopic
tags: [ddia2, local-index, document-partitioned, scatter-gather, tail-latency]
sources:
  - raw/ch07.md
---
# Local Secondary Indexes
> Each shard indexes only what it holds. Writes touch one shard; reads touch all of them.

## The Idea
**Each shard independently maintains its own secondary indexes, covering only the records in that shard**, and doesn't care what is stored elsewhere. Whenever you write — add, remove, or update a record — **you deal only with the shard containing that record**. Hence **local index**; in information retrieval it is also called a **document-partitioned index**.

## How It Works
The book's example is a used-car sales website. Each listing has a unique ID used as the partition key (IDs 0–499 in shard 0, 500–999 in shard 1, and so on). To let users filter by colour and make, you need secondary indexes on `color` and `make` — fields in a document database, columns in a relational one. **Once the index is declared, the database indexes automatically**: whenever a red car is added, that shard adds its ID to the list of IDs for the index entry `color:red`. **That list of IDs is a postings list.**

**Reading:** if you already know the partition key of the record you want, **you can search just the appropriate shard**. And **if you want only some results rather than all of them, you can send the request to any shard**. But **if you want all the results and don't know their partition key in advance, you must send the query to all shards and combine the results**, because matching records may be scattered — red cars appear in both shard 0 and shard 1.

## Trade-offs & Pitfalls
- **Scatter-gather reads are expensive.** Even querying shards in parallel, **this is prone to tail latency amplification.**
- **It limits scalability.** Adding more shards lets you **store** more data, but **doesn't increase query throughput if every shard has to process every query anyway.**
- **Don't hand-roll this.** The book warns: if your database supports only a key-value model, you might be tempted to implement a secondary index yourself by mapping values to IDs in application code. **If you go down that route you must take great care to keep indexes consistent with the underlying data** — **race conditions and intermittent write failures, where some changes were saved but others weren't, can very easily cause the data to go out of sync.**

**Nevertheless local secondary indexes are widely used**, which tells you the write-side simplicity usually wins.

## Examples & Systems
MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud, and VoltDB all use local secondary indexes.

## Since the 1st Edition
Essentially the 1st edition's "partitioning secondary indexes by document" section, promoted to a named subtopic. The used-car example, the `color:red` postings list, and the scatter-gather cost carry over. **Added:** the explicit warning against implementing secondary indexes in application code, and the framing of scatter-gather cost as **tail latency amplification**, connecting it to the performance vocabulary of Chapter 2.

## Related
- up: [[Sharding and Secondary Indexes (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Global Secondary Indexes (2e)]] — the opposite trade
- [[Use of Response Time Metrics (2e)]] — tail latency amplification
- 1st edition: [[Secondary Indexes]] — the closest predecessor
