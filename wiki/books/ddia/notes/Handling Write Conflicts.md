---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia, write-conflicts, conflict-resolution, crdt, last-write-wins]
sources:
  - raw/ch05.md
---
# Handling Write Conflicts

> When two leaders accept incompatible writes to the same data, someone — the database, the application, or a clever data structure — must make all replicas converge on one answer.

## The Idea

Picture a wiki page whose title is changed from A to B by one user and from A to C by another, each on a different leader. Both writes succeed locally; the conflict only surfaces when the changes replicate. A single-leader database would have serialized the two writes (blocking or aborting the second); a multi-leader one cannot. Worse, detection is inherently *asynchronous* — by the time the conflict is noticed, the users have moved on, so you can't just ask them. Making detection synchronous (wait for all replicas before confirming) would throw away the whole point of multiple leaders accepting writes independently.

## How It Works

- **Conflict avoidance** — route all writes for a given record through one designated leader (e.g., each user has a "home" datacenter). From that record's perspective the system is single-leader, so conflicts can't arise. It's the most-recommended strategy precisely because implementations handle conflicts poorly — but it breaks down whenever the home leader must change (datacenter failure, user relocation).
- **Convergent resolution** — every replica must reach the *same* final value once all changes propagate. Options: pick a winner by highest unique write ID (a timestamp makes this last write wins — popular and dangerously lossy, detailed in [[Detecting Concurrent Writes]]); let the higher-numbered replica always win (also lossy); merge values (e.g., concatenate to "B/C"); or record the conflict explicitly and let application code resolve it later.
- **Custom logic** — most tools let applications supply resolution code, executed *on write* (a fast background handler fired when the replication log detects a conflict — Bucardo runs a Perl snippet; no user prompting possible) or *on read* (store all versions, hand them to the application at read time — CouchDB's approach).
- Resolution applies per row or document, **not** per transaction: a transaction touching several rows has each write resolved independently.

## Trade-offs & Pitfalls

- Subtle conflicts exist beyond same-field writes: a meeting-room booking system can create overlapping bookings via two leaders even though each checked availability first.
- Amazon's shopping-cart resolver famously preserved additions but not removals, resurrecting deleted items.
- Research alternatives that merge automatically: CRDTs (two-way merges; in Riak 2.0), mergeable persistent data structures (Git-style three-way merges), and operational transformation (Etherpad, Google Docs).

## Examples & Systems

Bucardo (on-write handlers), CouchDB (on-read siblings), Riak 2.0 (CRDTs), Etherpad/Google Docs (operational transformation), Amazon's cart anomaly.

## Related

- up: [[Multi-Leader Replication]] · chapter: [[Ch 05 - Replication]]
- [[Detecting Concurrent Writes]] — same problem in leaderless systems, plus LWW's dangers
- [[Use Cases for Multi-Leader Replication]] — why we accept this pain at all
- [[Multi-Leader Replication Topologies]] — how conflicting writes travel between leaders
