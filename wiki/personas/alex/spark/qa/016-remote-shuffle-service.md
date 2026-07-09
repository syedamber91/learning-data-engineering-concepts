---
persona: alex
kind: concept
sources:
- vutr/remote-shuffle-service
last_updated: '2026-07-09'
qc: passed
slug: 016-remote-shuffle-service
topics:
- spark
learner: alex
source_note: remote-shuffle-service
mastery: learning
---

*What Alex understood:* Alex: So normally the reducers have to grab their matching data from tons of different mappers, which is messy and wears out the disks fast. Uber's RSS reverses it: every mapper dumps its same-partition data onto one RSS server, so each reducer just picks it up from that single spot. And that made the disks last way longer (3 months to ~3 years) and cut shuffle failures by 95 percent.

## Follow-up questions

**Alex:** In the old MapReduce shuffle, who is doing the pulling and who is doing the writing, and how is that different in RSS?

**vutr:** vutr: In the old MapReduce shuffle, the reducers do the pulling — each reducer pulls its same-partition data from many mappers. In RSS it's reversed: the mappers do the writing, each one writing its same-partition data to one unique RSS server, and the reducer fetches from that single place instead of from many mappers.

**Alex:** Why would writing to one RSS server instead of many mappers help the SSDs last longer?

**vutr:** vutr: The note doesn't spell out the exact disk-level reason, but it does tell us the result: with RSS, SSD wear-out went from about 3 months to nearly 3 years. So sending same-partition data to one RSS server instead of scattering the work across many mappers is what reduced the wear — the note gives us the outcome even though it doesn't detail the physical mechanism.
