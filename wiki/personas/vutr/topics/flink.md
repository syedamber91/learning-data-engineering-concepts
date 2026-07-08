---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: flink
---

Related: [[apache-flink]] · [[spark-structured-streaming]] · [[chandy-lamport-checkpointing]] · [[watermark]] · [[flink-memorysegments]] · [[rocksdb-state-store]] · [[dataflow-model]] · [[lambda-architecture]] · [[batch-vs-stream-tradeoff]] · [[exactly-once-needs-idempotent-sink]]

## Comparisons
The central axis is [[apache-flink]] versus [[spark-structured-streaming]]. Flink is a true streaming engine — everything is a stream, batch is the special case — while Spark aligns stream data into micro-batches and treats bounded data as the first-class citizen. The practical rule: for high-throughput near-real-time work that tolerates ~30s latency, [[spark-structured-streaming]] is enough (and covers 60-70% of streaming use cases); for low latency regardless of throughput, choose [[apache-flink]].

On fault tolerance, [[apache-flink]] uses [[chandy-lamport-checkpointing]] which never pauses the application, and manages memory explicitly via [[flink-memorysegments]] to dodge JVM per-record allocation. State backends overlap: [[rocksdb-state-store]] is available in Flink and, since Spark 3.2, in Spark as an alternative to the OOM-prone HDFS-backed default.

On philosophy, [[dataflow-model]] and [[lambda-architecture]] answer the completeness problem differently: Lambda hedges with a low-latency streaming estimate plus a batch correctness path, whereas the Dataflow model refuses to rely on completeness at all and reframes the world as unbounded vs bounded data.

## Open questions
- How much of the 30-40% of streaming use cases that [[spark-structured-streaming]] does *not* cover genuinely requires [[apache-flink]], versus other engines entirely?
- Where exactly should the eager-vs-relaxed [[watermark]] threshold sit for a given workload, and how is that tuned in practice?
- What is the concrete OOM boundary that pushes a Spark job from the HDFS-backed store to the [[rocksdb-state-store]]?
- Beyond overwriting a whole table, what other idempotent-sink patterns satisfy [[exactly-once-needs-idempotent-sink]] without full rewrites?
- How does the 32KB block size of [[flink-memorysegments]] interact with record size and throughput at scale?

## Synthesis
The through-line here is that stream processing is a trade against batch's completeness for latency, and every design choice flows from that ([[batch-vs-stream-tradeoff]]). [[apache-flink]] leans fully into streaming — [[chandy-lamport-checkpointing]] without pausing, explicit [[flink-memorysegments]] memory — while [[spark-structured-streaming]] keeps micro-batching and bounded data as first-class, which is why it comfortably handles the majority of near-real-time needs. Correctness ultimately lives at the edges: a [[watermark]] is only an estimate, and true exactly-once depends on [[exactly-once-needs-idempotent-sink]]. Underneath it all, the [[dataflow-model]] argues we should stop assuming completeness at all — a sharper answer than [[lambda-architecture]]'s estimate-then-correct hedge.
