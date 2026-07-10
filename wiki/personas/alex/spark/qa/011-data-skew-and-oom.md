---
persona: alex
kind: concept
sources:
- vutr/data-skew-and-oom
last_updated: '2026-07-10'
qc: passed
slug: 011-data-skew-and-oom
topics:
- spark
learner: alex
source_note: data-skew-and-oom
mastery: mastered
---

*What Alex understood:* Wait, so... the thing that clicked is that skew isn't actually the villain — it's more like skew is a loaded gun, and the join algorithm decides whether the trigger is even connected. ShuffleHashJoin is like insisting on carrying every box up to your apartment in one trip because you're sure it'll fit — if one box turns out way heavier than you guessed, you don't get to set it down halfway up the stairs, you just collapse. That's the in-memory hash table build: it has to hold the whole partition before it can even start comparing rows. SortMergeJoin is the smarter mover who lines everything up first and, if a box is too heavy, just sets it on the floor for a second (spills to disk) instead of dying under it. So it's not that SMJ is 'safer' in some vague sense — it structurally has an escape hatch that SHJ doesn't, and turning SHJ on is basically you promising the mover that every box really will fit.

The memory math made me realize 'does it fit' is a moving target, not a fixed number. A 2GB executor doesn't actually give you 2GB — the reserved 300MB and the 0.6 fraction chop it down to about 1GB before you even start, and then Parquet's compression means the on-disk size is a lie too, since a 2.6GB file ballooned to 3.7GB once actually read into memory. So a skewed partition isn't just 'more rows in one place' — it's more rows that each expand by that same compression-unpacking factor, all landing on one task instead of being spread out.

The part that really got me was the executor-memory result — going from 2GB to 4GB sped the task up but didn't cut spill at all, while just shrinking maxPartitionBytes did. It's like the bottleneck wasn't really 'not enough memory,' it was 'too much data assigned to one lane' — and widening the lane (more memory) doesn't fix an unbalanced lane assignment, only actually rebalancing the lanes (smaller partitions) does.

## Follow-up questions

**Alex:** You said AQE splits oversized partitions into smaller ones at runtime — but ShuffleHashJoin already commits to building the whole partition's hash table before any probing happens. Does AQE's split happen early enough to save an SHJ job from OOMing, or is that skew-handling really only useful for SMJ, since SHJ's build might already be underway by the time AQE reacts?

**vutr:** The note actually confirms your read: partition size, not total executor memory, is the lever that reliably controls spill. Halving maxPartitionBytes from 256MB to 128MB doubled task count (84 to 168) and halved spill per task, cutting task time from 35s to 12s — a 65.7% reduction — because smaller partitions give a skewed key less material to pile onto one task. Meanwhile raising executor memory to 4GB cut task time to 25s but left spill unchanged from the 2GB baseline — Vu flags this explicitly as counterintuitive and unresolved, and his own best guess (tied to the SortAggregate mechanism) is stated as unconfirmed, not a settled explanation. So the honest answer is: repartitioning is the well-evidenced fix for spill in the case study; adding memory is worth doing for latency, but the note doesn't establish it as a spill fix, and even Vu isn't sure why it fails to move that number.

**Alex:** If raising executor memory to 4GB didn't reduce spill at all but shrinking maxPartitionBytes cut it in half, doesn't that mean spill isn't really about how much total memory you give the executor, but about how much data lands on a single task? So why would anyone reach for 'give it more memory' as a fix for a skewed job instead of always just repartitioning smaller?

**vutr:** (the wiki does not cover this — see open questions)
