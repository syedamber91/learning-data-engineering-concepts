---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: topic
tags: [ddia2, secondary-index, local-index, global-index, sharding]
sources:
  - raw/ch07.md
---
# Sharding and Secondary Indexes
Every sharding scheme so far **relies on the client knowing the partition key for the record it wants**. That is easiest in a key-value model, where the partition key is the first part of the primary key (or the whole key), so the partition key determines the shard and routes reads and writes to the responsible node.

**Secondary indexes complicate this.** A secondary index usually **doesn't identify a record uniquely** but is a way of searching for occurrences of a particular value: find all actions by user 123, find all articles containing the word *hogwash*, find all cars whose colour is red.

Key-value stores often don't have secondary indexes, but they are **a standard feature of relational databases and common in document databases** — and this kind of indexing is **the raison d'être of full-text search engines such as Solr and Elasticsearch**. **The problem is that secondary indexes don't map neatly to shards**, and there are two main approaches: **local** and **global**.

## Subtopics
- [[Local Secondary Indexes (2e)]] — each shard indexes only its own records; document-partitioned.
- [[Global Secondary Indexes (2e)]] — one index across all shards, itself sharded by indexed value; term-partitioned.

## Key Takeaways
- The two approaches make **exactly opposite trade-offs**: local indexes are cheap to write and expensive to read; global indexes are cheap to read and expensive (and harder to keep consistent) to write.
- The choice therefore follows your read/write ratio and how long your postings lists get, not from one being technically superior.
- **A secondary index needs to be sharded too** — you cannot escape the problem by putting the index on one node, since that node becomes a bottleneck and defeats the purpose of sharding.

## Since the 1st Edition
The 1st edition's [[Partitioning and Secondary Indexes]] made the same local/global (document-/term-partitioned) split with the same used-car worked example, and the substance is largely intact. **Added:** an updated systems roster on both sides, and a sharper statement of the read/write trade. The 2nd edition also adds an explicit warning against hand-rolling secondary indexes in application code on top of a key-value store.

## Related
- chapter: [[Ch 07 - Sharding (2e)]]
- [[Multicolumn and Secondary Indexes (2e)]] — secondary indexes on a single node
- [[Full-Text Search (2e)]] — where postings lists and terms come from
- 1st edition: [[Partitioning and Secondary Indexes]] — the same topic
