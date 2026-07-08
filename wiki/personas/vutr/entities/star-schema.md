---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: star-schema
topics:
- dbt
---

The star schema puts a fact table at the center surrounded by dimension tables, deliberately denormalized for query performance. Kimball encourages me to keep low-level measurements in the fact table for flexibility, rather than pre-aggregating away detail I might later need.

*See also: [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]]*
