---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia2, lww, confidence-interval, truetime, spanner, clockbound, logical-clock]
sources:
  - raw/ch09.md
---
# Relying on Synchronized Clocks
> A defective CPU or misconfigured network fails loudly. A defective clock keeps working while drifting further from reality — so the result is silent, subtle data loss rather than a dramatic crash.

## The Idea
**Clocks seem simple and easy to use but have a surprising number of pitfalls**: a day may not have exactly 86,400 seconds, time-of-day clocks may move backward, and one node's time may differ substantially from another's. **Just as software must be designed on the assumption that the network will occasionally be faulty, robust software must be prepared to deal with incorrect clocks.**

**Part of the problem is that incorrect clocks easily go unnoticed.** A defective CPU or misconfigured network **most likely won't work at all, so the issue is quickly spotted and fixed.** But **if a quartz clock is defective or an NTP client misconfigured, most things will seem to work fine** even as the clock drifts further from reality. **If software relies on an accurately synchronized clock, the result is more likely to be silent and subtle data loss than a dramatic crash.**

**So if you use software requiring synchronized clocks, it is essential to carefully monitor the clock offsets between all machines in your cluster. Any node whose clock drifts too far from the others should be declared dead and removed** — so you notice faulty clocks before they cause too much damage.

## How It Works
**Timestamps for ordering events.** The tempting-but-dangerous case. In a multi-leader database: client A writes `x = 1` on node 1, the write replicates to node 3, client B increments `x` on node 3 (now `x = 2`), and both writes replicate to node 2. Each write is tagged with the time-of-day clock of the node where it originated. **Clock synchronization in the example is very good — skew under 3 ms, probably better than you can expect in practice.**

**Since the increment builds on the earlier write, `x = 2` should have the greater timestamp. It doesn't.** `x = 1` has timestamp 42.004 and `x = 2` has 42.003 — **B's write is causally later but has an earlier timestamp.** With **LWW** conflict resolution, **node 2 will incorrectly conclude `x = 1` is more recent and drop `x = 2`, so the increment is lost.**

**This can be prevented by ensuring the new value always has a higher timestamp than the value it overwrites, even if that is ahead of the writer's local clock** — **but that costs an additional read to find the greatest existing timestamp.** **Some systems, including Cassandra and ScyllaDB, avoid that round trip and simply use the client clock's timestamp with LWW.** Three serious problems follow:
- **Database writes can mysteriously disappear.** **A node with a lagging clock is unable to overwrite values previously written by a node with a faster clock until the clock skew has elapsed** — which **can cause arbitrary amounts of data to be silently dropped without any error being reported.**
- **LWW cannot distinguish sequential from truly concurrent writes.** B's increment definitely occurs after A's write, **but LWW can't tell that from a genuine concurrent pair.** **Additional causality tracking, such as version vectors, is needed.**
- **Two nodes could independently generate writes with the same timestamp**, especially at millisecond resolution. **An additional tiebreaker (a large random number) is required, but this can also lead to violations of causality.**

**Even with tightly NTP-synchronized clocks**, you could **send a packet at timestamp 100 ms by the sender's clock and have it arrive at 99 ms by the recipient's** — **so it appears the packet arrived before it was sent, which is impossible.** **Could NTP be made accurate enough to prevent this? Probably not**, because **NTP's accuracy is itself limited by network round-trip time**, and **you would need clock error significantly lower than network delay, which is not possible.**

**Logical clocks** — based on **incrementing counters rather than an oscillating quartz crystal** — **are a safer alternative for ordering events.** They **don't measure time of day or elapsed seconds, only the relative ordering of events.** Time-of-day and monotonic clocks, which measure actual elapsed time, are **physical clocks** by contrast.

**Clock readings with a confidence interval.** You may read a clock with microsecond or nanosecond resolution — **but that doesn't mean the value is accurate to such precision, and it most likely is not.** Quartz drift is easily several milliseconds even with local NTP sync every minute; **over the public internet the best accuracy is tens of milliseconds, and error may easily spike over 100 ms with congestion.**

**So it doesn't make sense to think of a clock reading as a point in time. It is more like a range of times, within a confidence interval** — a system may be 95% confident the time is between 10.3 and 10.5 seconds past the minute. **If you know the time only ±100 ms, the microsecond digits are essentially meaningless.**

**The uncertainty bound can be calculated from your time source**: a directly attached GPS receiver or atomic clock has an error range determined by the device and signal quality; from a server it is **expected quartz drift since last sync, plus the server's uncertainty, plus the network round-trip time.** **Unfortunately most systems don't expose this** — `clock_gettime` doesn't tell you **whether its confidence interval is five milliseconds or five years.**

**There are exceptions: Google Spanner's TrueTime API and Amazon ClockBound explicitly report the confidence interval**, returning **[earliest, latest]** — the actual current time is somewhere in that interval, and **its width depends on how long since the local quartz was last synchronized with a better source.**

## Trade-offs & Pitfalls
**Synchronized clocks for global snapshots.** MVCC needs a **monotonically increasing transaction ID**: a write with a greater ID than the snapshot is invisible to it. On one node a simple counter suffices. **Across many machines a global, monotonically increasing transaction ID is difficult to generate, because it requires coordination** — **and it must reflect causality**, so that if B reads or overwrites a value written by A, B has a higher ID. **With lots of small, rapid transactions this becomes an untenable bottleneck.**

**Can synchronized time-of-day timestamps serve as transaction IDs?** They would have the right property — later transactions have higher timestamps — **the problem is uncertainty about accuracy.**

**Spanner implements snapshot isolation across datacenters exactly this way.** It uses TrueTime's confidence interval and this observation: **if two confidence intervals do not overlap, then B definitely happened after A — there can be no doubt. Only if the intervals overlap are we unsure.** So **Spanner deliberately waits for the length of the confidence interval before committing a read/write transaction**, ensuring any transaction that may read the data is at a sufficiently later time that intervals don't overlap. **To keep the wait short, Google deploys a GPS receiver or atomic clock in each datacenter, synchronizing to within about 7 ms.**

**The atomic clocks and GPS receivers are not strictly necessary. The important thing is to have a confidence interval — accurate clock sources only help keep that interval small.** **Other systems are adopting similar approaches — YugabyteDB can leverage ClockBound when running on AWS.**

## Examples & Systems
Cassandra and ScyllaDB using client-clock LWW; Spanner's TrueTime; Amazon ClockBound; YugabyteDB on AWS.

## Since the 1st Edition
Close to the 1st edition's [[Relying on Synchronized Clocks]] — the same multi-leader timestamp example, the same three LWW problems, the same confidence-interval argument, and the same Spanner explanation. **Added:** **Amazon ClockBound** as a second system exposing confidence intervals, **YugabyteDB adopting it**, and the explicit statement that **atomic clocks aren't strictly necessary — having a confidence interval is what matters.** That last point reframes Spanner from an exotic Google-only design into a pattern others can copy.

## Related
- up: [[Unreliable Clocks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Dealing with Conflicting Writes (2e)]] — LWW's data loss from the replication side
- [[ID Generators and Logical Clocks (2e)]] — the safe alternative, in Chapter 10
- [[Snapshot Isolation and Repeatable Read (2e)]] — the MVCC transaction IDs being generated
- 1st edition: [[Relying on Synchronized Clocks]] — the same subtopic
