---
persona: alex
kind: concept
sources:
- vutr/remote-shuffle-service
last_updated: '2026-07-09'
qc: passed
slug: remote-shuffle-service
topics:
- spark
learner: alex
source_note: remote-shuffle-service
mastery: learning
---

Alex: So normally the reducers have to grab their matching data from tons of different mappers, which is messy and wears out the disks fast. Uber's RSS reverses it: every mapper dumps its same-partition data onto one RSS server, so each reducer just picks it up from that single spot. And that made the disks last way longer (3 months to ~3 years) and cut shuffle failures by 95 percent.

```mermaid
graph LR
  M1[Mapper 1] --> RSS[RSS Server]
  M2[Mapper 2] --> RSS
  M3[Mapper 3] --> RSS
  RSS --> R[Reducer]
```

*Source: [[remote-shuffle-service]] (vutr)*
