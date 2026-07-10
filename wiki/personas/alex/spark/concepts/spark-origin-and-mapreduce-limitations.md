---
persona: alex
kind: concept
sources:
- vutr/spark-origin-and-mapreduce-limitations
last_updated: '2026-07-10'
qc: passed
slug: spark-origin-and-mapreduce-limitations
topics:
- spark
learner: alex
source_note: spark-origin-and-mapreduce-limitations
mastery: mastered
---

Wait, so it's not that MapReduce was just "slow" and Spark is the turbo version — it's that MapReduce made one design choice, writing everything to disk between steps, to solve a completely different problem: not losing your work if a machine dies. That's like a group project where after every single step, everyone photocopies their work and mails it to a locker before anyone's allowed to start the next step. It's safe — nothing gets lost if someone drops out — but if you need to redo the same step twenty times in a row (like training an ML model pass after pass), you're re-mailing the photocopy every single time, and worse, under MapReduce you'd have to file a whole new "project request form" (a new job) for each pass too.

The other piece is that Map/Reduce only gives you two moves — Map, then group-by-key, then Reduce. That's rigid, like a recipe that only has "chop" and "combine" as steps, so anything with more structure has to be faked with multiple separate chop-combine rounds.

AMPLab looked at real Hadoop users doing iterative ML — not theory, actual people re-running passes over the same data — and saw both costs stacking: the disk round-trip AND the job-launch overhead, every single pass. So they built two matched fixes: a functional API so you can write a multistep program as one thing instead of a chain of separate jobs, and an in-memory engine (which becomes the RDD) so data just stays resident between steps instead of going back to the locker every time.

And importantly — Spark didn't just delete the safety net. It still needs a way to recover if a worker dies; it just does it with lineage (recomputing from a recorded recipe of how the data was derived) instead of disk copies. So the durability goal is the same, the mechanism to get there changed.

*Source: [[spark-origin-and-mapreduce-limitations]] (vutr)*
