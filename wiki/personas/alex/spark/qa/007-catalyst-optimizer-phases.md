---
persona: alex
kind: concept
sources:
- vutr/catalyst-optimizer-phases
last_updated: '2026-07-10'
qc: passed
slug: 007-catalyst-optimizer-phases
topics:
- spark
learner: alex
source_note: catalyst-optimizer-phases
mastery: mastered
---

*What Alex understood:* Wait, so it's not "Catalyst = query optimizer," it's more like a four-stage factory line, and only two of the four stations are actually "optimizing" anything. Station 1 (analysis) is just a bouncer checking IDs against the Catalog — does this table/column exist, what type is it — and if it can't verify you, you don't get into the building at all, forget optimizing. Station 2 (logical optimization) is RBO: it's applying fixed pattern-match-and-swap rules — predicate pushdown, projection pruning — that don't care what your data actually looks like, just what shape the plan is. Station 3 (physical planning) is where it finally looks at the data — CBO — generates a few candidate plans and picks the cheapest one using stats like row count and cardinality. And I almost said "so RBO and CBO are two different optimizer modes you'd choose" but that's the exact misconception vutr called out — they're not alternatives, they're just two different stations on the same line, RBO always runs first, CBO always runs at the end of physical planning. Station 4 just compiles the winning plan to bytecode.

The part that actually clicked for me is AQE: CBO's cost model is a guess made *before* any data has moved, so it can be wrong. But every shuffle forces Spark to stop and materialize results anyway — that's not wasted time, it's a free checkpoint where AQE can look at what *actually* happened (real partition sizes) and fix the guess, like swapping a sort-merge join for a broadcast join once it sees a side is actually under 10MB. And UDFs are the one place that's a total blind spot for the whole line — the optimizer can't even see inside a UDF, so it skips stations 2 and 3 entirely and just runs it row-by-row in Python.

## Follow-up questions

**Alex:** If AQE can already fix a bad plan for free using real stats at every shuffle boundary, why does Catalyst even bother generating a cost-based guess in phase 3 at all — why not just run the plain RBO plan and let AQE reshape everything once real data shows up?

**vutr:** Because CBO isn't optional busywork — some physical plan has to be chosen and start running before Spark ever reaches a shuffle boundary, and AQE's re-optimization only fires at those stage boundaries, after executors have already materialized intermediate results. Before that first pause, there are no real runtime stats yet, only the row-count/cardinality/min-max statistics CBO has going in. So CBO's job is to make the best upfront call with the information available at compile time; AQE's job is to correct that call using real information that literally doesn't exist until execution has already crossed a shuffle. They're not redundant — CBO covers the gap before any data has moved, AQE covers everything after.

**Alex:** You said UDFs skip the whole four-phase pipeline and fall back to row-at-a-time — but AQE's re-optimization also happens at stage/shuffle boundaries on the physical plan. So is a UDF actually invisible to AQE too (since AQE works off the same plan CBO produced), or can AQE still see the UDF as a node and reshuffle partitions around it even though it can't see inside it?

**vutr:** (the wiki does not cover this — see open questions)
