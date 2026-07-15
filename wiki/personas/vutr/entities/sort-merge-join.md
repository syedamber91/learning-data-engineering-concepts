---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/fundamentals-that-help-you-understand.md
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: sort-merge-join
topics:
- sql-fundamentals-and-execution-model
---

Sort-merge join (SMJ) carries out two phases. First, the system sorts both input tables on their join columns. Second, it walks through both sorted tables with a pointer on each: if the join condition matches, the rows are combined (and if the current join-key value has duplicates in one or both tables, all combinations of matching rows must be generated — which can mean moving one pointer backward while the other moves forward); if the left pointer's value is less than the right's, the left pointer advances; if the right's is less, the right pointer advances. This continues until one or both tables are exhausted.

Compared to [[nested-loop-join]], SMJ pays an extra cost up front — sorting both tables — but that cost is what buys the efficient merge walk afterward. It becomes particularly cheap when the inputs are already sorted on the join columns, or already carry clustered indexes on those columns (a clustered index means the database physically sorts and stores rows by the index columns), since that eliminates or shrinks the sort phase entirely. SMJ also pairs well with a query that needs its output sorted by the join key — an `ORDER BY` on that key comes essentially for free, since the merge phase already produces sorted output as a side effect.

Despite that efficiency, the vutr posts describe hash join as more widely used in OLAP systems in practice: Snowflake uses hash join for most cases and BigQuery only supports hash joins, leaving Spark as the main OLAP engine offering SMJ as a real alternative to [[hash-join]].

*See also: [[hash-join]] · [[nested-loop-join]] · [[query-lifecycle]]*
