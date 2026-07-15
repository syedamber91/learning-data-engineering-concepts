---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia, monotonic-clock, wall-clock, ntp]
sources:
  - raw/ch08.md
---
# Monotonic Versus Time-of-Day Clocks
> Computers carry two clocks for two jobs: a time-of-day clock for calendar timestamps (which NTP may yank backward) and a monotonic clock for measuring intervals (which never goes back but is meaningless across machines).

## The Idea
"What time is it?" and "how long did this take?" are different questions, and conflating them is a classic distributed-systems bug. Modern machines expose a clock for each, and each is unfit for the other's job.

## How It Works
**Time-of-day (wall-clock) clocks** return the current date and time per some calendar — `clock_gettime(CLOCK_REALTIME)` on Linux, `System.currentTimeMillis()` in Java — typically as seconds/milliseconds since the Unix epoch (midnight UTC, 1 January 1970, Gregorian, leap seconds not counted). They are NTP-synchronized, so a timestamp ideally means the same thing on every machine. But if the local clock has run too far ahead of the NTP server, it gets forcibly reset — applications can observe time jumping *backward*. Combined with leap-second blindness, this makes wall clocks unsuitable for measuring elapsed time. Historically they were also coarse (10 ms steps on older Windows).

**Monotonic clocks** — `clock_gettime(CLOCK_MONOTONIC)`, `System.nanoTime()` — are guaranteed to only move forward, which makes them right for durations: timeouts, response times. Read once, do work, read again; the difference is the elapsed time. The *absolute* value, though, is arbitrary (perhaps nanoseconds since boot), so comparing monotonic readings from two machines is nonsense. Multi-socket servers may have a timer per CPU, not perfectly synchronized; the OS papers over this as threads migrate between CPUs, but the monotonicity guarantee deserves mild skepticism. NTP may *slew* the monotonic rate — speed it up or slow it down by up to 0.05% — if the local quartz runs fast or slow, but it cannot make it jump. Resolution is good: microseconds or better.

## Trade-offs & Pitfalls
The engineering rule: measure timeouts and intervals with the monotonic clock, which needs no cross-node synchronization and shrugs off small inaccuracies. The wrong assumption engineers make is treating `currentTimeMillis()` deltas as durations — an NTP step-reset mid-measurement produces negative or wildly wrong intervals, which has real consequences in lease-expiry logic (see [[Process Pauses]]).

## Examples & Systems
Linux `CLOCK_REALTIME` vs `CLOCK_MONOTONIC`; Java `currentTimeMillis()` vs `nanoTime()`; NTP step corrections and 0.05% slew; per-CPU timers on multi-socket machines; older Windows' 10 ms tick.

## Related
- up: [[Unreliable Clocks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Clock Synchronization and Accuracy]] — sibling: how far wall clocks actually drift
- [[Timeouts and Unbounded Delays]] — timeouts, the monotonic clock's main customer
- [[Clock Skew]] — divergence between nodes' wall clocks
- [[Lamport Timestamps]] — logical alternative when ordering matters
