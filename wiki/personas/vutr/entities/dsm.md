---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: dsm
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

DSM (Decomposition Storage Model) is the true column store, where each column's values are stored completely separately. Because every value in a column has the same length, the DBMS can locate the i-th value directly by computing first_element_address + i * element_size.
