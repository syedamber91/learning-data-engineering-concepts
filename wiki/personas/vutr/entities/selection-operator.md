---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: selection-operator
topics:
- sql-fundamentals-and-execution-model
---

Relational algebra is the mathematical framework the database uses to translate a declarative SQL query into procedural steps, and Selection (σ) is its most-misunderstood operator. Selection is a unary operator that filters the tuples (rows) of a relation by a predicate — for example, σ salary>500 (Employees) is equivalent to `SELECT * FROM Employees WHERE salary > 500`. The name is the trap: Selection corresponds directly to the WHERE clause, *not* to SELECT, surprisingly.

Projection (Π), by contrast, is the operator that actually does correspond to SELECT: it's a unary operator that picks a subset of a relation's attributes (columns) — Π name, department (Employees) is `SELECT name, department FROM Employees`. The remaining core operators round out the algebra. Union (∪) is a binary operator combining two "union-compatible" relations (same set of columns), keeping all tuples that appear in either or both with duplicates removed — SQL's UNION. Set Difference (−) is a binary operator returning tuples in the first relation but not the second. Cartesian Product (×) is a binary operator combining every tuple of one relation with every tuple of the other, and it is the foundational operation for every SQL JOIN — CROSS JOIN implements it explicitly. Join (⨝) is a binary operator combining data from two relations by condition, and it is fundamentally a Cartesian Product followed by a Selection: an equi-join, specifically, is a Cartesian Product followed by a Selection that keeps only rows where the join keys are equal — the concept behind the whole family of SQL JOIN clauses (INNER, OUTER, and so on). Intersection (∩) is a binary operator returning tuples common to both relations; unlike Join it requires the two relations to share the same schema, and it can be derived from Set Difference (A−B = A ∩ −(A−B)) — it maps to SQL's INTERSECT, which is rarely seen in practice though it remains part of the (optional) ANSI standard.

*See also: [[relational-model]] · [[sql-execution-order]] · [[group-by]] · [[window-functions]]*
