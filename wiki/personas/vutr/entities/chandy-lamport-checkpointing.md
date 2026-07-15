---
persona: vutr
kind: entity
sources:
- raw/flink-additional/apache-flink-overview.md
- raw/flink-additional/i-spent-8-hours-understanding-which.md
last_updated: '2026-07-15'
qc: passed
slug: chandy-lamport-checkpointing
topics:
- flink
---

The naive way to take a checkpoint — pause the application, checkpoint, resume from the checkpoint on failure — is impractical: it requires the whole pipeline to stop before checkpointing, which raises latency. Flink instead implements checkpointing via the Chandy-Lamport algorithm, which decouples checkpointing from data processing without forcing the application to pause.

The mechanism: the JobManager initiates a checkpoint by sending a **checkpoint barrier** — a special record carrying a checkpoint ID — to every source operator (each data partition gets its own associated barrier). A barrier logically splits the stream into two parts: state modifications preceding it belong to the checkpoint it identifies, modifications after it belong to the next one. When a source receives the barrier, it pauses emitting events downstream just long enough to trigger a checkpoint of its own local state to the state backend; once the backend confirms completion, the source sends a checkpoint confirmation to the JobManager, then resumes normal operation and broadcasts the barrier onward to its outgoing partitions.

A downstream task waits for the barrier to arrive on *all* of its input partitions before checkpointing — since a task can handle more than one partition, it keeps processing data from partitions where the barrier hasn't arrived yet, while buffering (not processing) any data that arrives on a partition where the barrier already has, so records from before and after the checkpoint never get mixed. Once all of a task's partition-barriers have arrived, it checkpoints its own state to the local state backend and broadcasts the barrier to its downstream tasks; only then does it drain its buffered data before returning to normal input processing. The barriers eventually reach the sink tasks, which run the same wait-checkpoint-confirm sequence. The JobManager considers the whole application's checkpoint successful only once every task in the application has sent back its confirmation.

Vu flags, without elaborating further, that this checkpoint process is also what underpins Flink's exactly-once delivery guarantees — a connection his sources point to via an external Flink blog post rather than explain directly; how checkpointing composes with sink-side idempotence to actually deliver exactly-once semantics is left as a **source gap**.

*See also: [[apache-flink]] · [[flink-state-management-and-backends]] · [[flink-networking-and-flow-control]]*

## Related in the other wiki
- [[Fault Tolerance]] — DDIA's chapter-11 note describes Flink's barrier-based checkpointing as one of four exactly-once tactics (alongside microbatching, atomic commit, and idempotence), matching this note's account of a checkpoint barrier that splits the stream into pre/post-checkpoint state without pausing the application.
- [[Exactly-Once Semantics]] — DDIA's concept names atomically committing outputs plus offsets as one route to exactly-once; this note's own account of Flink's barrier confirmation reaching the JobManager only once every task acknowledges is the same commit-coordination idea, one level more mechanical.
