---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-8-hours-learning-apache-spark.md
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-overview-of-apache-spark.md
- raw/spark/is-this-feature-a-revolution-in-spark.md
last_updated: '2026-07-11'
qc: passed
slug: jobs-stages-tasks-dag-and-dependencies
topics:
- spark
---

People tend to flatten "job," "stage," and "task" into one fuzzy idea of "the Spark thing that runs." They're a strict hierarchy, and the boundary between them is not vague — it's decided by exactly one thing: whether a transformation needs to shuffle data across partitions.

**Job.** A job is a series of transformations applied to data, encompassing the entire workflow from start to finish. It's only triggered by an action such as `count()`, `collect()`, or `show()` — nothing runs before that. A single Spark application can, and usually does, contain more than one job.

**Stage.** A stage is a job segment executed *without* data shuffling. Spark splits a job into stages precisely when a transformation requires shuffling data across partitions. To know when that happens, you need the distinction between narrow and wide dependencies:

- **Narrow dependencies** — each partition in the child RDD depends on a limited, knowable set of parent partitions (a single parent for `map`, a known subset for `coalesce`). No shuffle is needed, so narrow-dependency operations are pipelined together into one set of tasks within a single stage.
- **Wide dependencies** — a single parent partition contributes to *multiple* child partitions. This is what `groupByKey`, `reduceByKey`, and `join` do, and it forces data to be repartitioned across the cluster. Wide dependencies are exactly where stage boundaries get drawn in Spark's execution plan.

Stages come in two flavors: **ResultStages** (the final stage of a job) and **ShuffleMapStages** (intermediate stages that perform the actual shuffle write). See [[shuffle-writes-to-disk-and-external-shuffle-service]] for what happens physically during that boundary.

**Task.** The smallest unit of execution. Each stage is divided into multiple tasks that run the same code in parallel, one per data partition, executed by individual executors.

**DAG.** The DAGScheduler builds a Directed Acyclic Graph of stages from RDD dependencies, and this DAG is what guarantees stages run in topological order — a stage isn't submitted until every stage it depends on has finished.

Mechanically, here's the walk: the DAGScheduler traverses the RDD lineage backward, starting from the final RDD (the one the action was called on) all the way back to the source RDD, building the DAG of stages based on where shuffle boundaries fall. Once a stage's turn comes up in topological order, the DAGScheduler creates a **TaskSet** for it — the set of fully independent, not-yet-computed tasks belonging to that stage — and hands it off to the TaskScheduler. Alongside the TaskSet, the DAGScheduler also computes *preferred locations* for each task, based on current cache status and the underlying RDDs' preferred locations (e.g. HDFS block locations), so the TaskScheduler can try to schedule tasks close to their data. That location-aware assignment is where [[data-locality-and-speculative-execution]] picks up.

Failure handling is split by cause, and this is a distinction worth holding onto rather than treating "task failed" as one bucket: if a stage fails because of **lost shuffle output files**, the DAGScheduler is responsible, and it may need to resubmit the earlier (producing) stages. If a stage fails for any *other* reason, that's the TaskScheduler's problem — it retries the individual task a limited number of times before giving up and canceling the whole stage.

The job is considered complete only when every stage in its DAG has finished, processed strictly in DAG order. Nothing about "job," "stage," or "task" here is arbitrary naming — it's the direct output of walking RDD lineage and marking wide-dependency boundaries. If you understand [[lazy-evaluation-transformations-actions]] (why nothing computes until an action fires) and [[rdd-fundamentals-and-properties]] (why lineage exists at all), the job → stage → task → DAG breakdown is just that lineage graph, cut at its shuffle points and handed to executors one topologically-ordered stage at a time.

## Related in the other wiki
- [[Beyond MapReduce]] — DDIA's claim that dataflow engines "generalize map/reduce into freely composable operators and only sort where needed" is the high-level description of exactly this job → stage → task → DAG breakdown at shuffle boundaries.
