---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
type: chapter-moc
tags: [ddia2, replication, single-leader, multi-leader, leaderless, consistency, moc]
sources:
  - raw/ch06.md
---
# Ch 06 – Replication
**Replication means keeping a copy of the same data on multiple machines connected via a network.** The reasons: keep data geographically close to users and reduce access latency; let the system keep working when parts fail, increasing availability and durability; and scale out the number of machines serving read queries. This chapter assumes the dataset is small enough for each machine to hold a full copy — Chapter 7 relaxes that with sharding.

**If replicated data doesn't change, replication is easy** — copy once and you're done. **All the difficulty lies in handling changes**, and the chapter covers the three families of algorithms for propagating them: **single-leader, multi-leader, and leaderless**. Almost all distributed databases use one of the three.

Replication is an old topic, and the principles haven't changed much since the 1970s because **the fundamental constraints of networks have remained the same** — yet concepts such as eventual consistency still cause confusion.

> **Backups and replication are not substitutes.** Replicas quickly reflect writes from one node on others; backups store old snapshots so you can go back in time. If you accidentally delete data, replication doesn't help — **the deletion propagates to the replicas too**. They are often complementary: backups are sometimes part of setting up replication, and archiving replication logs can be part of a backup process. Some databases maintain immutable snapshots of past states as a kind of internal backup, but that keeps old versions on the same storage medium as current state; with a lot of data it can be cheaper to keep backups in an object store optimised for infrequent access and keep only current state in primary storage.

## Map
- [[Single-Leader Replication (2e)]] — one node accepts writes and streams changes to the rest
  - [[Synchronous Versus Asynchronous Replication (2e)]] — semisynchronous, quorums, and the durability you give up
  - [[Setting Up New Followers (2e)]] — snapshot, copy, catch up; and databases backed by object storage
  - [[Handling Node Outages (2e)]] — catch-up recovery, failover, and everything that goes wrong during it
  - [[Implementation of Replication Logs (2e)]] — statement-based, WAL shipping, and logical (row-based) logs
  - [[Problems with Replication Lag (2e)]] — eventual consistency, read-your-writes, monotonic reads, consistent prefix reads
  - [[Solutions for Replication Lag (2e)]] — or: just use a database with strong consistency
- [[Multi-Leader Replication (2e)]] — several nodes accept writes, each a follower to the others
  - [[Geographically Distributed Operation (2e)]] — a leader per region, and the four-way comparison against single-leader
  - [[Sync Engines and Local-First Software (2e)]] — every device is a leader; offline-first and real-time collaboration
  - [[Dealing with Conflicting Writes (2e)]] — avoidance, LWW, manual resolution, CRDTs and OT
- [[Leaderless Replication (2e)]] — clients write to and read from several replicas directly
  - [[Writing to the Database When a Node Is Down (2e)]] — read repair, hinted handoff, anti-entropy, and quorums
  - [[Single-Leader Versus Leaderless Replication Performance (2e)]] — request hedging, gray failures, and quorum size
  - [[Multi-Region Operation (2e)]] — coordinator nodes and consistency levels across regions
  - [[Detecting Concurrent Writes (2e)]] — happens-before, siblings, and version vectors

## Chapter Summary
Replication serves five purposes: **high availability** (surviving a machine, zone, or region going down), **durability** (not losing data to a permanent failure), **disconnected operation** (working through a network interruption), **latency** (data near users), and **scalability** (more reads than one machine can serve). Despite the simplicity of the concept, it is **a remarkably tricky problem**, requiring careful thought about concurrency, everything that can go wrong, and the consequences of those faults.

The three approaches: **single-leader** (all writes to one node, which streams change events to followers; reads from any replica but follower reads may be stale), **multi-leader** (writes to any of several leaders, which stream change events to each other and to followers), and **leaderless** (writes to several nodes and reads from several nodes in parallel, detecting and correcting stale data). **Single-leader is popular because it is fairly easy to understand and offers strong consistency; multi-leader and leaderless can be more robust against faulty nodes, network interruptions, and latency spikes, at the cost of conflict resolution and weaker consistency.**

Replication may be **synchronous or asynchronous**, which profoundly affects behaviour under fault: asynchronous replication is fast when things run smoothly, but if a leader fails and an asynchronously updated follower is promoted, **recently committed data may be lost**. Three consistency models help reason about lag: **read-after-write** (users see their own submissions), **monotonic reads** (users don't see time go backward), and **consistent prefix reads** (users see a causally sensible state — question before reply). Finally, multi-leader and leaderless systems converge by using **version vectors** to detect which writes are concurrent and a conflict resolution algorithm such as a **CRDT** to merge them; LWW and manual resolution are also possible.

## Since the 1st Edition
This is the 1st edition's Chapter 5, and its three-way structure survives. **Restructured:** the 1st edition made [[Problems with Replication Lag]] a top-level topic with three subtopics ([[Reading Your Own Writes]], [[Monotonic Reads]], [[Consistent Prefix Reads]]); the 2nd edition folds all of it into one subtopic under single-leader replication and adds a new [[Solutions for Replication Lag (2e)]]. [[Partitioning]] moved out to become its own chapter under a new name. **Genuinely new:** [[Sync Engines and Local-First Software (2e)]] as a full subtopic (offline-first, local-first, real-time collaboration, netcode); the **databases-backed-by-object-storage** and **zero-disk architecture** material; **request hedging** and **gray failures** in the leaderless performance comparison; **CRDTs and operational transformation** covered properly with a worked merge example, where the 1st edition mentioned CRDTs only in passing; and **automatic conflict resolution / strong eventual consistency** as a named goal. **Renamed:** the 1st edition's [[Leaders and Followers]] becomes [[Single-Leader Replication (2e)]], [[Handling Write Conflicts]] becomes [[Dealing with Conflicting Writes (2e)]], and "multi-datacenter" becomes "multi-region" throughout. **Dropped:** the 1st edition's [[Limitations of Quorum Consistency]] as a separate note (folded into the quorum discussion) and its trigger-based replication material.

## Related
- home: [[Home (2e)]] · previous: [[Ch 05 - Encoding and Evolution (2e)]] · next: [[Ch 07 - Sharding (2e)]]
- [[Ch 10 - Consistency and Consensus (2e)]] — the strong guarantees this chapter's weaker models are measured against
- [[Ch 09 - The Trouble with Distributed Systems (2e)]] — the faults replication must survive
- 1st edition: [[Ch 05 - Replication]] — the chapter this one revises
