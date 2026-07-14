---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, batch-processing]
sources:
  - raw/ch02.md
  - raw/ch10.md
---
# MapReduce

A batch programming model: a mapper turns each input record into key-value pairs;
the framework shuffles (sorts and groups by key); a reducer processes each key's
values together. Simple retry-based fault tolerance (rerun failed tasks) because
inputs are immutable and outputs are written once.

Book home ground: [[MapReduce and Distributed Filesystems]] (Ch 10) with joins in
[[Reduce-Side Joins and Grouping]] and [[Map-Side Joins]]; critiqued and superseded
by dataflow engines in [[Beyond MapReduce]]. Appears early as a query pattern in
[[MapReduce Querying]] (Ch 2). Runs on [[Hadoop]]/[[HDFS]].

## Referenced In
- [[Batch Processing with Unix Tools]]
- [[Batch and Stream Processing]]
- [[Beyond MapReduce]]
- [[Ch 02 - Data Models and Query Languages]]
- [[Ch 10 - Batch Processing]]
- [[Cloud Computing and Supercomputing]]
- [[Comparing Hadoop to Distributed Databases]]
- [[Home]]
- [[Fault Tolerance]]
- [[Graphs and Iterative Processing]]
- [[High-Level APIs and Languages]]
- [[Map-Side Joins]]
- [[MapReduce Job Execution]]
- [[MapReduce Querying]]
- [[MapReduce and Distributed Filesystems]]
- [[Materialization of Intermediate State]]
- [[Part III - Derived Data]]
- [[Processing Streams]]
- [[Query Languages for Data]]
- [[Reduce-Side Joins and Grouping]]
- [[Simple Log Analysis]]
- [[The Output of Batch Workflows]]
- [[The Unix Philosophy]]
