---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: source
topics:
- data-pipeline-design-framework
---

The source is the one part of the pipeline you don't fully control, so I interrogate it hard: its type, how often to touch it, its performance impact (use a read replica for databases), retention, field availability, schema-change notification, exactly-once reads, delete handling, its data-quality contract, and its availability. And I respect the source team — they should not see my pipeline appear at an abnormal point on their monitoring dashboard.
