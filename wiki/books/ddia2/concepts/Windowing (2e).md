---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, streaming, time, event-time]
sources:
  - raw/ch12.md
---
# Windowing

Grouping unbounded stream events into bounded chunks so aggregation is possible — tumbling, hopping, sliding, session. Made hard by the gap between event time and processing time.

See [[Reasoning About Time (2e)]].

## Appears In
- [[Average, Median, and Percentiles (2e)]]
- [[Batch and Stream Processing (2e)]]
- [[Dealing with Conflicting Writes (2e)]]
- [[Detecting Concurrent Writes (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Log-Based Message Brokers (2e)]]
- [[Monotonic Versus Time-of-Day Clocks (2e)]]
- [[Processing Streams (2e)]]
- [[Reasoning About Time (2e)]]
- [[State, Streams, and Immutability (2e)]]
- [[Stream Joins (2e)]]
- [[Two-Phase Locking (2e)]]
- [[Understanding Load (2e)]]
- [[Use of Response Time Metrics (2e)]]

## In the vutr data-engineering wiki
- [[watermark]] — the mechanism that decides when a window is done.
- [[dataflow-model]] — the model that formalized windows, watermarks, and corrections together.
