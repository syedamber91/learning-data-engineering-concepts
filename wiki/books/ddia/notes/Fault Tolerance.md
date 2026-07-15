---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia, exactly-once, checkpointing, idempotence]
sources:
  - raw/ch11.md
---
# Fault Tolerance
> Batch discards a failed task's output and retries; a never-ending stream can't "wait until done," so exactly-once effects need microbatches, checkpoints, transactions, or idempotent writes.

## The Idea
[[MapReduce]] earns its clean semantics cheaply: immutable inputs, per-task output files, visibility only on success. The result looks as if every record were processed exactly once even when tasks retried — [[Exactly-Once Semantics]] (more honestly, *effectively-once*). Streams break the recipe because output must become visible continuously; there is no "job finished" moment at which to atomically publish.

## How It Works
**Microbatching** (Spark Streaming) chops the stream into ~1-second mini batch jobs — smaller batches cost more coordination, larger ones delay results — and implicitly imposes a processing-time tumbling window equal to the batch size. **Checkpointing** (Flink) instead injects barriers into the stream and periodically writes rolling snapshots of operator state to durable storage; on crash, restart from the last checkpoint and discard output produced since. Both give exactly-once *within* the framework, but once output escapes — a database write, an email — the framework can't un-send it, and a retry doubles the side effect. **Atomic commit, restricted:** make message acknowledgment (offset advance), state changes, and downstream sends take effect atomically or not at all. XA-style heterogeneous [[Two-Phase Commit]] proved fragile, but keeping the transaction *inside* the framework works — Google Cloud Dataflow and VoltDB do this, Kafka planned it — amortizing protocol overhead over many messages per transaction. **[[Idempotence]]:** make retried writes harmless. Naturally idempotent ops (set key = value) just work; others become idempotent with metadata, e.g. storing the triggering Kafka offset with each database write so already-applied updates are detected and skipped (Storm's Trident). This assumes deterministic processing, replay in the same order (a log-based broker provides it), no concurrent writers, and possibly [[Fencing Tokens]] against zombie nodes. **State rebuild:** windowed aggregates and join tables must survive failure — replicate state remotely (slow per-message), snapshot locally to durable storage (Flink → [[HDFS]]), stream state changes to a compacted changelog topic (Samza, Kafka Streams — CDC applied to yourself), process redundantly on several nodes (VoltDB), or simply replay inputs when the window is short.

## Trade-offs & Pitfalls
Microbatching couples latency to fault-tolerance granularity. External side effects remain the hard boundary for every checkpoint scheme. Idempotence is cheap but caveat-laden. Local vs remote state has no universal winner — it shifts with disk and network performance.

## Examples & Systems
Spark Streaming, Apache Flink, Google Cloud Dataflow, VoltDB, [[Apache Kafka]] (transactions; compacted changelogs), Storm Trident.

## Related
- up: [[Processing Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Atomic Commit and Two-Phase Commit (2PC)]] — the general protocol restricted here
- [[Distributed Transactions in Practice]] — why XA across systems disappointed
- [[Partitioned Logs]] — replayable offsets that make retries and idempotence possible
- [[The Output of Batch Workflows]] — the batch fault model being emulated
- [[exactly-once-needs-idempotent-sink]] — this note's idempotence tactic (storing the triggering Kafka offset with each write so replays are detected and skipped) is a concrete instance of vutr's general rule that exactly-once ultimately depends on an idempotent sink.
- [[chandy-lamport-checkpointing]] — this note's description of Flink injecting barriers for periodic state snapshots without pausing the stream is exactly the Chandy-Lamport algorithm vutr's entity note names.
