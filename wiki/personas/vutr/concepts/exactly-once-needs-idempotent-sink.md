---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: exactly-once-needs-idempotent-sink
topics:
- flink
---

Exactly-once delivery requires an idempotent sink — overwriting the whole table is the classic example. A Kafka source is at-least-once by default, and each micro-batch has at most one commit file, so the sink is where correctness actually gets pinned down.

*See also: [[spark-structured-streaming]] · [[apache-flink]] · [[flink-memorysegments]] · [[dataflow-model]] · [[lambda-architecture]] · [[rocksdb-state-store]]*

## Related in the other wiki
- [[Fault Tolerance]] — DDIA's chapter-11 note lists the concrete idempotence tactics (storing the triggering Kafka offset with each write so replays are detected and skipped) that make an idempotent sink possible in practice.
- [[Exactly-Once Semantics]] — DDIA's concept page frames exactly-once as retries made invisible via atomic commit or idempotence with end-to-end operation IDs, the same idempotent-sink dependency this note states directly.
