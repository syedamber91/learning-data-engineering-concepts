---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: watermark
topics:
- flink
---

A watermark is defined as the max observed event time minus a threshold, and it is a special event carrying a timestamp as a long value that flows in the stream just like a regular event. Watermarks are estimated indications, not absolute — if the watermark is at 10:15, data with event time 10:13 may still arrive; eager watermarks buy lower latency at the cost of accuracy, relaxed ones trade latency for less data loss.

*See also: [[spark-structured-streaming]] · [[apache-flink]] · [[flink-memorysegments]] · [[dataflow-model]] · [[lambda-architecture]] · [[rocksdb-state-store]]*

## Related in the other wiki
- [[Stream Joins]] — DDIA's stream-stream window join (e.g. matching search-and-click events within an hour) depends on the same eager-vs-relaxed timing trade-off this note describes for watermarks.
- [[Reasoning About Time]] — DDIA's note on event-time windowing and "watermark-style messages" for handling stragglers is the book's version of the max-observed-event-time-minus-threshold definition given here.
