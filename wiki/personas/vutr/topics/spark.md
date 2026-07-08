---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: spark
---

Related: [[spark-origin]] · [[executor-memory-model]] · [[spark-structured-streaming]] · [[rdd]] · [[catalyst-optimizer]] · [[adaptive-query-execution]] · [[sort-merge-join]] · [[shuffle-hash-join]] · [[photon]] · [[remote-shuffle-service]] · [[pyspark]] · [[data-locality]] · [[jvm-object-overhead]] · [[lazy-evaluation]] · [[data-skew-oom]] · [[shuffle-writes-to-disk]]

## Comparisons
**[[sort-merge-join]] vs [[shuffle-hash-join]]** — SMJ is the preferred and safer strategy because it can spill to disk; SHJ cannot, and it demands the build side of every partition fit entirely in memory, so a skewed partition makes it throw OOM. This is why the hint priority runs BROADCAST > MERGE > SHUFFLE_HASH. Broadcast Hash Join is triggered when a table falls below the autoBroadcastJoinThreshold (default 10MB), while a Bucket Join eliminates shuffle entirely by shuffling at write time rather than join time — worth it when you already know how tables are joined and aggregated.

**[[photon]] — vectorized (interpreted) vs code generation** — Databricks chose the interpreted vectorized path over code generation deliberately: prototyping took weeks instead of two months, and debugging native C++ with print statements was far easier than debugging code generated at runtime, where engineers must add extra code by hand to find issues.

**[[pyspark]] Python UDFs vs vectorized UDFs** — plain Python UDFs pay Py4J serialization overhead and skip Catalyst and Project Tungsten entirely; Pandas UDFs (Spark 2.3) and Arrow-optimized Python UDFs (Spark 3.5) exist precisely to claw back that lost efficiency.

**Fixing skew: more memory vs repartitioning** — for [[data-skew-oom]], adding memory does nothing because the skewed partition still lands on one task; the only real fix is breaking the partition apart.

## Open questions
- Given the default of 200 shuffle partitions is applied regardless of data size, what heuristic or signal should drive the tuned value in practice?
- With [[adaptive-query-execution]] able to switch join strategies and handle skew at runtime, how much of the manual join-hint and repartition tuning for [[data-skew-oom]] does it actually obviate?
- If [[photon]]'s JNI overhead is only 0.06% of execution time, where does the columnar C++ engine's real speedup come from relative to Spark SQL's row-oriented execution?
- Does the [[remote-shuffle-service]] paradigm generalize beyond Uber's environment, or are its 95% failure-rate and SSD wear-out gains tied to their specific shuffle scale?

## Synthesis
Spark's design threads back to one origin — [[spark-origin]] at Berkeley's AMPLab in 2009, built to spare iterative ML the disk-write penalty of MapReduce, which is why in-memory reuse of the [[rdd]] is foundational. From there the story is [[lazy-evaluation]] over the RDD building a DAG that [[catalyst-optimizer]] and later [[adaptive-query-execution]] can reshape before and during execution — and the same declarative plan carries over to [[spark-structured-streaming]], which treats a continuous stream as a subset of bounded data. Most of the operational pain lives in memory and shuffle: the [[executor-memory-model]] (300MB reserved, spark.memory.fraction 0.6, unified since 1.6) is the constrained arena, the shuffle writes to disk not memory (see [[shuffle-writes-to-disk]]), and [[data-skew-oom]] is the recurring failure mode that no amount of extra memory fixes and that makes join strategy choice ([[sort-merge-join]] vs [[shuffle-hash-join]]) load-bearing. Two lower-level facts shape all of this: [[data-locality]] and speculative execution govern where and how redundantly tasks run, and [[jvm-object-overhead]] (a 4-byte string costing 48+ bytes) is the tax that motivates columnar, off-heap execution. The frontier is doing the same work faster or more reliably — [[photon]]'s vectorized C++ operators, [[pyspark]]'s march toward vectorized UDFs, and Uber's [[remote-shuffle-service]] rethinking the shuffle itself.

## Related topics
- [[apache-arrow]] — Arrow-optimized PySpark UDFs use Arrow to claw back the Py4J serialization overhead that plain Python UDFs pay.
- [[flink]] — The central axis is Flink vs Spark Structured Streaming — a true streaming engine versus micro-batching — and they share the RocksDB state backend.
- [[single-node-engines-duckdb-polars-vs-distributed-systems]] — Spark is the distributed system these single-node engines are weighed against — reserved for genuinely distributed workloads where Polars and DuckDB are too small.
- [[history-of-data-engineering]] — Spark was built at AMPLab to spare iterative ML the disk-write penalty of MapReduce, the big-data era the history note traces.
- [[sql-fundamentals-and-execution-model]] — Spark's Catalyst planner chooses among the same physical joins — nested-loop, sort-merge, hash/broadcast — that the SQL execution model describes.
