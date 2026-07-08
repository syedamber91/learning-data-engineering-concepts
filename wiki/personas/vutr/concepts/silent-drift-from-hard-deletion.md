---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: silent-drift-from-hard-deletion
topics:
- change-data-capture-cdc-and-data-sourcing
---

When the source hard-deletes rows, the pipeline keeps accumulating records and slowly drifts away from the source — and nobody notices until someone manually reconciles months later. This is the quiet failure mode: missing data is harder to catch than duplicates because we don't know it's missing until we cross-check against the source.

*See also: [[log-based-cdc]] · [[read-replica]] · [[query-based-cdc]] · [[write-ahead-log]] · [[secrets-manager]] · [[trigger-based-cdc]]*
