---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: query-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Query-based CDC polls the source table on an interval, which means it requires an updated_timestamp column to know what changed. Its blind spot is that it cannot track DELETEs — a row that vanishes leaves no trace for the polling query to catch.

*See also: [[log-based-cdc]] · [[read-replica]] · [[write-ahead-log]] · [[secrets-manager]] · [[trigger-based-cdc]] · [[silent-drift-from-hard-deletion]]*
