---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: record-batch
topics:
- apache-arrow
---

A Record Batch is Arrow's unit of columnar in-memory data, and like Arrow arrays it is immutable. That immutability is what makes concurrent access to the same data safe.

*See also: [[arrow-flight]] · [[simd-memory-alignment]] · [[apache-arrow]] · [[arrow-ipc]] · [[zero-copy-data-sharing]]*
