---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: dimensional-modeling
topics:
- dbt
---

Dimensional modeling, introduced in Ralph Kimball's 1996 The Data Warehouse Toolkit, follows a four-step process: select the business process, declare the grain, identify dimensions, then identify facts. Its ultimate goals are facilitating communication and guiding how we transform, organize, and serve data — not just query performance — and dimension attributes should stay as close to business terminology as possible.
