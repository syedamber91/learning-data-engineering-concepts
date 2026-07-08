---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: rocksdb-state-store
topics:
- flink
---

RocksDB is a state backend option in both engines — in Flink alongside Java heap/off-heap, and in Spark since 3.2. In Spark's case the default HDFS-backed store keeps state in JVM memory and risks OOM, whereas the RocksDB state store pushes state into RocksDB's C++ memory and disk.

*See also: [[spark-structured-streaming]] · [[apache-flink]] · [[flink-memorysegments]] · [[dataflow-model]] · [[lambda-architecture]] · [[watermark]]*
