---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/fundamentals-that-help-you-understand.md
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: nested-loop-join
topics:
- sql-fundamentals-and-execution-model
---

Nested loop join (NLJ) is the most literal way to execute an equi-join: two loops. The outer loop walks every record in the left table; for each of those records, an inner loop walks the right table comparing rows against the join condition, and every match is emitted as a combined row. Its whole appeal is simplicity — it needs no auxiliary data structure like a hash table and no pre-sorted input, unlike [[sort-merge-join]] or [[hash-join]].

The naive version is also the least efficient of the three, because it re-scans the right table once per left-table row. Two refinements attack that cost from different angles. The Block-Nested Loop (BNL) join stops processing the left table row by row and instead reads a whole block of it into a memory buffer at once — a "block," in database terms, being the smallest unit of data a DBMS reads or writes from storage. With a block of left rows buffered, the right table only needs to be scanned once per block rather than once per row, comparing every buffered row against each right-table row as the scan proceeds; this significantly reduces the I/O compared to the naive per-row approach. The other refinement leans on an index: instead of sequentially scanning the whole right table for every left row, the system checks an index on the right table's join column to jump straight to the location of matching rows.

Put together, NLJ performs reasonably well precisely when it avoids its own worst case — when the left table is small (which caps the number of repeated right-table scans) and/or the right table carries an index on the join column, letting the inner loop become an index lookup instead of a full scan.

That size-and-index dependency is also why NLJ falls out of favor for OLAP. The posts are explicit that although PostgreSQL — an OLTP system — supports all three join algorithms, NLJ isn't well suited to OLAP workloads: those systems typically deal with large tables on *both* sides of the join, and they don't maintain point-lookup indexes the way an OLTP system does, so neither of NLJ's two escape hatches (a small left table, an indexed right table) is generally available.

*See also: [[sort-merge-join]] · [[hash-join]] · [[query-lifecycle]]*
