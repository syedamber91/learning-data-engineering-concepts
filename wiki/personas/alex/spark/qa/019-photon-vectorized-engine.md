---
persona: alex
kind: concept
sources:
- vutr/photon-vectorized-engine
last_updated: '2026-07-10'
qc: passed
slug: 019-photon-vectorized-engine
topics:
- spark
learner: alex
source_note: photon-vectorized-engine
mastery: mastered
---

*What Alex understood:* Wait, so — Photon isn't its own database engine competing with Snowflake, it's more like a turbocharger Spark bolts on for specific operators, and if it can't handle something it just hands the job back to normal SparkSQL. Got it.

The part that clicked for me is *why* vectorization matters beyond 'it's faster.' Code-gen compiles one big plan up front and commits to it, kind of like writing out your whole route before a road trip. Vectorization processes column batches at runtime, so Photon can actually look at the batch in front of it and go 'oh, no NULLs here, skip the null-check branch' or 'this batch is basically all ASCII, take the fast path' — it's adaptive per batch, not per query like AQE. That's a totally different kind of flexibility than just 'compiled code is fast.'

The filter thing is the other piece I had to rebuild in my head. I assumed a filter operator physically removes rows, like deleting from an array. But it doesn't — every batch carries a position list of which row indices are currently 'active,' and a filter just rewrites that list. The actual column data doesn't move. So operators downstream just read the position list to know which rows to touch. That's cheaper than shuffling memory around every single filter step.

And the C++-over-JVM call wasn't just 'C++ is faster than Java' in the abstract — it was specific JVM pain: GC falling over past 64GB heaps, having to hand-manage off-heap memory, and code-gen literally hitting method-size limits. Plus they wanted hand-written SIMD kernels the JVM wouldn't let them control.

The hash join numbers are the proof this isn't just theoretical: 3.5x on the join itself from better memory-hierarchy use, and the JNI crossing between Spark and the C++ engine — which sounds like it should be the expensive part — is basically free (0.06%/0.2%) compared to the ~95% Spark burns serializing rows into Scala objects on the old path.

## Follow-up questions

**Alex:** If a filter just marks rows inactive in the position list instead of deleting them, and a query chains several filters in a row, doesn't the batch end up dragging around a growing pile of 'dead' rows that every downstream operator still has to skip over? Is there something that actually reclaims that space, or does it just get worse the more filters you stack?

**vutr:** You're not wrong that a batch can accumulate inactive rows across chained filters, and yes, operators keep paying the position-list-lookup cost for as long as that stays true — the note is explicit that a batch only gets to *skip* the position-list lookup when it has no inactive rows at all. But it doesn't just get worse forever: batch-level adaptivity includes exactly this reclaim step — 'sparse batches can be compacted.' So once a batch has accumulated enough dead rows to be sparse, Photon compacts it, which is the mechanism that keeps the pile from growing unbounded. The tradeoff is real but bounded, not runaway.

**Alex:** Hash join splits into a reservation phase where spilling is handled and an allocation phase that's spill-free — but what happens if some other Spark memory consumer needs Photon to give memory back while it's mid-way through that spill-free allocation phase? Does Photon just refuse, or does that case get avoided some other way?

**vutr:** (the wiki does not cover this — see open questions)
