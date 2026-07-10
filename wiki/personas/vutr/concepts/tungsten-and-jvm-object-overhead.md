---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-fastest-way-to-learn-spark-is.md
- raw/spark/i-spent-6-hours-learning-pyspark.md
last_updated: '2026-07-11'
qc: passed
slug: tungsten-and-jvm-object-overhead
topics:
- spark
---

Here's the number that should bother you: a 4-byte string costs over 48 bytes once it becomes a JVM object. That's not a rounding error, that's more than 10x overhead just to hold plain-vanilla data on-heap. If you've ever wondered why a Spark executor with gigabytes of RAM still spills or OOMs on data that "shouldn't" be that big, this is a large part of the answer.

The root cause is [[executor-memory-model-and-caching|on-heap memory]] itself. On-heap data is managed as regular JVM objects, which means it's subject to the JVM garbage collector. Every object carries its JVM object header and boxing overhead on top of the actual bytes of data, and GC has to walk and reclaim all of it — which means the GC process periodically pauses the executor until it finishes. You pay twice: once in wasted memory footprint, once in stop-the-world pauses.

Project Tungsten exists to correct this, and the correction-first framing matters: Tungsten doesn't try to make GC faster, it tries to avoid needing GC at all for the hot path. It introduces a memory manager that operates directly against binary data rather than Java objects — representing rows as specialized Spark SQL Types objects instead of boxed Java objects. Even while still living on-heap, this is friendlier to GC because there's far less object graph to trace. But Tungsten can go further: it can manage data completely off the JVM heap. Off-heap is turned off by default — you enable it explicitly with `spark.memory.offHeap.enabled=True` and a positive `spark.memory.offHeap.size`. Once enabled, off-heap memory has only two regions (execution and storage, no separate reserved/user memory), and it's still governed by `spark.memory.storageFraction` just like on-heap. The total execution region Spark reports is the sum of the on-heap and off-heap execution regions, and the same holds for storage.

The concrete, binary-data representation Tungsten produces is called UnsafeRow — data laid out in off-heap memory, bypassing the JVM garbage collector entirely. This is the mechanism, not just a marketing name, and it directly explains a join/aggregation decision you can watch happen: Spark strongly prefers HashAggregate over [[sort-merge-join-vs-shuffle-hash-join|SortAggregate]] because it skips the sorting step. HashAggregate works by building a hash table keyed on the aggregation column, where the value is an aggregation buffer updated in place as matching keys arrive. For that in-place update to work efficiently under UnsafeRow, the buffer needs a fixed byte size — which is exactly what Integer, Long, and Double give you, since they always occupy the same number of bytes. A String doesn't; it can't be mutated "in place" inside a fixed-size slot. So when the data type being aggregated falls outside that fixed-size list, Spark falls back to SortAggregate. This isn't hypothetical: in Vu's 20GB aggregation case study, because the GroupBy touched every column including string fields like `l_comment` and `l_returnFlag`, Spark chose SortAggregate over HashAggregate — a direct, observable consequence of the UnsafeRow/Tungsten fixed-size constraint, visible in the physical plan.

The flip side worth flagging: Tungsten's binary-object efficiency only benefits code that stays inside Spark's own execution engine. A [[python-udf-overhead-and-arrow-optimization|Python UDF]] doesn't benefit from Catalyst or Tungsten at all — the row has to be pulled back out of Tungsten's binary format, serialized, shipped to a separate Python process, and deserialized again, on top of operating one row at a time instead of vectorized. So the GC-avoidance win from Tungsten is conditional: it holds for native DataFrame/SQL operations, and it evaporates the moment you drop into a UDF.
