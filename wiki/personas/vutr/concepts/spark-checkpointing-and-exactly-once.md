---
persona: vutr
kind: concept
sources:
- raw/spark/everything-you-need-to-know-about-46d.md
last_updated: '2026-07-15'
qc: passed
slug: spark-checkpointing-and-exactly-once
topics:
- spark
---

Structured Streaming's fault tolerance rests entirely on a configured checkpoint location (an HDFS-compatible path), to which Spark periodically writes the query's processed source offsets, its own query "identity," and its [[spark-stateful-operations-and-state-store|state]] — enough to resume exactly where a failed query left off rather than restart from scratch. The checkpoint directory has two subdirectories doing two distinct jobs: **offsets** acts as a write-ahead log — before Spark processes a batch, it writes down what it's *about* to process (e.g. "for batch #10, I will process Kafka offsets 501-600"); **commits** is the source of truth for what actually finished — a file numbered N in commits means batch N is fully processed and durably done.

That split is what makes recovery a simple diff rather than a guess. On restart, Spark looks at both folders: if offsets has an entry for batch #10 but commits does not, Spark concludes batch #10 started but never finished, and reprocesses it from the exact offset range recorded in the offsets file — which requires the source itself to be **replayable** (support requesting data from a specific prior offset, as Kafka does). This is why checkpointing depends on the source's own replay guarantee, not just on Spark's own bookkeeping.

**Exactly-once** is a stronger claim than "fault tolerant" — no data loss *and* no duplication — and Vu is explicit that it isn't something Structured Streaming can deliver on its own; it requires all three legs of the pipeline (source, processing engine, sink) to each hold up their end. On the **source** side, Kafka's own default guarantee is at-least-once, not exactly-once, because its design deliberately prioritizes no data loss and throughput over deduplication in an unreliable distributed environment — so getting to exactly-once requires an explicit dedup mechanism somewhere downstream of Kafka, not an assumption that Kafka already provides it. On the **processing** side, the checkpoint mechanism above directly guarantees no missed processing (the offsets log always has the range that must be (re)done) and, separately, guarantees each micro-batch is only ever *successfully* processed once, because a batch can only ever have one commit file — a second attempt at an already-committed batch simply never happens.

The gap that's left, and the one that actually needs an application-level answer, is the **sink**. A batch's result can be *materialized* to the sink before its commit file is written, and if the engine crashes in that exact window — output written, commit file not yet written — recovery sees no commit for that batch and reprocesses it, writing the same output to the sink a second time. Checkpointing prevents Spark from *skipping* or *double-committing* a batch internally, but it cannot prevent that batch's result from physically landing in the sink more than once. The only fix is for the sink itself to be idempotent — the source's example is overwriting the whole output table on each write, so a second write of the same batch's result simply replaces the first with an identical value rather than appending a duplicate. The conclusion Vu draws explicitly: exactly-once is not a property of your Structured Streaming application alone — it depends on reading your specific source's and sink's own documented guarantees, not assuming the framework covers the whole pipeline for you.

*See also: [[spark-stateful-operations-and-state-store]] · [[spark-structured-streaming-microbatch-and-triggers]] · [[idempotency]] · [[pipeline-failure-recovery-and-checkpointing]]*

## Related in the other wiki
- [[Idempotence]] — DDIA's own statement that "doing it twice has the same effect as doing it once" is the exact property this note's sink-idempotency requirement (overwrite-the-whole-table) is a concrete instance of.
- [[Databases and Streams]] — DDIA's treatment of exactly-once as a pipeline-wide property, not a single-component guarantee, is the general version of the source-processing-sink three-way split this note works out for Structured Streaming and Kafka specifically.
