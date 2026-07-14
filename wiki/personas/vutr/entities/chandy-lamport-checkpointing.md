---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: chandy-lamport-checkpointing
topics:
- flink
---

Flink implements checkpointing using the Chandy-Lamport algorithm, which does not force the application to pause and de-couples checkpointing from data processing. This is what lets Flink take consistent snapshots without stalling the pipeline.

*See also: [[spark-structured-streaming]] · [[apache-flink]] · [[flink-memorysegments]] · [[dataflow-model]] · [[lambda-architecture]] · [[rocksdb-state-store]]*

## Related in the other wiki
- [[Fault Tolerance]] — DDIA's chapter-11 note describes Flink's barrier-based checkpointing as one of four exactly-once tactics (alongside microbatching, atomic commit, and idempotence), matching this note's claim that Chandy-Lamport decouples checkpointing from processing without pausing the application.
