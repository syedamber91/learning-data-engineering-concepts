---
persona: alex
kind: concept
sources:
- vutr/catalyst-optimizer-phases
last_updated: '2026-07-10'
qc: passed
slug: catalyst-optimizer-phases
topics:
- spark
learner: alex
source_note: catalyst-optimizer-phases
mastery: mastered
---

Wait, so it's not "Catalyst = query optimizer," it's more like a four-stage factory line, and only two of the four stations are actually "optimizing" anything. Station 1 (analysis) is just a bouncer checking IDs against the Catalog — does this table/column exist, what type is it — and if it can't verify you, you don't get into the building at all, forget optimizing. Station 2 (logical optimization) is RBO: it's applying fixed pattern-match-and-swap rules — predicate pushdown, projection pruning — that don't care what your data actually looks like, just what shape the plan is. Station 3 (physical planning) is where it finally looks at the data — CBO — generates a few candidate plans and picks the cheapest one using stats like row count and cardinality. And I almost said "so RBO and CBO are two different optimizer modes you'd choose" but that's the exact misconception vutr called out — they're not alternatives, they're just two different stations on the same line, RBO always runs first, CBO always runs at the end of physical planning. Station 4 just compiles the winning plan to bytecode.

The part that actually clicked for me is AQE: CBO's cost model is a guess made *before* any data has moved, so it can be wrong. But every shuffle forces Spark to stop and materialize results anyway — that's not wasted time, it's a free checkpoint where AQE can look at what *actually* happened (real partition sizes) and fix the guess, like swapping a sort-merge join for a broadcast join once it sees a side is actually under 10MB. And UDFs are the one place that's a total blind spot for the whole line — the optimizer can't even see inside a UDF, so it skips stations 2 and 3 entirely and just runs it row-by-row in Python.

*Source: [[catalyst-optimizer-phases]] (vutr)*
