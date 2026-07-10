---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-overview-of-apache-spark.md
- raw/spark/why-apache-spark-rdd-is-immutable.md
last_updated: '2026-07-11'
qc: passed
slug: rdd-fundamentals-and-properties
topics:
- spark
---

People new to Spark tend to treat the RDD (Resilient Distributed Dataset) as an implementation detail they can skip past on the way to DataFrames. That's backwards. No matter which abstraction you use -- Dataset or DataFrame -- it gets compiled into RDDs behind the scenes, so the mechanism actually running your job is this one.

An RDD represents an immutable, partitioned collection of records that can be operated on in parallel. Data inside it is kept in memory for as long and as much as possible -- that's the whole point of Spark existing: [[spark-origin-and-mapreduce-limitations|MapReduce leaned on disk to exchange intermediate data between tasks]] for fault tolerance, which was fine for durability but slow for anything iterative (machine learning passes, interactive queries). Spark's answer was an in-memory data-sharing engine built on a functional-programming API, and RDD is the abstraction that engine is built around.

**The five properties, mechanically.** Every RDD carries exactly five things, and each one earns its place:

- **List of partitions** -- the RDD's data is chunked into partitions, which are Spark's actual unit of parallelism. Each partition is a logical subset of the data and can be processed independently by a different executor.
- **A computation function** -- determines how to compute the data for each partition. This is the "how do I produce this partition's rows" logic.
- **Dependencies** -- the RDD tracks which other RDDs it was derived from, i.e. how it was created. This is what makes lineage possible (more below).
- **A partitioner (optional)** -- for key-value RDDs, specifies how data is partitioned, e.g. a hash partitioner.
- **Preferred locations (optional)** -- lists where each partition is best computed, such as the data block locations in HDFS.

Note what's *not* on that list: nothing here says "here is my data, mutate it." The RDD is a description of how to produce data, not a container you write into.

**Why immutable -- the actual mechanism, not just a design preference.** Three things fall out of immutability directly:

1. *Concurrent processing without synchronization.* In a distributed environment, multiple nodes and threads may touch the same data. If that data can't change, there's nothing to race over -- no locks, no complex synchronization needed to keep it consistent.
2. *Lineage and fault tolerance.* Because a transformation never modifies an RDD in place -- it produces a brand-new RDD -- the chain of "which RDD came from which, via which transformation" (the dependencies property above) stays intact and deterministic. If a partition is lost to a node failure, Spark reconstructs it by walking the lineage graph and reapplying the recorded transformations to the original data. Mutable RDDs would break this: you couldn't deterministically regenerate a prior state if it had been overwritten. This is precisely why Spark can skip replicating data across nodes or writing it to disk the way MapReduce did -- lineage-based recomputation replaces both.
3. *Functional programming discipline.* RDDs follow functional-programming principles that treat immutability as a first-class constraint, which is what makes the failure-handling and integrity guarantees above hold in the first place.

**Laziness is the other half of the mechanism, and it depends on immutability.** When you define an RDD, its data isn't computed or made available immediately -- nothing runs until an action triggers execution. Transformations like `map` or `filter` only *describe* how data should change; because the RDD is immutable, applying a transformation can't mutate the source, so Spark creates a new RDD representing the result instead of executing anything yet. Actions are what actually drive computation and produce output or stored data. The payoff of deferring execution this way is that Spark gets to look at the whole chain of transformations before running any of them and pick the most efficient way to execute it, rather than being forced to execute each step the moment it's declared.

Put together: partitions give you the unit of parallel work, dependencies give you a lineage graph instead of replication, and immutability is what makes that lineage graph trustworthy enough to recompute from after a failure -- three properties from the same list, one mechanism.
