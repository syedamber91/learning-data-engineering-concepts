# Alex's open questions

Things the wiki didn't answer, and claims to double-check.

## spark-origin (2026-07-09)
- wiki gap: The note does not explain WHY disk is slower than memory (the hardware reason).
- wiki gap: The note does not define what an RDD actually is — it only links to a separate [[rdd]] note.

## catalyst-optimizer (2026-07-09)
- wiki gap: The note doesn't explain HOW the cost model estimates cost, what a 'quasiquote' actually is, why bytecode generation makes things faster, or what the Catalog contains beyond being what attributes are resolved against. It also doesn't give a concrete example query walked through all four phases.
- unverified (not in vutr wiki): Nothing stated outside the note. I stayed strictly within the note's four-phase description; I did not add outside facts about Tungsten, whole-stage codegen, or specific Spark versions even though they relate to this topic.

## adaptive-query-execution (2026-07-09)
- wiki gap: The note names three actions (coalesce shuffle partitions, switch join strategies, handle skew joins) but never explains HOW each one works or what problem each fixes in detail.
- wiki gap: It doesn't say what specific join strategies AQE switches between, though the 'See also' links to sort-merge-join and shuffle-hash-join hint they may be related.
- wiki gap: It doesn't explain what 'coalescing' partitions actually buys you (e.g. why too many small partitions is bad).
- wiki gap: It doesn't define what a 'skew join' problem looks like or why it's hard.
- wiki gap: It doesn't say whether AQE is on by default or needs to be enabled.
- unverified (not in vutr wiki): Any claim about which exact join strategies are swapped (e.g. sort-merge-join to broadcast/shuffle-hash-join) — the linked notes suggest a connection but this note does not state it.
- unverified (not in vutr wiki): Any performance numbers or benefits of AQE — none are given in this note.
- unverified (not in vutr wiki): How coalescing or skew handling are implemented internally — not described here.

## executor-memory-model (2026-07-09)
- wiki gap: Whether storage memory can reclaim from execution (the note only states execution reclaiming storage).
- wiki gap: The exact formula/size of the unified pool beyond 'reserved 300MB first, then 0.6 of the remainder' — no worked number is given.
- wiki gap: What happens to the portion of the remaining heap that is NOT in the unified pool (the other ~40%) — the note doesn't name it (e.g. user memory).
- wiki gap: How the pool is actually divided among concurrent tasks, or what 'starve' concretely means (task failure? spill to disk? OOM?).
- unverified (not in vutr wiki): That the non-unified remainder is 'user memory' — inferred, not stated in the note.
- unverified (not in vutr wiki): That storage can reclaim from execution in the reverse direction — not stated.
- unverified (not in vutr wiki): Any behavior of spark.memory.storageFraction or a protected storage sub-region — not mentioned in the note.

## shuffle-writes-to-disk (2026-07-09)
- wiki gap: The note doesn't explain WHY shuffle writes go to disk (the mechanism or reason), only that they do.
- wiki gap: It doesn't define what a shuffle actually is step-by-step, or what map/reduce stages involve.
- wiki gap: No guidance on HOW to pick a good number of shuffle partitions, only that 200 must be tuned.
- wiki gap: Doesn't say what groupByKey vs reduceByKey do internally beyond 'reduces before vs after the shuffle'.
- unverified (not in vutr wiki): The map->disk->reduce framing in the diagram: the note mentions shuffle writes going to disk and reducing before/after shuffle, but does not explicitly lay out a map-stage-then-reduce-stage pipeline, so that ordering is my inference for clarity.

## data-skew-oom (2026-07-09)
- wiki gap: The note doesn't explain HOW you break a skewed partition apart (no technique named). It also doesn't define OOM as a term, doesn't say why one partition becomes skewed in the first place, and doesn't explain the mechanism by which scheduling order flips a pass into a fail — it only states that it does.
- unverified (not in vutr wiki): My analogies (buckets, workers) and the definitions of 'partition' and 'task' are my own framing to make it concrete — the note uses those words but doesn't define them. Nothing in my answers adds facts beyond the note, but the intuition of WHY scheduling order matters is not spelled out in the note, so any deeper reasoning there would be unverified.

## sort-merge-join (2026-07-09)
- wiki gap: The note does not say who performs the sort or when, only that if it is already paid upstream SMJ fits well.
- wiki gap: It does not compare SMJ against the other join strategies hinted at in the links (shuffle-hash-join), so I cannot say when to pick one over another.
- wiki gap: No mention of what happens if the inputs are NOT sorted, or how big or small the tables should be for SMJ to make sense.
- unverified (not in vutr wiki): A BROADCAST > MERGE > SHUFFLE_HASH decision tree is common Spark knowledge, but the note gives no criteria (like table size thresholds) to build one, so I did not invent a diagram.
- unverified (not in vutr wiki): That SMJ requires a shuffle/partitioning step is widely true in Spark but is not stated in this note.

