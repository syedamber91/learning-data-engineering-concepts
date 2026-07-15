---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-8-hours-learning-about-the.md
last_updated: '2026-07-15'
qc: passed
slug: spark-scheduler-oom-nondeterminism-and-skew-diagnostics
topics:
- spark
---

[[data-skew-and-oom|Skew causing OOM]] explains the memory-side half of the failure — why a hash-based join or aggregation dies once one partition outgrows the executor's memory budget. What it doesn't explain is why the exact same job, on the exact same data, can pass on Monday and fail on Thursday. That non-determinism has a scheduler-level cause, separate from the memory math.

Spark's task scheduler is built to maximize resource utilization, not to protect against uneven task cost: when a set of tasks is ready to run, it looks at the executor's open slots (cores) and fills them as fast as it can, with no visibility into any given partition's actual size. Take a concrete case — two executors, 4 cores each, 8GB memory each, so 8 tasks can run concurrently across the cluster. If one of those tasks happens to carry a skewed partition needing 5GB while the other three sharing its executor need 2GB each, the scheduler still starts all four together, because from its point of view they're just four ready tasks and four open slots. The pool fills, the heavy task keeps asking for memory, the pool runs out, and the task fails, then the executor.

The reason this becomes *non*-deterministic rather than a reliable, reproducible failure is arithmetic, not randomness: if the stage's total task count doesn't divide evenly by the cluster's total concurrent-task capacity (e.g. 19 or 20 tasks against 8 slots), the tail end of the stage runs with only 3 or 4 tasks in flight per executor instead of a full 4. If the skewed task happens to land in that under-full tail — alone, or paired with only one normal task — the executor has enough headroom (all 8GB, or 7 of 8GB) to absorb it without ever hitting the OOM ceiling. Whether the skewed task lands in a full batch or the thinner tail batch is a function of scheduling order, which is not guaranteed to repeat run to run. That's the actual mechanism behind "passed Monday, failed Thursday" — not a change in data volume, but a different task-to-slot assignment sequence.

This same non-determinism is why Spark's retry mechanism (`spark.task.maxFailures`, default 4) can look like it "fixes itself" on a rerun without anyone changing anything: a failed task gets reset to pending and re-scheduled, and if it happens to be re-run later in the stage — when fewer other tasks remain and it gets an under-full batch instead of a full one — it can simply succeed where it failed the first time, for the identical partition and identical data.

**Diagnosing which failure mode you actually have.** The Spark UI's Stages tab, once a stage has failed, gives two distinguishable signatures. If *all* tasks in the stage are FAILED, the partition size itself is too big for any task, regardless of scheduling luck — this points at reducing partition size or raising executor memory generally, not at skew specifically. If only *some* tasks failed and their Input Size / Shuffle Read is disproportionately larger than the surviving tasks' (the source's example: one task reporting 4GB against others at 500MB), that's the skew signature specifically. The task list's other columns matter for narrowing further: Shuffle Read/Write show data moved into/out of a task; Spill (Memory) and Spill (Disk) track the same spilled bytes before and after compression (disk figure is normally smaller); and Duration flags stragglers even before a failure occurs, since a skewed task typically also runs far longer than its peers before it ever OOMs.

**AQE's skew-join threshold, made precise.** [[data-skew-and-oom]] and [[adaptive-query-execution]] both note that AQE splits oversized partitions but flag the actual detection threshold as an unspecified gap in the sources available at the time. This source closes that gap: AQE's `spark.sql.adaptive.skewJoin.enabled` feature requires *both* of two conditions to mark a partition as skewed before it acts — `spark.sql.adaptive.skewJoin.skewedPartitionFactor` (default 5, meaning a partition must be at least 5x the median partition size) and `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes` (default 256MB, an absolute floor so a small partition that's merely 5x an even-smaller median doesn't get needlessly split). Only when a partition clears both the relative and the absolute bar does AQE split it. If AQE's skew-join handling still isn't enough — the source says it usually is — "salting" the join key is the manual fallback: append a random suffix to the dominant key to spread its rows across multiple synthetic partitions, join, then strip the suffix afterward.

*See also: [[data-skew-and-oom]] · [[adaptive-query-execution]] · [[sort-merge-join-vs-shuffle-hash-join]] · [[executor-memory-model-and-caching]]*
