---
persona: vutr
kind: concept
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
- raw/sql-fundamentals-and-execution-model-additional/fundamentals-that-help-you-understand.md
last_updated: '2026-07-15'
qc: passed
slug: query-lifecycle
topics:
- sql-fundamentals-and-execution-model
---

A data professional rarely implements a query processing engine from scratch, but understanding the query life cycle pays off in debugging and optimization. Details vary by database implementation, but the typical process runs through five stages. **Parsing**: the DBMS receives the SQL statement as a string, breaks it into tokens (clauses, operators, identifiers, literal values), checks those tokens against the SQL dialect's grammar (raising "syntax errors" here), and builds an Abstract Syntax Tree (AST) — a hierarchical tree representing the query's grammatical structure. **Validation**: with syntax confirmed, the DBMS checks the query's semantics against the database catalog — its internal metadata repository describing tables, views, and columns — verifying that referenced tables and columns exist and are unambiguous, that filtered values are type-compatible with their columns, and that permissions allow the operation. **Logical Plan**: the validated tree is converted into a logical query plan expressed in relational algebra — a high-level blueprint of the data flow, where the optimizer can already apply optimizations like filter pushdown. **Physical Plan**: the logical plan becomes a physical plan with concrete execution instructions. The optimizer chooses among candidate physical plans using either **Cost-Based Optimization** — generating multiple plans and picking the one with the lowest total I/O, based on statistics like table row counts, cardinality, min/max metadata, and available indexes (e.g. B-Tree) — or **Rule-Based Optimization**, which applies predefined rules instead. This is the stage where the choice among [[nested-loop-join]], [[sort-merge-join]], and [[hash-join]] gets made, weighing table sizes, sortedness, and index availability. **Execution**: the physical plan is sent to workers and followed start to end, with the result returned to the client — and the plan can be dynamically adjusted at runtime, especially in OLAP systems, to adapt to new statistics produced by the plan's own earlier steps that weren't available at planning time.

That dynamic-adjustment note matters for OLAP specifically: because OLAP queries typically join large tables on both sides and lack the point-lookup indexes an OLTP system relies on, the physical-plan stage effectively narrows the field to [[sort-merge-join]] and [[hash-join]], and even the runtime can still swap strategies — Google's Dremel engine, for example, starts a join as a hash join shuffling both sides, then dynamically switches to a broadcast hash join mid-execution if one side turns out small enough.

*See also: [[nested-loop-join]] · [[sort-merge-join]] · [[hash-join]] · [[sql-execution-order]]*