## shuffle-hash-join (2026-07-09)
- wiki gap: The note states SHJ cannot safely spill to disk but never explains WHY (the underlying mechanism). It also doesn't define what a hash table actually is, what 'shuffle' means in the name, how Spark decides to use SHJ versus Sort Merge Join, or why it was removed in 1.6 and reintroduced in 2.0. It gives no concrete example of sizes or a walkthrough of the join steps.
- unverified (not in vutr wiki): Nothing was asserted beyond the note. The reason WHY SHJ cannot safely spill to disk is acknowledged as unknown from this note rather than guessed. No claims about hash table internals, shuffle mechanics, or the 1.6-removal/2.0-reintroduction rationale were invented.

## data-locality (2026-07-09)
- wiki gap: The note doesn't say how long 'briefly' is (the actual wait timeout), nor how Spark decides a task is running 'unusually slow' (the threshold for triggering speculation). It also doesn't explain why NO_PREF ranks above RACK_LOCAL in the ordering, which is a little counterintuitive.
- unverified (not in vutr wiki): Nothing was asserted beyond the note. Specific timeout values, the speculation threshold, and the reasoning behind NO_PREF's position were deliberately left out because the note doesn't state them.

## jvm-object-overhead (2026-07-09)
- wiki gap: Why padding exists (memory alignment) is never explained — it's just named.
- wiki gap: It's unclear whether the ~10x overhead is constant or only extreme for very small objects like the 4-byte example.
- wiki gap: 'Off-heap', 'columnar', and 'code-generated execution' are named as the fix but never actually defined — I don't really know what each one means.
- wiki gap: No explanation of what a JVM 'header' or 'reference' contains, just that they take space.

## pyspark (2026-07-09)
- wiki gap: The note doesn't explain what Catalyst or Project Tungsten actually do, only that Python UDFs miss out on them. It also doesn't say what Py4J, gRPC, or protobuf are under the hood, what serialization looks like in detail, or why Spark Connect's decoupling matters in practice. It doesn't define what a UDF is beyond context.
- unverified (not in vutr wiki): I did not pull in any outside knowledge about JVM, serialization, Catalyst, Tungsten, Arrow, or gRPC beyond what the note states. The mermaid diagram is my own rendering of the note's stated Python <-> Py4J <-> JVM flow, not extra facts.

## spark-structured-streaming (2026-07-09)
- wiki gap: The note doesn't define what each trigger type actually does mechanically (Default, Fixed-Interval, One-Time, Available-Now) beyond naming them and calling Available-Now multi-batch. It also doesn't explain what micro-batching costs (like latency) versus true record-by-record streaming, nor what the linked concepts (watermark, rocksdb-state-store, apache-flink) add. It gives percentages (60-70% of streaming use cases, ~10% of workloads) without saying what falls in the missing 30-40%.
- unverified (not in vutr wiki): I did NOT verify any of this against outside knowledge. I'm inferring that One-Time stops after a single run and that Available-Now processes multiple batches then stops from the 'multi-batch' label; the note doesn't state the stop behavior explicitly. Nothing here goes beyond the note except those small trigger inferences, which I've flagged.

## photon (2026-07-09)
- wiki gap: The note never spells out what JNI stands for or how the Java–C++ boundary actually works — only that its overhead was 0.06%.
- wiki gap: It doesn't explain the low-level reason vectorized/columnar execution is faster (e.g., cache behavior or CPU efficiency); it just states BigQuery and Snowflake use the same batch technique.
- wiki gap: It doesn't define 'shared-disk' or say why that architectural camp matters, only that Databricks sits in it alongside BigQuery and Snowflake.
- wiki gap: It doesn't say what 'physical operators' are in detail or how Photon 'plugs into' the Databricks Runtime beyond the phrase itself.
- unverified (not in vutr wiki): That the 'worry' about JNI was specifically about performance — the note gives the 0.06% figure but doesn't explicitly state people were worried; that's my inference.
- unverified (not in vutr wiki): Any claim about WHY columnar/vectorized is faster at the hardware level — not stated in the note.

## remote-shuffle-service (2026-07-09)
- wiki gap: The note states the SSD-life and 95% failure-rate improvements as results but does not explain the underlying mechanism — WHY consolidating writes to one RSS server reduces SSD wear or shuffle failures (e.g. fewer random I/O operations). It also doesn't define what a 'shuffle' or 'partition' is from scratch, or say how many RSS servers exist per partition versus overall.
- unverified (not in vutr wiki): I did not verify Uber's RSS design beyond this note — the exact disk-level cause of reduced SSD wear, the number of RSS servers, and the definitions of shuffle/partition are not stated in the note and I did not bring them in from outside.
