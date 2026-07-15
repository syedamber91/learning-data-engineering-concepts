---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9-4c5.md
last_updated: '2026-07-15'
qc: passed
slug: batch-vs-stream-throughput-and-latency
topics:
- data-pipeline-design-framework
---

Vu Trinh frames batch-vs-stream as the question that "shapes every infrastructure decision that follows," and one that should already be answered by the [[sink-first-requirements-gathering|sink]] and [[source-constraints-and-schema-risk|source]] requirements rather than decided independently. In batch, the two natural questions — how much data, and how long does processing have to finish — combine into throughput: the sustained rate the system must sustain (records/second, GB/hour, TB/day). Throughput, not raw data volume, is what should drive resourcing, because processing 1TB in 20 hours is a completely different system than processing it in 30 minutes. Higher throughput comes from more data at a fixed time window or a shorter window at fixed data, and it costs more (bigger workers, more of them, higher bills); lower throughput — less data or more time — needs fewer resources. His scaling ladder runs from DuckDB/Polars on a single well-resourced node, up to Spark or SQL-based distributed systems (Snowflake, BigQuery, Databricks, Trino) once the resource needs stop fitting on one machine.

Streaming can't answer "how much data" at all, since the data is unbounded, so it splits into two different constraints instead: latency (how fast must each individual record be processed — 100ms for fraud detection, 30 seconds tolerable for a near-real-time dashboard) and throughput (now an explicit, spiky metric — 1,000 records/second on a quiet day, 50,000 during a marketing-driven spike). The two interact: lowering per-record latency tends to raise throughput, and adding parallelism can improve both by spreading records across more workers. But every record carries fixed per-record overhead (serialization, network, disk I/O, function-call cost) regardless of its size, and that overhead is what makes micro-batching the pragmatic answer even inside stream processors — Flink itself batches records over a short window (e.g. 100ms) to pay the overhead once per batch instead of once per record, at the cost of every record waiting out that window before it's processed. His resulting rule of thumb: Spark Structured Streaming is enough when throughput matters but latency doesn't need to be very low; Flink is the choice when latency must be low regardless of throughput, since it was built for that purpose.

*See also: [[data-grain-and-serving-storage-shape]] · [[concurrency-and-resource-isolation-in-serving]] · [[clarifying-questions-before-tools]]*
