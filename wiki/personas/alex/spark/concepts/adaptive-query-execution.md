---
persona: alex
kind: concept
sources:
- vutr/adaptive-query-execution
last_updated: '2026-07-09'
qc: passed
slug: adaptive-query-execution
topics:
- spark
learner: alex
source_note: adaptive-query-execution
mastery: learning
---

So basically AQE (new in Spark 3.0) lets Spark rewrite its own plan mid-query. It can merge shuffle partitions, swap which join method it uses, and deal with lopsided skew joins. And it can only do this because a shuffle or broadcast creates a pause point (a query stage boundary), and that pause is where Spark checks the real data stats and fixes its plan.

```mermaid
flowchart TD
    A[Query starts with initial plan] --> B[Shuffle or broadcast exchange]
    B --> C[Query stage boundary = a pause]
    C --> D[Spark reads real statistics]
    D --> E{Re-optimize with real numbers}
    E --> F[Coalesce shuffle partitions]
    E --> G[Switch join strategy]
    E --> H[Handle skew joins]
```

*Source: [[adaptive-query-execution]] (vutr)*
