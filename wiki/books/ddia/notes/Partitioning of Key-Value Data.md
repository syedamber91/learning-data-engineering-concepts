---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
type: topic
tags: [ddia, partitioning, key-value, skew]
sources:
  - raw/ch06.md
---
# Partitioning of Key-Value Data
> Deciding which node stores which record: the goal is to spread data and query load evenly, and the enemy is skew.

If every node takes a fair share, ten nodes should handle roughly ten times the data and throughput of one. When some partitions carry disproportionately more data or traffic than others, the workload is *skewed*, and in the worst case one overloaded partition — a [[Hot Spots|hot spot]] — becomes the bottleneck while the rest of the cluster idles. Assigning records to nodes at random would balance perfectly but destroys addressability: every read would have to ask every node. So practical schemes derive the partition from the record's primary key, either by sorted key ranges or by hashing, each with distinct strengths around range queries and load distribution.

## Subtopics
- [[Partitioning by Key Range]] — sorted, contiguous key ranges per partition; great for range scans, prone to hot spots.
- [[Partitioning by Hash of Key]] — hash the key to spread load uniformly, sacrificing key ordering; includes the consistent-hashing terminology trap and Cassandra's compound-key compromise.
- [[Skewed Workloads and Relieving Hot Spots]] — when even hashing fails (celebrity keys) and application-level key-splitting tricks.

## Key Takeaways
- The twin goals are even data distribution and even request distribution; skew defeats both.
- Key-range [[Partitioning]] preserves sort order → efficient range scans, but adjacent-key access patterns (e.g., timestamps) pile writes onto one partition.
- Hash partitioning uniformly scatters keys → better load spread, but range queries must hit all partitions.
- Hybrid designs (Cassandra's compound primary key: hash the first column, sort by the rest) recover useful ordering within a partition.
- No current system automatically fixes extreme single-key skew; the application must split hot keys itself.

## Related
- up: chapter [[Ch 06 - Partitioning]] · part [[Part II - Distributed Data]]
- [[Partitioning and Replication]] — the layer beneath: partitions are themselves replicated
- [[Partitioning and Secondary Indexes]] — what happens when access isn't by primary key
- [[SSTables and LSM-Trees]] — sorted storage that makes in-partition range scans cheap
