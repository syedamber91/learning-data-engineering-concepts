---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sink
topics:
- data-pipeline-design-framework
---

The sink is where I begin every pipeline design — more accurately, I start from the end users and the business purpose they need served. Its questions decide everything downstream: the shape of the output, how it's served, how stale data can be, the usage and retention patterns, and whether the sink can even support atomicity.
