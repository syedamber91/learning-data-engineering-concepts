---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, replication, anti-entropy]
sources:
  - raw/ch05.md
---
# Read Repair

Fixing stale replicas opportunistically during reads: a client (or coordinator)
reading from several replicas notices one returned an older version and writes the
newer value back to it. Works well for frequently read data; rarely-read data can
stay stale for a long time, which is why systems pair it with a background
[[Anti-Entropy]] process.

Book home ground: [[Writing to the Database When a Node Is Down]] (Ch 5,
leaderless replication's catch-up mechanisms alongside hinted handoff).

## Referenced In
- [[Ch 05 - Replication]]
- [[Detecting Concurrent Writes]]
- [[Implementing Linearizable Systems]]
- [[Leaderless Replication]]
- [[Limitations of Quorum Consistency]]
- [[Writing to the Database When a Node Is Down]]
