---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: catalyst-optimizer
topics:
- spark
---

Catalyst phases: Analysis -> Logical Optimization (predicate pushdown, projection pruning) -> Physical Planning (cost model) -> Code Generation (quasiquotes to JVM bytecode).
