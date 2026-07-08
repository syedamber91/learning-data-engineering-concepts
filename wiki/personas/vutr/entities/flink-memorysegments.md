---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: flink-memorysegments
topics:
- flink
---

Flink's MemorySegments are fixed-size 32KB blocks allocated at TaskManager startup. They exist to avoid per-record JVM object allocation, sidestepping the garbage-collection pressure that would otherwise dog a long-running stream job.
