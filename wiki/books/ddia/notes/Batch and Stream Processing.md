---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Data Integration
type: subtopic
tags: [ddia, lambda-architecture, stream-processing, reprocessing]
sources:
  - raw/ch12.md
---
# Batch and Stream Processing

> Batch and stream processors are the engines of data integration; their convergence lets one system both reprocess history and react to fresh events.

## The Idea
Kleppmann defines integration's goal as getting data into the right form in all the right places, and batch/stream processors are how: they consume, transform, join, filter, and aggregate inputs into derived outputs (indexes, [[Materialized Views]], recommendations, metrics). The deep difference between the two paradigms is only bounded versus unbounded input — and even that is blurring: Spark runs streams as microbatches on a batch engine, while Flink runs batch jobs on a streaming core.

## How It Works
- **Functional flavor**: batch jobs encourage deterministic, pure derivation functions over immutable inputs with append-only outputs; stream processing adds managed, fault-tolerant state. Determinism aids both fault recovery and human reasoning about org-wide [[Dataflow]].
- **Asynchrony as robustness**: derived systems *could* update synchronously (like a database index inside a transaction), but async event logs contain faults locally, whereas distributed transactions amplify a single participant's failure. Cross-partition [[Secondary Indexes]] are likewise most reliable maintained asynchronously.
- **Reprocessing for evolution**: streams keep views fresh with low delay; batch reprocessing lets you restructure an entire dataset into a new model — far beyond the additive tweaks [[Schema Evolution]] normally permits. Kleppmann's railway analogy: converting track gauge by temporarily running dual gauge, so old and new coexist and every migration stage is reversible. Derived views enable exactly this gradual, testable, low-risk migration.
- **Lambda architecture**: record immutable events; run a stream processor for fast approximate views and a batch processor ([[Hadoop]] [[MapReduce]]) over the same events for corrected, exact views.
- **Unification instead**: one engine gains both abilities via (1) replaying history through the same code (log replay from a [[Log-Based Message Broker]] or [[HDFS]]), (2) [[Exactly-Once Semantics]] that discard partial failed output, and (3) event-time (not processing-time) windowing.

## Trade-offs & Pitfalls
- Lambda's costs: the same logic maintained in two frameworks; merging two outputs is hard once views involve joins or sessionization; frequent full reprocessing is expensive, and incrementalizing the batch layer reintroduces stragglers and window-boundary problems — recreating the complexity lambda meant to avoid.
- Microbatch stream emulation can perform poorly on hopping/sliding windows; emulation in either direction has performance caveats.

## Examples & Systems
Spark (microbatches), Apache Flink (stream-first batch), Storm (lambda's speed layer), Summingbird (dual-target abstraction), Apache Beam with Flink or Google Cloud Dataflow (event-time API), 19th-century English railway gauge standardization, BART's nonstandard gauge as the lingering cost.

## Related
- up: [[Data Integration]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Reasoning About Time]] — event-time vs processing-time windowing
- [[Fault Tolerance]] — exactly-once machinery in stream processors
- [[The Output of Batch Workflows]] — what derived outputs look like
- [[State, Streams, and Immutability]] — immutable event logs underlying lambda

## Related in the other wiki
- [[lambda-architecture]] — vutr's sharper verdict that Lambda "does not actually solve completeness — it just papers over the gap," complementing this note's account of lambda's dual-codebase costs.
- [[kappa-architecture]] — vutr's name for the "unification instead" alternative this note describes: replaying history through one stream-processing codebase via log replay.
- [[lambda-vs-kappa]] — vutr's production case studies (Uber/LinkedIn kept Lambda, Twitter pivoted to Kappa) showing how real teams resolved the trade-off this note lays out.
