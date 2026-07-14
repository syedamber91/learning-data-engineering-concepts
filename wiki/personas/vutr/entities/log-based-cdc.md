---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: log-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Log-based CDC reads directly from the database's write-ahead log, so it has the lowest impact on the source. The trade-off is the highest complexity of the three approaches — you're now coupled to the internals of how the database journals its changes.

*See also: [[read-replica]] · [[query-based-cdc]] · [[write-ahead-log]] · [[secrets-manager]] · [[trigger-based-cdc]] · [[silent-drift-from-hard-deletion]]*

## Related in the other wiki
- [[Change Data Capture]] — DDIA's note on parsing the replication log (MySQL binlog / PostgreSQL write-ahead log) as the more robust alternative to trigger-based capture — the book-side description of exactly this entity's technique.
- [[Event Sourcing]] — DDIA's application-layer sibling: instead of extracting row-level changes from the log the way log-based CDC does, the app itself writes immutable intent events straight to an append-only store.
