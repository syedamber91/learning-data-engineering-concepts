---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Partitioning and Secondary Indexes
type: subtopic
tags: [ddia, global-index, term-partitioned, secondary-indexes]
sources:
  - raw/ch06.md
---
# Partitioning Secondary Indexes by Term
> Build one global secondary index covering all data, then partition the *index itself* by the indexed value — reads hit one partition, writes fan out to many.

## The Idea
Instead of every partition indexing only its own documents, a *global* index spans the whole dataset. Storing it on one node would recreate the bottleneck [[Partitioning]] exists to remove, so the index is partitioned too — but by the indexed value (the *term*) rather than by document ID. In the used-car example, all red cars from every data partition appear under `color:red`, and the index is split so terms a–r live on one index partition and s–z on another (make gets its own split). The word *term* comes from full-text search, where terms are the words occurring in documents — full-text indexes being one flavor of [[Secondary Indexes]].

## How It Works
- The term determines the index partition, so a query for one value goes straight to exactly one partition — no scatter/gather.
- The index can be partitioned by the term itself (enables range scans over the term, e.g., asking-price brackets) or by a hash of the term (evener load spread) — the same range-vs-hash trade as [[Partitioning by Key Range]] vs [[Partitioning by Hash of Key]].
- A single document write may contain many terms landing on many different index partitions on different nodes, so keeping the index perfectly current would need a distributed transaction spanning them all — which most systems don't offer (see [[Distributed Transactions and Consensus]]).
- In practice updates are asynchronous: read the index right after a write and your change may not be visible yet.

## Trade-offs & Pitfalls
- Reads win, writes lose: targeted single-partition lookups versus slower, multi-partition index maintenance.
- Asynchrony means the index lags the data; Amazon DynamoDB documents sub-second propagation for its global secondary indexes under normal conditions, with longer delays during infrastructure faults.
- Choosing term-vs-hash partitioning of the index re-imports the range-query/hot-spot trade-off at the index layer.

## Examples & Systems
Amazon DynamoDB global secondary indexes; Riak's search feature; Oracle's data warehouse, which lets administrators pick local or global indexing per case. Implementation of term-partitioned indexes returns in Chapter 12 (see [[Composing Data Storage Technologies]]).

## Related
- up: [[Partitioning and Secondary Indexes]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning Secondary Indexes by Document]] — the local-index mirror image
- [[Distributed Transactions and Consensus]] — what synchronous global updates would require
- [[Composing Data Storage Technologies]] — Chapter 12 revisits building these indexes
