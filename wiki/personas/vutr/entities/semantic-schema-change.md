---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-15'
qc: passed
slug: semantic-schema-change
topics:
- data-pipeline-design-framework
---

A semantic schema change is the hardest failure to catch: the column still exists and the type is unchanged, but its meaning has shifted. You only notice it when a dashboard starts showing a weird trend.

*See also: [[source-constraints-and-schema-risk]] · [[pipeline-failure-recovery-and-checkpointing]] · [[data-quality-rules-and-anomaly-detection]] · [[sink-first-requirements-gathering]] · [[dead-letter-queue-and-bad-data-isolation]] · [[missing-data-vs-duplicates]]*
