---
persona: alex
kind: concept
sources:
- vutr/data-locality
last_updated: '2026-07-09'
qc: passed
slug: 011-data-locality
topics:
- spark
learner: alex
source_note: data-locality
mastery: familiar
---

*What Alex understood:* Alex: So Spark would rather run the work where the data already is than move the data, because moving data is expensive. It has a ranked wishlist of how close the data is, from same-process (PROCESS_LOCAL) all the way down to anywhere (ANY), and it waits a moment for a good spot before dropping to a worse one. And separately, if a task is dragging, Spark runs a second copy elsewhere and takes the faster one so a single slow machine doesn't hold everything up. That preferred spot comes from the RDD's fifth property.

## Follow-up questions

**Alex:** When Spark can't get PROCESS_LOCAL right away, does it immediately jump to ANY, or does it wait first?

**vutr:** vutr: Good questions. First one: no, it doesn't jump straight to ANY. The note says Spark waits briefly for a better level before falling back to a worse one, so it steps down the ranking rather than leaping to the bottom. Second one: they're separate. The locality ranking (PROCESS_LOCAL down to ANY) is about WHERE to place a task. Speculative execution is a different, companion mechanism about slow tasks: when a task runs unusually slow, Spark re-submits a duplicate copy to another executor and takes whichever finishes first, to hedge against a straggler.

**Alex:** Is speculative execution the same thing as the locality ranking, or a separate mechanism?

**vutr:** (the wiki does not cover this — see open questions)
