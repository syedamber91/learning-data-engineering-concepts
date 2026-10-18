---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia2, monotonic-clock, wall-clock, ntp, slewing, leap-second]
sources:
  - raw/ch09.md
---
# Monotonic Versus Time-of-Day Clocks
> One tells you what time it is and may jump backward. The other is a stopwatch whose absolute value is meaningless. Use the wrong one and your timeout logic breaks on a leap second.

## The Idea
**Modern computers have at least two kinds of clocks**, and although both measure time they serve different purposes.

## How It Works
**Time-of-day clocks** do what you intuitively expect: **return the current date and time according to a calendar** — also called **wall-clock time**. They are usually synchronized with NTP, which means **a timestamp from one machine ideally means the same as a timestamp on another.**

**But they have oddities.** **If the local clock is too far ahead of the NTP server, it may be forcibly reset and appear to jump back to a previous point in time.** **These jumps, and similar jumps caused by leap seconds, make time-of-day clocks unsuitable for measuring elapsed time.** They can also jump at **the start and end of Daylight Saving Time** — avoidable by **always using UTC**, which has no DST. Historically they had **coarse-grained resolution** (moving forward in steps of 10 ms on older Windows systems); **on recent systems this is less of a problem.**

**Monotonic clocks** are **suitable for measuring a duration** — a timeout or a service's response time. `clock_gettime(CLOCK_MONOTONIC)` or `clock_gettime(CLOCK_BOOTTIME)` on Linux, `System.nanoTime` in Java. **The name comes from the guarantee that this clock always moves forward**, whereas a time-of-day clock may jump back.

**You check the value, do something, and check again; the difference tells you elapsed time — more like a stopwatch than a wall clock.** **But the absolute value is meaningless** — it might be nanoseconds since boot, or something similarly arbitrary. **In particular, it makes no sense to compare monotonic clock values from two computers**, because they don't mean the same thing.

## Trade-offs & Pitfalls
- **On a server with multiple CPU sockets there may be a separate timer per CPU, not necessarily synchronized with the others.** Operating systems compensate and try to present a monotonic view to application threads even as they are scheduled across CPUs — **but it is wise to take this guarantee of monotonicity with a pinch of salt.**
- **NTP may adjust the frequency at which the monotonic clock moves forward — slewing the clock** — if it detects local quartz running fast or slow. **By default NTP allows the rate to change by up to 0.05%, but it cannot make the monotonic clock jump forward or backward.**
- **Resolution is usually quite good**: microseconds or better on most systems.
- **In a distributed system, using a monotonic clock for measuring elapsed time is usually fine**, because **it doesn't assume any synchronization between nodes' clocks and is not sensitive to slight measurement inaccuracies.**

## Examples & Systems
`CLOCK_MONOTONIC`, `CLOCK_BOOTTIME`, `System.nanoTime`; NTP slewing at up to 0.05%.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Monotonic Versus Time-of-Day Clocks]] — the same two clock types, the same slewing explanation, the same multi-socket caveat, and the same advice. **Added:** `CLOCK_BOOTTIME` alongside `CLOCK_MONOTONIC`, and the DST-avoidance note about using UTC.

## Related
- up: [[Unreliable Clocks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Clock Synchronization and Accuracy (2e)]] — why time-of-day clocks need NTP and why NTP disappoints
- [[Relying on Synchronized Clocks (2e)]] — the dangers of using wall-clock time for ordering
- 1st edition: [[Monotonic Versus Time-of-Day Clocks]] — the same subtopic
