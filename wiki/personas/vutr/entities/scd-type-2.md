---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: scd-type-2
topics:
- dbt
---

SCD Type 2 (most used) inserts a new row per change with start_date/end_date (9999-12-31 for current) and a surrogate key via MD5 of the natural key. Type 1 overwrites; Type 3 adds columns.
