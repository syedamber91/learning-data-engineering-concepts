---
persona: alex
kind: concept
sources:
- vutr/shuffle-hash-join
last_updated: '2026-07-09'
qc: passed
slug: shuffle-hash-join
topics:
- spark
learner: alex
source_note: shuffle-hash-join
mastery: mastered
---

Let me say it back so I know I actually get it. SHJ = shuffle first (repartition both tables by key so matching keys share a partition), then inside each partition build a hash table from the SMALLER side and probe it with the bigger side for O(1) lookups. The catch is that the ENTIRE build-side partition has to sit in memory at once as that hash table — a hash table is useless half-built, you can't probe it. So if one partition is fat (usually because of skew — one key hogging the rows), its build side won't fit, and the executor OOMs. The reason it OOMs and SMJ doesn't is that SMJ only sorts and walks with pointers, so it can dump sorted chunks to disk and merge them later — it spills. SHJ can't spill because it needs the whole hash table resident. That's the exact reason SHJ got yanked in 1.6 and only came back in 2.0, and why the priority is BROADCAST > MERGE > SHUFFLE_HASH. And it's the same story as the skew-OOM lesson: throwing more RAM at it doesn't help, you have to split the skewed partition.

```mermaid
flowchart TD
    A[Left table] -->|shuffle by join key| P[Partition k: same keys co-located]
    B[Right table] -->|shuffle by join key| P
    P --> C{Build side = smaller table}
    C -->|fits in memory| D[Build hash table in RAM]
    D --> E[Probe with larger side, O(1) lookups]
    E --> F[Join output]
    C -->|partition too big / skewed| G[Build side exceeds executor memory]
    G --> H[Cannot spill — hash table must be whole]
    H --> X[OutOfMemoryError]
```

*Source: [[shuffle-hash-join]] (vutr)*
