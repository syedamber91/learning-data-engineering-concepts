---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Partitioning and Secondary Indexes
type: subtopic
tags: [ddia, local-index, scatter-gather, secondary-indexes]
sources:
  - raw/ch06.md
---
# Partitioning Secondary Indexes by Document
> Each partition keeps a private (local) secondary index over only its own documents — writes stay local, but reads must scatter/gather across every partition.

## The Idea
Picture a used-car marketplace partitioned by listing ID (documents 0–499 on partition 0, 500–999 on partition 1, and so on). Shoppers filter by color and make, so you need [[Secondary Indexes]] on those fields. The simplest arrangement: let every partition maintain its own index entries — `color:red` on partition 0 lists only the red cars whose document IDs live on partition 0. Because each partition minds its own business, this is called a *local index* (versus the *global* index of the term-partitioned approach).

## How It Works
- When a document is added, updated, or removed, only the partition owning that document ID is involved; that partition updates its own index entries (e.g., appending the new car's ID under `color:red`) automatically if the index is declared.
- Index maintenance never crosses partition boundaries — the write path is exactly as cheap as a plain key-value write.
- Reads on the index are the mirror image: nothing guarantees red cars cluster on one partition, so a "red cars" query must be broadcast to *all* partitions, and the client (or coordinator) merges the answers — the pattern known as scatter/gather.

## Trade-offs & Pitfalls
- Scatter/gather makes secondary-index reads expensive even when partitions are queried in parallel, and it is prone to tail latency amplification — the slowest partition gates the whole query (the percentile effect from [[Describing Performance]]).
- Multiple filters in one query (color AND make) make it even harder to confine the query to one partition.
- Vendors advise designing the [[Partitioning]] scheme so common index queries hit a single partition — often impossible in practice.
- A DIY index over a plain key-value store risks going out of sync with the data via races and partial failures — a multi-object transaction concern ([[Single-Object and Multi-Object Operations]]).

## Examples & Systems
Widely used despite the read cost: MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud, and VoltDB all take the document-partitioned route.

## Related
- up: [[Partitioning and Secondary Indexes]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning Secondary Indexes by Term]] — the global alternative with the opposite costs
- [[Other Indexing Structures]] — what a secondary index is on a single node
- [[Parallel Query Execution]] — scatter/gather as the ceiling of NoSQL query sophistication
