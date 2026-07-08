---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: grain-declaration
topics:
- dbt
---

Declaring the grain is the most critical decision in dimensional modeling: it defines what one row in the fact table represents. Every row in a fact table must sit at the same grain, so I settle this before I ever touch dimensions or facts.
