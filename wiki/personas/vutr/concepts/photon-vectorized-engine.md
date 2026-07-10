---
persona: vutr
kind: concept
sources:
- raw/spark/a-closer-look-into-databrickss-photon.md
- raw/spark/why-did-databricks-build-the-photon.md
- raw/spark/how-is-databricks-spark-different.md
last_updated: '2026-07-11'
qc: passed
slug: photon-vectorized-engine
topics:
- spark
---

A common misread: Photon is not a standalone query engine competing head-on with BigQuery, Redshift, or Snowflake. It acts as an enhancement component bolted onto the existing SparkSQL engine — a new set of physical operators that [[spark-application-architecture-and-execution-modes|Databricks Runtime (DBR)]]'s query plan can call like any other Spark operator, with graceful fallback to legacy SparkSQL for anything Photon doesn't support.

**Why it exists.** The Lakehouse forces an execution engine to handle a much messier input distribution than a traditional warehouse: raw data, many small files, many columns, no reliable statistics. Databricks addressed this with two design decisions, not one. First, vectorized execution instead of Spark's code-generation approach — vectorization is what enables runtime adaptivity, since Photon can discover and react to a micro-batch's actual characteristics rather than committing to a compiled plan up front. Second, C++ instead of the JVM. Databricks named concrete JVM ceilings: garbage collection performance degraded once heaps exceeded 64GB, the JVM-based engine required manual off-heap memory management (adding codebase complexity), Java code generation hit method-size/code-cache limits, and engineers lacked control over custom [[tungsten-and-jvm-object-overhead|SIMD]] kernels.

**Vectorized vs. code-generated, with real numbers.** Databricks prototyped both. The interpreted/vectorized approach (MonetDB/X100 lineage) took a couple of weeks to prototype; the code-generated approach took two months, because runtime-generated code is harder to debug — engineers had to add extra instrumentation, whereas the vectorized path was plain, debuggable C++. Code generation collapses operators into a few fused functions, which kills per-operator observability ("the operator code may be fused into a row-at-a-time processing loop"); vectorization keeps operator boundaries intact, at some function-call overhead that SIMD-over-batches amortizes.

**The data layout.** Photon batches columns into column vectors — contiguous values plus a byte vector for NULLs — grouped into a column batch representing rows. A batch also carries a position list: the indices of currently "active" rows. Every operator reads a position list to know which rows are live, rather than physically removing filtered rows. Filters, concretely, are implemented as position-list rewrites, not row deletion.

**Execution kernels.** Kernels are functions doing tight loops over one or more batches, mostly auto-vectorized by the compiler and specialized per input type via C++ templates — an idea Photon borrows from MonetDB/X100. The vectorized hash table used for joins runs three kernel steps: hash the key batch, probe to load hash-entry pointers, then compare entries against lookup keys column-by-column, emitting a position list of non-matches.

**Memory management** splits transient vs. dynamic vs. long-lived: an internal buffer pool caches column-batch allocations by frequency to avoid OS-level allocation calls; a dedicated append-only pool handles variable-size data like strings and is freed before each new batch, with a global tracker that can shrink batch size if data grows too large; large cross-batch allocations (e.g., aggregation state) go through an external memory manager. Photon integrates with Spark's *unified memory manager* by separating reservation from allocation — a memory consumer API lets Spark ask Photon to spill (and vice versa); when N bytes must be freed, consumers are sorted least-to-most allocated and the first with ≥N bytes is spilled, to minimize spill count. Hash join specifically splits into a reservation phase (spilling handled) and an allocation phase (spill-free).

**Adaptivity is batch-level, not query-level like [[adaptive-query-execution|AQE]].** Photon inspects each batch at runtime: a NULL-free batch lets it drop branching; a batch with no inactive rows skips the position-list lookup; all-ASCII strings get an optimized path; sparse batches can be compacted; shuffle encoding adapts to observed data patterns.

**Measured payoff.** On 1GB integer inner joins, Photon's vectorized hash table beat DBR's join by 3.5×, chiefly from better memory-hierarchy use via parallel loads. `CollectList` grouping aggregation hit 5.7× over DBR (which leans on unoptimized Scala collections). A 200M-row, six-column Parquet write was 2× faster end-to-end, mostly from column encoding. JNI crossing overhead was negligible: 0.06% of execution time in JNI-internal methods, 0.2% in the adapter node — versus ~95% spent serializing rows into Scala objects on the legacy path, meaning the [[jobs-stages-tasks-dag-and-dependencies|adapter/transition]] boundary is not where the cost lives.
