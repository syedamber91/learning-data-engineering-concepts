---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-flink
topics:
- flink
---

Flink treats everything as a stream, with batch being just a special case. Its runtime has four JVM components — the Dispatcher, JobManager, ResourceManager, and TaskManagers — and it supports three window types: Fixed/Tumbling, Sliding, and Session. Reach for Flink when you need low latency regardless of throughput.

*See also: [[spark-structured-streaming]] · [[flink-memorysegments]] · [[dataflow-model]] · [[lambda-architecture]] · [[rocksdb-state-store]] · [[watermark]]*
