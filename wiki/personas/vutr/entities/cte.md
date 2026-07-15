---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: cte
topics:
- sql-fundamentals-and-execution-model
---

A Common Table Expression (CTE) is the odd one out among the FROM-clause "targets" a query can reference: unlike a table, a view, or a materialized view, a CTE is only referenced inside the single query where it's defined — think of it as a temporary, convenient name for a subquery, scoped to that one statement. See [[materialization-strategies]] for how it contrasts with the three that do persist beyond a single query.

The value CTEs add is entirely about how a query reads, not how it executes: instead of nesting queries inside other queries — producing what's often called "spaghetti code" — a CTE lets you break a complex problem down into a series of logical, readable steps, each named and referenced in order.

*See also: [[materialization-strategies]] · [[sql-execution-order]]*
