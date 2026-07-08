---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: query-lifecycle
topics:
- sql-fundamentals-and-execution-model
---

A SQL query moves through a lifecycle: Parsing → Validation → Logical Plan → Physical Plan → Execution. The physical plan is chosen either cost-based or rule-based, and that's where join-strategy decisions get made.

*See also: [[sort-merge-join]] · [[window-functions]] · [[relational-model]] · [[cte]] · [[selection-operator]] · [[hash-join]]*
