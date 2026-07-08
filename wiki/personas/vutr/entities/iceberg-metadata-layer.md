---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: iceberg-metadata-layer
topics:
- iceberg
---

Iceberg's Metadata Layer sits between the Parquet Data Layer and the Catalog Layer, built from manifest files plus a manifest list. Because manifest files hold min/max statistics centrally, planners can prune without opening each Parquet footer.
