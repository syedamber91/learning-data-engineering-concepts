---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: remote-shuffle-service
topics:
- spark
---

Uber's Spark RSS reverses the MapReduce shuffle paradigm: instead of reducers pulling same-partition data from many mappers, each mapper writes its same-partition data to one unique RSS server so the reducer fetches from a single place. In production this cut SSD wear-out from 3 months to nearly 3 years and dropped shuffle failure rates by 95%.
