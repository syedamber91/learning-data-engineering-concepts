---
persona: vutr
kind: concept
sources:
- raw/flink-additional/the-stream-processing-model-behind.md
last_updated: '2026-07-15'
qc: passed
slug: dataflow-triggers-and-refinement-modes
topics:
- flink
---

The Dataflow model treats every windowing strategy as **unaligned** by default — meaning windows can apply to specific subsets of the data rather than uniformly across all of it — while still allowing custom logic to build aligned windows when that's what's wanted. Structurally, any windowing process decomposes into two operations: **AssignWindows**, which assigns an element to zero or more windows (logically creating a copy of the element per window it belongs to), and **MergeWindows**, which merges windows together at grouping time. That merge step, which happens as part of `GroupByKeyAndWindow`, is specifically what lets data-driven windows — like sessions — get constructed as data actually arrives, rather than along a predetermined clock.

Relying on watermarks alone to decide when a window's result should be emitted turns out to be a genuine dilemma: watermarks can be "too fast," letting late data arrive behind them, or "too slow," stalling the whole pipeline while it waits on a straggler. The paper's answer is the **trigger** — a mechanism, independent of the watermark's own accuracy, for specifying exactly when a window's result should materialize. The authors draw this back explicitly to the Lambda Architecture: Lambda's two-pipeline hedge doesn't solve the completeness problem by being faster, it gives a fast, low-latency estimate from the streaming layer and later corrects it with the batch layer's answer. Triggers let a single pipeline do the analogous thing by emitting multiple panes (successive answers) for the same window over time.

Named trigger implementations: triggering at a **completion estimate** (i.e., a watermark); triggering at a **point in processing time**; triggering on **data-arriving characteristics** (counts, bytes, punctuation, pattern matches); and **composite triggers** that combine any of the above via loops, sequences, or logical AND/OR — with users free to mix runtime primitives (watermark timers, processing-time timers) and external signals (data-injection requests, external progress metrics).

Beyond *when* a trigger fires, **refinement modes** govern how successive panes for the same window relate to each other. **Discarding**: each firing's window contents are thrown away afterward, so later results have no relation to earlier ones — the most buffer-space-efficient option, useful when downstream consumers need each trigger's value treated independently. **Accumulating**: window contents persist across firings, so later results build on and overwrite earlier ones — this is the mode Lambda Architecture effectively uses, since the batch layer's output later overwrites the streaming layer's earlier estimate. **Accumulating & Retracting**: like Accumulating, but the previously emitted value is also persisted, so the next firing first emits an explicit retraction of the old value before emitting the new one.

Vu's notes also carry forward the paper's own account of *why* these choices were made, drawn from real internal Google pipelines: a **Unified Model** (one pipeline instead of separate batch and streaming code) was motivated partly by customers who stopped trusting the weakly-consistent gap between a MillWheel streaming pipeline and a nightly MapReduce "truth" batch job. **Sessions** became an indispensable, first-class case because of their use across search, ads, analytics, social media, and YouTube. Two MillWheel **billing teams'** pain with watermark-based completion — one built its own bespoke update/retraction system from scratch, another suffered watermark lag caused by stragglers — directly motivated triggers plus accumulation. **Recommendation pipelines** favored processing-time triggers over waiting for watermark-based completeness, since a regularly-updated partial view was worth more to them than a delayed, more-complete one. And Google's own web-search **anomaly-detection** systems — running several spike-detectors concurrently and multiplexing their start/stop output — specifically motivated data-driven and composite triggers.

*See also: [[dataflow-model]] · [[windowing-triggers-and-late-events]] · [[watermark]] · [[apache-beam]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's own note on Lambda's dual-codebase cost and the batch/stream convergence (Spark microbatching on a batch engine, Flink running batch on a streaming core) is the book's version of the same completeness problem this note's triggers and refinement modes are built to answer without two pipelines.
