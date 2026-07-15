---
persona: vutr
kind: concept
sources:
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: materialization-strategies
topics:
- sql-fundamentals-and-execution-model
---

Every SQL query starts with a FROM clause, and FROM needs a "target" to point at. That target is always one of three things — a table, a view, or a materialized view — and the differences between them are entirely about whether and when the result gets physically stored.

A **table** is the physical container for data: inserts, updates, and deletes directly manipulate information stored in structured files on disk, which the database engine organizes into pages for efficient access before exposing the familiar row-and-column abstraction to the user. A table can start empty and be written to later, or be created straight from a query result (`CREATE TABLE AS (SELECT …)`).

A **view** never materializes anything. It's just a stored SQL query; every time it's referenced, that query re-executes from scratch, and the result is retained only for the duration of that execution — the view's query runs fresh, every single time it's accessed. That makes views useful for hiding and reusing complex queries, especially for end users who need to query the data but shouldn't have to know the complexity behind it (which tables to join, for instance). But if a view is referenced frequently in a transformation pipeline and its result set is substantial, the repeated re-execution cost is a reason to materialize it into a table instead. Views also serve as an access-control mechanism: a view can expose only restricted rows (via its WHERE clause) or restricted columns (by selecting only some of them).

A **materialized view (MV)** is the hybrid: like a view, it's defined by a query; like a table, it physically stores that query's result set on disk. When a materialized view is created, the database executes the defining query once and stores the results, and every subsequent read against the materialized view reads that pre-computed, stored data rather than re-running the query. The cost this shifts elsewhere is staleness: because the stored data doesn't automatically track changes to the underlying base tables, it must be refreshed — on a fixed schedule (e.g. hourly), via a full refresh when the source table changes, or via incremental refresh keyed to source-table changes.

A [[cte]] sits outside this whole materialize-or-not spectrum: it isn't a persistent FROM target at all, just a named subquery scoped to the one statement that defines it.

*See also: [[cte]] · [[sql-execution-order]] · [[query-lifecycle]]*
