---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk
last_updated: '2026-07-09'
qc: passed
slug: shuffle-writes-to-disk
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk
mastery: learning
---

Alex: So even though Spark is famous for being in-memory, the shuffle step actually writes to disk. And the default is 200 shuffle partitions no matter the data size, so I should tune that. And reduceByKey is better than groupByKey because it cuts the data down before the shuffle instead of after.

```mermaid
flowchart LR
  M[Map stage] -->|reduceByKey shrinks data before shuffle| S[Shuffle: writes to DISK, not memory<br/>split into 200 partitions by default]
  S --> R[Reduce stage]
```

*Source: [[shuffle-writes-to-disk]] (vutr)*
