---
persona: vutr
kind: concept
sources:
- raw/spark/everything-you-need-to-know-about-46d.md
last_updated: '2026-07-15'
qc: passed
slug: spark-watermark-event-time-and-windowing
topics:
- spark
---

Stream processing has to reconcile two different clocks: **event time** (when something actually happened) and **processing time** (when the engine observes it). In an ideal world they'd be equal; in practice, network latency, machine failures, and human error mean processing time always lags event time, and the gap between them is **time skew**. That gap matters concretely the moment you want to aggregate over an event-time window — "sum visited users from 12:00 to 12:10" can't be answered until the engine has some way of knowing all the 12:00-12:10 data has actually arrived, not just that its own clock passed 12:10.

Watermark is Spark's answer to that completeness question. Spark's watermark is computed as the maximum event time observed so far, minus a user-specified threshold — call the result W. W does two jobs at once: it decides when an event-time window can close and emit its result (a window ending at 11:00 event time closes once W passes 11:00), and it decides which incoming events count as late (anything with an event time older than W is considered late and may be dropped from its window). Because Spark computes W only at the end of each micro-batch — not continuously — the watermark inherits [[spark-structured-streaming-microbatch-and-triggers|the micro-batch cycle's]] own granularity: minimum end-to-end latency is at least the batch interval plus the watermark delay, which the source flags directly as a reason micro-batch watermarking isn't a fit for true millisecond-latency requirements.

The threshold itself carries a hidden assumption worth being explicit about: it only works well if the gap between event time and processing time stays roughly constant. A 5-minute threshold assumes records arrive within 5 minutes of their event time; if most early records are under that bound but a later shift in network conditions pushes most records past 6 minutes late, the fixed threshold now discards records it was originally tuned to keep — the threshold doesn't adapt to a changing skew distribution, it just keeps enforcing the number it was given.

**Windowing** is the general mechanism that gives stateful operations (sum, count, join) a bounded search scope to work within, rather than searching the entire infinite stream for matching keys every time — stateless operations like `filter` don't need it at all. Spark supports three window shapes: **tumbling** (fixed, non-overlapping size, e.g. hourly buckets), **sliding** (a window size plus a slide period, e.g. 30-minute windows starting every 5 minutes, so windows overlap), and **session** (per-key windows bounded by a timeout gap in activity, rather than a fixed clock boundary). Event-time windowing specifically requires a watermark to be defined alongside it — the watermark is what tells the window when it's safe to close and what to do with data that shows up after it already did.

*See also: [[spark-structured-streaming-microbatch-and-triggers]] · [[spark-stateful-operations-and-state-store]] · [[spark-checkpointing-and-exactly-once]] · [[watermark]] · [[windowing-triggers-and-late-events]]*

## Related in the other wiki
- [[Processing Streams]] — DDIA's own treatment of windowing and time-skew handling in stream processors is the general vocabulary this note's Spark-specific watermark formula (max observed event time minus threshold) and three window types instantiate concretely.
