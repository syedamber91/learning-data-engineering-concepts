---
persona: vutr
kind: entity
sources:
- raw/flink-additional/apache-flink-overview.md
- raw/flink-additional/batch-and-stream-processing.md
- raw/flink-additional/the-stream-processing-model-behind.md
last_updated: '2026-07-15'
qc: passed
slug: watermark
topics:
- flink
---

Across Vu's writing on Flink and the Dataflow model, a watermark carries almost the same wording each time: it tells the system "no more data which have event time sooner this point of time will appear [in the pipeline]." If the watermark is at value T, the system assumes no event with a timestamp earlier than T will still show up. In Flink specifically, a watermark is implemented as a special event carrying a timestamp as a long value, flowing through the stream exactly like a regular event — not an out-of-band signal.

Watermarks exist to make **time domain skew** — the gap between event time (when something actually happened) and processing time (when the system observes it) — visible and actionable. That skew comes from ordinary causes: network/communication delays, or time spent processing at each pipeline stage. Event time never changes once recorded; processing time keeps changing as data moves through the pipeline. In a "super-ideal world," Vu notes, the skew would always be zero — everything would be processed the instant it happened.

The watermark is deliberately a *configurable trade-off between accuracy and latency*, not a fixed setting: an eager watermark buys low latency but risks lower accuracy, since late events can still arrive after it has already passed; a relaxed watermark gives late data more chance to catch up (better accuracy) at the cost of added processing latency from waiting. Vu is also explicit that a watermark is an *estimate*, not an absolute guarantee — even at a watermark of 10:15, there's a chance data with event time 10:13 arrives afterward.

One nuance he flags but doesn't resolve: "Spark Structured Streaming and Flink implement the watermark differently," which he calls out as something to keep in mind when building a streaming job — without spelling out what that implementation difference actually is. That's a genuine **source gap**.

*See also: [[apache-flink]] · [[dataflow-model]] · [[windowing-triggers-and-late-events]]*

## Related in the other wiki
- [[Reasoning About Time]] — DDIA's note on event-time windowing, stragglers, and "watermark-style messages" is the book's version of this same never-certain, estimate-not-guarantee framing of watermarks.
- [[Stream Joins]] — DDIA's stream-stream window join (matching events across streams within a bounded window, e.g. an hour) depends on the same eager-vs-relaxed timing trade-off this note describes for watermarks.
