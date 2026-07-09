---
persona: alex
kind: concept
sources:
- vutr/executor-memory-model
last_updated: '2026-07-09'
qc: passed
slug: executor-memory-model
topics:
- spark
learner: alex
source_note: executor-memory-model
mastery: mastered
---

Okay, so an executor's heap is basically a stack of layers. Bottom layer: 300MB reserved, hardcoded, off-limits — that's Spark's own emergency cushion, my data never gets it. Then of whatever heap is LEFT after those 300MB, spark.memory.fraction = 0.6 grabs 60% and calls it the unified region — the part my job lives in. That 60% is shared between two roommates: EXECUTION (the live work — shuffles, joins, sorts, the scratchpad a running task scribbles on) and STORAGE (cached/persisted data and broadcasts). Here's the part I want to make sure I've got: before Spark 1.6 those two roommates had FIXED walls — execution couldn't touch storage's half even if storage was mostly empty, so you could OOM with free memory just sitting there unused. The unified model (1.6+) turned the wall into a sliding door: when execution is starving, it can RECLAIM storage's space by kicking out cached blocks. And the reason it's execution that gets to bully storage — not the other way around — is that execution work is mid-flight and can't be cheaply redone, while a cached block can always be recomputed from its lineage, so evicting it is the cheaper loss. Where this bites: OOM = a task wanting more than its slice. Two causes — a skewed partition that's just too fat for one task, or bumping parallelism (more tasks at once) without more memory so each slice gets thinner. And the gotcha: the sliding door helps with normal pressure, but it does NOT save you from skew — that one giant partition still lands on one task and still overflows. You fix skew by splitting the partition, not by throwing memory at it.

```mermaid
graph TD
  A[Executor JVM Heap] --> B[Reserved Memory<br/>300MB hardcoded<br/>never used by data]
  A --> C[Usable = Heap - 300MB]
  C --> D[Unified Region<br/>spark.memory.fraction = 0.6<br/>60% of usable]
  C --> E[User Memory<br/>~40%<br/>user data structures & metadata]
  D --> F[Execution Memory<br/>shuffles, joins, sorts, aggregations]
  D --> G[Storage Memory<br/>cached/persisted RDDs & broadcasts]
  F -. reclaims by evicting cached blocks<br/>Spark 1.6+ unified model .-> G
```

*Source: [[executor-memory-model]] (vutr)*
