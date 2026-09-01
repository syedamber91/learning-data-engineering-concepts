---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: topic
tags: [ddia2, sharding, horizontal-scaling, partition-key, numa]
sources:
  - raw/ch07.md
---
# Pros and Cons of Sharding
**The primary reason for sharding a database is scalability.** It is the solution when data volume or write throughput has become too great for a single node, letting you spread both across multiple nodes. (**If read throughput is the problem you don't necessarily need sharding** — read scaling with followers works.)

Sharding is one of the main tools for **horizontal scaling** — growing capacity by adding more, smaller machines rather than moving to a bigger one. If you can divide the workload so each shard handles a roughly equal share, you can assign shards to different machines and process their data and queries in parallel.

## Key Takeaways
- **Replication is useful at both small and large scale** because it enables fault tolerance and offline operation. **Sharding is a heavyweight solution mostly relevant at large scale.** If a single machine can handle your data volume and write throughput — **and a single machine can do a lot nowadays** — it is often better to avoid sharding and stick with a single-shard database.
- **The reason is complexity.** You typically must decide which records go in which shard by choosing a **partition key**; all records with the same partition key land in the same shard. **This choice matters because accessing a record is fast if you know its shard, and requires an inefficient search across all shards if you don't.** And **the sharding scheme is difficult to change.**
- **Sharding often works well for key-value data**, where you can shard by key, **but is harder with relational data**, where you may want to search by a secondary index or join records distributed across shards.
- **Cross-shard writes need distributed transactions.** A write may need to update related records in several shards; single-node transactions are common, but ensuring consistency across shards requires a **distributed transaction** — available in some databases but **usually much slower than single-node transactions**, and potentially a bottleneck for the system as a whole.
- **Sharding is also used on a single machine.** Some systems run **one single-threaded process per CPU core** to exploit CPU parallelism, or to take advantage of a **NUMA** architecture where some memory banks are closer to one CPU than others. **Redis, VoltDB, and FoundationDB** use one process per core and rely on sharding to spread load across cores in the same machine.

## Since the 1st Edition
New as an explicit topic. The 1st edition opened its partitioning chapter with a brief statement that the main reason is scalability and moved straight into schemes. **The 2nd edition adds the counterargument** — sharding is heavyweight, avoid it if one machine suffices — mirroring the same "don't distribute prematurely" stance it added to [[Distributed Versus Single-Node Systems (2e)]] in Chapter 1. The partition-key discussion, the relational-data difficulty, the distributed-transaction cost, and single-machine sharding for CPU cores and NUMA are all new here.

## Related
- chapter: [[Ch 07 - Sharding (2e)]]
- [[Distributed Versus Single-Node Systems (2e)]] — the same caution, one chapter's worth earlier
- [[Sharding and Secondary Indexes (2e)]] — why relational data is harder
- [[Distributed Transactions (2e)]] — the cost of cross-shard writes
