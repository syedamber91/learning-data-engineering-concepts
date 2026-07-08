---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: photon
topics:
- spark
---

Photon is a C++ vectorized query engine that plugs into Databricks Runtime as physical operators, using a columnar in-memory representation instead of Spark SQL's row-oriented layout. Databricks deliberately chose the vectorized (interpreted) approach over code generation — weeks to prototype versus two months, and print-debugging native C++ was far more manageable than debugging runtime-generated code. The JNI overhead came out at just 0.06% of execution time.
