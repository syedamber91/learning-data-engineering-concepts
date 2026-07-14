---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 6
chapter_title: Partitioning
topic: Partitioning of Key-Value Data
type: subtopic
tags: [ddia, partitioning, hashing, consistent-hashing]
sources:
  - raw/ch06.md
---
# Partitioning by Hash of Key
> Run every key through a hash function and assign partitions ranges of *hashes*, trading away key ordering for uniform load distribution.

## The Idea
Key-range [[Partitioning]] invites skew whenever the application touches nearby keys together. A good hash function is a skew-destroyer: feed it similar strings and it returns numbers scattered uniformly across its output range (e.g., 0 to 2³²−1 for a 32-bit hash). Assign each partition a slice of that hash range and even pathological key distributions spread out evenly.

## How It Works
- The hash need not be cryptographic — Cassandra and MongoDB use MD5, Voldemort uses Fowler–Noll–Vo. What it *must* be is stable across processes: Java's `Object.hashCode()` and Ruby's `Object#hash` can give the same key different values in different runtimes, which disqualifies them.
- Partition boundaries over the hash range can be evenly spaced or chosen pseudorandomly. The pseudorandom variant is often labeled *consistent hashing*, after Karger et al.'s technique for CDN-style caching that avoids central coordination. Kleppmann's advice: the term misleads — it has nothing to do with replica or ACID consistency, and the original algorithm works poorly for databases — so just say *hash partitioning*.
- **Cassandra's compromise:** a compound primary key hashes only its first column to pick the partition, then uses the remaining columns as a sort key within the partition (stored in its SSTables). A key like (user_id, update_timestamp) lets a social app keep each user's posts on one partition, time-ordered, while different users spread across the cluster — an elegant one-to-many pattern.

## Trade-offs & Pitfalls
- The big loss: range queries. Once-adjacent keys scatter everywhere, so MongoDB's hash-sharded mode broadcasts range queries to all partitions, and Riak, Couchbase, and Voldemort simply don't support primary-key range queries.
- Hashing reduces but cannot eliminate [[Hot Spots]] — identical keys always hash identically (see [[Skewed Workloads and Relieving Hot Spots]]).
- Never assign nodes via `hash mod N` — see the rebalancing pitfall in [[Strategies for Rebalancing]].

## Examples & Systems
Cassandra and MongoDB (MD5), Voldemort (FNV), MongoDB ≥2.4 hash-sharding; Riak, Couchbase, Voldemort forgo key-range queries entirely.

## Related
- up: [[Partitioning of Key-Value Data]] · chapter: [[Ch 06 - Partitioning]]
- [[Partitioning by Key Range]] — what hashing gives up
- [[SSTables and LSM-Trees]] — Cassandra's in-partition sort order lives here
- [[Strategies for Rebalancing]] — hash ranges enable fixed and per-node partition schemes
