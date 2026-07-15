---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
type: chapter-moc
tags: [ddia, batch-processing, mapreduce, dataflow-engines]
sources:
  - raw/ch10.md
---
# Ch 10 – Batch Processing
Part III's opening chapter leaves request/response behind: batch systems consume a large *bounded* input, run for minutes to days, and are judged on throughput, with output *derived* from immutable input (see [[Derived Data]]). The arc runs from a Unix one-liner over web logs, through [[MapReduce]] on [[HDFS]] — job execution, the join-algorithm toolbox, what batch workflows actually produce, and how [[Hadoop]] differs from MPP databases — to the post-MapReduce world of [[Dataflow]] engines (Spark, Tez, Flink), Pregel-style graph processing, and declarative high-level APIs.

## Map
- [[Batch Processing with Unix Tools]]
  - [[Simple Log Analysis]] — a five-command pipeline versus a custom script; sorting versus in-memory aggregation
  - [[The Unix Philosophy]] — one thing well, uniform interfaces, logic/wiring separation, immutable inputs
- [[MapReduce and Distributed Filesystems]]
  - [[MapReduce Job Execution]] — mappers, reducers, the shuffle, and workflows chained through HDFS directories
  - [[Reduce-Side Joins and Grouping]] — sort-merge joins, GROUP BY, sessionization, and handling skewed hot keys
  - [[Map-Side Joins]] — broadcast hash, partitioned hash, and merge joins when input layout permits
  - [[The Output of Batch Workflows]] — search indexes, bulk-built key-value stores, and the immutability philosophy
  - [[Comparing Hadoop to Distributed Databases]] — storage freedom, processing-model diversity, fault-handling design
- [[Beyond MapReduce]]
  - [[Materialization of Intermediate State]] — dataflow engines replace HDFS temp files with pipelined operators and recomputation
  - [[Graphs and Iterative Processing]] — the Pregel/BSP model for iterate-until-converged algorithms
  - [[High-Level APIs and Languages]] — Hive/Pig-style APIs, cost-based optimizers, convergence with MPP databases

## Chapter Summary
Unix design principles — immutable inputs, output destined to feed some unknown next program, small tools composed to solve big problems — carry straight into batch processing; the uniform interface just changes from pipes and files to a distributed filesystem. Distributed batch frameworks must solve two core problems. *Partitioning:* MapReduce ties map tasks to input blocks, then repartitions, sorts, and merges into reducer partitions so related records land together; later engines keep the approach but skip sorting where possible. *Fault tolerance:* MapReduce buys cheap task-level retry with constant disk writes; dataflow engines materialize less, keep more in memory, and recompute lost data from lineage — with deterministic operators shrinking how much must be recomputed. Three join algorithms recur (and reappear inside MPP databases and dataflow engines alike): sort-merge joins, broadcast hash joins, and partitioned hash joins. The programming model is deliberately restricted — stateless callbacks, no side effects beyond declared output — letting the framework hide crashes, retries, and network failures behind a guarantee that output looks as if nothing failed: far stronger semantics than online systems enjoy. The defining trait of batch is *bounded* input of known size, so jobs finish; Chapter 11 asks what changes when input never ends.

## Related
- [[Part III - Derived Data]] — parent part MOC
- [[Home]] — book index
- prev: [[Ch 09 - Consistency and Consensus]]
- next: [[Ch 11 - Stream Processing]]
