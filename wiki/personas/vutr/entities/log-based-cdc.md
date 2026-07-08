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
