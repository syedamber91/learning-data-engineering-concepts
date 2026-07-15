---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia, last-write-wins, truetime, spanner, causality]
sources:
  - raw/ch08.md
---
# Relying on Synchronized Clocks
> Ordering writes by wall-clock timestamp silently drops data under clock skew; honest systems treat a clock reading as a confidence interval — which is exactly how Spanner's TrueTime makes global snapshots work.

## The Idea
Clocks fail quietly. A dead CPU gets noticed immediately; a drifting quartz or misconfigured NTP client leaves everything *seemingly* fine while timestamps rot, so the damage shows up as subtle, silent data loss instead of a crash. If your software depends on synchronized clocks, you must monitor inter-node offsets and evict any node whose clock strays too far — treat a bad clock as a dead node.

## How It Works
**The ordering trap.** Consider multi-leader replication where each write carries the originating node's wall-clock timestamp, and conflicts are resolved by *last write wins* (LWW) — as in Cassandra and Riak. In the book's example, client B's increment causally follows client A's write, yet B's node clock lags under 3 ms behind A's — excellent sync by real-world standards — so B's write gets timestamp 42.003 s against A's 42.004 s. Node 2 keeps the "newer" A value and silently discards B's causally-later increment. The general failures: a lagging clock's writes cannot overwrite a fast clock's until the [[Clock Skew]] elapses (arbitrary silent loss, no errors reported); LWW cannot tell rapid sequential writes from truly concurrent ones, so [[Causality]] needs explicit tracking like [[Version Vectors]]; and millisecond-resolution timestamps collide, requiring tiebreakers (e.g., random numbers) that themselves violate causality. Tighter NTP cannot save you — its accuracy is bounded by network round-trip time, the very thing you would need to out-measure. *Logical clocks* (counters tracking only relative order, e.g., [[Lamport Timestamps]]) are the safe tool; time-of-day and monotonic clocks are "physical clocks."

**Confidence intervals.** A nanosecond-resolution reading is not nanosecond-accurate: drift plus NTP uncertainty plus round-trip time means the true time lies in a range — perhaps ±100 ms — making the small digits noise. Most APIs hide this; Google Spanner's TrueTime instead returns [earliest, latest] bounds. **Global snapshots.** Distributed [[Snapshot Isolation and Repeatable Read]] needs causally consistent transaction IDs across datacenters, and a coordinated global counter would be a bottleneck. Spanner uses TrueTime timestamps: if interval A ends before interval B begins, A definitely preceded B. To guarantee non-overlap, Spanner deliberately *waits out the confidence interval* before committing a read-write transaction — and keeps intervals short by putting a GPS receiver or atomic clock in every datacenter (~7 ms sync).

## Trade-offs & Pitfalls
LWW's convenience hides that "recent" is defined by a possibly-wrong local clock. Twitter's Snowflake-style ID generators scale but cannot promise causal order. Clock-based transaction semantics remain research territory outside Google.

## Examples & Systems
Cassandra and Riak LWW; Spanner + TrueTime with GPS/atomic clocks; Snowflake ID generation; the impossible packet that "arrives before it was sent."

## Related
- up: [[Unreliable Clocks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Detecting Concurrent Writes]] — Ch 5 home of LWW and version vectors
- [[Snapshot Isolation and Repeatable Read]] — the guarantee Spanner distributes
- [[Ordering and Causality]] — Ch 9's ordering theory
- [[Handling Write Conflicts]] — where conflict resolution strategies live
