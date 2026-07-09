---
persona: alex
kind: concept
sources:
- vutr/spark-origin
last_updated: '2026-07-09'
qc: passed
slug: spark-origin
topics:
- spark
learner: alex
source_note: spark-origin
mastery: mastered
---

Okay, let me say it back in mechanism terms, not just 'Spark is faster.' The core pain was that MapReduce, for an algorithm that loops over the same data many times (like training an ML model), dumped each round's results to DISK and then the next round had to read them back from disk. So every iteration ate a write-to-disk AND a read-from-disk, on data you literally already had in hand. Spark's fix is to hold that dataset in memory as an RDD and REUSE it across iterations — so the next pass reads from RAM instead of paying the disk round-trip. The disk write-between-iterations was the bottleneck; keeping the RDD resident in memory is what removes it. And an RDD isn't magic storage — it's immutable and lazy: transformations just build up a DAG plan, and only an action actually kicks off the compute.

```mermaid
flowchart TB
  subgraph MR["MapReduce: iterative ML"]
    A1["Iteration 1 compute"] --> D1[("write to DISK")]
    D1 --> A2["Iteration 2: read from DISK"]
    A2 --> D2[("write to DISK")]
    D2 --> A3["Iteration 3: read from DISK"]
  end
  subgraph SP["Spark: in-memory RDD reuse"]
    B1["Iteration 1 compute"] --> M[["RDD kept in MEMORY"]]
    M --> B2["Iteration 2: reuse from RAM"]
    B2 --> M
    M --> B3["Iteration 3: reuse from RAM"]
  end
  note["Penalty removed: no disk write+read between passes over the SAME data"]
```

*Source: [[spark-origin]] (vutr)*
