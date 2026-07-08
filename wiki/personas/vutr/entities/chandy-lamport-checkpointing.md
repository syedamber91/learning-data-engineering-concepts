---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: chandy-lamport-checkpointing
topics:
- flink
---

Flink implements checkpointing using the Chandy-Lamport algorithm, which does not force the application to pause and de-couples checkpointing from data processing. This is what lets Flink take consistent snapshots without stalling the pipeline.
