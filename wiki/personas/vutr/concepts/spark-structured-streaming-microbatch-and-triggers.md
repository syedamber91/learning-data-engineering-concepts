---
persona: vutr
kind: concept
sources:
- raw/spark/everything-you-need-to-know-about-46d.md
last_updated: '2026-07-15'
qc: passed
slug: spark-structured-streaming-microbatch-and-triggers
topics:
- spark
---

Spark Structured Streaming's core design move is to treat a continuous stream as a subset of bounded data, so it can reuse the existing [[spark-application-architecture-and-execution-modes|batch driver/executor architecture]] wholesale rather than build a separate streaming engine. Starting a streaming query starts a long-running Spark application — the driver stays alive for the query's entire lifetime instead of exiting after one job, which is the one structural difference from ordinary batch execution.

Each stream has a **trigger**, which answers a single question: when should Spark check for new data? When a trigger fires, Spark queries the source for its latest position (e.g. asking Kafka for current offsets), identifies what's new since the last check, and packages that increment as a **micro-batch** — internally just a small, static DataFrame. Because [[rdd-fundamentals-and-properties|Spark transformations are lazy]], nothing about that micro-batch actually executes until its action fires; in Structured Streaming, the sink write (`.writeStream.format(...).start(...)`) is that action. For each micro-batch, Spark forms a full query plan (transformations plus the sink action), builds logical and physical plans, and the driver schedules tasks for executors from that physical plan — the same [[catalyst-optimizer-phases|Catalyst pipeline]] batch queries go through, just re-run once per micro-batch rather than once total.

Four trigger types control *when* this cycle runs: **Default** fires a new micro-batch immediately once the previous one completes and new data exists — no waiting for a scheduled interval. **Fixed-Interval** targets a specific cadence; if a batch finishes before the interval elapses, Spark waits out the remainder, but if a batch runs long, the next one starts immediately on completion rather than waiting for the next scheduled tick — so a slow batch doesn't get further delayed, and duration doesn't accumulate. **One-Time** processes whatever data currently exists and then stops, making a streaming query behave as a single finite batch job. **Available-now, micro-batch** is the same idea but can split that data across multiple micro-batches rather than one, depending on the source.

Batch size is throttled independently of the trigger's timing via three source-side knobs: `maxOffsetsPerTrigger` caps the number of records consumed per micro-batch for offset-based sources (Kafka, Kinesis); `maxFilesPerTrigger` caps the number of files processed per micro-batch for file-based sources (Delta Lake, JSON, Parquet); `maxBytesPerTrigger` softly caps total bytes processed per micro-batch for those same file sources — "softly" because the cap can be exceeded when the last file needed to satisfy it is itself larger than the remaining budget (three 2GB files still get processed fully even against a 5GB cap, landing at 6GB). The trigger interval *can* implicitly bound batch size too, but only indirectly and only when source throughput is known and stable — a stable stream gives every trigger roughly the same volume, letting the interval double as an approximate size control, but it's not a direct or reliable substitute for the explicit knobs above.

Batch size is a genuine two-sided trade-off, not a "smaller is safer" default. Too small a batch means the fixed per-batch planning/scheduling overhead — the source's example: 7 seconds of per-batch planning times 100 batches is 12 minutes spent purely planning — dominates actual processing time, and a batch that's too small in volume may leave cluster resources idle rather than fully utilized. Too large a batch drives up latency directly, since every record in the batch has to wait for the *entire* batch to finish before reaching the sink (a 10-minute batch means even the freshest record in it is 10 minutes stale by the time it's written), and for stateful operations specifically — aggregations, joins — a large batch also pressures executor memory harder than a small one would.

*See also: [[jobs-stages-tasks-dag-and-dependencies]] · [[catalyst-optimizer-phases]] · [[spark-watermark-event-time-and-windowing]] · [[spark-stateful-operations-and-state-store]] · [[batch-vs-stream-tradeoff]]*
