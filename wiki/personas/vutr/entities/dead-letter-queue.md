---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: dead-letter-queue
topics:
- data-pipeline-design-framework
---

For a streaming pipeline, bad data goes to a dead-letter queue — the designated place to hold records that fail the rules rather than letting them corrupt the output. The batch equivalent is a dedicated dataset for the same purpose.
