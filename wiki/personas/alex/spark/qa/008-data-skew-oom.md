---
persona: alex
kind: concept
sources:
- vutr/data-skew-oom
last_updated: '2026-07-09'
qc: passed
slug: 008-data-skew-oom
topics:
- spark
learner: alex
source_note: data-skew-oom
mastery: mastered
---

*What Alex understood:* Let me say it back the way it clicked for me. A partition is one chunk of data that Spark gives to exactly ONE task. Skew means one key hogs a huge partition. Here's the WHY that memory can't fix it: memory is a shared pool, but the skewed partition is indivisible — it's still one lump handed to one task. When I add memory, I'm making the whole pool bigger, but I haven't split the lump, so the lump still goes to one task, and if the lump is bigger than what one task can hold, it dies anyway. It's like a 300-pound suitcase at an airport with a 50-pound-per-bag limit: buying a bigger plane (more total memory) doesn't help because one person still has to lift that one bag. The only fix is repacking it into several bags — breaking the partition apart so the weight spreads across tasks. And the Monday-vs-Thursday thing isn't the data being different — it's that Spark schedules tasks in a different order each run, so sometimes the heavy tasks pile onto the same executor at the same time (crash) and sometimes they don't (survives). Same suitcase, different luck on which bags hit the belt together.

## Follow-up questions

**Alex:** If adding total memory doesn't help because the partition is indivisible, would raising parallelism (more tasks, smaller partitions) fix a SKEWED job? My gut says no — splitting evenly still leaves the one hot key's rows together, plus the source lists 'increased parallelism without increased memory' as its OWN OOM cause, so it feels like that could make things worse, not better. Which is it?

**vutr:** Right instinct. Raising parallelism does NOT fix skew, and it can hurt. Repartitioning cuts the data into more, smaller pieces — but all the rows for the one hot key hash to the SAME partition, so that skewed partition stays whole while everything else gets tinier. You still have one oversized task. Worse, as you flagged, the source lists 'increased parallelism without increased memory' as its own OOM cause: more tasks running concurrently means each task's slice of the fixed memory pool is smaller, so you've now shrunk the budget for the very task that was already too big. The fix isn't more pieces of the same cut — it's changing HOW the hot key is cut, e.g. salting (append a random suffix so one key becomes key-0, key-1, ... spread across partitions) or AQE skew-join handling, which splits the skewed partition specifically. That's the difference between 'more partitions' and 'breaking the skewed partition apart' — only the latter targets the lump.

**Alex:** The source says Sort Merge Join can safely spill to disk but Shuffle Hash Join cannot. If SMJ can spill to disk when it runs low on memory, why doesn't spilling just save a skewed SMJ task from OOM too — does spilling escape the 'one partition, one task' trap or not?

**vutr:** Sharp question, and it's the exact seam. Spilling helps within one task by moving data it isn't actively touching from memory out to disk, so a heavy-but-not-pathological SMJ task survives where a hash join would die. But spilling does NOT escape the 'one partition, one task' trap for true skew. To make progress a task still needs a working set in memory; if the skewed partition is so lopsided that even the minimum in-flight data for that one key exceeds the share, you OOM regardless of spill. SMJ's spill ability raises the survivable ceiling — that's why the source calls SMJ safer and SHJ unable to spill — but it doesn't split the partition, so extreme skew still lands one monster task on one executor and can still crash. Spilling buys headroom; breaking the partition apart removes the cause. That's why the source's fix is the latter, not 'just let it spill.'
