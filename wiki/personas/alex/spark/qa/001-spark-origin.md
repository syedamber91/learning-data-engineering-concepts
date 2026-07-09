---
persona: alex
kind: concept
sources:
- vutr/spark-origin
last_updated: '2026-07-09'
qc: passed
slug: 001-spark-origin
topics:
- spark
learner: alex
source_note: spark-origin
mastery: mastered
---

*What Alex understood:* Okay so let me try — Spark was born at a Berkeley lab in 2009 because the older thing, MapReduce, was really slow for machine-learning jobs that keep looping over the same data. MapReduce was slow because it kept saving stuff to disk after every step, and disk is slow. Spark fixed that by keeping the data in memory instead so you don't pay that disk cost every loop, and that in-memory reuse idea is basically the core of the RDD.

## Follow-up questions

**Alex:** Why is writing to disk between stages so much slower than keeping the data in memory?

**vutr:** The note doesn't explain the physics of why disk is slower than memory — it just tells us that MapReduce's write-to-disk-between-stages model is 'punishing' for iterative jobs that reuse the same dataset across many passes, and that Spark avoids this by keeping data in memory for reuse.

**Alex:** What exactly is an RDD — is it just the name for the data Spark keeps in memory?

**vutr:** The note doesn't give a full definition of an RDD; it only says that in-memory reuse of the [[rdd]] sits at the heart of Spark's original design, so the RDD is the thing at the center of that in-memory reuse idea. For the actual definition you'd need to look at the [[rdd]] note itself.
