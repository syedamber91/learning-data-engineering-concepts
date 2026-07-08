---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sort-merge-join
topics:
- spark
- sql-fundamentals-and-execution-model
---

The Sort-Merge Join (SMJ) is efficient when its inputs are already sorted on the join columns, and a nice bonus is that it produces sorted output. If you already paid the sorting cost upstream, SMJ is a natural fit.
