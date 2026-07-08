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
---

ETL has existed since the 1970s, when tightly-coupled, expensive warehouse storage and compute forced us to load only a small curated subset. ELT became accessible with cloud warehouses — pay-as-you-go pricing, cheaper storage, faster networks, columnar storage as standard — moving transformation from outside to inside the warehouse; it's not just swapping T and L, it reflects a change in economics and architecture, and it will not completely replace ETL.
