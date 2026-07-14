---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Request Routing
type: subtopic
tags: [ddia, mpp, parallel-queries, analytics]
sources:
  - raw/ch06.md
---
# Parallel Query Execution
> Most NoSQL stores stop at single-key reads and scatter/gather, but MPP analytic databases decompose whole join-filter-aggregate queries into stages that run in parallel across partitions.

## The Idea
Everything in this chapter so far routes *simple* operations: read or write one key, or at most scatter/gather over document-partitioned [[Secondary Indexes]]. That is roughly the ceiling of query sophistication in most distributed NoSQL datastores. Analytics demands more — a typical data warehouse query strings together joins, filters, groupings, and aggregations over huge swaths of data — and a different class of system, the massively parallel processing (MPP) relational database, exists to run exactly those.

## How It Works
The MPP query optimizer takes a complex declarative query and breaks it into a graph of execution stages and partitions, scheduling as many as possible to run concurrently on different nodes of the cluster. Instead of routing one request to one partition, the engine orchestrates coordinated work across many partitions at once. Queries that scan large fractions of the dataset benefit the most, since scan work divides naturally across nodes.

## Trade-offs & Pitfalls
- This is specialist territory: fast parallel warehouse execution is a deep subfield with heavy commercial investment, driven by the business value of analytics (the OLTP/OLAP divide from [[Transaction Processing or Analytics]]).
- The simplicity gap is real — key-value routing is easy to reason about; multi-stage distributed query plans are not, which is partly why NoSQL stores kept their query models minimal.
- Kleppmann defers the techniques: batch-oriented parallel processing is treated in Chapter 10 (see [[MapReduce and Distributed Filesystems]] and [[Comparing Hadoop to Distributed Databases]]), with the DeWitt/Gray parallel-database literature as further reading.

## Examples & Systems
MPP relational warehouse products (the Teradata lineage noted at the chapter's start) versus the single-key access model of most NoSQL datastores; [[Hadoop]]-based warehouses revisit the same ideas in batch form.

## Related
- up: [[Request Routing]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning Secondary Indexes by Document]] — scatter/gather, the simpler multi-partition read
- [[MapReduce and Distributed Filesystems]] — Chapter 10's parallel execution machinery
- [[Comparing Hadoop to Distributed Databases]] — MPP versus MapReduce head-to-head
- [[Data Warehousing]] — the workload that motivates MPP engines
