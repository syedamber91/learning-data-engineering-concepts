---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: skew-oom
topics:
- spark
---

OOM is caused by a skewed partition needing more than its share of memory. Adding memory does not fix skew — the fix is breaking the skewed partition apart.
