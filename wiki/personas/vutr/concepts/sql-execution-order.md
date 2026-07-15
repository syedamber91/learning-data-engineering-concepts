---
persona: vutr
kind: concept
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: sql-execution-order
topics:
- sql-fundamentals-and-execution-model
---

SQL's clauses are the "verbs" that describe what you want the data to do, and they run in a physical order that differs from the order you write them in. The order is: **FROM / JOIN** — the database first identifies the required tables and performs any joins to build the complete dataset; **WHERE** — filters that dataset, dropping rows that fail the condition (e.g. `A > 3`); **GROUP BY** — groups the remaining rows by one or more columns to prepare them for aggregation ([[group-by]]); **HAVING** — filters out groups that don't meet an aggregate condition (e.g. `SUM(A) > 7`); **SELECT** — determines which columns, expressions, and aggregated values go into the final result (window functions are also processed here, see [[window-functions]]); **DISTINCT** — removes duplicate rows if specified; **ORDER BY** — sorts the final result set; **LIMIT / OFFSET** — caps the output to a specific number of rows. This is presented as covering roughly 95% of real-world SQL queries.

The clearest illustration of why this ordering matters is the contrast between [[group-by]] and [[window-functions]]: GROUP BY collapses multiple rows into one summary row per group, while a window function computes a value for each row over a defined "window" without collapsing anything — both can compute the same aggregate (e.g. `SUM(sales)`), but GROUP BY loses row-level detail that a window function's `OVER (PARTITION BY …)` preserves. That difference is a direct consequence of where each sits in the execution order: GROUP BY runs as its own dedicated stage before SELECT, while window functions are evaluated inside the SELECT stage itself.

*See also: [[group-by]] · [[window-functions]] · [[selection-operator]] · [[query-lifecycle]]*
