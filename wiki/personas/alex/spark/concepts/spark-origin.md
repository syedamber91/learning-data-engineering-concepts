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

Okay so let me try — Spark was born at a Berkeley lab in 2009 because the older thing, MapReduce, was really slow for machine-learning jobs that keep looping over the same data. MapReduce was slow because it kept saving stuff to disk after every step, and disk is slow. Spark fixed that by keeping the data in memory instead so you don't pay that disk cost every loop, and that in-memory reuse idea is basically the core of the RDD.

*Source: [[spark-origin]] (vutr)*
