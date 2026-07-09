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
mastery: familiar
---

So let me say it back: an executor's heap has three parts — a fixed 300MB reserved chunk that's off-limits, then 60% (by default) of what's left is a shared 'unified' pool, and the rest is other stuff. The unified pool is used by both execution and storage, and since Spark 1.6 execution can steal from storage by evicting cached blocks when it needs to. That's why adding more tasks without adding more memory can starve them — the pool doesn't grow, it just gets split thinner. Did I get the reclaim part right?

```mermaid
graph TD
  A[Executor Heap] --> B[300MB Reserved memory - hardcoded, off-limits]
  A --> C[Remaining heap]
  C --> D[Unified pool = spark.memory.fraction, default 0.6]
  C --> E[Rest of remaining heap]
  D --> F[Execution memory: shuffle / sort / join scratch]
  D --> G[Storage memory: cached blocks]
  F -.->|since Spark 1.6: reclaims by evicting cached blocks| G
```

*Source: [[executor-memory-model]] (vutr)*
