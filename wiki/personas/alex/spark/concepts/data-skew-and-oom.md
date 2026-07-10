---
persona: alex
kind: concept
sources:
- vutr/data-skew-and-oom
last_updated: '2026-07-10'
qc: passed
slug: data-skew-and-oom
topics:
- spark
learner: alex
source_note: data-skew-and-oom
mastery: mastered
---

Wait, so... the thing that clicked is that skew isn't actually the villain — it's more like skew is a loaded gun, and the join algorithm decides whether the trigger is even connected. ShuffleHashJoin is like insisting on carrying every box up to your apartment in one trip because you're sure it'll fit — if one box turns out way heavier than you guessed, you don't get to set it down halfway up the stairs, you just collapse. That's the in-memory hash table build: it has to hold the whole partition before it can even start comparing rows. SortMergeJoin is the smarter mover who lines everything up first and, if a box is too heavy, just sets it on the floor for a second (spills to disk) instead of dying under it. So it's not that SMJ is 'safer' in some vague sense — it structurally has an escape hatch that SHJ doesn't, and turning SHJ on is basically you promising the mover that every box really will fit.

The memory math made me realize 'does it fit' is a moving target, not a fixed number. A 2GB executor doesn't actually give you 2GB — the reserved 300MB and the 0.6 fraction chop it down to about 1GB before you even start, and then Parquet's compression means the on-disk size is a lie too, since a 2.6GB file ballooned to 3.7GB once actually read into memory. So a skewed partition isn't just 'more rows in one place' — it's more rows that each expand by that same compression-unpacking factor, all landing on one task instead of being spread out.

The part that really got me was the executor-memory result — going from 2GB to 4GB sped the task up but didn't cut spill at all, while just shrinking maxPartitionBytes did. It's like the bottleneck wasn't really 'not enough memory,' it was 'too much data assigned to one lane' — and widening the lane (more memory) doesn't fix an unbalanced lane assignment, only actually rebalancing the lanes (smaller partitions) does.

*Source: [[data-skew-and-oom]] (vutr)*
