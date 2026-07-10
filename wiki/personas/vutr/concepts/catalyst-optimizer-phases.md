---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/how-is-databricks-spark-different.md
- raw/spark/a-closer-look-into-databrickss-photon.md
- raw/spark/i-spent-6-hours-learning-pyspark.md
last_updated: '2026-07-11'
qc: passed
slug: catalyst-optimizer-phases
topics:
- spark
---

Most people describe Catalyst as "the thing that optimizes your Spark SQL query," which undersells what's actually happening: it's a four-phase pipeline that turns a logical description of intent into JVM bytecode, and each phase has a different job and a different failure mode when it's under-informed.

Phase 1, analysis, isn't optimization at all — it's validation. The optimizer walks the unresolved logical plan and uses the Catalog object (Spark's interface to table/database/function metadata) to answer two questions: does this column or table actually exist, and what's its type? The Catalog can list, retrieve, and refresh metadata so Spark's view stays in sync with the underlying source. If analysis can't resolve a name, nothing downstream runs.

Phase 2, logical optimization, is where the classic rule-based transformations happen: predicate pushdown, projection pruning, null propagation, and similar heuristics. This is rule-based optimization (RBO) — Catalyst applies predefined rules and heuristics without needing to know anything about the actual data. The rules themselves aren't a monolith: Databricks describes a Catalyst rule as "a list of pattern-matching statements and corresponding substitutions applied to a query plan" — which matters beyond query optimization, because Photon reuses this exact rule mechanism to convert plan nodes it can execute natively into Photon operators, inserting a transition node wherever it hits an operator Photon doesn't support ([[photon-vectorized-engine]]).

Phase 3, physical planning, is where the optimizer stops being purely rule-based. Based on the logical plan, it generates one or more candidate physical plans and picks the final one using a cost model — this is cost-based optimization (CBO), which leans on statistics like row count, cardinality, and max/min values to estimate which plan is cheapest. Correction worth making explicit: RBO and CBO aren't alternative optimizers you choose between — Catalyst runs RBO during logical optimization and CBO at the end of physical planning, as two different phases of the same pipeline.

Phase 4, code generation, is the last step — it takes the chosen physical plan and generates actual Java bytecode for execution on the executors.

The physical-planning phase is where Catalyst's design has a known weak point: the cost model is only as good as the statistics feeding it. What happens when those statistics are outdated or missing? Spark 3, released in 2020, answered this with Adaptive Query Execution ([[adaptive-query-execution]]): because each stage boundary forces executors to materialize intermediate results before the next stage can start (jobs are split into stages at shuffle boundaries — see [[jobs-stages-tasks-dag-and-dependencies]]), that pause is a free re-optimization checkpoint. AQE uses the real runtime statistics collected at that point to combine small partitions into bigger ones, split oversized partitions, or switch join strategies — most visibly, converting a sort-merge join to a broadcast hash join ([[broadcast-join-and-bucket-join]], [[sort-merge-join-vs-shuffle-hash-join]]) once a join side turns out to be under the `spark.sql.autoBroadcastJoinThreshold` (default 10MB) after the real partitioned size is known — a call the static plan couldn't safely make up front.

One place Catalyst's machinery doesn't reach: Python UDFs. Because a UDF is an opaque function to the optimizer, code wrapped in `udf()` skips both Catalyst's plan rewriting and Tungsten's binary-object handling — the optimizer can't push predicates through it, prune it, or factor it into the cost model, and execution falls back to row-at-a-time processing in a separate Python process ([[python-udf-overhead-and-arrow-optimization]]). That's the real cost of a UDF: not just the serialization overhead of crossing the JVM/Python boundary, but opting out of the four-phase pipeline entirely.
