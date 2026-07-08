---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: hudi-index
topics:
- iceberg
---

The index is Hudi's key differentiator and the feature that sets it apart from Delta Lake or Iceberg. It maps hoodie keys to file groups (fileIds), so updates and deletes can be routed to the right files rather than scanned for.
