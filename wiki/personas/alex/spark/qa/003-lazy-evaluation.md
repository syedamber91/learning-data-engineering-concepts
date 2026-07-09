---
persona: alex
kind: concept
sources:
- vutr/lazy-evaluation
last_updated: '2026-07-09'
qc: passed
slug: 003-lazy-evaluation
topics:
- spark
learner: alex
source_note: lazy-evaluation
mastery: familiar
---

*What Alex understood:* So Spark waits. My transformations just add steps to a plan (a DAG), and nothing runs until I ask for a result with an action or output. A Spark DataFrame is a recipe, not the cooked meal, unlike Pandas which cooks immediately. And waiting is good because Catalyst can improve the whole recipe before Spark runs it.

## Follow-up questions

**Alex:** What actually makes Spark start running the plan instead of just adding to it?

**vutr:** Spark starts running only when an action or an output operation is called. Until then, transformations just keep building the logical plan (the DAG) and nothing executes.

**Alex:** Why is being lazy a good thing instead of just slow?

**vutr:** Because Spark defers work and holds the whole plan before running it, the Catalyst optimizer gets room to optimize it. A Spark DataFrame is a plan to compute a dataset rather than the computed dataset itself, and that plan-first approach is exactly what lets Catalyst make it better before real work happens.
