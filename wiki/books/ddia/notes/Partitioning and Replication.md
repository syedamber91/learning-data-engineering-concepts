---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: topic
tags: [ddia, partitioning, replication, distributed-data]
sources:
  - raw/ch06.md
---
# Partitioning and Replication
> Partitioning and replication are orthogonal: each record lives in exactly one partition, yet that partition is usually copied onto several nodes for fault tolerance.

## The Idea
[[Replication]] alone (Chapter 5) keeps full copies of the data on multiple machines, which helps availability and read scaling — but it never shrinks the dataset any single node must hold. Once data volume or write throughput outgrows one machine, the dataset itself has to be split into pieces. That splitting is [[Partitioning]] (also widely called [[Sharding]]): each record, row, or document is assigned to exactly one partition, and each partition behaves like a miniature database of its own. Scalability is the driving motive — spread a big dataset over many disks in a shared-nothing cluster and spread query load over many processors.

Vocabulary varies wildly by system: MongoDB, Elasticsearch, and SolrCloud say *shard*; HBase says *region*; Bigtable says *tablet*; Cassandra and Riak say *vnode*; Couchbase says *vBucket*. They all mean the same thing. Note also that partitioning a database has nothing to do with a *network partition* (netsplit), which is a network fault (Chapter 8 territory).

## How It Works
In practice the two techniques are layered together. A cluster stores several partitions per node, and every partition is replicated to multiple nodes. Under a leader–follower scheme, each partition has its own leader on one node and followers on others — so a single node typically acts as leader for some partitions while simultaneously following others. This interleaving lets the cluster spread both write leadership and storage evenly.

The key design insight: the choice of partitioning scheme is essentially independent of the choice of replication scheme. Everything from [[Leaders and Followers]], [[Multi-Leader Replication]], and [[Leaderless Replication]] applies per-partition without changing how you decide which key goes where. That independence is why Chapter 6 can analyze partitioning while setting replication aside.

## Trade-offs & Pitfalls
- Single-partition queries scale linearly with node count; queries spanning partitions are much harder to parallelize well.
- Partitioned systems date back to 1980s products like Teradata and Tandem NonStop SQL, later rediscovered by NoSQL stores and [[Hadoop]]-style warehouses — transactional vs. analytic tuning differs (see [[Transaction Processing or Analytics]]), but the partitioning fundamentals are the same.
- Because a node hosts many partition roles at once, a node failure affects several partitions' leaders/followers simultaneously — failover logic from Chapter 5 runs per partition.

## Examples & Systems
Teradata and Tandem NonStop SQL pioneered the model; MongoDB, Elasticsearch, SolrCloud, HBase, Bigtable, Cassandra, Riak, and Couchbase are the modern systems whose differing shard terminology all describes this same idea.

## Related
- up: chapter [[Ch 06 - Partitioning]] · part [[Part II - Distributed Data]]
- [[Partitioning of Key-Value Data]] — how keys get assigned to partitions
- [[Rebalancing Partitions]] — moving partitions as nodes change
- [[Leaders and Followers]] — the replication model layered per partition
- [[Handling Node Outages]] — failover applies to each partition's leader
