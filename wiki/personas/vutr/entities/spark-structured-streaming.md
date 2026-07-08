---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: spark-structured-streaming
topics:
- flink
- spark
---

Structured Streaming is a stream processing engine built on the Spark SQL engine, and its core design principle is to treat a continuous stream as a subset of bounded data — micro-batching, where bounded data is the first-class citizen. The same declarative DataFrame/SQL plan that runs over a static table runs incrementally over the unbounded stream, so [[catalyst-optimizer]] and the rest of the batch machinery apply unchanged rather than being reinvented for streaming. It offers Default, Fixed-Interval, One-Time, and Available-Now (multi-batch) trigger types, and covers 60-70% of the streaming use cases that themselves are only ~10% of all workloads.
