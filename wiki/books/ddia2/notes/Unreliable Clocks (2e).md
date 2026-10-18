---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia2, clocks, ntp, time, quartz]
sources:
  - raw/ch09.md
---
# Unreliable Clocks
Clocks and time are important, and applications depend on them in various ways. The book's eight questions split cleanly into two kinds:
- **Durations** — Has this request timed out yet? What's the 99th percentile response time of this service? How many queries per second did it handle in the last five minutes? How long did the user spend on our site?
- **Points in time** — When was this article published? At what date and time should the reminder email be sent? When does this cache entry expire? What is the timestamp on this error message in the log file?

**In a distributed system, time is a tricky business, because communication is not instantaneous.** A message takes time to travel across the network, so **the time a message is received is always later than when it was sent — but because of variable delays, we don't know how much later.** **This makes it difficult to determine the order in which things happened when multiple machines are involved.**

**Moreover, each machine has its own clock** — a hardware device, usually a **quartz crystal oscillator**. **These are not perfectly accurate, so each machine has its own notion of time**, slightly faster or slower than others. Clocks can be synchronized to some degree; **the most commonly used mechanism is the Network Time Protocol (NTP)**, which adjusts the computer clock according to a group of servers, which in turn get their time from a more accurate source such as a GPS receiver.

## Subtopics
- [[Monotonic Versus Time-of-Day Clocks (2e)]] — two clocks, two purposes, and one common mistake.
- [[Clock Synchronization and Accuracy (2e)]] — eight reasons your clock is wrong.
- [[Relying on Synchronized Clocks (2e)]] — LWW's silent data loss, and confidence intervals as the fix.
- [[Process Pauses (2e)]] — the clock problem you meet *inside* one machine.

## Key Takeaways
- **The duration/point-in-time split is the organising distinction** and maps directly onto the two clock types: monotonic clocks for durations, time-of-day clocks for points in time. Most clock bugs come from using one where the other belongs.
- Network delay and clock inaccuracy compound: **you cannot order events across machines by timestamp**, because the error in each clock may exceed the interval between the events.
- **The chapter's structural argument is that clocks deserve the same treatment as networks**: they work most of the time, so **robust software must be designed on the assumption they will occasionally be wrong**, and handle it gracefully.

## Since the 1st Edition
The 1st edition's [[Unreliable Clocks]] opened with the same eight questions and the same duration/point-in-time split, and had the same subtopic structure. Content is broadly stable; the changes are in the individual subtopics, most notably the addition of Amazon ClockBound alongside Spanner's TrueTime and updated garbage-collection material.

## Related
- chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Unreliable Networks (2e)]] — the other source of uncertainty
- [[ID Generators and Logical Clocks (2e)]] — the safe alternative for ordering
- 1st edition: [[Unreliable Clocks]] — the same topic
