---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
type: topic
tags: [ddia2, single-leader, primary-backup, replication-log, failover]
sources:
  - raw/ch06.md
---
# Single-Leader Replication
Each node storing a copy of the database is a **replica**, which raises the obvious question: how do we ensure all the data ends up on all the replicas? Every write must be processed by every replica, or they would diverge. The most common solution is **leader-based**, **primary-backup**, or **active/passive** replication:

1. One replica is designated the **leader** (also **primary** or **source**). Clients send write requests to the leader, which first writes the new data to its local storage.
2. The other replicas are **followers** (also **read replicas**, **secondaries**, or **hot standbys**). Whenever the leader writes new data locally, it also sends the change to all followers as part of a **replication log** or **change stream**. Each follower takes the log and updates its local copy by applying all writes **in the same order as the leader processed them**.
3. A client can read from the leader or any follower — but **writes are accepted only by the leader**; followers are read-only from the client's point of view.

If the database is sharded, **each shard has one leader**; different shards may have leaders on different nodes, but each shard must have exactly one.

## Subtopics
- [[Synchronous Versus Asynchronous Replication (2e)]] — whether the leader waits, and what that costs.
- [[Setting Up New Followers (2e)]] — bringing a new replica online without downtime.
- [[Handling Node Outages (2e)]] — follower recovery, leader failover, and split brain.
- [[Implementation of Replication Logs (2e)]] — the three log formats and their operational consequences.
- [[Problems with Replication Lag (2e)]] — the three anomalies asynchronous followers produce.
- [[Solutions for Replication Lag (2e)]] — application-level fixes versus choosing a stronger database.

## Key Takeaways
- Single-leader replication is **very widely used**: built into many relational databases (PostgreSQL, MySQL, Oracle Data Guard, SQL Server Always On availability groups), some document databases (MongoDB, DynamoDB), message brokers such as **Kafka**, replicated block devices such as **DRBD**, and some network filesystems.
- **Many consensus algorithms are also single-leader.** Raft — used for replication in CockroachDB, TiDB, etcd, and RabbitMQ quorum queues — is based on a single leader and **automatically elects a new one if the old one fails**.
- **Terminology:** older documents use *master–slave replication*, which means the same thing but **should be avoided as it is widely considered offensive**.
- The defining property is **ordering**: the leader decides the order in which writes are processed, and every follower applies them in that order. Everything single-leader replication can guarantee — and everything the other two families struggle with — follows from that.

## Since the 1st Edition
This is the 1st edition's [[Leaders and Followers]], **renamed** to Single-Leader Replication for symmetry with the other two families. The mechanism is unchanged. **Added:** the explicit note that Raft-based systems (CockroachDB, TiDB, etcd, RabbitMQ quorum queues) are single-leader with automatic election, and DynamoDB and Kafka added to the roster. The master–slave terminology note is stated more firmly.

## Related
- chapter: [[Ch 06 - Replication (2e)]]
- [[Multi-Leader Replication (2e)]] and [[Leaderless Replication (2e)]] — the alternatives
- [[Consensus (2e)]] — where automatic leader election gets its guarantees
- 1st edition: [[Leaders and Followers]] — the same topic under its old name

## In the vutr data-engineering wiki
- [[leader-follower-replication]] — vutr applies this same single-leader mechanism to Kafka partitions, where the durability guarantee turns into a concrete cross-AZ replication *bill* — the cost pressure that produced the diskless brokers the 2nd edition now mentions.
