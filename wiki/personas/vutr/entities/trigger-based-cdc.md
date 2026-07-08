---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: trigger-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Trigger-based CDC installs database triggers that write changes into a shadow table as they happen. You pay for this with a double-write overhead on every mutation, since each change is now recorded twice.
