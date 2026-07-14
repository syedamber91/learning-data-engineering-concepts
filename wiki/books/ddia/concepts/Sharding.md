---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, partitioning]
sources:
  - raw/ch06.md
---
# Sharding

Synonym for [[Partitioning]] — splitting a dataset so each node owns a subset;
the term used by MongoDB, Elasticsearch, and others (region/tablet/vnode elsewhere).
All the same design questions: how to assign keys ([[Partitioning by Key Range]] vs
[[Partitioning by Hash of Key]]), how to handle [[Hot Spots]], how to rebalance
([[Rebalancing Partitions]]) and route requests ([[Request Routing]]).

See [[Ch 06 - Partitioning]] for the full treatment.

## Referenced In
- [[Approaches for Coping with Load]]
- [[Ch 06 - Partitioning]]
- [[Part II - Distributed Data]]
- [[Partitioning and Replication]]
- [[Partitioning by Key Range]]

## Related in the other wiki
- [[message-key-partitioning-strategies]] — Kafka never uses the word "sharding," but message-key routing is this note's disjoint-subset-per-node idea under Kafka's own name: the producer's key hash is functionally the shard key deciding which partition a message belongs to.
