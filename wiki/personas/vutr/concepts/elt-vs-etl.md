---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: elt-vs-etl
topics:
- dbt
- history-of-data-engineering
---

ETL has existed since the 1970s, when tightly-coupled, expensive warehouse storage and compute forced us to load only a small curated subset. The shift to ELT happened once cloud data warehouses made it accessible — pay-as-you-go pricing, cheaper storage, faster networks, and columnar storage as standard — making it economical to load raw data first and transform it in place inside the warehouse, rather than transforming before loading. It's not just swapping T and L: it reflects a change in economics and architecture, and it will not completely replace ETL.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]]*
