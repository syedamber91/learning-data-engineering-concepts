---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, clocks, distributed-systems]
sources:
  - raw/ch08.md
---
# Clock Skew

Disagreement between clocks on different machines. Quartz drift (~ppm level, tens
of ms per NTP sync window in practice), NTP corrections that jump or slew time,
leap seconds, and VM pauses all mean time-of-day clocks on two nodes can differ by
milliseconds to seconds — silently.

In the book: [[Ch 08 - The Trouble with Distributed Systems]]'s clock topic —
[[Monotonic Versus Time-of-Day Clocks]], [[Clock Synchronization and Accuracy]],
and the disasters in [[Relying on Synchronized Clocks]]: last-write-wins dropping
writes, lease expiry misjudged. Antidotes: monotonic clocks for durations,
confidence intervals (Spanner TrueTime), [[Fencing Tokens]], and logical clocks
([[Lamport Timestamps]]).

## Referenced In
- [[Clock Synchronization and Accuracy]]
- [[Detecting Concurrent Writes]]
- [[Implementing Linearizable Systems]]
- [[Limitations of Quorum Consistency]]
- [[Monotonic Versus Time-of-Day Clocks]]
- [[Multi-Leader Replication Topologies]]
- [[Reading Your Own Writes]]
- [[Reasoning About Time]]
- [[Relying on Synchronized Clocks]]
- [[Sequence Number Ordering]]
- [[Unreliable Clocks]]
