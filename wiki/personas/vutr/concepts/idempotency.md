---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: idempotency
topics:
- airflow
- data-pipeline-design-framework
---

For idempotency I make the pipeline itself idempotent, so re-running any step produces the same final result without duplicates, corruption, or inconsistent states. Concretely: every step must be idempotent, overwrite whole tables or partitions rather than doing naive inserts, and avoid non-deterministic functions like now().
