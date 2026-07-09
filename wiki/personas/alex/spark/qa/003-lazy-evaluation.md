---
persona: alex
kind: concept
sources:
- vutr/lazy-evaluation
last_updated: '2026-07-09'
qc: passed
slug: 003-lazy-evaluation
topics:
- spark
learner: alex
source_note: lazy-evaluation
mastery: mastered
---

*What Alex understood:* Here is how I would say it back. When I write filter, select, join and so on, Spark does not actually run any of them. Those are transformations, and they are lazy - each one just adds a node to a DAG, a dependency graph of steps with no cycles (line 4). My code is really building a logical plan, not a result (line 26). The plan just sits there. Only when I call an action - count, collect, or write to disk, the 'special output operation' from line 26 - does Spark finally trigger execution of the whole DAG (line 4). The payoff of waiting: because Spark holds the entire plan before running it, the Catalyst optimizer (line 5) can rewrite the whole thing first. In its Logical Optimization phase it does predicate pushdown (shove filters down early so fewer rows get read) and projection pruning (throw away columns nobody uses). Those global rewrites are only possible because nothing ran yet - if each transformation executed on the spot, it would be too late to move a later filter earlier. So the mechanism is: lazy transformations build the DAG -> action triggers -> Catalyst optimizes the full plan -> then it runs. Laziness is not slowness; it is Spark buying itself the chance to be smart about the whole job at once.

## Follow-up questions

**Alex:** The source says Catalyst optimizes before running, and separately that AQE (line 6) re-optimizes at runtime at a shuffle 'query stage boundary.' If Catalyst already optimized the whole plan up front thanks to laziness, why is a SECOND round of optimization at runtime needed - what does AQE know at the shuffle boundary that the lazy up-front pass could not know?

**vutr:** vutr: Good instinct - you spotted the tension exactly. The up-front Catalyst pass is smart but blind to one thing: the actual data. When it does predicate pushdown and projection pruning, it is reasoning about the SHAPE of the plan, not the real sizes and distributions, because no data has moved yet (that is the whole point of laziness - decide before moving data). AQE (line 6) only kicks in at a shuffle or broadcast exchange, and the source is precise about why: 'A shuffle/broadcast exchange creates a query stage boundary - the pause enables re-optimization.' At that boundary Spark has just written and measured real shuffle output, so now it knows true partition sizes. That is knowledge the lazy up-front pass literally could not have. With it, AQE does three things the source lists: it coalesces shuffle partitions (the default is a fixed 200 regardless of data size per line 8, often wrong, so it merges tiny ones), it switches join strategies at runtime (e.g. discover a side is small enough to broadcast under the 10MB autoBroadcastJoinThreshold, line 8/10), and it handles skew joins by splitting an oversized partition - which line 9/21 calls the only real fix for skew. So: laziness buys the up-front structural optimization; the exchange pause buys the data-aware optimization. Two different kinds of knowledge, two passes.

**Alex:** If transformations only build a plan and never run, what happens to that carefully built DAG when I call two separate actions on the same DataFrame - does the lazy plan get executed from scratch both times, or is the built-up plan reused?

**vutr:** vutr: This is the sharp edge of laziness and the source hints at it without spelling it out, so I will flag the honest limit. The source establishes that a DataFrame 'represents a logical plan' and 'no execution occurs until the user calls a special output operation' (line 26). It does not, in this material, say what happens across two separate actions. Mechanically, from what the source DOES give us: each action triggers execution of the DAG (line 4), and the plan is a description, not a cached result - so by default each action re-runs the plan from its sources. Line 26's framing ('a logical plan to compute a dataset', recomputed on the output operation) is consistent with recompute-per-action. The source mentions Spark's in-memory reputation and unified storage memory (line 7) and reduceByKey reducing data before shuffle (line 13), but it never introduces caching/persist as the escape hatch for repeated actions - so I will not claim it does. Honest answer: two actions means two triggers, and nothing in THIS source promises the built plan is reused between them; whether persist/cache would change that is beyond what the source states.
