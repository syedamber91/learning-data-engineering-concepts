---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-fastest-way-to-learn-spark-is.md
- raw/spark/10-minutes-to-learn-apache-spark.md
- raw/spark/how-is-databricks-spark-different.md
last_updated: '2026-07-11'
qc: passed
slug: adaptive-query-execution
topics:
- spark
---

The common assumption is that Spark's [[catalyst-optimizer-phases|Catalyst optimizer]] picks the final physical plan once, before execution starts, using stored table statistics — row count, cardinality, max/min values. That's wrong for anything running Spark 3.0 or later. The cost model those statistics feed is frequently working off numbers that are outdated or simply unavailable, and Spark 3 (released 2020) introduced Adaptive Query Execution (AQE) specifically to fix that: AQE lets query plans get adjusted mid-flight, based on runtime statistics collected during execution, instead of trusting the pre-run estimate all the way through.

The mechanism rides on a structural fact about [[jobs-stages-tasks-dag-and-dependencies|stage boundaries]]: when a stage finishes, its executors materialize that stage's intermediate results, and the next stage cannot begin until the previous one is fully complete. That forced pause is the reoptimization window — once every partition has written its output, Spark has exact statistics for the data, not estimates, and AQE re-plans what comes next using those real numbers.

Three concrete things AQE does at that boundary, all grounded in the same hands-on runs:

**Coalescing shuffle partitions.** Shuffle partitions default to 200 (`spark.sql.shuffle.partitions`). In the 20GB TPC-H aggregation project, the Exchange step hash-partitioned the data into that default 200 — but AQE looked at the actual post-shuffle partition sizes, decided 200 was unnecessary, and coalesced them down to a single partition before the reduce-side aggregation ran. The physical plan shows this directly as a `ShuffleQueryStage` feeding an `AQEShuffleRead` operator. The join project shows the identical pattern: `AQEShuffleRead` nodes (steps 6 and 13 in that plan) coalesce small post-shuffle partitions before the sort-merge join executes, so the join doesn't do wasted work against tiny partitions.

**Splitting oversized partitions** — the mirror case, done to keep one overloaded task from stalling a single worker.

**Switching join strategy at runtime**, which is the case worth being precise about because pre-AQE Spark had a real, documented limitation here. Before Spark 3.0, the optimizer defaulted to [[sort-merge-join-vs-shuffle-hash-join|sort-merge join]] over shuffle hash join even for a small table, because it couldn't guarantee the smaller side would fit in memory once partitioned — shuffle hash join has to build its hash table in memory and OOMs if a partition is larger than expected (e.g. from skew), while sort-merge join can safely spill to disk instead. AQE removes the guesswork: it waits for real, post-shuffle partition sizes, and only then decides. If a join side comes in under `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` — which defaults to 0, meaning Spark will *always* skip shuffle hash join unless you raise it — Spark converts the join to shuffle hash join. The join hands-on project sets that threshold to 256MB and `spark.sql.join.preferSortMergeJoin` to False to actually exercise this path. The same runtime logic applies to [[broadcast-join-and-bucket-join|broadcast join]]: if a join side's true size drops under `spark.sql.autoBroadcastJoinThreshold` (default 10MB) only after filtering or aggregation — something the static, pre-run plan had no way to know — AQE can convert a sort-merge join into a broadcast hash join mid-query.

The trade-off worth naming plainly: AQE isn't free re-optimization. It's re-optimization purchased with a barrier Spark already pays for — the materialization pause between stages connected by a shuffle. It doesn't reoptimize anything within a stage, and it doesn't shrink the requirement that a stage fully complete before its statistics can be trusted. What it does is spend that existing pause on something Spark wasn't doing before: building the next part of the plan from real numbers instead of Catalyst's stale or missing ones.
