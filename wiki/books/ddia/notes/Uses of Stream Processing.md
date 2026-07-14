---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia, cep, stream-analytics, materialized-views]
sources:
  - raw/ch11.md
---
# Uses of Stream Processing
> Stream processors serve four distinct masters — pattern detection, windowed statistics, view maintenance, and standing search queries — each stressing different capabilities.

## The Idea
Streaming grew out of monitoring: fraud detection on card usage, algorithmic trading on price feeds, factory-machine supervision, military early warning. All need an answer *now*, not in tomorrow's batch run. But "process events continuously" hides several distinct application shapes, and the right framework depends on which one you have.

## How It Works
**Complex event processing (CEP)**, from 1990s research, is regex-for-events: you declare a pattern (often in a SQL-like language), the engine keeps a state machine per query, and emits a *complex event* when a sequence matches. The usual database relationship is inverted — queries are stored long-term while data flows past transiently. **Stream analytics** cares less about specific sequences and more about aggregates: rates, rolling averages, comparisons against last week, computed over a *window* of time. Analytics pipelines often accept approximation, using [[Bloom Filters]] for set membership, HyperLogLog for cardinality, and percentile sketches to shrink memory — an optimization, not an inherent lossiness of streaming. **Materialized view maintenance** applies a change stream to keep [[Materialized Views]] — caches, indexes, warehouses, or event-sourced application state — up to date; unlike analytics it needs *all* events since the beginning of time (modulo [[Log Compaction]]), not just a recent window. **Search on streams** stores full-text queries and runs each arriving document past them (Elasticsearch's percolator), the mirror image of indexing documents then querying. Actor frameworks look similar but are a concurrency mechanism, not a data-management technique: actor communication is ephemeral and arbitrary-topology, while stream jobs form durable, acyclic, multi-subscriber pipelines.

## Trade-offs & Pitfalls
Analytics-oriented frameworks assume bounded windows, so they fit view maintenance poorly — that needs indefinitely retained state. Probabilistic algorithms trade exactness for memory; use them knowingly. Testing every document against every stored query is O(queries), so large-scale stream search must index the queries too. Actor frameworks typically don't guarantee delivery across crashes, so they aren't fault-tolerant stream processors without added retry logic.

## Examples & Systems
CEP: Esper, IBM InfoSphere Streams, Apama, TIBCO StreamBase, SQLstream. Analytics: Apache Storm, Spark Streaming, Flink, Concord, Samza, Kafka Streams; hosted — Google Cloud Dataflow, Azure Stream Analytics. View maintenance: Samza and Kafka Streams atop [[Apache Kafka]] compaction. Storm's distributed RPC interleaves user queries with stream events.

## Related
- up: [[Processing Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Reasoning About Time]] — the windows analytics aggregates over
- [[State, Streams, and Immutability]] — why views derive from full event logs
- [[Aggregation - Data Cubes and Materialized Views]] — the warehouse-side view concept
- [[Message-Passing Dataflow]] — the actor/RPC world contrasted here
