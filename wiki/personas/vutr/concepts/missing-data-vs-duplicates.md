---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-15'
qc: passed
slug: missing-data-vs-duplicates
topics:
- data-pipeline-design-framework
---

Missing data is harder to catch than duplicates, because you don't actually know it's missing until you cross-check against the source. Duplicates announce themselves; absence stays silent.

*See also: [[source-constraints-and-schema-risk]] · [[pipeline-failure-recovery-and-checkpointing]] · [[data-quality-rules-and-anomaly-detection]] · [[sink-first-requirements-gathering]] · [[dead-letter-queue-and-bad-data-isolation]] · [[semantic-schema-change]]*
