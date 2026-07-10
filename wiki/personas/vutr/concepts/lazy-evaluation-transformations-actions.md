---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-overview-of-apache-spark.md
last_updated: '2026-07-11'
qc: passed
slug: lazy-evaluation-transformations-actions
topics:
- spark
---

The common mental model — that a chain of `.map()`/`.filter()` calls runs line by line as you write it — is wrong. When you define an RDD (and everything above it, since DataFrames and Datasets compile down to RDDs behind the scenes), its data is not available or transformed immediately. Nothing computes until an **action** triggers execution. This is Spark's lazy evaluation, and it is not a side detail — it is the mechanism that makes the rest of [[rdd-fundamentals-and-properties]] (immutability, lineage-based fault tolerance) actually work.

**What a transformation does, mechanically.** Operations like `map` or `filter` are transformations: they define how data should be transformed but don't execute. Because an RDD is immutable, Spark never modifies the RDD you call a transformation on — it creates a *new* RDD that represents the result. That new RDD carries a computation function (how to compute each partition) and a dependency link back to the RDD it came from. Chain ten transformations and you haven't touched any data; you've built a chain of RDD objects, each one pointing at its parent and describing how it would be computed if asked. This chain of dependencies is what Spark uses to build the DAG (Directed Acyclic Graph) of stages for a job, scheduled in topological order.

**Two shapes of dependency matter here.** A transformation like `map` or `coalesce` has a narrow dependency — each partition in the child RDD depends on only a single parent partition (or a known subset). A transformation like `groupByKey`, `reduceByKey`, or `join` has a wide dependency — a single parent partition can contribute to multiple child partitions, which requires shuffling data across the cluster. Wide dependencies are exactly where stage boundaries appear: a stage is a job segment that executes without shuffling, so the DAG splits into a new stage whenever a wide-dependency transformation shows up. This is a direct consequence of laziness — Spark can only draw stage boundaries because it has the *entire* dependency chain in front of it before running anything, rather than being told to run each step in isolation the way MapReduce made you launch each Map/Reduce pass as its own job.

**What an action does.** Actions are the commands Spark actually runs to produce output or store data — they are what drives execution of everything upstream. Only at that point does the driver formulate an execution plan (starting from the logical plan, refined into a physical plan) and start scheduling tasks on executors. Caching follows the same rule: `cache()`/`persist()` is lazy too — the data isn't stored until an action triggers the computation, so calling `.cache()` alone materializes nothing.

**Why build it this way at all — the payoff isn't just "efficiency."** The sources tie laziness directly to two things. First, it "allows Spark to determine the most efficient way to execute the transformations" — having the whole chain up front, rather than one imperative step at a time, is what makes later optimization possible. Second, and more load-bearing: laziness is what fault tolerance through lineage depends on. Because nothing computes until an action, Spark only has to remember the *series of transformations* that produced an RDD — its lineage — not the RDD's materialized output. If a partition is lost to a node failure, Spark reconstructs it by reapplying the transformations described in the lineage to the original data, rather than replicating data across nodes or writing intermediate state to disk the way MapReduce relied on disk-based exchange between Map and Reduce tasks for fault tolerance. Lazy evaluation is the precondition for that trade: it's the reason Spark can skip disk replication and still recover cleanly.

Where this shows up further downstream: the DAG that laziness builds is what [[jobs-stages-tasks-dag-and-dependencies]] schedules stage-by-stage, and the pause between stages (execution can't start on a stage until the prior one's results are materialized) is also what gives [[adaptive-query-execution]] a checkpoint to re-optimize using runtime statistics that weren't available when the logical plan was first analyzed by [[catalyst-optimizer-phases]].
