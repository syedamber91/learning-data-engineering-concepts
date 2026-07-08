---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: read-replica
topics:
- change-data-capture-cdc-and-data-sourcing
---

For databases, point the pipeline at a read replica so it reads from the replica while the master stays untouched. This is how you keep CDC from stealing capacity from the system of record.
