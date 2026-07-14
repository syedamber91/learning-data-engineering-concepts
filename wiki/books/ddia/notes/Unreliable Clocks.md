---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia, clocks, ntp, time, ordering]
sources:
  - raw/ch08.md
---
# Unreliable Clocks

Applications lean on clocks constantly — has this request timed out, what is the p99 response time, when should the reminder email fire, when does this cache entry expire? Half of these questions measure *durations*, the other half name *points in time*, and the distinction matters because computers keep two different kinds of clock for the two jobs. In a distributed system, time is treacherous: messages take variable, unknown time to travel, so receipt time is always later than send time by an unknowable amount, and each machine's quartz oscillator ticks at its own slightly wrong rate. NTP can discipline clocks toward a shared reference (ultimately GPS), but only within limits set by quartz drift and network round-trip variability. This topic covers the monotonic/time-of-day split, how bad synchronization actually gets (drift figures, leap seconds, VM clock jumps), the disasters that follow from trusting timestamps for ordering ([[Clock Skew]] plus last-write-wins equals silent data loss), Google Spanner's confidence-interval workaround, and the process pauses — GC stops, VM suspensions, page faults — that make even a locally correct clock reading stale by the time you act on it.

## Subtopics
- [[Monotonic Versus Time-of-Day Clocks]] — wall-clock time (settable, can jump backward) vs monotonic time (only for intervals, meaningless across machines).
- [[Clock Synchronization and Accuracy]] — quartz drift (~200 ppm), NTP's failure modes, leap seconds, VM clock virtualization, and what precision money can buy.
- [[Relying on Synchronized Clocks]] — LWW ordering hazards, confidence intervals, and Spanner's TrueTime approach to global snapshots.
- [[Process Pauses]] — GC stops, VM suspensions, and why a node can act on an expired lease without noticing.

## Key Takeaways
- Use monotonic clocks for durations and timeouts; time-of-day clocks only for calendar timestamps — never for measuring elapsed time.
- Clock error is invisible: a drifting clock breaks nothing obvious, so damage surfaces as silent data loss rather than crashes; monitor clock offsets and evict outliers.
- Ordering events by timestamp across nodes is unsafe; causality needs logical clocks or [[Version Vectors]], not physical time.
- A clock reading is honestly a confidence interval, not a point — Spanner's TrueTime exposes this and waits out the uncertainty before committing.
- Any thread can be preempted for seconds or minutes at any line of code; correctness must not depend on "not much time passes here."

## Related
- up: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Detecting Concurrent Writes]] — LWW and version vectors in Ch 5
- [[Snapshot Isolation and Repeatable Read]] — the isolation level Spanner globalizes
- [[Ordering and Causality]] — Ch 9's deeper treatment of event ordering
- [[Lamport Timestamps]] — logical clocks as the safe alternative
