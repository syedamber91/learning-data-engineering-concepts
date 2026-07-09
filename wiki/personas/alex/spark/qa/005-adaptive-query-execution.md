---
persona: alex
kind: concept
sources:
- vutr/adaptive-query-execution
last_updated: '2026-07-09'
qc: passed
slug: 005-adaptive-query-execution
topics:
- spark
learner: alex
source_note: adaptive-query-execution
mastery: mastered
---

*What Alex understood:* Here's how I'd say it back. A normal Spark query gets planned ONCE at the start, and the planner is guessing at data sizes with a cost model. AQE (new in Spark 3.0) refuses to commit to those guesses. The trick is the query-stage boundary. A shuffle or broadcast exchange splits the plan into stages, and because the map side of a shuffle has to fully finish and write to disk before the reduce side reads, there's a forced pause there. That pause is a checkpoint where Spark can peek at the shuffle output that was really written and get REAL statistics — actual total size, actual per-partition sizes — instead of estimates. Then it re-optimizes the rest of the plan before running it. With the real numbers it can: coalesce the dumb fixed 200 shuffle partitions down to a sensible number if the data is small; flip a Sort Merge Join into a Broadcast Hash Join if a side really came in under the 10MB broadcast threshold; and split a skewed partition apart so one monster task doesn't OOM. So the whole idea is: the exchange boundary buys a pause, the pause buys real statistics, and real statistics buy a smarter plan for the part that hasn't run yet.

## Follow-up questions

**Alex:** The source says a shuffle OR a broadcast exchange creates a query-stage boundary. A shuffle I get — the map side writes to disk and the reduce side has to wait, so there's a real pause with real output to measure. But a broadcast exchange doesn't shuffle across the whole cluster the same way. Why does a broadcast exchange also count as a re-optimization boundary?

**vutr:** Good instinct to separate the two. With a shuffle, the boundary is unmistakable: the map side must materialize its output to disk (remember — Spark shuffle writes to disk, not memory, despite the in-memory reputation) before the reduce side reads, so there is a hard hand-off AND real written bytes to measure. A broadcast exchange is a boundary for the same structural reason even though the data movement is different: the broadcast side has to be fully collected and built before the downstream join operator can consume it. That 'must be complete before the next operator runs' hand-off is exactly what a query-stage boundary IS. So both are boundaries because both force the upstream to finish and produce a concrete, measurable artifact before the downstream starts — that completed artifact is what Spark measures to get real statistics. The source lists them together precisely because both create that pause; the pause, not the specific transport, is what enables re-optimization.

**Alex:** The source says default shuffle partitions is 200 regardless of data size, and AQE coalesces them. Does AQE ever go the OTHER way and SPLIT partitions, or is coalescing strictly a merge-down operation — and is splitting for skew a separate mechanism from the coalescing?

**vutr:** Coalescing and skew handling are described as distinct capabilities in the source — it lists 'dynamically coalesces shuffle partitions' and 'handles skew joins' as separate items. Coalescing is the merge-down direction: the fixed 200 partitions are often way too many for small real data, so Spark measures the real sizes at the boundary and merges adjacent small partitions into fewer right-sized ones — fewer wasteful near-empty tasks. Skew handling is the opposite motion and a separate mechanism: when the real per-partition statistics reveal one partition is dramatically larger than the rest, Spark splits that one skewed partition apart into sub-partitions so the load spreads across tasks. That directly implements the OOM fix the source insists on — adding memory won't help because the skewed partition still lands on one task; the fix is to break it apart. So: coalesce = merge many small ones down (efficiency), skew handling = split one big one up (avoid the OOM). Same enabling trick, real statistics at the stage boundary, applied in opposite directions.
