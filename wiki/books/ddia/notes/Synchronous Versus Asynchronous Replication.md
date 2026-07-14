---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaders and Followers
type: subtopic
tags: [ddia, replication, durability, availability]
sources:
  - raw/ch05.md
---
# Synchronous Versus Asynchronous Replication

> Whether the leader waits for followers to confirm a write determines the trade-off between guaranteed durability and system availability.

## The Idea

When a leader forwards a write to its followers, it has a choice: block until a follower confirms receipt before telling the client the write succeeded (synchronous), or fire-and-forget and confirm immediately (asynchronous). This single configuration decision shapes what happens when nodes fail. Relational databases usually make it configurable; other systems hardwire one mode.

## How It Works

- **Synchronous follower**: the leader withholds its success response (and hides the write from other clients) until that follower acknowledges. If the leader then dies, the write is guaranteed to survive on the synchronous follower.
- **Asynchronous follower**: the leader streams the change but never waits. Followers usually apply changes in under a second, but there is no upper bound — recovery, saturation, or network trouble can push lag to minutes.
- **Semi-synchronous**: since making *every* follower synchronous would let any single node outage freeze all writes, the practical compromise is exactly one synchronous follower plus asynchronous ones. If the synchronous follower goes slow or dies, an asynchronous one is promoted to the synchronous role, keeping an up-to-date copy on at least two nodes.
- **Chain replication** is a research variant of synchronous replication that keeps durability without sacrificing throughput; Microsoft Azure Storage uses it. Replication consistency connects deeply to [[Consensus]], explored in Chapter 9.

## Trade-offs & Pitfalls

- Fully synchronous: any one follower outage halts every write — availability collapses to the weakest node.
- Fully asynchronous: if the leader fails unrecoverably, all writes not yet replicated are gone, so a write acknowledged to the client is **not guaranteed durable**. This is the hidden cost behind the speed.
- Despite that weakness, fully async is common in practice, especially with many or geographically scattered followers, because the leader never stalls waiting on a slow replica.
- Lag is the seed of the read anomalies catalogued in [[Problems with Replication Lag]] and of lost-write scenarios during failover ([[Handling Node Outages]]).

## Examples & Systems

- PostgreSQL and MySQL expose sync/async as configuration.
- Facebook popularized the semi-synchronous MySQL configuration.
- Microsoft Azure Storage implements chain replication.
- Kafka and RabbitMQ mirrored queues follow the same leader-based pattern with configurable acknowledgment depth.

## Related

- up: [[Leaders and Followers]] · chapter: [[Ch 05 - Replication]]
- [[Handling Node Outages]] — async lag makes failover lossy
- [[Problems with Replication Lag]] — anomalies caused by lagging followers
- [[Eventual Consistency]] — the guarantee async followers actually give
- [[Fault-Tolerant Consensus]] — theory linking replication and agreement
