---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Rebalancing Partitions
type: subtopic
tags: [ddia, rebalancing, mod-n, dynamic-partitioning]
sources:
  - raw/ch06.md
---
# Strategies for Rebalancing
> Four ways to assign partitions to nodes: the mod-N trap to avoid, and three real strategies — fixed partition count, dynamic splitting, and per-node proportional partitions.

## The Idea
Rebalancing should move as little data as possible while restoring fairness. The naive scheme fails exactly this test, and the three production strategies differ in how the *number* of partitions relates to data size and node count.

## How It Works
**How not to do it — hash mod N.** Mapping a key to node `hash(key) mod N` looks obvious but couples every key's placement to the node count. Take hash 123456: with 10 nodes it sits on node 6, at 11 nodes it must move to node 3, at 12 nodes to node 0. Nearly every key relocates on every cluster resize — ruinously expensive. Hence hash *ranges*, not mod.

**Fixed number of partitions.** Create far more partitions than nodes from day one — say 1,000 partitions on a 10-node cluster, ~100 each. A joining node steals a few partitions from every existing node; a leaving node's partitions are redistributed. Keys never change partitions; only whole partitions change nodes, and the old assignment keeps serving traffic until the transfer completes. You can even hand more partitions to beefier machines. Used by Riak, Elasticsearch, Couchbase, and Voldemort.

**Dynamic partitioning.** With key-range [[Partitioning]], fixed boundaries guessed wrong could dump all data into one partition. Instead, HBase and RethinkDB split a partition when it exceeds a size threshold (HBase default 10 GB) and merge neighbors when one shrinks — behavior akin to the top level of a [[B-Trees|B-tree]]. Split halves can migrate to other nodes (HBase moves files via [[HDFS]]). Partition count tracks data volume. MongoDB ≥2.4 splits dynamically for both key-range and hash schemes.

**Proportional to nodes.** Cassandra and Ketama fix the partitions *per node* (Cassandra: 256 by default). Partition sizes grow with data until nodes are added; a joining node randomly picks existing partitions to split and takes half of each. Random boundary picking requires hash partitioning and is the closest real-world descendant of Karger-style consistent hashing; Cassandra 3.0 added an allocation algorithm avoiding unfair splits.

## Trade-offs & Pitfalls
- Fixed count: the initial number caps your maximum node count and is hard to size when data volume is unpredictable — too-large partitions make recovery slow, too many partitions waste overhead; "just right" is elusive.
- Dynamic: an empty database starts as a single partition, bottlenecking on one node until the first split — mitigated by *pre-splitting* (HBase, MongoDB), which itself demands advance knowledge of the key distribution.
- Proportional: random splits can be individually unfair; fairness emerges only on average across many partitions.

## Examples & Systems
Riak, Elasticsearch, Couchbase, Voldemort (fixed); HBase, RethinkDB, MongoDB (dynamic); Cassandra, Ketama (per-node).

## Related
- up: [[Rebalancing Partitions]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning by Hash of Key]] — hash ranges enable these schemes; consistent-hashing caveats
- [[Partitioning by Key Range]] — the scheme that forces dynamic splitting
- [[Operations - Automatic or Manual Rebalancing]] — who triggers all this movement
