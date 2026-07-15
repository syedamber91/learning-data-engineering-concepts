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

## Related in the other wiki
- [[partition]] — Kafka's partition operationalizes this concept directly: the unit a topic is split into so brokers and consumers each own a disjoint slice, with the "more consumers than partitions leaves some idle" rule echoing this note's skew/hot-spot concern about uneven load.
- [[bigquery-internals]] — vutr's notes show a metadata-only version of this concept: BigQuery tags storage sets with a partition ID so a query's filter is applied by skipping irrelevant partitions at the metadata layer alone, and separately shows the same skew concern this note raises resurfacing inside Dremel's shuffle layer, resolved by dynamic runtime repartitioning rather than a fixed scheme.
