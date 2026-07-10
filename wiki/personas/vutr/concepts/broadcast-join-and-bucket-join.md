---
persona: vutr
kind: concept
sources:
- raw/spark/10-minutes-to-learn-apache-spark.md
- raw/spark/if-youre-learning-apache-spark-this.md
last_updated: '2026-07-11'
qc: passed
slug: broadcast-join-and-bucket-join
topics:
- spark
---

A common mental slip is treating broadcast join as its own algorithm, separate from [[sort-merge-join-vs-shuffle-hash-join]]. It isn't -- it's an optimization layered on top of hash join. Suppose one of the two tables is small enough to fit entirely into memory. Instead of shuffling both sides across the cluster so matching keys land on the same partition, Spark sends that whole small table to every executor. Each executor then builds its own in-memory hash table from the broadcast copy and probes it locally against its slice of the large table. Because only the small "build" table moves over the network -- not both tables -- there is no `Exchange` (shuffle) step in the physical plan at all before the join node.

Whether this kicks in is governed by `spark.sql.autoBroadcastJoinThreshold`, 10MB by default, and it's on by default: if one table's size is under that threshold, Spark broadcasts it automatically. In the walkthrough project, generating a much smaller `order` table (~60MB) and raising the threshold to 65MB was enough to flip the physical plan from sort-merge to broadcast -- the resulting plan showed the entire `order` table broadcast and no `Exchange` steps before the join, and the application finished noticeably faster.

The correction that matters here for [[adaptive-query-execution]]: before Spark 3.0, if a table didn't clear the broadcast threshold, Spark defaulted to sort-merge join rather than shuffle hash join, because building a hash table per partition risked running out of memory. AQE (Spark 3.0+) changes this at runtime -- once shuffle materializes real partition sizes, the optimizer can convert a sort-merge join into a broadcast hash join if a side turns out to be small enough after partitioning, or switch to shuffle hash join generally now that it has actual statistics instead of stale ones.

## Bucket join

The second misconception: that a bucket join removes shuffle from the pipeline. It doesn't remove it -- it relocates it. Every join still needs matching keys co-located on the same partition; a bucket join just does that co-location once, at write time, instead of once per join. Bucketing hashes a column's values into a fixed number of buckets and physically organizes the data that way when it's written. If both tables being joined are already bucketed by the join key, Spark can skip the shuffle phase entirely at join time, because the data was effectively pre-shuffled when it landed on disk. The cost shows up earlier instead: writing bucketed tables takes longer, since the engine has to do the extra work of organizing rows into buckets.

Mechanically, `bucketBy()` only works with `saveAsTable()`, not `write.parquet()`, and this isn't arbitrary -- bucketing metadata (which column, how many buckets) has to be persisted somewhere so a later job can recognize the tables are compatible for a bucket join. That "somewhere" is the Hive metastore: the write path needs `enableHiveSupport` (a local Derby DB by default) and `spark.sql.warehouse.dir` to tell Spark where to physically store the table files. `saveAsTable("orders_bucketed")` both writes the data and registers the bucketing info in the metastore in one step. On the join side, reading the two bucketed tables back and joining on the bucketed key produces a plan with no `Exchange` steps before the join -- and if the query also aggregates on that same key, the aggregation skips its own shuffle too, since the data was already partitioned correctly at write time.

Neither optimization is free, and neither is a substitute for the other: broadcast join trades network cost for a memory constraint on the small side (still bounded by `spark.sql.autoBroadcastJoinThreshold`), while bucket join trades a one-time shuffle cost at write time for repeated joins that never shuffle again -- useful specifically when you know the join pattern in advance. On the hint side, users can nudge the optimizer toward `BROADCAST`, `MERGE`, or `SHUFFLE_HASH` (only `BROADCAST` was available before Spark 3.0), but a hint is a request, not a guarantee -- the optimizer still decides, and a strategy may not even support the logical join type in play (LEFT, RIGHT, INNER, etc.).
