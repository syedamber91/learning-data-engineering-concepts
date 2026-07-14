---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: topic
tags: [ddia, rebalancing, partitioning, operations]
sources:
  - raw/ch06.md
---
# Rebalancing Partitions
> Clusters change — more queries, more data, failed machines — so partitions must migrate between nodes without breaking the fairness of the load split or the availability of the database.

Growth in query throughput calls for more CPUs; growth in data calls for more disks and RAM; machine failures force survivors to absorb the dead node's work. All three push data and requests from one node to another — a process called *rebalancing*. Whatever [[Partitioning]] scheme is in play, a good rebalance meets three requirements: afterwards, load (storage, reads, writes) is shared fairly across nodes; during it, the database keeps serving reads and writes; and throughout it, no more data moves than necessary, keeping network and disk I/O in check. The chapter's strategies differ mainly in how they keep the key-to-partition mapping stable while shuffling the partition-to-node mapping.

## Subtopics
- [[Strategies for Rebalancing]] — the mod-N anti-pattern, fixed partition counts, dynamic splitting/merging, and partitions proportional to nodes.
- [[Operations - Automatic or Manual Rebalancing]] — the automation gradient and why fully automatic rebalancing plus automatic failure detection can cascade.

## Key Takeaways
- Never use `hash mod N` to place keys: changing the node count reshuffles nearly every key.
- Fixed-partition schemes (Riak, Elasticsearch, Couchbase, Voldemort) over-provision partitions up front and move whole partitions between nodes.
- Dynamic partitioning (HBase, RethinkDB, MongoDB ≥2.4) splits big partitions and merges shrunken ones, like a [[B-Trees|B-tree]] at its top level.
- Cassandra/Ketama fix the partition count *per node*, the closest practical relative of original consistent hashing.
- Rebalancing is expensive and risky enough that a human approval step is often the safer default.

## Related
- up: chapter [[Ch 06 - Partitioning]] · part [[Part II - Distributed Data]]
- [[Partitioning of Key-Value Data]] — the schemes whose boundaries rebalancing preserves or splits
- [[Request Routing]] — routing must track every rebalance
- [[Setting Up New Followers]] — Chapter 5's analogous data-copying-without-downtime problem
- [[partition-reassignment-and-cluster-balancing]] — Kafka's broker-side partition reassignment wrestles with exactly this note's three requirements (fair load, no downtime, minimal data moved), and shows three different answers — the error-prone native tool, Cruise Control's plan-only automation, and AutoMQ's data-free metadata edit.
- [[consumer-group-rebalancing]] — a distinct flavor of the same problem: instead of migrating partition data between storage nodes, Kafka reassigns partition *ownership* between consumers, and this note's availability-during-rebalance requirement maps to Kafka's eager (whole group stops) vs. cooperative (only affected partitions pause) distinction.
