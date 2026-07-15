---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: topic
tags: [ddia, secondary-indexes, partitioning, search]
sources:
  - raw/ch06.md
---
# Partitioning and Secondary Indexes
> Secondary indexes don't map cleanly onto partitions, forcing a choice between per-partition local indexes and a separately partitioned global index.

Primary-key partitioning works because the key alone determines the partition. [[Secondary Indexes]] break that assumption: they answer "find all records where color = red"-style queries, where matching records can live on any partition. They are indispensable — the bread and butter of relational databases, common in document stores, and the entire reason search servers like Solr and Elasticsearch exist — yet some key-value stores (HBase, Voldemort) skipped them to dodge the implementation complexity, while others (Riak) later added them because modeling without them is painful. Two architectures resolve the mismatch: index locally per partition (cheap writes, expensive scatter/gather reads) or index globally by term (cheap targeted reads, expensive multi-partition writes).

## Subtopics
- [[Partitioning Secondary Indexes by Document]] — each partition indexes only its own documents (local index); reads scatter/gather.
- [[Partitioning Secondary Indexes by Term]] — one global index, itself partitioned by the indexed value (term); writes touch many partitions.

## Key Takeaways
- A secondary index rarely identifies records uniquely — it locates all occurrences of a value, which naturally spans partitions.
- Document-partitioned (local): write updates one partition; read must query all partitions and merge — scatter/gather, vulnerable to tail latency amplification.
- Term-partitioned (global): read hits only the partition owning the term; a single document write may touch many index partitions, so updates are typically asynchronous.
- Synchronous global-index updates would require a distributed transaction across index partitions — support for which is uneven (see [[Distributed Transactions and Consensus]]).
- Rolling your own secondary index over a bare key-value store risks index/data divergence from races and partial write failures — this is a multi-object transaction problem ([[Single-Object and Multi-Object Operations]]).

## Related
- up: chapter [[Ch 06 - Partitioning]] · part [[Part II - Distributed Data]]
- [[Other Indexing Structures]] — Chapter 3's single-node secondary index foundations
- [[Partitioning of Key-Value Data]] — the primary-key schemes these indexes complicate
- [[The Slippery Concept of a Transaction]] — why index consistency needs transactions
