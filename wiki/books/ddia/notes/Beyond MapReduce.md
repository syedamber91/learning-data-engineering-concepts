---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
type: topic
tags: [ddia, dataflow-engines, spark, pregel]
sources:
  - raw/ch10.md
---
# Beyond MapReduce
[[MapReduce]] earned its late-2000s hype by being robust and conceptually simple — a clear abstraction over a distributed filesystem — but simple to *understand* is not simple to *use*: writing real jobs against the raw API is laborious (you implement joins yourself), and the execution model itself performs poorly for whole classes of workloads no wrapper API can fix. This topic surveys what came next along three fronts: [[Dataflow]] engines that treat an entire workflow as one job instead of a chain of independent jobs stitched together through [[HDFS]]; specialized models for iterative graph algorithms that MapReduce's single-pass nature handles wastefully; and high-level, increasingly declarative APIs that let a query optimizer pick join strategies — pulling batch frameworks and MPP databases toward each other. Stream processing (Chapter 11) is the fourth response: another way of making batch-style computation faster.

## Subtopics
- [[Materialization of Intermediate State]] — why writing every intermediate result to HDFS hurts, and how Spark, Tez, and Flink replace it with pipelined operators plus recomputation-based fault tolerance.
- [[Graphs and Iterative Processing]] — "repeat until converged" algorithms like PageRank, and the Pregel/BSP vertex-message model that makes them tractable.
- [[High-Level APIs and Languages]] — Hive, Pig, Cascading, Crunch and dataflow APIs; declarative touches, cost-based optimizers, and convergence with MPP databases.

## Key Takeaways
- MapReduce's chief costs: mandatory sort between every map and reduce, redundant mapper stages, stragglers blocking whole downstream jobs, and triple-replicating temp data.
- Dataflow engines generalize map/reduce into freely composable *operators* and only sort where needed — often orders of magnitude faster, with Pig/Hive/Cascading code portable across engines via a config switch.
- Losing durable intermediate state means fault tolerance shifts to recomputation from lineage (Spark's RDDs) or checkpoints (Flink) — and recomputation demands deterministic operators.
- Graph iteration needs vertex state that survives across rounds; Pregel provides it via fault-tolerant message passing between vertices.
- As batch engines add declarative optimization and MPP databases add arbitrary-code flexibility, both end up as "systems for storing and processing data."

## Related
- [[Ch 10 - Batch Processing]] — parent chapter MOC
- [[MapReduce and Distributed Filesystems]] — the baseline these systems improve on
- [[Batch Processing with Unix Tools]] — dataflow engines are the return of Unix pipes
- [[Processing Streams]] — the stream-processing continuation of this arc
