---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
type: topic
tags: [ddia, replication, leader-follower, high-availability]
sources:
  - raw/ch05.md
---
# Leaders and Followers

Leader-based replication (also called active/passive or master–slave) is the most widespread answer to the core question of [[Replication]]: how do you make sure every write lands on every replica? One node is designated the leader and is the only node that accepts writes; it records each change locally and streams it to follower nodes through a replication log, and every follower applies those changes in the leader's order. Clients may read from the leader or any follower, so reads scale horizontally while writes stay serialized through a single point. The pattern shows up far beyond relational databases — PostgreSQL, MySQL, Oracle Data Guard, SQL Server, MongoDB, RethinkDB, Espresso, and even message brokers like [[Apache Kafka]] and RabbitMQ all use it.

## Subtopics

- [[Synchronous Versus Asynchronous Replication]] — whether the leader waits for follower acknowledgment before confirming a write, trading durability against availability and latency.
- [[Setting Up New Followers]] — bringing a fresh replica online from a consistent snapshot plus log catch-up, without downtime.
- [[Handling Node Outages]] — catch-up recovery for followers and the perilous failover dance when the leader itself dies.
- [[Implementation of Replication Logs]] — four ways to ship changes: SQL statements, [[Write-Ahead Log]] bytes, logical row-level records, or application-level triggers.

## Key Takeaways

- A single leader gives writes a total order, which sidesteps write conflicts entirely — the main reason this model is so popular.
- Fully synchronous replication is impractical (one dead follower blocks all writes); real systems use semi-synchronous or fully asynchronous setups.
- Asynchronous replication means confirmed writes can be lost if the leader dies before followers receive them — durability is weaker than it looks.
- Failover is where the model gets dangerous: stale new leaders, discarded writes, [[Split Brain]], and badly tuned timeouts have all caused real production incidents.
- The choice of log format (physical WAL vs. logical row-based) decides whether you can run mixed software versions and do zero-downtime upgrades.

## Related

- chapter: [[Ch 05 - Replication]]
- [[Problems with Replication Lag]] — the anomalies async followers create for readers
- [[Multi-Leader Replication]] — relaxing the single-writer constraint
- [[Leaderless Replication]] — abandoning the leader concept entirely
- [[Fault-Tolerant Consensus]] — leader election is at heart a consensus problem
- [[Partitioning and Replication]] — each partition gets its own leader in sharded systems
