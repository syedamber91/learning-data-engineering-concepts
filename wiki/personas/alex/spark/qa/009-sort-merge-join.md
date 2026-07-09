---
persona: alex
kind: concept
sources:
- vutr/sort-merge-join
last_updated: '2026-07-09'
qc: passed
slug: 009-sort-merge-join
topics:
- spark
learner: alex
source_note: sort-merge-join
mastery: learning
---

*What Alex understood:* So SMJ is fast when the two tables are already sorted on the column you are joining, and as a freebie the answer comes out sorted too. If something earlier already did the sorting, SMJ just slots right in.

## Follow-up questions

**Alex:** Why does SMJ being efficient depend on the inputs already being sorted?

**vutr:** Because SMJ works by merging two sorted inputs, like zipping down two alphabetized lists at once. If they are already sorted on the join columns, it can march straight through and match rows without extra searching, which is what makes it efficient. The note frames it exactly that way: SMJ is efficient when its inputs are already sorted on the join columns.

**Alex:** You said sorting has a cost upstream. Does SMJ do that sorting itself, or does it count on someone else having done it?

**vutr:** The note does not spell out who does the sorting. It only says that if you already paid the sorting cost upstream, SMJ is a natural fit. So from the note alone I can only say SMJ benefits from sorting done earlier, and it produces sorted output as a bonus, but whether SMJ itself sorts is not stated here.
