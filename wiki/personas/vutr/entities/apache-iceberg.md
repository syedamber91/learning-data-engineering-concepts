---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-iceberg
topics:
- iceberg
---

Iceberg layers a Data Layer of Parquet files under a Metadata Layer of manifest files and a manifest list, topped by a Catalog Layer that commits via an atomic pointer swap. Its manifest files store min/max statistics, centralizing what Parquet otherwise keeps per-file in each footer. It also supports hidden partitioning and partition evolution, and DoorDash chose it over Delta Lake for its more mature Flink support.

*See also: [[iceberg-metadata-layer]] · [[hudi-index]] · [[conditional-writes]] · [[hudi-timeline]] · [[open-table-formats]] · [[copy-on-write-vs-merge-on-read]]*
