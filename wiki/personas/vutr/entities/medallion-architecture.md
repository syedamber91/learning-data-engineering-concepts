---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: medallion-architecture
topics:
- dbt
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

The medallion architecture, also coined by Databricks, organizes data into bronze/silver/gold layers. To me it is more of a pattern than an architecture — a reusable solution to a specific problem, not the high-level blueprint of how data is ingested, stored, processed, and served. And don't mistake these layers for data modeling — arranging tables into tiers is not the same as defining how data is structured and related.
