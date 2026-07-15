---
persona: vutr
kind: concept
sources:
- raw/flink-additional/batch-and-stream-processing.md
last_updated: '2026-07-15'
qc: passed
slug: batch-vs-stream-tradeoff
topics:
- flink
---

Batch processing waits for data to reach a threshold (daily, weekly, whatever the boundary is) and then processes it all in one operation; stream processing instead handles each piece of data right after it happens, one after another, continuously. Vu's central trade: batch buys operational simplicity by knowing its search scope up front — since aggregation and joins are fundamentally a search for records sharing a key, and batch already knows the full boundary of what it's processing, that search space is bounded "for free." Streaming has no such luck; the system never sees a natural search scope at all, which is exactly the problem [[windowing-triggers-and-late-events|windowing]] exists to solve.

Reprocessing and fault tolerance are correspondingly easy in batch, given three conditions Vu lays out explicitly: (1) the data source stays available for reprocessing — achieved in practice by keeping the CSV or database snapshot around in object storage; (2) the processing is **deterministic** — the same input always produces the same output; (3) the processing's *effect* is **idempotent** — running it once has the same effect as running it many times, his example being f(x) = 1·x. He draws a careful line between the two: "deterministic refers to the output, while idempotence pertains to the effect of the output on the system." In batch practice, idempotence means the next run's output must entirely *replace* the previous run's — `CREATE OR REPLACE TABLE` and dbt's insert-overwrite strategy are his named examples — otherwise reruns risk duplicating data or mixing runs together. Spark improves on the brute-force "reprocess the whole batch" fallback specifically because it tracks each RDD's lineage — the chain of transformations that produced it — so a lost partition can be rebuilt by replaying just that lineage against the original data, not by rerunning everything.

Stream processing gets implemented one of two ways, per Vu: **micro-batching** (Spark Structured Streaming) or **record-by-record** processing (Flink); the concepts below apply to either. Its latency win comes bundled with real complexity: source and sink must both be able to produce/accept an unbounded stream (reading a file means streaming it row by row, not loading it whole); event time versus processing time becomes unavoidable, along with the [[watermark]] that estimates the gap between them; [[windowing-triggers-and-late-events|windowing]] manufactures the finite search scope batch got for free, and a trigger decides when a window's result actually computes and emits; late events need an explicit policy — drop them, or accept them within a configured grace period; and any stateful operation (like a running count) needs its own fault-tolerance, scalability, and cleanup story (see [[flink-state-management-and-backends]]). Underneath both paradigms, checkpointing is the shared fault-tolerance primitive — periodically persisting job state to durable external storage (HDFS, S3) so a failure resumes from the last checkpoint instead of from scratch.

Vu's own verdict, stated plainly: batch is the paradigm "most of us are familiar with," simpler and lower-complexity; implement streaming "only if your organization truly gets benefit from stream processing," because it comes with a real, added learning curve.

*See also: [[apache-flink]] · [[windowing-triggers-and-late-events]] · [[watermark]] · [[flink-state-management-and-backends]] · [[dataflow-model]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's own note that the deep difference between the paradigms is only bounded vs. unbounded input, and that even that line is blurring (Spark microbatches on a batch engine, Flink runs batch on a streaming core), is the book's version of the exact trade-off this note works through with Vu's own worked examples.
- [[Idempotence]] — DDIA's concept ("doing it twice has the same effect as doing it once") is the general statement of the idempotent-effect condition this note ties to batch's `CREATE OR REPLACE TABLE`/insert-overwrite reprocessing pattern.
