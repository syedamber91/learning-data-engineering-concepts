---
persona: alex
kind: concept
sources:
- vutr/sort-merge-join
last_updated: '2026-07-09'
qc: passed
slug: 009-sort-merge-join
topics:
- spark
learner: alex
source_note: sort-merge-join
mastery: mastered
---

*What Alex understood:* SMJ = shuffle both sides, sort each partition, zipper-merge the two sorted runs. It's the safe default because a sort can SPILL TO DISK, so a partition bigger than memory just gets slower, not fatal. SHJ builds an in-memory hash table on the small side and streams the big side through it — faster, but the build side MUST fit in memory, so a skewed partition throws OOM (no on-disk hash table exists). BHJ skips shuffling entirely by copying a <10MB table to every executor. Bucket join skips the shuffle by pre-partitioning at write time. Hint order BROADCAST > MERGE > SHUFFLE_HASH ranks them fastest-when-applicable down to the fragile fallback.

## Follow-up questions

**Alex:** If AQE (Adaptive Query Execution, Spark 3.0) can switch join strategies at runtime, why is SMJ still the default one the planner picks BEFORE runtime — why not just start with the faster SHJ and let AQE fix it if it OOMs?

**vutr:** vutr: Good instinct, but you've got the failure cost backwards. The planner picks SMJ first precisely because a wrong guess is expensive to recover from. Before runtime, the cost model doesn't reliably know partition sizes or skew — that's exactly the information that's missing until data actually moves. If it optimistically started with SHJ and a skewed partition blew the executor's memory, you don't get a clean 'oops, switch strategies' — you get an OutOfMemoryError that can kill the task and cascade into stage/job failure, and the same job can 'pass on Monday and fail on Thursday' because scheduling order changed which partition landed where. AQE re-optimizes at query-STAGE boundaries created by a shuffle exchange — it coalesces partitions and handles skew — but it works by making the SAFE strategy adaptive, not by rescuing a strategy that already crashed. So the design principle is: default to the strategy that CANNOT fail catastrophically (SMJ spills), and let broadcast be the runtime UPGRADE when AQE sees a side is actually tiny. You start safe and get faster, never start fast and hope you don't die.

**Alex:** The source says adding more memory doesn't fix a skewed partition. But SHJ OOMs on skew and SMJ survives skew by spilling — so does that mean for a badly skewed join you'd actually WANT SMJ even though it's slower, and is spilling-to-disk really 'safe' or does it just move the pain to being really slow?

**vutr:** vutr: Yes — you've reasoned to exactly the right place, and you also caught the honest caveat. For a badly skewed join, SMJ is what keeps the job ALIVE, because SHJ's build side won't fit and throws OOM, while SMJ spills the oversized sorted run to disk and finishes. So 'safe' here means 'completes without crashing,' NOT 'fast.' You're right to be suspicious: spilling moves the pain, it doesn't erase it — that skewed partition still lands on one task, still has to be sorted through disk, and becomes a straggler that drags the whole stage. The source is blunt about this: 'Adding more memory won't help here... The right fix is to break the skewed partition apart.' So the real hierarchy is three levels: SHJ = crashes on skew; SMJ = survives skew but crawls; and the actual FIX = salting or otherwise splitting the hot key so no single partition is oversized in the first place. SMJ safety is the seatbelt that stops the crash; fixing the skew is not driving into the wall.
