---
persona: alex
kind: concept
sources:
- vutr/adaptive-query-execution
last_updated: '2026-07-10'
qc: passed
slug: 008-adaptive-query-execution
topics:
- spark
learner: alex
source_note: adaptive-query-execution
mastery: mastered
---

*What Alex understood:* Wait, so — okay, I think I had it backwards. I thought Spark basically wrote out the *entire* route before the trip even started, like typing an address into GPS once and just driving blind even if there's traffic. But that's not it. It's more like a road trip where Spark is only allowed to check traffic conditions at rest stops — and the rest stops are the stage boundaries, because that's the point where every car (partition) has already arrived and the results are physically written down. Spark can't peek at traffic mid-highway, only at the stop, because the next leg of the trip literally can't start until everyone's pulled in anyway. So AQE isn't adding a new pause — it's just finally using a pause that was already happening.

And then at that rest stop it does three things. If the 200 default shuffle partitions turn out to be way more lanes than it needs — like the TPC-H example where 200 collapsed into basically one — it merges them so it's not paying overhead moving between a bunch of near-empty lanes. If one lane got way overloaded instead, it splits it so one truck isn't holding up the whole convoy. And for joins, it's not guessing anymore whether the small side fits in memory — pre-Spark-3 it always played it safe with sort-merge join because a shuffle-hash join that guesses wrong just crashes (OOM) if a partition is bigger than expected from skew, while sort-merge can just spill to disk. Now that it has the real post-shuffle size at the rest stop, it can actually risk the faster hash join, or even upgrade to a broadcast join, when the real numbers say it's safe.

The part that clicked hardest: this isn't AQE being magic, it's AQE cashing in a pause Spark was going to take anyway.

## Follow-up questions

**Alex:** Splitting oversized partitions is called 'the mirror case' of coalescing, but coalescing clearly happens after the shuffle write, using exact post-shuffle sizes at the rest-stop boundary. Does splitting also wait for that same boundary, or does Spark have to detect the straggler partition earlier, while it's still mid-stage, before it's even finished writing?

**vutr:** Yes — out of the box, AQE's shuffle-hash-join conversion is effectively dormant. The note is explicit that spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold defaults to 0, and at 0 'Spark will always skip shuffle hash join unless you raise it.' That's exactly why the hands-on join project had to deliberately set it to 256MB (and flip spark.sql.join.preferSortMergeJoin to False) just to exercise that path at all — a default cluster wouldn't take it. The broadcast-join conversion, by contrast, uses spark.sql.autoBroadcastJoinThreshold, which the note gives a real non-zero default (10MB), so that upgrade path is live without any config changes — AQE can convert a sort-merge join to broadcast the moment a side's post-filter/aggregation size drops under 10MB. So yes: for most people who never touch the shuffle-hash threshold, the broadcast-join conversion is the one they actually get for free.

**Alex:** The shuffle-hash-join threshold defaults to 0, which you said means Spark always skips shuffle hash join unless someone raises it. So out of the box, does that mean AQE's join-strategy switching basically never fires for shuffle hash join in a default cluster, and the only join upgrade most people actually get for free is the broadcast-join conversion?

**vutr:** (the wiki does not cover this — see open questions)
