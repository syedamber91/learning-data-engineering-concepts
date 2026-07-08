---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: nested-loop-join
topics:
- sql-fundamentals-and-execution-model
---

The Nested Loop Join (NLJ) performs well when the left table is small or the right table has an index. It's the simplest join strategy but its cost grows quickly when neither of those conditions holds.
