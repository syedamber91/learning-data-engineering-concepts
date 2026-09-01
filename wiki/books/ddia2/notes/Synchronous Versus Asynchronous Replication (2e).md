---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, synchronous, asynchronous, semisynchronous, quorum, durability]
sources:
  - raw/ch06.md
---
# Synchronous Versus Asynchronous Replication
> Making all followers synchronous means any one node outage stops the whole system. Making none of them synchronous means a confirmed write can still be lost. Everyone lands somewhere in between.

## The Idea
Whether replication happens synchronously or asynchronously is an important detail of a replicated system — in relational databases it is often configurable; other systems are hardcoded one way or the other.

Consider a user updating their profile image. **Synchronous** replication to a follower means the leader **waits until that follower confirms it received the write** before reporting success to the user and before making the write visible to other clients. **Asynchronous** (or nonblocking) replication means the leader sends the message and **doesn't wait for a response**.

## How It Works
- **Normally replication is quite fast** — most systems apply changes to followers in less than a second — but **there is no guarantee how long it might take**. Followers can fall behind by several minutes or more: if a follower is recovering from a failure, if the system is near maximum capacity, or if there are network problems between nodes.
- **The advantage of synchronous replication** is that the follower is guaranteed to have an up-to-date copy consistent with the leader's, so if the leader suddenly fails the data is still available on the follower.
- **The disadvantage** is that if the synchronous follower doesn't respond — crashed, network fault, any reason — **the write cannot be processed**. The leader must block all writes and wait until the synchronous replica is available again.
- **Therefore it is impracticable for all followers to be synchronous**; any one node outage would grind the whole system to a halt. In practice, a database offering synchronous replication usually means **one follower is synchronous and the others asynchronous**, and if the synchronous one becomes unavailable or slow, an asynchronous one is promoted to synchronous. This guarantees an up-to-date copy on **at least two nodes** — leader plus one synchronous follower — and is called **semisynchronous**.
- **Quorum-based configurations** are another point on the spectrum: a **majority of replicas** (three out of five, including the leader) updated synchronously and the remaining minority asynchronously. Majority quorums are often used in eventually consistent systems or systems using a consensus protocol for automatic leader election.

## Trade-offs & Pitfalls
- **Fully asynchronous configurations lose data on failover.** If the leader fails and is not recoverable, **any writes not yet replicated to followers are lost** — meaning **a write is not guaranteed to be durable even if it has been confirmed to the client**.
- That sounds like a bad trade, but **asynchronous replication is nevertheless widely used**, especially with many followers or geographically distributed ones. The compensating advantage: **the leader can continue processing writes even if all its followers have fallen behind.**

## Examples & Systems
Semisynchronous configurations in relational databases; majority-quorum synchronous replication in consensus-based systems.

## Since the 1st Edition
Very close to the 1st edition's [[Synchronous Versus Asynchronous Replication]] — the same profile-image example, the same semisynchronous argument, the same durability warning. **Added:** the explicit treatment of majority quorums as a middle configuration, linking forward to consensus-based automatic leader election, which the 1st edition did not connect here.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Problems with Replication Lag (2e)]] — what asynchronous replication does to readers
- [[Handling Node Outages (2e)]] — where asynchronous replication's data loss actually bites
- [[Writing to the Database When a Node Is Down (2e)]] — quorums treated in full
- 1st edition: [[Synchronous Versus Asynchronous Replication]] — the same subtopic
