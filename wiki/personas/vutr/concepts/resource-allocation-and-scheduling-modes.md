---
persona: vutr
kind: concept
sources:
- raw/spark/i-spent-4-hours-learning-apache-spark.md
- raw/spark/if-youre-learning-apache-spark-this.md
last_updated: '2026-07-11'
qc: passed
slug: resource-allocation-and-scheduling-modes
topics:
- spark
---

People tend to lump "how Spark gets resources" and "how Spark shares resources between jobs" into one mental bucket. They're two separate mechanisms. Resource allocation decides how many executors an application *has*. Scheduling mode decides how those executors get divided *among the jobs running inside that one application*. Get this distinction wrong and you'll tune the wrong knob when jobs sit pending.

## Resource allocation: static vs. dynamic

On a physical cluster, a Spark application gets its own isolated set of executors — JVM processes that only process and store data for that application. Spark gives you two ways to allocate them.

**Static allocation** reserves a finite, user-defined maximum amount of resources for the entire lifetime of the SparkContext. Whatever you request up front is what you hold, whether you're using it or not.

**Dynamic allocation** (`spark.dynamicAllocation.enabled = True`, available since Spark 1.2) lets the application give resources back when they're idle and ask for more when demand returns. Since Spark can't know in advance whether an executor about to be removed will soon get a task, or whether a freshly added executor will sit idle, it leans on a pair of heuristics rather than a predictive model.

**Request policy**: the app requests more executors once tasks have been pending for `spark.dynamicAllocation.schedulerBacklogTimeout` seconds, then requests again every `spark.dynamicAllocation.sustainedSchedulerBacklogTimeout` seconds as long as the backlog persists. The size of each request round grows exponentially — 1 executor in round one, then 2, then 4, then 8. The reasoning is deliberately conservative on the way up: start small so you don't over-provision when a handful of executors would have been enough, but be able to ramp fast if the workload genuinely needs it.

**Remove policy** is the simpler side: an executor is removed once it has been idle for `spark.dynamicAllocation.executorIdleTime`.

## Graceful decommission: the catch dynamic allocation introduces

Under static allocation, an executor only exits once the whole application is done — so it's always safe to discard. Dynamic allocation breaks that guarantee: if the app later needs data that lived on a now-removed executor, it has to recompute it.

The fix is to make the executor "stateless" before removing it. During a shuffle, an executor normally writes its map outputs to local disk and then serves as the fetch point for other executors — so removing it mid-application would strand that shuffle data. The **external shuffle service** solves this: a long-running process on each cluster node, independent of any specific Spark application or executor. Executors fetch shuffle files from this service instead of from each other, so shuffle output produced by an executor keeps being served even after that executor is terminated. See [[shuffle-writes-to-disk-and-external-shuffle-service]] for the write-side mechanics this depends on.

Cached data doesn't get the same protection by default — when an executor is removed, its cache is gone. Users can configure cache-holding executors to never be removed. Looking forward, cache may eventually move off-heap and be managed independently of executor lifetime, mirroring how the external shuffle service already decouples shuffle data from executor lifetime — see [[executor-memory-model-and-caching]].

## Scheduling mode: FIFO vs. Fair

This is the layer that decides how *jobs within one application* share the executors that resource allocation gave it.

**FIFO** is the default: the first job gets priority on all available resources, and later jobs queue behind it. If the first job doesn't consume the whole cluster, later jobs start immediately in the leftover space; if it does consume everything, later jobs simply wait.

**Fair scheduling** (available since Spark 0.8) assigns tasks between jobs round-robin instead, so resources are shared roughly equally. A short job submitted while a long job is already running can start getting resources right away instead of queuing behind it. The model is copied from the Hadoop Fair Scheduler. It supports grouping jobs into *pools*, each configurable with:

- **Scheduling Mode** (default FIFO) — the pool's internal policy, itself either FIFO or FAIR
- **Weight** (default 1) — relative cluster share; a pool with weight 2 gets double the resources of a weight-1 pool
- **minShare** (default 0) — a guaranteed minimum (e.g., minimum CPU cores); the scheduler satisfies every active pool's minShare before distributing anything left over according to weight

Pools let you isolate workloads — e.g., guarantee a critical job's pool a resource floor regardless of what else is running — which plain FIFO or flat Fair sharing can't do on its own.
