---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, partitioning]
sources:
  - raw/ch06.md
---
# Partitioning

Splitting a large dataset into disjoint subsets (partitions/shards) so different
nodes own different pieces. The goal is scalability: spread data volume and query
load evenly. The enemies are skew and [[Hot Spots]] — a partitioning scheme that
sends disproportionate load to one node forfeits the benefit.

Book home ground: [[Ch 06 - Partitioning]] — key-range vs hash schemes
([[Partitioning by Key Range]], [[Partitioning by Hash of Key]]), secondary-index
strategies, [[Rebalancing Partitions]], and [[Request Routing]]. Pairs with
[[Replication]]; revisited by batch/stream systems that partition work the same way
([[MapReduce]], [[Partitioned Logs]]).

## Referenced In
- [[Actual Serial Execution]]
- [[Approaches for Coping with Load]]
- [[Ch 06 - Partitioning]]
- [[Consistent Prefix Reads]]
- [[Home]]
- [[Enforcing Constraints]]
- [[MapReduce Job Execution]]
- [[Network Faults in Practice]]
- [[Part II - Distributed Data]]
- [[Partitioned Logs]]
- [[Partitioning Secondary Indexes by Document]]
- [[Partitioning Secondary Indexes by Term]]
- [[Partitioning and Replication]]
- [[Partitioning by Hash of Key]]
- [[Partitioning of Key-Value Data]]
- [[Processing Streams]]
- [[Rebalancing Partitions]]
- [[Scalability]]
- [[Serializability]]
- [[Skewed Workloads and Relieving Hot Spots]]
- [[Strategies for Rebalancing]]
- [[The Birth of NoSQL]]
