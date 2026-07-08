---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pax-vs-dsm-distinction
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

The core lesson is that 'columnar' is not one thing — PAX partitions horizontally into row groups first and only then stores columns together, whereas true DSM only splits vertically with each column stored separately. Most blogs and docs conflate the two, so verifying which one a product actually uses matters.
