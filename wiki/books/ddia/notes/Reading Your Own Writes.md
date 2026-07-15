---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Problems with Replication Lag
type: subtopic
tags: [ddia, read-after-write, replication-lag, consistency-models]
sources:
  - raw/ch05.md
---
# Reading Your Own Writes

> Read-after-write consistency guarantees a user always sees their own submissions, even when their reads land on lagging replicas.

## The Idea

A common flow: user submits data (write goes to the leader), then immediately views it (read may go to a follower). If the follower hasn't yet received the write, the user's comment or profile edit seems to have vanished — they'll assume the save failed. **Read-after-write consistency** (a.k.a. read-your-writes) promises: *your own* writes are always visible to *you*. It says nothing about seeing other users' writes promptly — that's fine, since users only notice their own data disappearing.

## How It Works

Techniques for leader-based systems:

- **Route by ownership**: read anything the user could have modified from the leader, everything else from followers. Works when editability is predictable — e.g., a social profile only its owner can edit, so "own profile → leader, others' profiles → follower."
- **Route by recency heuristics**: if most content is user-editable, ownership routing sends everything to the leader and kills read scaling. Instead, read from the leader for one minute after the user's last update, and/or bar queries from any follower lagging more than a minute.
- **Client-remembered timestamp**: the client keeps the timestamp of its latest write; any replica serving that user must have applied writes up to that timestamp, else the read waits or reroutes. The timestamp can be logical (a log sequence number ordering writes) or wall-clock — the latter makes clock sync critical ([[Unreliable Clocks]], [[Clock Skew]]).
- **Multi-datacenter**: leader-bound reads must be routed to the datacenter housing the leader, adding routing complexity.

**Cross-device consistency** is harder: a user edits on desktop, then checks on phone, and expects to see the edit. Client-side timestamps break because devices don't know each other's writes — the metadata must be centralized — and different devices may route to entirely different datacenters (home broadband vs. cellular), so requests may need forcing to one datacenter.

## Trade-offs & Pitfalls

- Leader-reads erode the read-scaling benefit that motivated followers in the first place.
- Wall-clock timestamps import all the hazards of distributed clocks.
- The guarantee is per-user, deliberately weak — cheap, but insufficient if users share visibility of each other's data quickly.

## Examples & Systems

The chapter's running examples: social-network profiles, comment threads, customer records — any submit-then-view interaction on an asynchronously replicated store.

## Related

- up: [[Problems with Replication Lag]] · chapter: [[Ch 05 - Replication]]
- [[Monotonic Reads]] — sibling anomaly: time moving backward
- [[Unreliable Clocks]] — why wall-clock timestamps are risky
- [[Eventual Consistency]] — the weak baseline this guarantee strengthens
- [[Request Routing]] — steering reads to the right node
