---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: sql-fundamentals-and-execution-model
---

Related: [[relational-model]] · [[selection-operator]] · [[group-by]] · [[window-functions]] · [[nested-loop-join]] · [[sort-merge-join]] · [[hash-join]] · [[cte]] · [[sql-execution-order]] · [[query-lifecycle]] · [[oltp-vs-olap-access]]

## Comparisons
Three join strategies trade off along different axes. [[nested-loop-join]] wins when the left table is small or the right table is indexed. [[sort-merge-join]] is best when inputs are already sorted on the join columns and, unlike the others, hands you sorted output for free. [[hash-join]] builds a hash table from the smaller table and probes it — degrading to a Grace Hash Join when memory runs out, or a Broadcast Hash Join that ships the small table to every worker to skip the network shuffle.

On the aggregation side, [[group-by]] and [[window-functions]] look similar but differ on one point: GROUP BY collapses rows into summary rows, while window functions compute over a window without collapsing it.

And on the algebra side, the [[selection-operator]] (σ) maps to WHERE, not SELECT — the projection you write as SELECT is a different operator entirely.

## Open questions
- When the physical planner picks a join, is it choosing cost-based or rule-based, and what tips it toward [[hash-join]] over [[sort-merge-join]] in practice?
- At what data volume does the Grace Hash Join fallback actually kick in for [[hash-join]], and how is the memory threshold determined?
- Given [[oltp-vs-olap-access]], if a look-up index won't help in OLAP, which structures do minimize the volume of data read from storage?
- Where exactly do [[window-functions]] slot into the [[sql-execution-order]] relative to SELECT, and does that constrain what columns they can reference?

## Synthesis
The through-line here is that SQL's surface syntax hides its real machinery. The [[sql-execution-order]] explains why WHERE (the [[selection-operator]] σ, not SELECT) runs before GROUP BY, and why [[group-by]] collapses rows while [[window-functions]] don't. Underneath, the [[query-lifecycle]] turns your text into a physical plan that chooses among [[nested-loop-join]], [[sort-merge-join]], and [[hash-join]] based on table size, sortedness, and indexes. And the workload matters: [[oltp-vs-olap-access]] shows that the map-like lookup which serves OLTP is the wrong tool for OLAP's scan-and-summarize queries — the honest lesson being, as I learned the hard way, everybody speaks SQL in the data world.
