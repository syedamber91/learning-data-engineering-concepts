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
mastery: familiar
---

*What Alex understood:* So let me say it back: an executor's heap has three parts — a fixed 300MB reserved chunk that's off-limits, then 60% (by default) of what's left is a shared 'unified' pool, and the rest is other stuff. The unified pool is used by both execution and storage, and since Spark 1.6 execution can steal from storage by evicting cached blocks when it needs to. That's why adding more tasks without adding more memory can starve them — the pool doesn't grow, it just gets split thinner. Did I get the reclaim part right?

## Follow-up questions

**Alex:** You said execution can reclaim storage memory by evicting cached blocks — can it go the other way too, where storage kicks out execution when caching needs room?

**vutr:** On your first question — the note only tells me one direction: execution memory can reclaim storage memory by evicting cached blocks when it needs to. It does NOT say whether storage can push back against execution, so I honestly can't confirm the reverse from this note.

**Alex:** The 60% is 'of what remains' after the 300MB — so is the 300MB taken out BEFORE the 0.6 is applied, or after?

**vutr:** On the second — the note phrases it as '300MB is hardcoded as reserved memory, and of what remains, spark.memory.fraction (default 0.6)...'. So the 300MB comes out first, and the 0.6 fraction applies to what remains after that. The exact arithmetic formula isn't spelled out beyond that ordering.
