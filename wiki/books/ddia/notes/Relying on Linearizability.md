---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia, locking, uniqueness-constraints, leader-election]
sources:
  - raw/ch09.md
---
# Relying on Linearizability
> Some correctness requirements — distributed locks, leader election, uniqueness constraints, and multi-channel dataflows — genuinely break without a recency guarantee.

## The Idea
A stale sports score is harmless; a stale lock is not. This section identifies the situations where [[Linearizability]] is a hard requirement rather than a nicety, so you can tell when the cost is worth paying.

## How It Works
**Locking and leader election.** Single-leader replication only works if everyone agrees who the leader is; two self-declared leaders is [[Split Brain]] and usually means data loss. One election method: whoever acquires a distributed lock becomes leader. That lock *must* be linearizable — all nodes must agree on its current owner or it is worthless. Coordination services like [[ZooKeeper]] and [[Etcd|etcd]] provide this by running [[Consensus]] internally (with libraries like Apache Curator layering recipes on top). Note the fine print: both systems give linearizable *writes* by default, but reads may be stale unless you explicitly request a quorum read (etcd) or call sync() first (ZooKeeper). Oracle RAC takes distributed locking to the extreme — a linearizable lock per disk page, on the critical path, justifying a dedicated cluster interconnect.

**Uniqueness constraints.** Enforcing "one user per username" or "one file per path" *at write time* requires linearizability: registering a name is effectively acquiring a lock on it, or an atomic compare-and-set from null to your user ID. The same shape appears in bank balances that must not go negative, stock that must not oversell, and seats that must not double-book — all demand a single up-to-date value every node agrees on. Softer constraints (overbooking with compensation) can skip linearizability; hard relational-style uniqueness cannot. Foreign-key and attribute constraints, by contrast, do not need it.

**Cross-channel timing dependencies.** When two components communicate through *two* channels, a race appears if the storage lacks recency. The chapter's example: a web server writes a photo to file storage, then queues a resize instruction. If the queue outruns the storage's internal replication, the resizer reads an old or missing image and produces permanently inconsistent thumbnails. Alice's voice telling Bob the score was exactly such a second channel. Linearizability closes the race automatically; alternatives (read-your-writes techniques) work only when you control the extra channel, at added complexity.

## Trade-offs & Pitfalls
- The violation is invisible without the second channel — systems can run non-linearizably for years unnoticed.
- Default reads on ZooKeeper/etcd are NOT linearizable; forgetting sync()/quorum reads is a classic bug.
- Fencing is still required even with a linearizable lock service, because clients can pause ([[Fencing Tokens]]).

## Examples & Systems
[[ZooKeeper]], [[Etcd|etcd]], Apache Curator, Oracle Real Application Clusters; the photo-resizer message-queue architecture.

## Related
- up: [[Linearizability]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[The Truth Is Defined by the Majority]] — why a node cannot trust its own leadership belief
- [[Membership and Coordination Services]] — how ZooKeeper packages these primitives
- [[Reading Your Own Writes]] — the cheaper per-channel alternative
- [[Timeliness and Integrity]] — loosening constraints instead of paying for recency
