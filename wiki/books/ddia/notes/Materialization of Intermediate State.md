---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: Beyond MapReduce
type: subtopic
tags: [ddia, dataflow-engines, spark-flink-tez, fault-tolerance]
sources:
  - raw/ch10.md
---
# Materialization of Intermediate State
> [[MapReduce]] writes every job's output to [[HDFS]] like a shell writing temp files; dataflow engines (Spark, Tez, Flink) stream data between operators like Unix pipes and recompute lost state instead of persisting it.

## The Idea
In a multi-job workflow, each job's HDFS output often exists only to feed the next job owned by the same team — it is *intermediate state*, and eagerly writing it out is called materialization (the same eager-compute idea as [[Materialized Views]]; see [[Aggregation - Data Cubes and Materialized Views]]). Publishing a dataset to a well-known HDFS location is great for loose coupling across teams, but recommendation workflows chaining 50–100 jobs mostly shuffle private temp data — and paying full durability for it is waste.

## How It Works
Materialization hurts three ways: a job can't start until *every* task of its predecessor finishes (one straggler stalls the workflow, whereas piped Unix processes run concurrently); mapper stages are often redundant re-readers of what a reducer just wrote; and temp files get replicated across nodes — overkill.

[[Dataflow]] engines — Spark, Tez, Flink, descending from research systems Dryad and Nephele — fix this by modelling a whole workflow as one job. User functions become *operators*, composable more flexibly than strict map/reduce alternation, with three connection patterns: repartition-and-sort (enables sort-merge joins as in [[Reduce-Side Joins and Grouping]]); repartition without sorting (enough for partitioned hash joins, where hashing randomizes order anyway); and broadcast, sending one operator's output to every partition of a join (see [[Map-Side Joins]]). Wins: sorting only where required; no redundant mappers; locality scheduling because dependencies are explicit; intermediate state kept in memory or local disk instead of replicated HDFS; operators start as soon as input arrives; JVM reuse instead of per-task startup. Tez is a thin library over YARN's shuffle service; Spark and Flink are full frameworks with their own transport and schedulers. Pig/Hive/Cascading workflows can switch execution engines by configuration, code unchanged.

**Fault tolerance.** Without durable intermediate files, lost state is *recomputed*: Spark tracks lineage through its resilient distributed datasets (RDDs); Flink checkpoints operator state. Recomputation requires knowing inputs and operators applied — and works cleanly only if operators are deterministic. Hash-iteration order, random numbers, and clock reads sneak nondeterminism in; otherwise downstream operators holding old data must be killed and rerun too. Fixed-seed pseudorandomness is the standard cure. When intermediate data is small or expensive to recompute, materializing it can still be the cheaper choice.

## Trade-offs & Pitfalls
- Sorting operators inherently block — they must consume all input before emitting anything — so full pipelining has limits.
- Final job output still goes to HDFS: immutable inputs, replaced outputs; the savings are purely on the *intermediate* hops.

## Examples & Systems
Spark (RDD lineage), Apache Tez, Flink (pipelined execution, checkpointing), Dryad, Nephele; FlumeJava-inspired APIs.

## Related
- up: [[Beyond MapReduce]] · chapter: [[Ch 10 - Batch Processing]]
- [[The Unix Philosophy]] — the pipes-versus-temp-files analogy made precise
- [[MapReduce Job Execution]] — the per-stage shuffle being generalized here
- [[The Output of Batch Workflows]] — durability discipline retained at workflow edges
