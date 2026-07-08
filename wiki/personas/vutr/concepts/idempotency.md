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
---

Idempotency means performing the same operation multiple times produces the same result as performing it once, and it is a required property of any well-designed pipeline task. In practice: overwrite instead of append, use MERGE/upsert on a unique key, and avoid non-deterministic functions like NOW(), CURRENT_TIMESTAMP, and RAND(). One more important note — idempotency must be end-to-end, otherwise it's not effective.
