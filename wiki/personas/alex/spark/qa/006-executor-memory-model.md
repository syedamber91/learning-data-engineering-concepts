---
persona: alex
kind: concept
sources:
- vutr/executor-memory-model
last_updated: '2026-07-09'
qc: passed
slug: 006-executor-memory-model
topics:
- spark
learner: alex
source_note: executor-memory-model
mastery: mastered
---

*What Alex understood:* Okay, so an executor's heap is basically a stack of layers. Bottom layer: 300MB reserved, hardcoded, off-limits — that's Spark's own emergency cushion, my data never gets it. Then of whatever heap is LEFT after those 300MB, spark.memory.fraction = 0.6 grabs 60% and calls it the unified region — the part my job lives in. That 60% is shared between two roommates: EXECUTION (the live work — shuffles, joins, sorts, the scratchpad a running task scribbles on) and STORAGE (cached/persisted data and broadcasts). Here's the part I want to make sure I've got: before Spark 1.6 those two roommates had FIXED walls — execution couldn't touch storage's half even if storage was mostly empty, so you could OOM with free memory just sitting there unused. The unified model (1.6+) turned the wall into a sliding door: when execution is starving, it can RECLAIM storage's space by kicking out cached blocks. And the reason it's execution that gets to bully storage — not the other way around — is that execution work is mid-flight and can't be cheaply redone, while a cached block can always be recomputed from its lineage, so evicting it is the cheaper loss. Where this bites: OOM = a task wanting more than its slice. Two causes — a skewed partition that's just too fat for one task, or bumping parallelism (more tasks at once) without more memory so each slice gets thinner. And the gotcha: the sliding door helps with normal pressure, but it does NOT save you from skew — that one giant partition still lands on one task and still overflows. You fix skew by splitting the partition, not by throwing memory at it.

## Follow-up questions

**Alex:** If execution can reclaim storage memory by evicting cached blocks, does that mean caching an RDD can actually get silently wiped out mid-job and I wouldn't know — and would that hurt performance because Spark then has to recompute it from lineage?

**vutr:** Yes — that's exactly the trade the unified model makes, and it's deliberate. When execution is under pressure it can evict cached blocks to reclaim storage memory, so a block you .cache()'d can be dropped mid-job. You don't get an error because nothing broke: Spark just recomputes that block from its lineage (the recorded chain of transformations that produced it) the next time it's needed. So the cost isn't correctness, it's performance — you pay to rebuild what you thought was cached. That's WHY execution is the one allowed to reclaim from storage and not vice versa: execution work is live and can't be cheaply redone, whereas cached data is always reconstructible from lineage, so it's the cheaper thing to sacrifice. Practical takeaway: caching is a hint, not a guarantee — under execution pressure your cache is the first thing on the chopping block.

**Alex:** The 300MB reserved and the 0.6 fraction are the defaults — but since OOM comes from a task needing more than its share, when would raising spark.memory.fraction above 0.6 actually help, and when is it useless (like the skew case)?

**vutr:** Raising spark.memory.fraction helps in the ordinary case: a task legitimately needs more execution scratch space (a big sort or aggregation, a hash table for a join) and the shortfall is real but modest. Bumping the fraction gives the unified region a bigger pool, so execution has more headroom before it has to spill or fail — this is the 'increased parallelism without increased memory' scenario, where each of many concurrent tasks got a slice that's just slightly too thin. But it's useless against SKEW. If one partition is genuinely larger than any per-task share, the problem is that ONE task must hold more than the executor can give it — a bigger fraction just moves the ceiling up a little while the skewed partition is far above it. The source is explicit: adding memory doesn't fix skew, the skewed partition still lands on one task, and the real fix is breaking that partition apart. So: raise the fraction for broad, mild pressure; split the partition for skew.
