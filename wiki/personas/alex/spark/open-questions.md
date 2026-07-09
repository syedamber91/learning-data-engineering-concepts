# Alex's open questions

Things the wiki didn't answer, and claims to double-check.

## spark-origin (2026-07-09)
- unverified (not in vutr wiki): Whether Spark provides meaningful benefit for a single-pass (non-iterative) job — the source frames the origin advantage only around iterative reuse and does not quantify the single-pass case.
- unverified (not in vutr wiki): The explicit failure-recovery step (recomputing a lost in-memory partition from its lineage/dependencies) is inferred from the listed RDD properties and DAG; the source names the properties but does not describe the recovery procedure verbatim.

## rdd (2026-07-09)
- wiki gap: The source does not specify the exact caching/persistence mechanism (e.g., persist/cache, storage levels) that decides whether a materialized RDD stays resident in memory for reuse versus being recomputed from lineage — so 'in-memory reuse' is grounded as the motivation but not as a step-by-step mechanism here.
- wiki gap: The source names the DAG and lineage-based recovery but does not detail how the DAG is split into stages or how partition-level recomputation is scheduled on failure.
- unverified (not in vutr wiki): The precise rule for when an intermediate RDD is held in memory versus recomputed on demand (source establishes in-memory reuse is foundational but not the mechanism).
- unverified (not in vutr wiki): Whether all five properties are always present or only conditionally — the source marks partitioner and preferred locations as 'optional' but does not elaborate the conditions beyond partitioner being for key-value RDDs.

## lazy-evaluation (2026-07-09)
- wiki gap: The source states RDDs and DataFrames are lazy and that transformations build a DAG while actions trigger (lines 4, 26), but never gives a concrete list distinguishing which named operations are transformations vs actions (e.g. it does not say count/collect/save ARE the actions) - I inferred the examples.
- wiki gap: The source does not mention caching / persist at all, so the behavior of the lazy plan across multiple actions (recompute vs reuse) cannot be fully answered from this source - my second answer is bounded by that.
- wiki gap: The source lists Catalyst's Logical Optimization examples (predicate pushdown, projection pruning) but does not explicitly say these depend on laziness / seeing the whole plan - that causal link is my reasoning connecting line 5 to line 26, not a verbatim claim.
- unverified (not in vutr wiki): That count, collect, and write-to-disk are specifically 'actions' - the source says actions trigger execution but does not name these operations; I supplied them as examples.
- unverified (not in vutr wiki): The claim that a lazy plan is recomputed from scratch on each separate action (rather than reused) is my mechanistic inference; the source does not state multi-action behavior.
- unverified (not in vutr wiki): That predicate pushdown and projection pruning are impossible without laziness is my causal reasoning linking line 5 and line 26, not stated verbatim in the source.

