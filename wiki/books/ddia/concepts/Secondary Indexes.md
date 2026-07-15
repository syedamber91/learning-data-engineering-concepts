---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, indexing]
sources:
  - raw/ch03.md
  - raw/ch06.md
  - raw/ch07.md
---
# Secondary Indexes

Indexes on attributes other than the primary key, letting you find records by any
field. On one machine they're routine ([[Other Indexing Structures]], Ch 3); once
data is partitioned they get interesting: index locally per partition (document-
partitioned — writes stay local, reads must scatter/gather) or index globally by
term (term-partitioned — reads hit one partition, writes touch several, usually
asynchronously).

In the book: [[Partitioning and Secondary Indexes]] (Ch 6); rebuilt as
[[Derived Data]] by batch/stream pipelines in Part III ([[The Output of Batch Workflows]], [[Observing Derived State]]).

## Referenced In
- [[Actual Serial Execution]]
- [[Batch and Stream Processing]]
- [[Ch 03 - Storage and Retrieval]]
- [[Ch 06 - Partitioning]]
- [[Ch 07 - Transactions]]
- [[Composing Data Storage Technologies]]
- [[Data Structures That Power Your Database]]
- [[Designing Applications Around Dataflow]]
- [[Observing Derived State]]
- [[Other Indexing Structures]]
- [[Parallel Query Execution]]
- [[Part II - Distributed Data]]
- [[Part III - Derived Data]]
- [[Partitioning Secondary Indexes by Document]]
- [[Partitioning Secondary Indexes by Term]]
- [[Partitioning and Secondary Indexes]]
- [[Single-Object and Multi-Object Operations]]
- [[Sort Order in Column Storage]]
- [[The Output of Batch Workflows]]
- [[The Slippery Concept of a Transaction]]
