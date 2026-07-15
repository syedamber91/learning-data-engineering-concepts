---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
type: topic
tags: [ddia, stream-processing, operators, unbounded-data]
sources:
  - raw/ch11.md
---
# Processing Streams

Once a stream exists, three things can be done with it: write its events into a database, cache, or search index for others to query; push them to humans (alerts, dashboards, notifications); or transform one or more input streams into derived output streams — the focus here. The code doing that transformation is an *operator* or *job*, a close cousin of Unix pipes and [[MapReduce]]: it consumes inputs read-only and appends output elsewhere, with the same [[Partitioning]] and parallelization patterns as batch [[Dataflow]] engines. The one crucial difference — the input never ends — cascades everywhere. Sorting is impossible, so sort-merge joins are out; a job may run for years, so "restart from the beginning" is not a fault-tolerance strategy; and "the last five minutes" turns out to be a genuinely slippery notion once event creation and event processing drift apart.

## Subtopics
- [[Uses of Stream Processing]] — complex event processing, stream analytics, keeping [[Materialized Views]] fresh, full-text search on streams, and how these differ from actor-style messaging.
- [[Reasoning About Time]] — event time vs processing time, straggler events, untrustworthy device clocks, and the four window types (tumbling, hopping, sliding, session).
- [[Stream Joins]] — stream-stream, stream-table, and table-table joins, and why joins against changing state become time-dependent and nondeterministic.
- [[Fault Tolerance]] — recreating batch-style [[Exactly-Once Semantics]] on infinite input via microbatching, checkpointing, restricted atomic commit, [[Idempotence]], and state rebuilding.

## Key Takeaways
- A stream operator is a pipeline stage: read-only inputs, append-only outputs — batch's dataflow discipline carried into unbounded time.
- Windowing by the processor's own clock produces artifacts (a redeploy looks like a traffic spike); event-time windows are honest but must handle stragglers by dropping or issuing corrections.
- All three join types keep state from one input and probe it with the other; the ordering of events across streams decides the result, which makes joins nondeterministic unless versions are pinned (the slowly changing dimension trick).
- Exactly-once effects on infinite streams require making output visible atomically with offset advancement — via microbatches, checkpoints, in-framework transactions, or idempotent writes.

## Related
- chapter: [[Ch 11 - Stream Processing]] · part: [[Part III - Derived Data]]
- [[Transmitting Event Streams]] — the transport layer these operators consume from
- [[Databases and Streams]] — change streams as operator input, materialized views as output
- [[Batch and Stream Processing]] — Ch 12 on unifying the two paradigms
- [[Reduce-Side Joins and Grouping]] — the batch join machinery streams must replace
