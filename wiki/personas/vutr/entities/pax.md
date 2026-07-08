---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pax
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

PAX is the hybrid storage model: data is first split horizontally into row groups, and within each group the column values are stored next to each other. This is what most systems that claim 'column store' are actually running under the hood, not true DSM.
