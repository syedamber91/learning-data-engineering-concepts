---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia2, exactly-once, microbatching, checkpointing, idempotence, flink, kafka]
sources:
  - raw/ch12.md
---
# Fault Tolerance (Stream Processing)
> Batch fault tolerance works by throwing away a failed task's output and starting over. You can't finish a stream, so you need something finer-grained.

## The Idea
**Batch frameworks tolerate faults fairly easily: if a task fails, restart it on another machine and discard the failed task's output.** **This transparent retry is possible because input files are immutable, each task writes its output to a separate file, and output is made visible only when a task completes successfully.**

**In particular, the batch approach ensures the output is the same as if nothing had gone wrong.** **It appears as though every input record was processed exactly once — no records skipped, none processed twice.** **Although restarting means records may be processed multiple times, the visible effect is as if processed once. This is exactly-once semantics** — **although effectively-once would be a more descriptive term.**

**The same issue arises in stream processing but is less straightforward.** **Waiting until a task is finished before making its output visible is not an option, because a stream is infinite — you can never finish processing it.**

## How It Works
**Microbatching and checkpointing.** **One solution: break the stream into small blocks and treat each like a miniature batch process.** **This is microbatching, used in Spark Streaming.** **The batch size is typically around one second, a performance compromise: smaller batches incur greater scheduling and coordination overhead, larger batches mean a longer delay before results become visible.** **Microbatching also implicitly provides a tumbling window equal to the batch size — windowed by processing time, not event timestamps — so jobs needing larger windows must explicitly carry state from one microbatch to the next.**

**A variant, used in Apache Flink, is to periodically generate rolling checkpoints of state and write them to durable storage.** **If an operator crashes it restarts from its most recent checkpoint and discards any output generated between the checkpoint and the crash.** **Checkpoints are triggered by barriers in the message stream, similar to microbatch boundaries but without forcing a particular window size.**

**Within the confines of the framework, both approaches provide the same exactly-once semantics as batch processing.** **But as soon as output leaves the stream processor** — writing to a database, publishing to an external broker, triggering emails — **the framework can no longer discard the output of a failed microbatch.** **Restarting a failed task then causes the external side effect to happen twice, and microbatching or checkpointing alone is not sufficient.**

**Atomic commit revisited.** **To give the appearance of exactly-once processing in the presence of faults, all outputs and side effects of processing an event must persist if and only if the processing is successful.** **That includes messages sent to downstream operators or external messaging systems (including email or push notifications), database writes, changes to operator state, and acknowledgments of input messages — including moving the consumer offset forward in a log-based broker.** **These must all happen atomically: either they all occur, or none of them do.**

**This is the same distributed transaction and two-phase commit problem seen earlier.** **The traditional implementations such as XA have problems — but in more restricted environments an atomic commit facility can be implemented efficiently.** **Google Cloud Dataflow, VoltDB, and Apache Kafka do this.** **Unlike XA, these implementations do not attempt transactions across heterogeneous technologies but keep the transactions internal, managing both state changes and messaging within the stream processing framework.** **The overhead of the protocol can be amortized by processing several input messages within a single transaction.**

**Idempotence.** **The goal is to discard the partial output of failed tasks so they can be safely retried. Distributed transactions are one way; another is idempotence.** **An idempotent operation can be performed multiple times with the same effect as performing it once** — **deleting a key in a key-value store is idempotent; incrementing a counter is not.**

**Even if an operation is not naturally idempotent, it can often be made so with a bit of extra metadata.** **When consuming from Kafka, every message has a persistent, monotonically increasing offset** — **when writing a value to an external database, include the offset of the message that triggered the last write with the value, so you can tell whether an update has already been applied and avoid performing it again.** **The state handling in Storm's Trident is based on a similar idea.**

## Trade-offs & Pitfalls
**Relying on idempotence implies several assumptions:** **restarting a failed task must replay the same messages in the same order** (a log-based broker does this), **the processing must be deterministic, and no other node may concurrently update the same value.** **When failing over from one processing node to another, fencing may be required to prevent interference from a node thought to be dead but actually alive.** **Despite all those caveats, idempotent operations can be an effective way of achieving exactly-once semantics with only a small overhead.**

**Rebuilding state after a failure.** **Any stream process requiring state — windowed aggregations such as counters, averages, and histograms, and any tables and indexes used for joins — must ensure the state can be recovered.**

**One option is keeping state in a remote datastore and replicating it, although querying a remote database for each message can be slow.** **An alternative is keeping state local to the processor and replicating it periodically**, so a recovering task reads the replicated state and resumes without data loss. **Flink periodically captures snapshots of operator state and writes them to durable storage such as a distributed filesystem; Kafka Streams replicates state changes by sending them to a dedicated Kafka topic with log compaction, similar to CDC; VoltDB replicates state by redundantly processing each input message on several nodes.**

**In some cases replicating state may not even be necessary, because it can be rebuilt from the input streams.** **If the state consists of aggregations over a fairly short window, it may be fast enough to simply replay the input events for that window.** **If the state is a local replica of a database maintained by CDC, the database can be rebuilt from the log-compacted change stream.**

**All this depends on the performance characteristics of the underlying infrastructure.** **In some systems network delay may be lower than disk access latency, and network bandwidth comparable to disk bandwidth.** **No solution is universally ideal, and the merits of local versus remote state may shift as storage and networking technologies evolve.**

## Examples & Systems
Spark Streaming (microbatching); Flink (checkpoint barriers, state snapshots); Google Cloud Dataflow, VoltDB, Kafka (internal atomic commit); Storm's Trident; Kafka Streams state replication via a log-compacted topic.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Fault Tolerance]] — the same microbatching and checkpointing, the same atomic-commit-revisited argument, the same idempotence discussion with the offset-metadata trick and its three assumptions, and the same state-rebuilding options. The one adjustment is contextual: **the atomic commit discussion now points back to Chapter 8, where distributed transactions and 2PC moved**, rather than to the consistency chapter.

## Related
- up: [[Processing Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Exactly-Once Message Processing Revisited (2e)]] — the message-ID pattern
- [[Distributed Job Orchestration (2e)]] — the batch fault-tolerance approaches
- [[Distributed Locks and Leases (2e)]] — the fencing idempotence may need
- 1st edition: [[Fault Tolerance]] — the same subtopic
