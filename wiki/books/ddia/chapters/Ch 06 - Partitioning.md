---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: chapter-moc
tags: [ddia, partitioning, sharding, moc]
sources:
  - raw/ch06.md
---
# Ch 06 – Partitioning
When a dataset or its query load outgrows what [[Replication]] alone can absorb, the data itself must be split across nodes — [[Partitioning]], a.k.a. [[Sharding]]. This chapter walks the full lifecycle of a partitioned database: how keys are assigned to partitions (sorted ranges versus hashes, and what each does to range queries and [[Hot Spots]]), how [[Secondary Indexes]] complicate the picture (local document-partitioned indexes versus global term-partitioned ones), how partitions migrate when nodes join, leave, or fail (rebalancing strategies and the automation-risk gradient), and how requests find the right node at all (routing tiers, [[ZooKeeper]]-based coordination, gossip, and MPP query engines at the sophisticated end).

## Map
- [[Partitioning and Replication]] — partitions and replicas layer independently; a node leads some partitions and follows others
- [[Partitioning of Key-Value Data]] — spreading data and load evenly by primary key
  - [[Partitioning by Key Range]] — encyclopedia-style sorted ranges; great scans, skew risk
  - [[Partitioning by Hash of Key]] — uniform spread, lost ordering; Cassandra's compound-key middle path
  - [[Skewed Workloads and Relieving Hot Spots]] — celebrity keys and application-side key splitting
- [[Partitioning and Secondary Indexes]] — indexes that don't map neatly onto partitions
  - [[Partitioning Secondary Indexes by Document]] — local indexes, scatter/gather reads
  - [[Partitioning Secondary Indexes by Term]] — global indexes, multi-partition writes, async updates
- [[Rebalancing Partitions]] — moving load as clusters grow, shrink, and fail
  - [[Strategies for Rebalancing]] — mod-N anti-pattern; fixed, dynamic, and per-node partition counts
  - [[Operations - Automatic or Manual Rebalancing]] — automation gradient and cascading-failure risk
- [[Request Routing]] — service discovery for partitioned data: any-node, routing tier, or smart client
  - [[Parallel Query Execution]] — MPP engines beyond single-key access

## Chapter Summary
Partitioning becomes necessary when one machine can no longer store or process the data; the aim is to spread data and query load evenly while avoiding hot spots. Two main key-assignment approaches emerged. *Key-range partitioning* keeps keys sorted so range queries stay efficient, at the cost of hot spots when the application concentrates on adjacent keys; its partitions are typically rebalanced by dynamically splitting oversized ranges. *Hash partitioning* destroys key order but spreads load more evenly; it usually pairs with a fixed set of partitions created up front and moved wholesale between nodes, though dynamic partitioning works here too. Hybrids exist, such as compound keys that hash one component for placement and sort by the rest.

Secondary indexes must themselves be partitioned, two ways: *document-partitioned (local)* indexes colocate index entries with each partition's data, making writes single-partition but reads scatter/gather; *term-partitioned (global)* indexes partition by the indexed value, making reads single-partition but writes multi-partition (and usually asynchronous). Routing techniques span simple partition-aware load balancing up to MPP parallel query execution. The chapter closes on the property that makes partitioned databases scale — partitions operating largely independently — and the trouble that follows when a write spans several partitions and only partially succeeds, the doorway to [[Ch 07 - Transactions]].

## Related
- part: [[Part II - Distributed Data]] · home: [[Home]]
- previous: [[Ch 05 - Replication]] — copies of each partition; replication schemes compose with partitioning
- next: [[Ch 07 - Transactions]] — what happens when operations span partitions
- [[Ch 09 - Consistency and Consensus]] — the agreement machinery behind routing metadata and coordination services
