---
persona: vutr
kind: concept
sources:
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/the-fastest-way-to-learn-spark-is.md
- raw/spark/i-spent-8-hours-learning-apache-spark.md
last_updated: '2026-07-11'
qc: passed
slug: executor-memory-model-and-caching
topics:
- spark
---

`spark.executor.memory` is not the amount of memory your data-processing actually gets. That's the misconception to correct first: an executor's JVM heap splits into three regions — **reserved**, **user**, and **unified** — and only a fraction of the unified region is yours for shuffling, joins, aggregations, and caching.

The **reserved memory** is hardcoded to 300 MB (visible directly in Spark's `UnifiedMemoryManager.scala`, line 200) — Spark burns this off the top for internal objects no matter what you set `spark.executor.memory` to. The **user memory** region holds your own data structures (hash tables, arrays) and Spark's internal metadata, and doubles as a safeguard against OOM in some cases. What's left is the **unified memory**, sized by `spark.memory.fraction` (default 0.6).

So the actual formula for usable memory is: `(spark.executor.memory - 300MB) * spark.memory.fraction`. Worked example from Vu's hands-on 20GB project: with `spark.executor.memory=2048MB`, `(2048 - 300) * 0.6 = 1048.8MB` is what an executor actually has for processing and storage — barely half the configured 2GB.

Inside the unified region, `spark.memory.storageFraction` (default 0.5) splits it further into **execution** (shuffling, joins, aggregations, sorting — memory released as soon as the task finishes) and **storage** (caching). With a 4GB executor at defaults, that works out to roughly the storage half and the execution half of the unified pool.

This boundary used to be fixed — pre-1.6, storage couldn't touch execution's space and vice versa, which wasted memory for jobs that didn't cache much. Since Spark 1.6's unified approach, the boundary is crossable, but under specific rules, not free-for-all: if execution has spare space, storage can borrow it; when execution wants it back, storage is forced to evict using LRU until it falls under the R threshold. Conversely, if storage has spare space, execution can borrow it — but here the roles are asymmetric: storage *cannot* forcibly reclaim from execution, because the design prioritizes execution. Storage only gets room back by evicting its own cached data (LRU) to fit new data. So execution always wins the tug-of-war.

**Off-heap** exists to route around a different problem: on-heap data is subject to JVM garbage collection, and JVM objects carry real overhead — a 4-byte string balloons to over 48 bytes as a JVM object. Project Tungsten's memory manager operates on binary data instead of Java objects to cut this overhead and reduce GC pauses; it's off by default (`spark.memory.offHeap.enabled=true` plus a positive `spark.memory.offHeap.size` turns it on). Off-heap only has two regions — execution and storage, still governed by `spark.memory.storageFraction` — and the *total* execution region spans both on-heap and off-heap execution memory combined (same for storage).

**Caching** lives in the storage region and is lazy like any transformation — nothing materializes until an action fires. Storage levels: `MEMORY_ONLY` (unserialized, in memory), `MEMORY_AND_DISK` (spills to disk when memory's full), `DISK_ONLY` (serialized, disk-only), `OFF_HEAP`. Append `_SER` to store serialized (saves space, costs deserialization CPU), or `_X` for replication factor — `MEMORY_ONLY_SER_3` replicates cached data to 3 nodes for faster fault tolerance. `cache()` always uses `MEMORY_AND_DISK`; `persist()` lets you pick the level.

The hands-on project makes the memory-vs-disk gap concrete: caching a 2.6GB on-disk Parquet file showed 3.7GB in memory — Parquet is Snappy-compressed on disk, and Spark deserializes/decompresses on read, so in-memory size always exceeds on-disk size. That gap is also why [[data-skew-and-oom|spill]] happens: in the same project, with `spark.executor.memory=2GB` and 2 cores, each task spilled 832MB (358.7MB to disk) — driven both by the parquet-expansion effect and by [[sort-merge-join-vs-shuffle-hash-join|SortAggregate's]] sort overhead. Doubling executor memory to 4GB (same core count) didn't shrink the spill at all — counterintuitive, and Vu flags it as unresolved, guessing it's tied to the SortAggregate mechanism rather than raw memory pressure. Meanwhile shrinking partition size (256MB → 128MB, doubling task count from 84 to 168) *halved* spill and cut per-task time from 35s to 12s, and raising executor cores from 2 to 4 (same memory) *increased* spill from 832MB to 1GB — more concurrent tasks sharing one memory pool shrinks each task's slice. The lesson: memory-per-task, not raw executor memory, is what controls spill.
