---
persona: vutr
kind: concept
sources:
- raw/spark/10-minutes-to-learn-apache-spark.md
- raw/spark/if-youre-learning-apache-spark-this.md
last_updated: '2026-07-11'
qc: passed
slug: sort-merge-join-vs-shuffle-hash-join
topics:
- spark
---

SMJ is the join strategy Spark reaches for today, but that wasn't always true — Shuffle Hash Join (SHJ) used to hold the crown. The correction matters because it explains why SHJ still exists as an option you have to explicitly opt into rather than the default.

Both strategies share the same first step: the [[shuffle-writes-to-disk-and-external-shuffle-service|shuffle]]. Before the join can happen, Spark ensures that rows carrying the same join key from both tables land on the same physical partition. In the physical plan this shows up as an `Exchange` operator, and Adaptive Query Execution runs `AQEShuffleRead` right after it to coalesce small partitions so the join reads efficiently.

From there the two strategies diverge.

**Sort-Merge Join** adds an explicit `Sort` operator on both branches of the join tree — once the shuffle has co-located matching keys, each partition is sorted locally. Only after both sides are partitioned identically and sorted does the merge itself happen: Spark does a linear scan through both sorted streams simultaneously, comparing the keys at each stream's current pointer. If the keys match, it produces a joined row; if the left key is smaller, the left pointer moves forward; if the right key is smaller, the right pointer moves forward. Because the data is sorted, Spark only needs to pass through each dataset once — O(n + m) complexity.

**Shuffle Hash Join** skips sorting entirely. After the shuffle, for every partition Spark identifies the smaller of the two datasets and builds an in-memory hash table from it — the join keys become the hash keys, mapping to the actual row data (the build phase). It then probes that hash table using the larger dataset: for each row, it hashes the join key and looks it up in the table; a match combines the rows (the probe phase).

The trade-off that dethroned SHJ: it requires the build side of every partition to fit entirely in memory to build the hash table. If a partition is large — say, due to skew — the executor throws an OutOfMemoryError. SMJ has no such requirement: it can safely spill to disk if a partition is too big, making processing more reliable. That's the actual reason SHJ was removed in Spark 1.6 and only reintroduced in Spark 2.0 — reintroduced because it's genuinely helpful *when* the build-side partitions are known to fit in memory, since it lets both sides skip sorting.

Because of that history, SHJ isn't the default — it has to be forced on. Two settings: set `spark.sql.join.preferSortMergeJoin` to `False`, and raise `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` (the max size in bytes per partition Spark will allow to build a hash table locally) above its default of 0 — a default that means Spark will *always* skip ShuffleHashJoin unless you touch it.

In the demonstrated project — TPC-H `lineitem` (~2.6GB) joined to `order` (~600MB) across 2 executors, each with 2 cores and 4GB RAM (application parallelism 4) — the SMJ run used `spark.sql.files.maxPartitionBytes` at 256MB. Forcing SHJ meant setting `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` to 256MB and dropping `spark.sql.files.maxPartitionBytes` to 128MB, so input partitions stayed smaller than the threshold and thus eligible to build a hash table locally. With `preferSortMergeJoin` set to False, the physical plan then showed ShuffledHashJoin.

The warning that comes with this: in a production Spark application, know what you're doing before enabling SHJ — it's only efficient when the build-side partitions fit in memory. If they get larger for some reason, the application will likely OOM.

If you hint the optimizer explicitly, when different strategy hints are specified on both sides, Spark prioritizes them in order: `BROADCAST`, then `MERGE` (sort-merge), then `SHUFFLE_HASH` (hash join). For the hash-join-type hints, Spark still chooses which table becomes the build side based on table size — and a hint is never guaranteed to be picked, since a strategy may not support all logical join types (LEFT, RIGHT, INNER, etc.).

Zooming out to the general OLAP mechanism behind both: with sort-merge join, both tables are sorted and matching rows are merged using two pointers; with hash join, one table (the optimizer prefers the smaller one) builds a hash table by hashing the join keys, and the system then loops through the remaining table, applying the same hash function to look up matches. In a distributed engine like Spark, the only real difference from a single-machine version is that the join executes on more than one machine — data from both tables is divided (usually by a hash function) and distributed to workers to perform the join locally, which is exactly the shuffle step both SMJ and SHJ depend on. See also [[broadcast-join-and-bucket-join]] for the strategies that avoid this shuffle altogether, and [[adaptive-query-execution]] for how Spark can convert a sort-merge join into a broadcast hash join at runtime when a side's statistics fall under the broadcast threshold.
