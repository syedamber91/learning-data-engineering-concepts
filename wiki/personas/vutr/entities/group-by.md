---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: group-by
topics:
- sql-fundamentals-and-execution-model
---

GROUP BY collapses rows: it takes multiple rows and aggregates them into a single summary row per group. For example, `SELECT product, SUM(sales) FROM tables GROUP BY product` returns exactly one row per product, showing that product's total sales — the original per-transaction rows are gone from the result. In the physical execution order ([[sql-execution-order]]), rows are grouped by GROUP BY before HAVING filters the aggregated groups and SELECT determines the final output columns and aggregated values.

The one point that distinguishes GROUP BY from [[window-functions]] is exactly this collapsing behavior: a window function computes over a set of rows without collapsing them, returning a value per original row rather than one row per group.

*See also: [[window-functions]] · [[sql-execution-order]] · [[selection-operator]]*
