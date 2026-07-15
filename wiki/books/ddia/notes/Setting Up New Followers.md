---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaders and Followers
type: subtopic
tags: [ddia, replication, snapshots, operations]
sources:
  - raw/ch05.md
---
# Setting Up New Followers

> A new replica bootstraps from a consistent snapshot of the leader plus a replay of everything written since — no downtime required.

## The Idea

You periodically need fresh followers: to grow read capacity or to replace dead nodes. A naive file copy from the leader won't work because clients write continuously, so different files would be captured at different moments and the result would be internally incoherent. Locking the database for the copy would restore consistency but destroys availability — the very thing [[Replication]] is supposed to provide.

## How It Works

The standard no-downtime procedure has four steps:

1. Take a **consistent snapshot** of the leader's data at a point in time, ideally without a global lock — most databases can do this because backups need it anyway (MySQL sometimes needs a third-party tool like innobackupex).
2. Copy that snapshot onto the new follower machine.
3. The follower connects to the leader and asks for every change since the snapshot. This only works if the snapshot is tied to an exact offset in the replication log — PostgreSQL's *log sequence number*, MySQL's *binlog coordinates*.
4. Once the follower has drained that backlog it is **caught up** and simply keeps consuming the live change stream like any other follower.

## Trade-offs & Pitfalls

- The snapshot-to-log-position association is the crux: without a precise offset the follower cannot know where replay begins, risking gaps or duplicates.
- Operational maturity varies wildly by database — some fully automate this, others require an administrator to walk a fragile multi-step manual runbook.
- Snapshot copying of a large dataset takes time; during that window the backlog grows, so the leader must retain enough log history for the follower to catch up.
- The same log-position mechanism underpins crash recovery for existing followers ([[Handling Node Outages]]) — it's one idea reused twice.

## Examples & Systems

- **PostgreSQL**: snapshot plus log sequence number for streaming replication.
- **MySQL**: snapshot via innobackupex, replay from binlog coordinates.
- The log formats being replayed are the ones described in [[Implementation of Replication Logs]], often a [[Write-Ahead Log]] or logical row-based log.

## Related

- up: [[Leaders and Followers]] · chapter: [[Ch 05 - Replication]]
- [[Handling Node Outages]] — followers recover from crashes with the same catch-up replay
- [[Implementation of Replication Logs]] — the change stream the follower consumes
- [[Strategies for Rebalancing]] — moving data when partitions, not replicas, change
