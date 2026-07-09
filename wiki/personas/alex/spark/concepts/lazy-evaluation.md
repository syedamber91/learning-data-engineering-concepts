---
persona: alex
kind: concept
sources:
- vutr/lazy-evaluation
last_updated: '2026-07-09'
qc: passed
slug: lazy-evaluation
topics:
- spark
learner: alex
source_note: lazy-evaluation
mastery: familiar
---

So Spark waits. My transformations just add steps to a plan (a DAG), and nothing runs until I ask for a result with an action or output. A Spark DataFrame is a recipe, not the cooked meal, unlike Pandas which cooks immediately. And waiting is good because Catalyst can improve the whole recipe before Spark runs it.

```mermaid
flowchart LR
    A[Transformations] --> B[Build logical plan / DAG]
    B --> C{Action or output called?}
    C -- No --> B
    C -- Yes --> D[Catalyst optimizes plan]
    D --> E[Execute]
```

*Source: [[lazy-evaluation]] (vutr)*
