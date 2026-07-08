---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: simd-memory-alignment
topics:
- apache-arrow
---

Arrow aligns its memory buffers to multiples of 8 or 64 bytes, following Intel's AVX-512 guidelines. This alignment is what enables SIMD optimization on top of Arrow data.

*See also: [[record-batch]] · [[arrow-flight]] · [[apache-arrow]] · [[arrow-ipc]] · [[zero-copy-data-sharing]]*
