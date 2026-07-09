---
persona: alex
kind: concept
sources:
- vutr/shuffle-hash-join
last_updated: '2026-07-09'
qc: passed
slug: 010-shuffle-hash-join
topics:
- spark
learner: alex
source_note: shuffle-hash-join
mastery: learning
---

*What Alex understood:* Alex (learner): Let me try to say it back so I know I get it. Shuffle Hash Join is a Spark way of joining two tables. It got removed in Spark 1.6 and added back in Spark 2.0. It takes the smaller table (the build side), and for each partition it builds a hash table in memory. But the whole build side of a partition has to fit in memory. If one partition is too big because of skew (uneven data), the worker runs out of memory and errors out. And unlike Sort Merge Join, it can't safely spill to disk to save itself. Did I get that right?

## Follow-up questions

**Alex:** Why can't Shuffle Hash Join just spill to disk like Sort Merge Join does when a partition is too big?

**vutr:** Vutr (teacher): Great questions, and honest answer time. For your second question, yes, the note is clear on that: the build side IS the smaller table, so that part I can confirm. For your first question, though, the note only tells us the fact THAT Shuffle Hash Join cannot safely spill to disk while Sort Merge Join can. It doesn't actually explain the deeper reason WHY the spilling isn't safe for SHJ. So the honest answer is: I can tell you it's true, but the note doesn't give us the mechanism behind it, so I won't make something up. Just know that because it can't spill, a skewed partition that doesn't fit in memory leads to that OutOfMemoryError instead of a graceful fallback.

**Alex:** When you say 'build side,' is that always the smaller of the two tables?

**vutr:** (the wiki does not cover this — see open questions)
