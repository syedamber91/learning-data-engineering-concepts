---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: hash-join
topics:
- sql-fundamentals-and-execution-model
---

The Hash Join has a build phase, where the smaller table is loaded into a hash table, and a probe phase against it. When the hash table exceeds memory you fall back to a Grace Hash Join, and the Broadcast Hash Join variant sends the small table to all workers to skip the expensive network shuffle.

*See also: [[sort-merge-join]] · [[window-functions]] · [[relational-model]] · [[cte]] · [[selection-operator]] · [[group-by]]*
