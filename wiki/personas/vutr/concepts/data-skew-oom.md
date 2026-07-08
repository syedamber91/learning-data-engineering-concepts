---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: data-skew-oom
topics:
- spark
---

The most stubborn source of Spark OOM is skew — one partition needing more memory than its fair share — and adding more memory doesn't fix it, because the skewed partition still lands on a single task that still needs more than you can give. The real fix is to break the skewed partition apart. Skew also explains why the same job passes on Monday and fails on Thursday: a different scheduling order, not a change in data volume, produces a different outcome.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[shuffle-hash-join]] · [[catalyst-optimizer]]*
