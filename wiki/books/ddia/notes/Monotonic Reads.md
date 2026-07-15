---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Problems with Replication Lag
type: subtopic
tags: [ddia, monotonic-reads, replication-lag, consistency-models]
sources:
  - raw/ch05.md
---
# Monotonic Reads

> A guarantee that a user's successive reads never observe the database moving backward in time.

## The Idea

When each read is routed to a random replica, a user can first hit a nearly-caught-up follower and then a badly lagging one. Example: user 2345 queries a comment thread twice (say, refreshing a page). The first query, served by a fresh replica, returns user 1234's new comment; the second, served by a stale replica that hasn't received that write, returns nothing. The comment appears, then *disappears* — the user has watched time run backward. Curiously, the anomaly would have been invisible had the first read also been stale; it's the fresh-then-stale sequence that confuses.

## How It Works

**Monotonic reads** guarantees that if a user performs several reads in sequence, later reads never return older state than earlier ones. It sits strictly between guarantees: weaker than [[Strong Consistency]] (you may still read stale data), stronger than [[Eventual Consistency]] (staleness can never regress).

The standard implementation: pin each user to a single replica — for instance, choose the replica by hashing the user ID instead of picking randomly. One user always reads one replica's timeline, which by construction only moves forward; different users may read different replicas.

## Trade-offs & Pitfalls

- **Failure re-routing breaks the pin**: if the user's designated replica dies, their queries must move to another replica, which may be behind — the anomaly can reappear at exactly the moment of failure.
- Hash-based pinning can concentrate heavy users on one replica, an echo of the [[Hot Spots]] problem.
- The guarantee is per-user-session; it does not order one user's reads against another user's writes.
- Leaderless quorum systems generally do not provide monotonic reads either — see [[Limitations of Quorum Consistency]].

## Examples & Systems

- The web-page-refresh scenario with two followers at different lag is the chapter's canonical illustration.
- Any load-balanced read-replica fleet (MySQL/PostgreSQL read pools) exhibits this unless session affinity or replica pinning is added.

## Related

- up: [[Problems with Replication Lag]] · chapter: [[Ch 05 - Replication]]
- [[Reading Your Own Writes]] — sibling guarantee for one's own writes
- [[Consistent Prefix Reads]] — sibling guarantee for causal order
- [[Limitations of Quorum Consistency]] — why quorums don't grant this either
