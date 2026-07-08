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

Catalyst is Spark SQL's query optimizer, running four phases: Analysis (resolving attributes against the Catalog), Logical Optimization (predicate pushdown, projection pruning), Physical Planning (choosing plans via a cost model), and Code Generation (turning Scala quasiquotes into Java bytecode). It's the engine that turns your declarative query into an efficient physical plan.

*See also: [[sort-merge-join]] · [[spark-origin]] · [[spark-structured-streaming]] · [[remote-shuffle-service]] · [[shuffle-hash-join]] · [[pyspark]]*
