---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, eventual-consistency, read-after-write, monotonic-reads, consistent-prefix, replication-lag]
sources:
  - raw/ch06.md
---
# Problems with Replication Lag
> Three specific ways a stale follower confuses a user: your own write vanishes, time runs backward, and an answer arrives before its question.

## The Idea
Beyond fault tolerance, replication also serves **scalability** and **latency**. Leader-based replication requires all writes through one node, but **read-only queries can go to any replica** — so for mostly-read workloads (common in online services) there is an attractive option: **create many followers and distribute reads across them**, removing load from the leader and letting reads be served by nearby replicas. In this **read-scaling architecture** you increase read capacity simply by adding followers.

**But this realistically works only with asynchronous replication.** Synchronously replicating to all followers would make a single node failure or network outage take the entire system unavailable for writing — and the more nodes, the likelier one is down, so a fully synchronous configuration would be very unreliable.

An application reading from an asynchronous follower may therefore **see outdated information**. Run the same query on the leader and a follower at the same time and you may get different results. The inconsistency is temporary — stop writing, wait, and followers catch up — which is why the effect is called **eventual consistency**.

> The term was coined by Douglas Terry et al. and popularised by Werner Vogels, becoming the battle cry of many NoSQL projects. **But it's not only NoSQL databases that are eventually consistent**; followers in an asynchronously replicated relational database have exactly the same characteristics.

**"Eventually" is deliberately vague; in general there is no limit to how far a replica can fall behind.** In normal operation the **replication lag** may be a fraction of a second and unnoticeable — but near capacity or with network problems it can easily reach several seconds or even minutes, at which point the inconsistencies become a real problem.

## How It Works
**1. Reading your own writes.** Many applications let a user submit data and then view it — a customer record, a comment on a discussion thread. The write goes to the leader, but the view can be read from a follower, which is especially appropriate when data is frequently viewed and only occasionally written. With asynchronous replication, **if the user views the data shortly after writing, the new data may not have reached the replica** — so **to the user it looks as though their submission was lost.**

The guarantee needed is **read-after-write consistency** (also **read-your-writes consistency**): if the user reloads the page, they will always see updates they submitted themselves. It **makes no promises about other users** — their updates may not be visible until later — but it reassures the user that their own input was saved. Techniques:
- **Read from the leader anything the user may have modified**, and from a follower otherwise. This requires knowing whether something might have been modified without querying it. Social-network profile information is normally editable only by its owner, so the rule becomes: **always read the user's own profile from the leader, and other users' profiles from a follower.**
- If most things are potentially editable by the user, that fails (nearly everything would come from the leader, negating read scaling). Then use other criteria: **track the time of the last update and for one minute afterward make all reads from the leader**, and **monitor replication lag, preventing queries on any follower more than one minute behind**.
- **The client can remember the timestamp of its most recent write**, and the system ensures the replica serving reads is at least that current.

**2. Monotonic reads.** A user can **see things moving backward in time** if they read from different replicas. User 2345 makes the same query twice — first to a follower with little lag, then to one with greater lag (quite likely if they refresh a page and each request is routed to a random server). The first query returns a comment recently added by user 1234; **the second returns nothing**, because the lagging follower hasn't picked up that write. The second query observes an earlier state than the first. It wouldn't be so bad if the first query had returned nothing — user 2345 wouldn't know the comment existed — **but it's very confusing to see a comment appear and then disappear.**

**Monotonic reads** is a **lesser guarantee than strong consistency but a stronger one than eventual consistency**: you may still read an old value, but **if one user makes several reads in sequence they will not see time go backward**. One way to achieve it is to **ensure each user always reads from the same replica** — chosen by a hash of the user ID rather than randomly. (If that replica fails, their queries must be rerouted.)

**3. Consistent prefix reads.** A violation of causality. The book's dialogue:
> **Mr. Poons:** How far into the future can you see, Mrs. Cake?
> **Mrs. Cake:** About 10 seconds usually, Mr. Poons.

There is a **causal dependency**: Mrs. Cake heard the question and answered it. If a third person listens through followers where Mrs. Cake's words have little lag and Mr. Poons's have longer lag, the observer hears **the answer before the question**. "Such psychic powers are impressive but very confusing."

**Consistent prefix reads** guarantees that **if a sequence of writes happens in a certain order, anyone reading them sees them in the same order**. This is a particular problem in **sharded databases**: if the database always applies writes in the same order, reads always see a consistent prefix and the anomaly cannot happen — **but in many distributed databases different shards operate independently, so there is no global ordering of writes**, and a reader may see some parts of the database in an older state and others in a newer one. One solution is to **ensure causally related writes go to the same shard** — but in some applications that cannot be done efficiently. Some algorithms explicitly track causal dependencies.

## Trade-offs & Pitfalls
- Cross-region deployments make lag worse and are where these anomalies show up first. A **zone** is a separate datacenter in its own physical facility with its own power and cooling; zones in the same **region** are connected by very high-speed links, with latency low enough that most distributed systems can span zones as though they were one. **Multi-zone configurations survive zonal outages but not regional ones**; surviving a regional outage requires deploying across multiple regions, which brings **higher latencies, lower throughput, and increased cloud networking bills**.
- Implementing these guarantees in application code is possible but, as the next subtopic argues, complex and easy to get wrong.

## Examples & Systems
Reading a user's own profile from the leader; hashing user IDs to pin a replica for monotonic reads; the Poons/Cake dialogue as the causality example.

## Since the 1st Edition
**Structurally demoted.** In the 1st edition [[Problems with Replication Lag]] was a top-level *topic* with three subtopics — [[Reading Your Own Writes]], [[Monotonic Reads]], and [[Consistent Prefix Reads]] — plus a fourth, [[Solutions for Replication Lag]]. The 2nd edition compresses all three anomalies into this single subtopic under single-leader replication and promotes solutions to a sibling. The content of each anomaly, including the Poons/Cake dialogue, is essentially unchanged. **Added:** the zone-versus-region terminology box, and the cross-device complication is handled more briefly.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Solutions for Replication Lag (2e)]] — what to actually do about it
- [[Eventual Consistency (2e)]] — the cross-cutting concept note
- [[Linearizability (2e)]] — the strong guarantee these fall short of
- 1st edition: [[Problems with Replication Lag]], [[Reading Your Own Writes]], [[Monotonic Reads]], [[Consistent Prefix Reads]] — the four notes this merges
