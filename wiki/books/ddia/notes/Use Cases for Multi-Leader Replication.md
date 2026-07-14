---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia, multi-leader, multi-datacenter, offline-first, collaborative-editing]
sources:
  - raw/ch05.md
---
# Use Cases for Multi-Leader Replication

> Multi-leader setups earn their complexity only when writers are separated by slow or unreliable links: datacenters, offline devices, or concurrent document editors.

## The Idea

Inside a single datacenter, multiple leaders rarely pay for the added complexity. The model becomes attractive when the network between writers is the problem — high latency between regions, devices that go offline for days, or humans typing into the same document at once. In all three cases, the win is the same: accept the write locally *now*, replicate asynchronously *later*.

## How It Works

**Multi-datacenter operation.** Put one leader in each datacenter; within a datacenter, ordinary leader–follower [[Replication]] applies, while leaders exchange changes across datacenters asynchronously. Compared with a single leader, this improves three things: *performance* (writes commit in the local datacenter, hiding inter-datacenter latency), *datacenter-outage tolerance* (each site keeps running independently and catches up later, no cross-site failover needed), and *network-fault tolerance* (a flaky public-internet link only delays replication rather than blocking writes).

**Clients with offline operation.** A calendar app on your phone and laptop must accept reads and writes with no connectivity. Each device holds a local database acting as a leader, syncing with the others whenever a connection appears — architecturally multi-leader replication where every device is a tiny "datacenter" and replication lag can stretch to days.

**Collaborative editing.** Real-time editors let many people modify a document simultaneously. Locking the whole document reduces this to single-leader replication with transactions; making the unit of change a single keystroke and skipping locks gives fast collaboration but imports every multi-leader challenge, above all conflict resolution.

## Trade-offs & Pitfalls

- Concurrent modification of the same data in two places is now possible, so write conflicts are inherent — see [[Handling Write Conflicts]].
- Multi-leader support is often bolted on after the fact, producing surprising interactions with autoincrementing keys, triggers, and integrity constraints; many practitioners treat it as territory to avoid unless forced.
- The long history of broken calendar-sync implementations is evidence of how hard the offline case is in practice.

## Examples & Systems

- External multi-leader tooling: Tungsten Replicator (MySQL), BDR (PostgreSQL), GoldenGate (Oracle).
- CouchDB is designed around the offline/sync mode of operation.
- Etherpad and Google Docs are the canonical collaborative editors; their merging algorithm is operational transformation.

## Related

- up: [[Multi-Leader Replication]] · chapter: [[Ch 05 - Replication]]
- [[Handling Write Conflicts]] — the price of writing in two places
- [[Leaders and Followers]] — the single-leader baseline being extended
- [[Sloppy Quorums and Hinted Handoff]] — leaderless take on multi-datacenter operation
