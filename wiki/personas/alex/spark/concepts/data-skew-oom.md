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
mastery: mastered
---

Let me say it back the way it clicked for me. A partition is one chunk of data that Spark gives to exactly ONE task. Skew means one key hogs a huge partition. Here's the WHY that memory can't fix it: memory is a shared pool, but the skewed partition is indivisible — it's still one lump handed to one task. When I add memory, I'm making the whole pool bigger, but I haven't split the lump, so the lump still goes to one task, and if the lump is bigger than what one task can hold, it dies anyway. It's like a 300-pound suitcase at an airport with a 50-pound-per-bag limit: buying a bigger plane (more total memory) doesn't help because one person still has to lift that one bag. The only fix is repacking it into several bags — breaking the partition apart so the weight spreads across tasks. And the Monday-vs-Thursday thing isn't the data being different — it's that Spark schedules tasks in a different order each run, so sometimes the heavy tasks pile onto the same executor at the same time (crash) and sometimes they don't (survives). Same suitcase, different luck on which bags hit the belt together.

```mermaid
graph TD
    A[Input data with one hot key] --> B[Skewed partition: all hot-key rows glued together]
    B --> C[Spark hands the whole partition to ONE task]
    C --> D{Does the task fit in its memory share?}
    D -->|No, partition too big| E[OutOfMemoryError]
    F[Add more total memory] -.-> G[Partition still indivisible]
    G -.-> C
    E --> H[Real fix: break the skewed partition apart]
    H --> I[Rows spread across many tasks - no single oversized task]
```

*Source: [[data-skew-oom]] (vutr)*