## catalyst-optimizer (2026-07-09)
- wiki gap: The source names the cost model but does not spell out WHICH statistics feed it; vutr's answer supplies the standard detail (table/column stats + thresholds) which goes slightly beyond the source text.
- wiki gap: The source does not describe HOW Analysis walks or resolves the tree internally (it only says 'resolve attributes via Catalog'); the strict dependency of Logical Optimization on a typed/resolved plan is a reasoned inference, confirmed by vutr, not a verbatim claim.
- wiki gap: Alex has not yet seen a concrete before/after query example showing a filter physically moving during predicate pushdown -- understanding is structural/conceptual, not yet worked through on a real plan tree.
- unverified (not in vutr wiki): That the cost model uses column-level statistics specifically (row counts/sizes are safe; finer column stats are vutr's elaboration beyond the source line).
- unverified (not in vutr wiki): The precise internal ordering claim that Logical Optimization is *defined only over* resolved plans -- presented as reasoning/confirmation, not stated verbatim in the source.
- unverified (not in vutr wiki): Any statement about how many candidate physical plans Catalyst generates or the exact cost formula -- the source says 'cost model' only, no numbers.

## adaptive-query-execution (2026-07-09)
- wiki gap: The source states WHAT AQE does and that the stage boundary's pause enables re-optimization, but does not detail the internal config that turns AQE on (e.g. spark.sql.adaptive.enabled) or the specific thresholds/knobs governing coalescing and skew detection.
- wiki gap: It does not spell out how AQE decides the target post-coalesce partition size, nor the exact criterion for declaring a partition 'skewed' (e.g. a size ratio versus the median).
- unverified (not in vutr wiki): The specific config flag names (spark.sql.adaptive.enabled, spark.sql.adaptive.skewJoin.*) are general Spark knowledge and are NOT in the provided source.
- unverified (not in vutr wiki): The claim that a broadcast exchange must 'fully collect and build' before the downstream join consumes it is my reasoning extending the source's statement that a broadcast exchange creates a stage boundary; the source does not describe the broadcast build step in that detail.

## executor-memory-model (2026-07-09)
- wiki gap: The source states the 0.6 fraction and 300MB reserved but does not give the exact formula for how the unified region is computed as (heap - 300MB) * 0.6 — I inferred that standard formula; the source only names the two knobs.
- wiki gap: The source does not specify the default execution/storage split WITHIN the unified region (commonly 50/50 via spark.memory.storageFraction) — I described them as sharing the region without a fixed default ratio because the source doesn't state one.
- wiki gap: The source does not mention the ~40% 'user memory' region by name — I named it to complete the picture of where the non-fraction heap goes, but that label is outside the source.
- unverified (not in vutr wiki): The exact formula usable = (heap - 300MB) and unified = usable * 0.6 (source gives the two values but not the arithmetic combining them).
- unverified (not in vutr wiki): The default within-unified split of 50% execution / 50% storage and the spark.memory.storageFraction knob (not in source).
- unverified (not in vutr wiki): The term 'user memory' for the ~40% outside spark.memory.fraction (not in source).
- unverified (not in vutr wiki): That evicted cached blocks are recomputed specifically 'from lineage' — the source establishes RDD lineage/DAG generally (line 4) but does not explicitly tie cache eviction recovery to it; I bridged these two source facts.

## shuffle-writes-to-disk (2026-07-09)
- wiki gap: The source states shuffle writes to disk but does not describe the mechanism in detail — e.g. shuffle files, the sort-based shuffle writer, or how reduce tasks locate and fetch map outputs. I inferred the map-write/reduce-fetch flow from the RSS bullet (mapper writes, reducer fetches) rather than a direct shuffle-file explanation.
- wiki gap: The source gives no guidance on HOW to pick a good value for spark.sql.shuffle.partitions (e.g. target partition size or a rule of thumb) — only that 200 is the default and 'must be tuned.'
- wiki gap: The source states reduceByKey reduces before shuffling but does not spell out the map-side combine mechanism or give a data-volume example, so the 'much smaller shuffle' claim is mechanism-level reasoning, not a quoted number.
- unverified (not in vutr wiki): My phrase 'map-side pre-aggregation / combine' for how reduceByKey shrinks data before the shuffle — the source says it 'reduces data before shuffling' but does not use the term combiner or describe the map-side combine step.
- unverified (not in vutr wiki): My characterization that intermediate shuffle data 'can be huge and outlive the task' as the reason disk is used — the source asserts the disk fact but does not give this durability/size justification explicitly.
- unverified (not in vutr wiki): The implied link that AQE coalescing shuffle partitions directly replaces manual tuning of the 200 default — the source states both facts separately but does not explicitly say AQE removes the need to set spark.sql.shuffle.partitions.

## data-skew-oom (2026-07-09)
- wiki gap: The source names the fix as 'breaking the skewed partition apart' and mentions AQE handles skew joins (Spark 3.0), but it does not spell out the concrete mechanics of HOW (e.g. salting the key, AQE's split threshold). I inferred salting/AQED-split from general knowledge — flagged as unverified.
- wiki gap: The source doesn't quantify what 'more memory than its share' means numerically (e.g. how the 0.6 unified fraction divides per task), so the exact memory-per-task math is not grounded in the text.
- unverified (not in vutr wiki): Salting (appending a random suffix to the hot key) as a specific technique for breaking the skewed partition apart — this is my inference; the source says 'break the skewed partition apart' and cites AQE skew-join handling but does not name salting.
- unverified (not in vutr wiki): That AQE splits the skewed partition by a size threshold specifically — the source says AQE 'handles skew joins' but gives no split mechanism detail.

## sort-merge-join (2026-07-09)
- wiki gap: The source doesn't give the exact mechanism of HOW a sort spills (external merge sort: sort in-memory chunks, write sorted runs to disk, k-way merge them) — I inferred that; the source only asserts 'SMJ can safely spill to disk.'
- wiki gap: The source doesn't state whether Broadcast Hash Join itself can OOM (broadcasting a table that's near the threshold to every executor still costs memory per executor) — it only says BHJ triggers below 10MB.
- wiki gap: The exact tie-break / conflict rule when multiple hints are present is stated only as the priority order BROADCAST > MERGE > SHUFFLE_HASH; the source doesn't show how SHUFFLE_REPLICATE_NL or other hints fit in.
- wiki gap: The source doesn't quantify how much slower SMJ is than SHJ when data DOES fit in memory — it only frames SHJ as 'faster when it fits.'
- unverified (not in vutr wiki): That SMJ's spill is implemented specifically as an external merge sort with k-way merge — this is my mechanistic inference, not stated verbatim in the source.
- unverified (not in vutr wiki): That salting is the concrete technique to 'break the skewed partition apart' — the source says to break it apart but does not name salting.
- unverified (not in vutr wiki): That AQE upgrades SMJ to BHJ at runtime when it detects a small side — the source says AQE 'switches join strategies at runtime' and handles skew, but does not specify SMJ->BHJ as the exact switch.

## shuffle-hash-join (2026-07-09)
- wiki gap: The source states the build side must fit in memory but does not quantify HOW MUCH memory a hash table costs relative to raw data — though the JVM object-overhead quote ('A 4-byte string would have over 48 bytes in the JVM object') hints the in-memory hash table can be far larger than the on-disk partition, which would make OOM easier to hit than partition size alone suggests. I'm inferring the connection; the source doesn't explicitly link object overhead to SHJ.
- wiki gap: The source doesn't say exactly HOW SMJ spills (sorted runs merged from disk) — I brought that in as standard external-sort knowledge to explain WHY SMJ survives; the source only asserts 'SMJ can safely spill to disk; SHJ cannot' without the mechanism.
- wiki gap: Unclear from the source whether SHJ is ever chosen automatically by the optimizer or only via the SHUFFLE_HASH hint — the hint-priority list implies it's hint-driven, but that's my inference.
- unverified (not in vutr wiki): That a hash table is O(1) to probe and useless when half-built — this is general hashing/CS knowledge I used to explain the mechanism, not stated in the source.
- unverified (not in vutr wiki): That SMJ's spill works via writing sorted runs to disk and merge-passing them — general external-sort knowledge, not in the source.
- unverified (not in vutr wiki): That the JVM 48-bytes-for-a-4-byte-string overhead applies to the SHJ hash table specifically — the quote is real but the source never ties it to SHJ memory sizing.

## data-locality (2026-07-09)
- wiki gap: The source states the locality ordering and speculative execution in a single line but does not describe the locality-wait timeout, how long Spark waits before relaxing a level, or how the loser copy in speculation is cancelled — I inferred those mechanisms rather than reading them verbatim.
- wiki gap: The source does not quantify the cost difference between levels (e.g. how much slower ANY is than PROCESS_LOCAL) or explain what makes data PROCESS_LOCAL in the first place (caching vs. task output), so my 'cached in the executor' example is illustrative.
- unverified (not in vutr wiki): The existence of a locality-wait timeout and step-by-step fallback (PROCESS_LOCAL -> NODE_LOCAL -> ... -> ANY) is my inference; the source only lists the ordering nearest-to-farthest.
- unverified (not in vutr wiki): That the losing speculative copy is killed once the winner finishes is my reasoning, not stated in the source.
- unverified (not in vutr wiki): The specific example that PROCESS_LOCAL data is 'cached in the executor JVM' is illustrative; the source does not give an example of how data becomes PROCESS_LOCAL.

## jvm-object-overhead (2026-07-09)
- wiki gap: The source states the 48-byte total and names 'the JVM object' but does not itemize the exact byte breakdown (header size, reference size, padding). The specific components (object header, class pointer, char-array reference, 8-byte alignment padding) are standard JVM-layout knowledge used to explain the 'over 48 bytes' figure, not spelled out line-by-line in the material.
- wiki gap: The source does not explicitly connect JVM-object overhead to garbage-collection pressure; the GC angle in the first answer is reasoned mechanism, not a quoted claim.
- wiki gap: The source establishes Tungsten only implicitly via Photon's contrast ('columnar in-memory representation (not Spark SQL's row-oriented)') and the PySpark note that Python UDFs 'don't benefit from Catalyst or Project Tungsten'; it names Tungsten but does not detail its off-heap binary layout — that mechanism is inferred to explain the WHY.
- unverified (not in vutr wiki): Exact per-component byte breakdown of the 48-byte JVM object (header/reference/padding sizes) — inferred from standard JVM layout, not itemized in source.
- unverified (not in vutr wiki): That off-heap Tungsten memory is excluded from the spark.memory.fraction 0.6 execution accounting and/or bypasses garbage collection — reasoned consequence, not stated in source.
- unverified (not in vutr wiki): That Tungsten specifically uses an off-heap columnar binary layout with values at fixed offsets — the source names Tungsten and describes Photon's columnar representation, but does not spell out Tungsten's internal layout.

## pyspark (2026-07-09)
- wiki gap: Source states Python UDFs 'don't benefit from Catalyst or Project Tungsten' but does not detail WHY Catalyst treats a UDF as an opaque black box (the black-box framing is my inference, reasonable but not spelled out in source).
- wiki gap: Source names Apache Arrow's role only indirectly for Pandas/Arrow UDFs; the mechanics of Arrow as the transport (shared columnar format, batch transfer) are standard Spark knowledge but not fully spelled out verbatim in this source.
- wiki gap: Whether the Tungsten->Arrow handoff is true zero-copy or just a cheap columnar copy is not stated in the source — flagged honestly in the answer rather than asserted.
- wiki gap: Source does not give quantitative speedup numbers for Pandas/Arrow UDFs vs plain Python UDFs, so the magnitude of the 'claw back' is qualitative here.
- unverified (not in vutr wiki): The step-by-step 7-stage serialize/ship/deserialize round-trip is my mechanistic reconstruction of 'serialization overhead' — the source asserts the overhead exists but does not enumerate these exact steps.
- unverified (not in vutr wiki): The claim that plain PySpark DataFrame ops run 'as fast as Scala' is a widely-known consequence of the wrapper architecture but is my inference from the source's architecture description, not a verbatim source claim.
- unverified (not in vutr wiki): The description of Apache Arrow as a 'shared columnar in-memory format both sides understand' with near-zero translation is standard knowledge applied to the source's mention of Arrow-optimized/Pandas UDFs, not verbatim in the source.
- unverified (not in vutr wiki): Spark Connect using a 'thin client sends the logical plan to a remote cluster' elaborates on the source's 'gRPC/protobuf' mention; the client-server decoupling detail is inference consistent with the source but not spelled out.

## spark-structured-streaming (2026-07-09)
- wiki gap: The source does not describe HOW state is carried across slices (no mention of a state store, checkpointing, or watermarks), so stateful streaming like running aggregations is only inferable, not grounded.
- wiki gap: The source does not name or explain the streaming trigger/execution loop that replaces the one-shot batch output operation.
- wiki gap: The source gives no detail on micro-batch vs continuous processing, latency characteristics, or how big each bounded slice is.
- wiki gap: No mention of how event-time versus processing-time is handled, which matters for correctness in real streams.
- unverified (not in vutr wiki): That Spark keeps running state across slices via a dedicated state store (implied by 'subset of bounded data' + reuse, but not stated in the source).
- unverified (not in vutr wiki): The specific name/config of the repeating trigger that keeps the lazy plan executing over new data (inferred from the laziness quote, not stated).
- unverified (not in vutr wiki): Whether the 'bounded slice' is literally a micro-batch (a reasonable reading, but the source never uses that term).

## photon (2026-07-09)
- wiki gap: Source doesn't quantify Photon's actual speedup over row-oriented Spark SQL — it explains the mechanisms (columnar + vectorized) but gives no benchmark numbers for end-to-end query gains.
- wiki gap: Source doesn't describe how a mixed plan is stitched together — whether/where columnar-to-row conversion happens at the Photon/Spark operator boundary, or what that conversion costs (only JNI crossing at 0.06% is given).
- wiki gap: Source doesn't say which operators Photon covers or when a query falls back to the JVM operators (coverage of the engine is unstated).
- unverified (not in vutr wiki): That row/columnar layout conversion happens at Photon-to-Spark operator seams — a reasonable inference and generally true of such engines, but NOT stated in the source; the source only names JNI (call-boundary) overhead at 0.06%.
- unverified (not in vutr wiki): That vectorization and code generation could be combined in one engine — true in the broader field, but the source only discusses Databricks choosing interpreted vectorization instead of codegen, not combining them.

## remote-shuffle-service (2026-07-09)
- wiki gap: Source gives outcome metrics (SSD 3mo to ~3yr, 95% fewer failures) but does not spell out the byte-level write mechanism (write amplification, small vs sequential writes), so the 'why disks last longer' reasoning is inferred standard explanation, not stated verbatim.
- wiki gap: No detail on how RSS handles an RSS server failure itself (replication, failover, recomputation) — so whether concentrating a partition onto one server introduces a new single point of failure is unresolved from this source.
- wiki gap: No description of where RSS servers physically live relative to mappers/reducers, how many RSS servers exist per job, or how partitions are assigned to servers.
- unverified (not in vutr wiki): That RSS reduces total bytes written (source does not claim this; likely only pattern/shape changes).
- unverified (not in vutr wiki): The specific SSD physics (write amplification, wear leveling) driving the 3-month-to-3-year improvement — mechanism is inferred, not in the source.
- unverified (not in vutr wiki): Any RSS fault-tolerance or replication behavior for a downed RSS server.
