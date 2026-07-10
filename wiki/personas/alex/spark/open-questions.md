# Alex's open questions

Things the wiki didn't answer, and claims to double-check.

## lazy-evaluation-transformations-actions (2026-07-10)
- wiki gap: Okay but here's the one that's bugging me — you said Spark needs the WHOLE dependency chain in front of it before running anything, so it can decide where the stage boundaries go. But what if I call an action partway through a chain, and then keep transforming the result afterward with more transformations? Does Spark start building a completely fresh chain/DAG from that point on, or does it somehow remember the earlier lineage too when it's deciding the next set of stage boundaries?

## spark-application-architecture-and-execution-modes (2026-07-10)
- wiki gap: How does the cluster manager actually decide which physical worker nodes to place executors on, and whether two different Spark applications' executors can end up competing for CPU cores on the same worker node?

## jobs-stages-tasks-dag-and-dependencies (2026-07-10)
- wiki gap: You said the DAGScheduler computes preferred locations from cache status and things like HDFS block locations so tasks get scheduled close to their data — but what actually happens if that preferred executor is busy or the data isn't local at scheduling time? Does the task just wait, or does it run somewhere else and eat the network cost?

## data-locality-and-speculative-execution (2026-07-10)
- wiki gap: When speculative execution launches that duplicate copy of a slow task on a different executor, does that copy get to skip the delay-scheduling wait and just land wherever's free, or does it have to earn its own locality level the same way the original task did?

## catalyst-optimizer-phases (2026-07-10)
- wiki gap: You said UDFs skip the whole four-phase pipeline and fall back to row-at-a-time — but AQE's re-optimization also happens at stage/shuffle boundaries on the physical plan. So is a UDF actually invisible to AQE too (since AQE works off the same plan CBO produced), or can AQE still see the UDF as a node and reshuffle partitions around it even though it can't see inside it?

## adaptive-query-execution (2026-07-10)
- wiki gap: Splitting oversized partitions is called 'the mirror case' of coalescing, but coalescing clearly happens after the shuffle write, using exact post-shuffle sizes at the rest-stop boundary. Does splitting also wait for that same boundary, or does Spark have to detect the straggler partition earlier, while it's still mid-stage, before it's even finished writing?

## tungsten-and-jvm-object-overhead (2026-07-10)
- wiki gap: If off-heap memory is completely outside the JVM heap, what actually frees it back up once Spark's done with a shuffle or a cached partition — since there's no GC out there to walk it, doesn't it just leak forever unless something else is cleaning it?

## data-skew-and-oom (2026-07-10)
- wiki gap: You said AQE splits oversized partitions into smaller ones at runtime — but ShuffleHashJoin already commits to building the whole partition's hash table before any probing happens. Does AQE's split happen early enough to save an SHJ job from OOMing, or is that skew-handling really only useful for SMJ, since SHJ's build might already be underway by the time AQE reacts?

## shuffle-writes-to-disk-and-external-shuffle-service (2026-07-10)
- wiki gap: The removal trigger is executorIdleTime — an executor only gets killed once it's sat idle for that interval. But during an active shuffle, is the executor serving files 'idle' the whole time, or could Spark try to remove an executor that's mid-write on its shuffle output, and if so does graceful decommissioning cover that in-progress case or only the already-idle case?

## broadcast-join-and-bucket-join (2026-07-10)
- wiki gap: If I only bucket ONE of the two tables by the join key and leave the other one un-bucketed, does the join still skip shuffle for the bucketed side, or does the whole thing just fall back to a normal full shuffle like neither table was bucketed at all?

## resource-allocation-and-scheduling-modes (2026-07-10)
- wiki gap: If a Fair-scheduling pool has a minShare that's supposed to guarantee it a floor of resources, but dynamic allocation's remove policy just cuts any executor that's been idle past the timeout — does removal check whether killing that executor would break some pool's minShare guarantee, or could a quiet pool's guaranteed floor get scaled away just because nothing's running on it that exact moment?

## pyspark-architecture-and-py4j (2026-07-10)
- wiki gap: You said Spark Connect removes the Py4j JVM-driver step by talking to a remote server over gRPC instead -- does that mean UDFs stop paying the serialization tax under Spark Connect, or does gRPC just move where that same cost happens?
- unverified (not in vutr wiki): The 'million-row table' figure Alex uses to illustrate the per-row UDF cost is his own invented example, not a number stated in the note.

## python-udf-overhead-and-arrow-optimization (2026-07-10)
- wiki gap: You said the JVM literally can't run my custom Python function, so it has to hand off to a separate process — but does that apply to every bit of Python code I write, or only stuff wrapped as a UDF? Like if I write .filter() with a plain Python lambda instead of calling udf(), does that hit the same wall and force the same process hop, or is there a line where Python code stays 'built-in enough' to avoid it?

## photon-vectorized-engine (2026-07-10)
- wiki gap: Hash join splits into a reservation phase where spilling is handled and an allocation phase that's spill-free — but what happens if some other Spark memory consumer needs Photon to give memory back while it's mid-way through that spill-free allocation phase? Does Photon just refuse, or does that case get avoided some other way?
