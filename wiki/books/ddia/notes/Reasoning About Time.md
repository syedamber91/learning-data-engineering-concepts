---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia, event-time, windowing, stragglers]
sources:
  - raw/ch11.md
---
# Reasoning About Time
> "The last five minutes" is ambiguous: windowing by when events *happened* is honest but never certainly complete; windowing by when they're *processed* is simple but lies under lag.

## The Idea
Batch jobs obviously use timestamps embedded in events — a job crunching a year of history in minutes cares about the year, not the minutes, and embedded timestamps keep reprocessing deterministic. Many stream frameworks instead window by the processing machine's local clock (*processing time*), which is fine only while the gap between an event occurring and being processed stays negligible. Queueing, network faults ([[Unreliable Networks]]), broker contention, consumer restarts, and replays all break that assumption.

## How It Works
Delays also reorder: two events emitted in sequence by different servers can reach the broker in reverse. Kleppmann's analogy is watching the Star Wars films in release order — episode number is event time, viewing date is processing time. Confusing the two fabricates data: a request-rate monitor that windows by processing time shows a phantom traffic spike while it burns through a backlog after a redeploy. Event-time windows have their own hard problem — *completeness*: you can never be sure all events for the 37th minute have arrived. After declaring a window done you must handle **stragglers**, either by dropping them (tracking the drop rate as a metric) or by publishing a *correction* and possibly retracting earlier output; some systems emit watermark-style messages ("no more events before *t*"), though multiple producers each need their own tracked threshold. Worse, whose clock stamps the event? A mobile app may buffer events offline for days, and user-controlled device clocks can't be trusted ([[Clock Skew]] and worse). The three-timestamp trick: record event-occurred and event-sent per the device clock, plus event-received per the server clock; the difference between the last two estimates the device's clock offset, which corrects the first. Window shapes then follow: **tumbling** (fixed length, each event in exactly one window), **hopping** (fixed length, overlapping by a hop, smoothing), **sliding** (all events within some interval of each other, no fixed boundaries), **session** (no fixed duration — a burst of one user's activity, closed by inactivity).

## Trade-offs & Pitfalls
Processing time buys simplicity, event time buys correctness plus straggler-handling machinery. Dropping stragglers silently corrupts counts; corrections complicate downstream consumers. Batch has the identical timestamp problems — streaming just makes them visible.

## Examples & Systems
Snowplow logs the three timestamps for mobile analytics; the Dataflow model formalized watermarks and corrections; sessionization is standard in website analytics.

## Related
- up: [[Processing Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Clock Synchronization and Accuracy]] — why device and server clocks disagree
- [[Monotonic Versus Time-of-Day Clocks]] — the timestamp source events rely on
- [[Uses of Stream Processing]] — analytics, the main consumer of windows
- [[Fault Tolerance]] — replays that widen the event/processing-time gap
