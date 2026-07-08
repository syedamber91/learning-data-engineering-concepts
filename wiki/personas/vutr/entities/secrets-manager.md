---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: secrets-manager
topics:
- change-data-capture-cdc-and-data-sourcing
---

Credentials belong in a secrets manager, not in a .env file checked into the repo. Pair this with the principle of least privilege — grant the pipeline the fewest permissions it can possibly run with.

*See also: [[log-based-cdc]] · [[read-replica]] · [[query-based-cdc]] · [[write-ahead-log]] · [[trigger-based-cdc]] · [[silent-drift-from-hard-deletion]]*
