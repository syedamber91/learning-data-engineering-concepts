---
persona: vutr
kind: concept
sources:
- raw/spark/everything-you-need-to-know-about-46d.md
last_updated: '2026-07-15'
qc: passed
slug: spark-stateful-operations-and-state-store
topics:
- spark
---

A **stateful** streaming query needs Spark to remember something across [[spark-structured-streaming-microbatch-and-triggers|micro-batches]] — a running counter, a set of keys already seen, buffered rows waiting on a match — because the correct result at micro-batch N depends on more than just that batch's own data. That memory is the **state**, and because a stream is unbounded, state can in principle grow forever; [[spark-watermark-event-time-and-windowing|the watermark]] is what gives Spark a defensible point to actually clean it up — once the watermark passes a window's end, Spark can assume all data for that window (including anything late but still within the watermark's threshold) has arrived, so the window's aggregation is final and its state can be discarded.

Four categories of stateful operation are named: **streaming (grouped/running) aggregation** — the common case, continuous sum/count/average either over the whole stream or over a window; **stream-stream joins** — joining two continuous, unbounded streams, which is structurally harder than a batch-batch join because the engine never has a complete view of either side at any given moment (a key with no match yet might simply not exist, or might still be about to arrive) — both streams are buffered in state to give matching a chance to happen, and that buffer's growth is bounded the same way window state is: by the watermark; **dropDuplicates** — guaranteeing a uniquely-keyed record is processed only once within a configured period, which requires Spark to store every distinct key it has seen during that window so it can recognize a repeat; and **custom/arbitrary stateful operations**, where users implement their own stateful logic directly.

The state itself has to live somewhere Spark's executors can read and write it, and Structured Streaming supports two backends. The **HDFS-backed state store** is the default: it holds state in the executor's own JVM memory first, which means it inherits two of that architecture's known costs directly — large state can trigger the same [[executor-memory-model-and-caching|executor OOM]] risk as any other in-memory workload, and heavy state churn adds garbage-collection overhead on top of whatever the query itself is doing. The state is then persisted transactionally out to an HDFS-compatible filesystem for durability. The **RocksDB state store**, available since Spark 3.2, routes around both costs by storing state in the RocksDB instance's own memory and disk rather than the executor's JVM heap — an embedded C++ key-value store, so state growth doesn't compete with the executor's own JVM memory pool or trigger JVM garbage collection at all.

*See also: [[spark-watermark-event-time-and-windowing]] · [[spark-checkpointing-and-exactly-once]] · [[executor-memory-model-and-caching]] · [[stream-state-saving-mechanisms]]*

## Related in the other wiki
- [[Stream Joins]] — DDIA's general treatment of the stream-stream join problem (buffering both sides against an incomplete view of either) is the book-level statement of the exact mechanism this note ties to Spark's watermark-bounded state store.
