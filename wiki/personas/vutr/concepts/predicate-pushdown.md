---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: predicate-pushdown
topics:
- parquet
---

Predicate pushdown is the data-skipping payoff of Parquet's min/max statistics: because each column chunk records its min and max in the footer, a reader can rule out whole chunks that can't satisfy a filter without reading them. It's the main reason well-partitioned Parquet is fast for analytical scans.
