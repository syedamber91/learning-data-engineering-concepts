---
persona: alex
kind: concept
sources:
- vutr/photon-vectorized-engine
last_updated: '2026-07-10'
qc: passed
slug: photon-vectorized-engine
topics:
- spark
learner: alex
source_note: photon-vectorized-engine
mastery: mastered
---

Wait, so — Photon isn't its own database engine competing with Snowflake, it's more like a turbocharger Spark bolts on for specific operators, and if it can't handle something it just hands the job back to normal SparkSQL. Got it.

The part that clicked for me is *why* vectorization matters beyond 'it's faster.' Code-gen compiles one big plan up front and commits to it, kind of like writing out your whole route before a road trip. Vectorization processes column batches at runtime, so Photon can actually look at the batch in front of it and go 'oh, no NULLs here, skip the null-check branch' or 'this batch is basically all ASCII, take the fast path' — it's adaptive per batch, not per query like AQE. That's a totally different kind of flexibility than just 'compiled code is fast.'

The filter thing is the other piece I had to rebuild in my head. I assumed a filter operator physically removes rows, like deleting from an array. But it doesn't — every batch carries a position list of which row indices are currently 'active,' and a filter just rewrites that list. The actual column data doesn't move. So operators downstream just read the position list to know which rows to touch. That's cheaper than shuffling memory around every single filter step.

And the C++-over-JVM call wasn't just 'C++ is faster than Java' in the abstract — it was specific JVM pain: GC falling over past 64GB heaps, having to hand-manage off-heap memory, and code-gen literally hitting method-size limits. Plus they wanted hand-written SIMD kernels the JVM wouldn't let them control.

The hash join numbers are the proof this isn't just theoretical: 3.5x on the join itself from better memory-hierarchy use, and the JNI crossing between Spark and the C++ engine — which sounds like it should be the expensive part — is basically free (0.06%/0.2%) compared to the ~95% Spark burns serializing rows into Scala objects on the old path.

*Source: [[photon-vectorized-engine]] (vutr)*
