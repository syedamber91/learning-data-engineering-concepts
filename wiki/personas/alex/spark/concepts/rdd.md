---
persona: alex
kind: concept
sources:
- vutr/rdd
last_updated: '2026-07-09'
qc: passed
slug: rdd
topics:
- spark
learner: alex
source_note: rdd
mastery: familiar
---

So an RDD is Spark's most basic piece of data, and I can fully describe one with five things — its partitions (the pieces), a function to compute each piece, its dependencies (what it came from), an optional partitioner just for key-value ones, and optional preferred locations. It never changes once created. And it's lazy: transformations just stack up a DAG plan, and only an action makes Spark actually run everything.

```mermaid
graph LR
  T[Transformations] -->|build up| D[DAG]
  D -->|triggered by| A[Action]
  A --> E[Execution]
```

*Source: [[rdd]] (vutr)*
