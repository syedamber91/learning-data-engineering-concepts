---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: scd-type-1-and-3
topics:
- dbt
---

SCD Type 1 simply overwrites, keeping no history, while SCD Type 3 adds new columns to hold a prior value but is used infrequently — in modern SQL a LAG window function over a Type 2 table achieves the same effect. Types 5-7 are hybrid approaches I don't see widely adopted in real life.
