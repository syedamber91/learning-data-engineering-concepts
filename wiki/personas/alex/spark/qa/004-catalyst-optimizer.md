---
persona: alex
kind: concept
sources:
- vutr/catalyst-optimizer
last_updated: '2026-07-09'
qc: passed
slug: 004-catalyst-optimizer
topics:
- spark
learner: alex
source_note: catalyst-optimizer
mastery: mastered
---

*What Alex understood:* Let me walk the whole pipeline to prove I get it. I start with a lazy DataFrame -- it's just a logical plan, nothing runs until an action fires. (1) ANALYSIS: Spark has names I typed but hasn't verified them, so it uses the Catalog to resolve attributes -- bind each column name to a real, typed column and fail early if it's fake. You can't optimize what you haven't verified. (2) LOGICAL OPTIMIZATION: with a valid plan, Catalyst rewrites it cheaper -- predicate pushdown shoves my WHERE filters down to the data source so I read fewer rows, and projection pruning drops columns I never use. It's reshaping WHAT to compute to move less data. (3) PHYSICAL PLANNING: one logical plan has many physical realizations (which join algorithm, how to move data), so Catalyst generates candidates and a cost model picks the cheapest -- that's how a sub-10MB table gets a broadcast join instead of a shuffle. This decides HOW. (4) CODE GENERATION: rather than interpret the plan row by row, Catalyst emits specialized Java via Scala quasiquotes, compiled to JVM bytecode, killing interpretation overhead -- fast, but harder to debug, which is literally why Photon went interpreted-C++ instead. The through-line: Analysis makes it CORRECT and typed, Logical makes it move LESS data, Physical picks the cheapest ALGORITHM, Code Gen makes the execution itself FAST. And because all that planning uses estimates, AQE later re-optimizes at shuffle boundaries with real numbers.

## Follow-up questions

**Alex:** In Phase 2, if predicate pushdown depends on knowing a column is a real, filterable column of a certain type -- does that mean Logical Optimization literally CAN'T run correctly unless Analysis already resolved the attributes via the Catalog? Is that the real reason Analysis has to come first, or is it just convention?

**vutr:** vutr: Exactly right, and that's the deep point -- it's not convention, it's a hard dependency. Predicate pushdown and projection pruning are transformations over a TYPED, resolved tree. To push a filter 'revenue > 100' down to Parquet, Catalyst must know that 'revenue' is a real column, its data type, and which relation it lives in -- all of which is precisely what Analysis produces by resolving attributes against the Catalog. An unresolved plan has dangling names with no type; you literally cannot reason about whether a rewrite is safe or even meaningful. That's why the source orders them Analysis -> Logical Optimization and not the reverse: optimization is defined only over resolved plans. Good instinct catching that the phase order encodes a data dependency, not just a pipeline habit.

**Alex:** The cost model in Phase 3 needs numbers to estimate cost -- but before anything runs, where do those numbers even come from, and if they're just estimates, is that the exact gap that AQE (line 6) was invented to patch at runtime?

**vutr:** vutr: Sharp -- you've found the seam. The cost model's numbers come from statistics: things like table/column stats (row counts, sizes, and when available column-level stats) plus fixed thresholds like autoBroadcastJoinThreshold (10MB). The catch is those are ESTIMATES gathered before the query runs, and they're often wrong -- stale stats, or intermediate results whose size Catalyst can only guess. That is exactly the gap AQE patches. The source says it plainly (line 6): 'A shuffle/broadcast exchange creates a query stage boundary -- the pause enables re-optimization.' At that boundary the ACTUAL sizes are now known, so AQE can do what static Physical Planning couldn't: switch join strategies at runtime, coalesce the 200 default shuffle partitions down to fit real data, and split skewed partitions. So yes: Physical Planning is best-effort with estimates up front; AQE is the runtime correction once reality is measurable. One nuance to keep: AQE doesn't replace the cost model, it re-invokes that same style of decision with better inputs.
