---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: parquet-origin
topics:
- parquet
---

Parquet was born in the early 2010s as a joint effort between Twitter and Cloudera, with version 1.0 released in July 2013. It was designed from the start around the PAX hybrid layout rather than a purely columnar one, which is why its physical model still surprises people who assume 'columnar' means column-at-a-time on disk.
