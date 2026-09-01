---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia2, event-time, processing-time, stragglers, windows, sessionization]
sources:
  - raw/ch12.md
---
# Reasoning About Time
> "The average over the last five minutes" seems unambiguous. It isn't — and confusing event time with processing time produces graphs of spikes that never happened.

## The Idea
**In a batch process, tasks rapidly crunch through a large collection of historical events.** **If a breakdown by time is needed, the process looks at the timestamp embedded in each event** — **there is no point looking at the system clock of the machine running the process, because the time it runs has nothing to do with when the events occurred.** **A batch process may read a year's worth of history in a few minutes; the timeline of interest is the year, not the few minutes.** **Using event timestamps also makes processing deterministic: rerun on the same input, get the same result.**

**Many stream frameworks instead use the local system clock — the processing time — to determine windowing.** **Simple, and reasonable if the delay between event creation and processing is negligibly short.** **But it breaks down with any significant processing lag.**

## How It Works
**Event time versus processing time.** **Processing may be delayed by queueing, network faults, contention in the broker or processor, a consumer restart, or reprocessing of past events while recovering from a fault or after a bug fix.**

**Delays also lead to unpredictable ordering.** **A user makes one request handled by server A, then a second handled by server B; both emit events, but B's reaches the broker first, so stream processors see B then A even though they occurred in the opposite order.**

**The book's analogy: the Star Wars movies.** **Episode IV was released in 1977, V in 1980, VI in 1983, then I, II, and III in 1999, 2002, and 2005, and VII, VIII, and IX in 2015, 2017, and 2019.** **Watch them in release order and the order you processed them is inconsistent with the order of their narrative.** **The episode number is like the event timestamp; the date you watched is the processing time.** **As humans we cope with such discontinuities, but stream processing algorithms must be specifically written to accommodate them.**

**Confusing the two leads to bad data.** **A processor measuring requests per second, redeployed and shut down for a minute, processes the backlog on restart.** **Measured by processing time, it looks as if there was a sudden anomalous spike of requests — when in fact the real rate was steady.**

**Handling straggler events.** **Defining windows in event time means you can never be sure whether you have received all the events for a window.** **You've counted events in the 37th minute of the hour; time has moved on and most incoming events fall in the 38th and 39th. When do you declare the 37th minute finished and output its counter?**

**You can time out and declare a window ready after not seeing new events for a while — but some events could be buffered on another machine, delayed by a network interruption.** **You must handle stragglers arriving after the window was declared complete. Broadly, two options:**
- **Ignore them**, as they are probably a small percentage in normal circumstances. **Track the number of dropped events as a metric and alert if you start dropping a significant amount.**
- **Publish a correction** — an updated value for the window including the stragglers. **You may also need to retract the previous output.**

**In some cases you can use a special message meaning "from now on there will be no more messages with a timestamp earlier than t," which consumers use to trigger windows.** **But if several producers on different machines each have their own minimum timestamp thresholds, consumers must track each producer individually — and adding and removing producers is trickier.**

**Whose clock are you using?** **Assigning timestamps is even harder when events are buffered at several points.** **A mobile app reporting usage metrics may be used offline, buffering events locally and sending them hours or days later** — **to consumers, these appear as extremely delayed stragglers.**

**The timestamp should really be the time the user interaction occurred according to the device's local clock.** **But the clock on a user-controlled device often cannot be trusted, as it may be accidentally or deliberately set wrong.** **The time the server received the event is more likely accurate, since the server is under your control, but less meaningful as a description of the interaction.**

**To adjust for incorrect device clocks, log three timestamps:** **the time the event occurred according to the device clock; the time it was sent according to the device clock; and the time it was received according to the server clock.** **Subtracting the second from the third estimates the offset between device and server clocks** (assuming network delay is negligible relative to the accuracy needed), **and applying that offset to the event timestamp estimates the true time it occurred** (assuming the device clock offset didn't change in between).

**This problem is not unique to stream processing — batch processing has exactly the same issues.** **It is just more noticeable in a streaming context, where we are more aware of the passage of time.**

## Trade-offs & Pitfalls
**Types of windows.** Four in common use:
- **Tumbling windows** — **fixed length, every event belongs to exactly one window.** A one-minute tumbling window groups **10:03:00–10:03:59** into one window and **10:04:00–10:04:59** into the next. **Implement by rounding each event timestamp down to the nearest minute.**
- **Hopping windows** — **fixed length with overlap between consecutive windows to provide smoothing.** A five-minute window hopping by one minute covers **10:03:00–10:07:59**, then **10:04:00–10:08:59**. **Implement by first calculating one-minute tumbling windows, then aggregating over several adjacent ones.**
- **Sliding windows** — **all events occurring within a certain interval of each other.** A five-minute sliding window covers events at **10:03:39 and 10:08:12**, because they are less than five minutes apart — **note that tumbling and hopping windows would not put these together, since they use fixed boundaries.** **Implement by keeping a buffer of events sorted by time and removing old ones as they expire.**
- **Session windows** — **no fixed duration.** **Defined by grouping all events for the same user occurring closely together, ending when the user has been inactive for some time** (30 minutes, say). **Sessionization is a common requirement for website analytics.**

**Window operations usually maintain temporary state.** **Sometimes that state is fixed in size regardless of window or event count — a counting operation has one counter.** **But sliding windows and stream joins require events to be buffered until the window finishes**, so **large windows or high-throughput streams can make stream processors keep a lot of temporary state** — **you must ensure the machines have enough capacity to maintain it, in memory or on disk.**

## Examples & Systems
The Star Wars release-order analogy; the three-timestamp device-clock correction; tumbling, hopping, sliding, and session windows.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Reasoning About Time]] — the same event-time/processing-time distinction, the same Star Wars analogy (updated to include Episodes VII–IX), the same straggler options, the same three-timestamp trick, and the same four window types. One of the most stable sections in the book, which fits: these are conceptual problems, not technological ones.

## Related
- up: [[Processing Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Stream Joins (2e)]] — where windows are used for matching
- [[Clock Synchronization and Accuracy (2e)]] — why device clocks can't be trusted
- [[Monotonic Versus Time-of-Day Clocks (2e)]] — the clock the timestamps come from
- 1st edition: [[Reasoning About Time]] — the same subtopic
