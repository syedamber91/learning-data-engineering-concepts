---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: dataflow-model
topics:
- flink
---

The Dataflow model's core design principle is to 'never rely on any notion of completeness,' and it deliberately avoids the terms 'streaming/batch' in favor of 'unbounded/bounded' data. Its authors argue the major weakness of prior systems is assuming unbounded input will eventually be complete — an assumption that breaks against today's enormous, highly disordered data.

*See also: [[spark-structured-streaming]] · [[apache-flink]] · [[flink-memorysegments]] · [[lambda-architecture]] · [[rocksdb-state-store]] · [[watermark]]*

## Related in the other wiki
- [[Reasoning About Time]] — DDIA's note on the ambiguity of event-time vs processing-time windows credits "the Dataflow model" with formalizing watermarks and corrections, the same never-assume-completeness principle this note states.
