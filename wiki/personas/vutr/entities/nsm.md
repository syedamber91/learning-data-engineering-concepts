---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: nsm
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

NSM (N-ary Storage Model), the classic row store, keeps a whole record together, which makes it ideal for OLTP where you want fast insertion and mutation. Its weakness is compression: since data from different columns lacks common patterns, you don't get much squeeze out of it.
