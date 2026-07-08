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

SCD Type 2 is the most-used slowly-changing-dimension pattern: on a change it inserts a new row and tracks history with start_date and end_date (9999-12-31 marks the current row), keyed by a surrogate MD5 of the natural key. In the end these are just labels (type n) — do what works for your requirements and don't worry about the naming.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]]*
