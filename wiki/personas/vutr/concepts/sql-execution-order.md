---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sql-execution-order
topics:
- sql-fundamentals-and-execution-model
---

SQL runs in a physical execution order that differs from how you write it: FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT (with window functions) → DISTINCT → ORDER BY → LIMIT/OFFSET. Understanding this order is why WHERE can't see a SELECT alias and why LIMIT applies last.
