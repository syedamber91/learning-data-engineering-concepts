---
persona: alex
kind: concept
sources:
- vutr/sort-merge-join
last_updated: '2026-07-09'
qc: passed
slug: sort-merge-join
topics:
- spark
learner: alex
source_note: sort-merge-join
mastery: mastered
---

SMJ = shuffle both sides, sort each partition, zipper-merge the two sorted runs. It's the safe default because a sort can SPILL TO DISK, so a partition bigger than memory just gets slower, not fatal. SHJ builds an in-memory hash table on the small side and streams the big side through it — faster, but the build side MUST fit in memory, so a skewed partition throws OOM (no on-disk hash table exists). BHJ skips shuffling entirely by copying a <10MB table to every executor. Bucket join skips the shuffle by pre-partitioning at write time. Hint order BROADCAST > MERGE > SHUFFLE_HASH ranks them fastest-when-applicable down to the fragile fallback.

```mermaid
graph TD
    A[Join two tables] --> B{Is one side below<br/>autoBroadcastJoinThreshold?<br/>default 10MB}
    B -->|Yes: BROADCAST wins| C[Broadcast Hash Join<br/>ship small table to every executor<br/>NO shuffle of big side]
    B -->|No| D{MERGE hint /<br/>default?}
    D -->|Yes: MERGE| E[Sort Merge Join<br/>shuffle + sort both sides<br/>zipper-merge<br/>CAN spill to disk = safe]
    D -->|No, SHUFFLE_HASH forced| F[Shuffle Hash Join<br/>build in-memory hash table<br/>build side MUST fit in memory<br/>CANNOT spill = OOM on skew]
    E --> G[Priority: BROADCAST &gt; MERGE &gt; SHUFFLE_HASH]
    C --> G
    F --> G
```

*Source: [[sort-merge-join]] (vutr)*
