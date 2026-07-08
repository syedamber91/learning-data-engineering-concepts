---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: structured-streaming
topics:
- spark
---

Structured Streaming is a stream-processing engine built on the Spark SQL engine. Its core design principle is to treat a continuous stream as a subset of bounded data — the same declarative DataFrame/SQL plan that runs over a static table runs incrementally over the unbounded stream, so [[catalyst-optimizer]] and the rest of the batch machinery apply unchanged rather than being reinvented for streaming.
