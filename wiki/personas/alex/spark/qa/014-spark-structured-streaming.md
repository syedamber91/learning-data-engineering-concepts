---
persona: alex
kind: concept
sources:
- vutr/spark-structured-streaming
last_updated: '2026-07-09'
qc: passed
slug: 014-spark-structured-streaming
topics:
- spark
learner: alex
source_note: spark-structured-streaming
mastery: learning
---

*What Alex understood:* So instead of building a brand-new streaming system, Spark pretends the endless stream is just lots of small chunks of normal finite data (micro-batches), and it keeps running the same SQL/DataFrame plan on each chunk. That way all the old batch tools like the Catalyst optimizer still work without being rebuilt, and triggers decide the timing of when a chunk gets processed.

## Follow-up questions

**Alex:** Why does treating the stream as bounded micro-batches mean they didn't have to rebuild the Catalyst optimizer for streaming?

**vutr:** Because the stream is broken into micro-batches of bounded data, and bounded data is treated as the first-class citizen, the exact same declarative DataFrame/SQL plan that runs over a static table runs incrementally over each batch. Since the plan is the same shape, the Catalyst optimizer and the rest of the batch machinery apply unchanged rather than being reinvented for streaming.

**Alex:** The Available-Now trigger is called multi-batch, but One-Time isn't. What's the difference in how they run?

**vutr:** The note lists both as trigger types and specifically labels Available-Now as multi-batch, which tells me it processes across multiple batches (and then presumably stops). One-Time is listed as its own separate trigger type, but the note doesn't spell out exactly how its single run differs mechanically, so beyond the multi-batch label on Available-Now I'd be guessing.
