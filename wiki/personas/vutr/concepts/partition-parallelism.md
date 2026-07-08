---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: partition-parallelism
topics:
- kafka
---

A partition is the smallest unit of parallelism; if a group has more consumers than partitions, the surplus consumers get no messages.
