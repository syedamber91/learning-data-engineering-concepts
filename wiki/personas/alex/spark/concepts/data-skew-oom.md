---
persona: alex
kind: concept
sources:
- vutr/data-skew-oom
last_updated: '2026-07-09'
qc: passed
slug: data-skew-oom
topics:
- spark
learner: alex
source_note: data-skew-oom
mastery: learning
---

So skew is when one partition is way bigger than the others, and because that big partition goes to just one task, adding more memory doesn't help — you have to split that partition up. And that's also why the same job can randomly pass one day and fail another: it's the scheduling order, not the data size, that changed.

```mermaid
flowchart TD
    A[Skewed partition\n(way bigger than the rest)] --> B[Lands on a single task]
    B --> C[Task needs more memory\nthan can be given]
    C --> D[OOM]
    C -.more total memory\ndoesn't help.-> C
    A --> E[Real fix:\nbreak the partition apart]
```

*Source: [[data-skew-oom]] (vutr)*
