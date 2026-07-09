---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk
last_updated: '2026-07-09'
qc: passed
slug: 007-shuffle-writes-to-disk
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk
mastery: mastered
---

*What Alex understood:* So the shuffle is Spark's step for regrouping data by key across the cluster — and here's the trap: even though Spark is sold as 'in-memory,' the shuffle actually WRITES to disk, because the map side has to dump its intermediate results somewhere durable for the reduce side to fetch. On top of that, Spark always cuts the shuffled data into 200 partitions by default no matter how big the data is, so you have to tune spark.sql.shuffle.partitions to fit your actual size. And reduceByKey beats groupByKey because it shrinks the data on each node BEFORE the shuffle, so there's less to write to disk and less to send over the wire — groupByKey shuffles everything raw and only combines afterward.

## Follow-up questions

**Alex:** If the shuffle already writes to disk, does that mean Spark isn't really 'in-memory' at all — or is the in-memory part happening somewhere else in the job?

**vutr:** Great instinct, and the source lets me answer half of it precisely. Spark IS genuinely in-memory for the parts it can keep in RAM: the source describes an executor's 'unified' memory (spark.memory.fraction default 0.6) split between execution and storage, and it says the whole reason Spark was built in 2009 was that MapReduce was too slow for iterative ML — Spark keeps working data in memory across steps instead of hitting disk every iteration. So computation, caching, and the hash tables for joins live in memory. The shuffle is the specific exception: the intermediate data that must survive being handed from map tasks to reduce tasks gets written to disk. Notice the source even contrasts join strategies on exactly this point — 'SMJ can safely spill to disk; SHJ cannot' — which confirms that spilling-to-disk is a normal, deliberate part of how Spark survives big shuffles, not a failure. So: in-memory for compute, disk for the shuffle handoff. Both are true at once.

**Alex:** You said default 200 partitions is bad for both tiny and huge data — is there a newer Spark feature that fixes the wrong number automatically so I don't have to guess?

**vutr:** Yes — and the source names it exactly: AQE, Adaptive Query Execution, introduced in Spark 3.0 in 2020. The source says AQE 'dynamically coalesces shuffle partitions' at runtime. That's the direct fix for your 200-partitions problem: instead of you guessing the right number up front, AQE looks at how much data actually came out of the shuffle and merges those 200 fixed partitions down to a sensible count. The source explains WHY it can do this: 'A shuffle/broadcast exchange creates a query stage boundary — the pause enables re-optimization.' In plain terms, the shuffle forces Spark to stop and materialize data (partly why it writes to disk!), and that pause is the moment Spark peeks at the real sizes and re-plans. So the same disk-writing shuffle boundary that makes people think 'not in-memory' is also the checkpoint that lets AQE clean up the partition count for you.
