---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: surrogate-keys
topics:
- dbt
---

Kimball suggests surrogate keys, not operational system keys, as dimension primary keys. In practice I generate them via an MD5 hash of the natural key, which keeps the warehouse decoupled from whatever the source systems happen to use.
