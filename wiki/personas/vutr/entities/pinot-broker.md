---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: pinot-broker
topics:
- apache-pinot-druid-and-real-time-olap
---

In Pinot, brokers drive query processing using a scatter-gather-merge pattern. Multi-tenancy on top of this uses a token bucket to distribute resources across tenants.
