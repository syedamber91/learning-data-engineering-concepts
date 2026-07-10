---
persona: vutr
kind: concept
sources:
- raw/spark/10-minutes-to-learn-apache-spark.md
- raw/spark/the-fastest-way-to-learn-spark-is.md
- raw/spark/a-closer-look-into-databrickss-photon.md
- raw/spark/if-youre-learning-apache-spark-this.md
last_updated: '2026-07-11'
qc: passed
slug: data-skew-and-oom
topics:
- spark
---

People treat skew as a "slow job" problem. It's really a "which join strategy did you pick" problem — skew is what turns a survivable disk spill into a fatal `OutOfMemoryError`, and the difference comes down to whether the join algorithm is even allowed to spill.

Take [[sort-merge-join-vs-shuffle-hash-join]]. In ShuffleHashJoin (SHJ), Spark identifies the smaller side within each partition and builds an **in-memory hash table** from it — the whole build side of that partition has to fit in memory before probing can happen. If one partition is abnormally large because of skew, the executor tries to build that hash table anyway and throws OOM. SortMergeJoin (SMJ) has no such requirement: once both sides are partitioned and sorted, it "can safely spill to disk if the partition is too big to fit in memory," which is exactly why SMJ, not SHJ, is Spark's preferred default. SHJ was actually removed in Spark 1.6 and reintroduced in 2.0 specifically because it's faster *when* build-side partitions fit in memory — but it is opt-in for a reason: `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` defaults to 0, meaning "Spark will always skip the ShuffleHashJoin" unless you raise it. Vu's own project sets `spark.sql.join.preferSortMergeJoin=False` and the threshold to 256MB, then keeps `spark.sql.files.maxPartitionBytes` at 128MB specifically so the input partitions stay under that ceiling — proof that enabling SHJ safely means you first have to guarantee no partition (skewed or not) can exceed the threshold. His own warning: "it's only efficient when the build-side partitions fit in memory. If they get larger for some reason, your application will likely get an OOM error."

Whether a given partition fits comes down to the [[executor-memory-model-and-caching]] math, not the raw on-disk size. Usable unified memory per executor is `(spark.executor.memory - reserved memory) * spark.memory.fraction`, with reserved memory hardcoded to 300MB and `spark.memory.fraction` defaulting to 0.6 — a 2GB executor nets only `(2048-300)*0.6 = 1048.8MB` for execution + storage combined, split again by `spark.memory.storageFraction` (0.5 default). And the on-disk size understates the real footprint: Parquet is SNAPPY-compressed at rest, so a 2.6GB file expanded to 3.7GB once deserialized in memory during a cache test, with 530.8MB spilling. A skewed partition inflates by the same deserialization factor, just concentrated in one task instead of spread evenly — so a partition that looked fine on disk can blow the per-task memory budget on read alone.

The case-study numbers show spill is tunable, but not always predictably. Halving `maxPartitionBytes` from 256MB to 128MB doubled the task count (84 → 168), halved spill per task, and cut task time 35s → 12s (a 65.7% reduction) — smaller partitions give a skewed key less material to pile up in one task. Raising executor cores from 2 to 4 without raising memory did the opposite: more tasks now share the same memory pool, spill rose from 832MB to ~1GB, and task time went up to ~40s. Raising executor memory to 4GB cut task time to 25s but — Vu flags this explicitly as counterintuitive and unresolved — spill stayed the same as the 2GB baseline; his best guess is it's tied to the SortAggregate mechanism, not confirmed.

Two more contributing mechanisms worth naming: JVM object overhead — a 4-byte string can cost "over 48 bytes in the JVM object" — means skewed partitions holding many strings inflate faster than the raw byte count suggests, which is part of why [[tungsten-and-jvm-object-overhead]] and off-heap `UnsafeRow` layouts exist. And [[adaptive-query-execution]] does react to skew at runtime — it "splits huge partitions into smaller ones to reduce stress on a single worker" alongside coalescing undersized ones — though the sources don't spell out AQE's skew-join-split algorithm beyond that one line, so don't overclaim precision there. On the [[photon-vectorized-engine]] side, the same failure mode reappears in a different form: off-heap size is a static per-node allocation, and if memory consumers overuse it, "it can lead to out-of-memory (OOM) errors" — skew is dangerous regardless of engine, because any allocator with a hard ceiling will hit it once one partition gets big enough.

Bottom line: SMJ degrades under skew, SHJ dies under skew. If you flip on SHJ for its speed, you've implicitly promised the optimizer that no partition — skewed or not — will exceed your memory threshold.
