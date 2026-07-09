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
mastery: learning
---

So SMJ is fast when the two tables are already sorted on the column you are joining, and as a freebie the answer comes out sorted too. If something earlier already did the sorting, SMJ just slots right in.

*Source: [[sort-merge-join]] (vutr)*
