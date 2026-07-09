---
persona: alex
kind: concept
sources:
- vutr/spark-structured-streaming
last_updated: '2026-07-09'
qc: passed
slug: spark-structured-streaming
topics:
- spark
learner: alex
source_note: spark-structured-streaming
mastery: learning
---

So instead of building a brand-new streaming system, Spark pretends the endless stream is just lots of small chunks of normal finite data (micro-batches), and it keeps running the same SQL/DataFrame plan on each chunk. That way all the old batch tools like the Catalyst optimizer still work without being rebuilt, and triggers decide the timing of when a chunk gets processed.

*Source: [[spark-structured-streaming]] (vutr)*
