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
mastery: mastered
---

*What Alex understood:* Let me say it back so I know I actually get it. SHJ = shuffle first (repartition both tables by key so matching keys share a partition), then inside each partition build a hash table from the SMALLER side and probe it with the bigger side for O(1) lookups. The catch is that the ENTIRE build-side partition has to sit in memory at once as that hash table — a hash table is useless half-built, you can't probe it. So if one partition is fat (usually because of skew — one key hogging the rows), its build side won't fit, and the executor OOMs. The reason it OOMs and SMJ doesn't is that SMJ only sorts and walks with pointers, so it can dump sorted chunks to disk and merge them later — it spills. SHJ can't spill because it needs the whole hash table resident. That's the exact reason SHJ got yanked in 1.6 and only came back in 2.0, and why the priority is BROADCAST > MERGE > SHUFFLE_HASH. And it's the same story as the skew-OOM lesson: throwing more RAM at it doesn't help, you have to split the skewed partition.

## Follow-up questions

**Alex:** If SHJ needs the build side in memory and that's dangerous, why does Broadcast Hash Join — which ALSO builds a hash table in memory — sit at the TOP of the priority list (BROADCAST > MERGE > SHUFFLE_HASH) instead of being even riskier?

**vutr:** vutr answering Q1: Great instinct — the difference is WHICH side is guaranteed small, and the source gives the number. Broadcast Hash Join only triggers 'below autoBroadcastJoinThreshold,' default 10MB. So the build side in a broadcast join is a table Spark has already confirmed is tiny — under 10MB — and it's broadcast whole to every executor, no shuffle needed. The 10MB gate is a hard safety bound: you know it fits before you start. SHJ has no such guaranteed cap: its build side is just 'the smaller table' relative to the other, and per-partition after a shuffle that partition can still be huge if the key is skewed. So both build hash tables in memory, but broadcast is bounded-by-threshold-and-verified-small, while SHJ is only relatively-smaller-and-unbounded. That's why broadcast ranks safest and SHJ ranks last — same mechanism, wildly different worst case.

**Alex:** AQE was introduced in Spark 3.0 and the source says it 'handles skew joins' and 'switches join strategies at runtime.' If skew is exactly what makes SHJ OOM, can AQE just rescue a SHJ that's about to blow up — and if so why isn't SHJ safe again?

**vutr:** vutr answering Q2: Sharp question, and the source lets me answer it precisely without overclaiming. AQE (Spark 3.0, 2020) does two relevant things: it 'switches join strategies at runtime' and it 'handles skew joins,' and the reason it can is that 'a shuffle/broadcast exchange creates a query stage boundary — the pause enables re-optimization.' So at that boundary AQE sees the ACTUAL partition sizes (not just planner estimates) and can react — e.g. split a skewed partition apart (which is exactly the source's prescribed fix, 'break the skewed partition apart') or pick a different join. That's what makes SHJ less of a footgun in modern Spark: AQE can defuse the skew before SHJ ever tries to build an oversized hash table. But — and this is the honest limit — the source never says AQE makes SHJ itself able to spill. SHJ's own mechanism still 'cannot' spill (that property is unchanged); AQE prevents the bad partition from reaching SHJ rather than making SHJ survive it. And AQE only re-optimizes at exchange boundaries, so it isn't a blanket guarantee. So: AQE greatly reduces the OOM risk in practice, but SMJ is still 'the preferred join strategy' and BROADCAST > MERGE > SHUFFLE_HASH still holds.
