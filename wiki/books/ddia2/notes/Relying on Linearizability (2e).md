---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia2, leader-election, uniqueness-constraint, cross-channel, zookeeper]
sources:
  - raw/ch10.md
---
# Relying on Linearizability
> Three cases where you actually need it: electing exactly one leader, enforcing a hard uniqueness constraint, and any time two communication channels connect the same two parties.

## The Idea
**Viewing the final score of a sporting match is a frivolous example** — a result outdated by a few seconds is unlikely to cause real harm. **But in a few areas linearizability is an important requirement for correctness.**

## How It Works
**Locking and leader election.** A single-leader system must ensure **there is indeed only one leader, not several (split brain).** One way to elect one is a **lease**: every node that starts up tries to acquire it, and the one that succeeds becomes leader. **However this is implemented, it must be linearizable — it shouldn't be possible for two nodes to acquire the lease at the same time.**

**Coordination services like ZooKeeper and etcd are often used to implement distributed leases and leader election**, using consensus algorithms to provide linearizable operations fault-tolerantly. **Many subtle details are involved** — the fencing issue among them — and **libraries like Apache Curator help by providing higher-level recipes on top of ZooKeeper. But a linearizable storage service is the basic foundation for these coordination tasks.**

> **Strictly speaking, ZooKeeper provides linearizable writes, but reads may be stale**, since there is no guarantee they are served from the current leader. **etcd since version 3 provides linearizable reads by default.**

**Distributed locking is also used at a much more granular level in some databases** — **Oracle Real Application Clusters (RAC)** uses **a lock per disk page**, with multiple nodes sharing access to the same disk storage. **Since these linearizable locks are on the critical path of transaction execution, RAC deployments usually have a dedicated cluster interconnect network** for communication between database nodes.

**Constraints and uniqueness guarantees.** A username or email address must uniquely identify one user; a file storage service cannot have two files with the same path. **If you want to enforce this as the data is written — such that if two people concurrently create a user with the same name, one gets an error — you need linearizability.**

**The situation is similar to a lock**: registering a username is like **acquiring a lock on the chosen name**, and **very similar to an atomic CAS** setting the username to the claimer's ID provided it isn't already taken. **Similar issues arise for ensuring a bank balance never goes negative, not selling more items than you have in stock, or two people not booking the same seat.** **These constraints all require a single up-to-date value that all nodes agree on.**

**In real applications it is sometimes acceptable to treat such constraints loosely** — **if a flight is overbooked, you can move customers to a different flight and offer compensation.** In such cases linearizability may not be needed. **But a hard uniqueness constraint, such as you typically find in relational databases, requires linearizability.** **Other kinds of constraints, such as foreign-key or attribute constraints, can be implemented without it.**

**Cross-channel timing dependencies.** Notice something about the sports-website example: **if Aaliyah hadn't exclaimed the score, Bryce wouldn't have known his result was stale.** **The violation was noticed only because there was an additional communication channel** — Aaliyah's voice to Bryce's ears.

**The same arises in computer systems.** A website lets users upload a video, and a background process transcodes it to a lower quality. **The transcoder must be explicitly instructed via a message queue** — the video isn't put on the queue, since brokers are designed for small messages, so **the video is first written to file storage, and once the write completes the instruction is placed on the queue.**

**If the file storage is linearizable, this works. If not, there is a race condition: the message queue might be faster than the internal replication inside the storage service.** Then when the transcoder fetches the original video **it might see an old version or nothing at all** — and **if it processes an old version, the original and transcoded videos become permanently inconsistent.**

**The problem arises because there are two communication channels between the web server and the transcoder** — the file storage and the message queue — **and without linearizability's recency guarantee, race conditions between them are possible.** **The same shape as Aaliyah and Bryce**, where the two channels were database replication and real-life audio.

**A similar race occurs with push notifications**: if a mobile app fetches data on receiving a notification **and the fetch goes to a lagging replica, the notification arrives quickly but the fetch doesn't see the data it was about.**

## Trade-offs & Pitfalls
**Linearizability is not the only way of avoiding this race condition, but it's the simplest to understand.** **If you control the additional communication channel — as with the message queue, but not with Aaliyah and Bryce — you can use approaches similar to those for reading your own writes, at the cost of additional complexity.**

## Examples & Systems
ZooKeeper, etcd, Apache Curator; Oracle RAC's per-page locks; the video-transcoding pipeline as the cross-channel example.

## Since the 1st Edition
Very close to the 1st edition's [[Relying on Linearizability]] — the same three cases, the same video transcoder example, and the same Oracle RAC note. **Updated:** the observation that **etcd version 3 onward provides linearizable reads by default**, sharpening the 1st edition's caveat that consensus systems don't automatically give linearizable reads.

## Related
- up: [[Linearizability (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Distributed Locks and Leases (2e)]] — the fencing detail this defers to
- [[Coordination Services (2e)]] — the systems providing this foundation
- [[Enforcing Constraints (2e)]] — loosely interpreted constraints, in Chapter 13
- 1st edition: [[Relying on Linearizability]] — the same subtopic
