---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-pinot
topics:
- apache-pinot-druid-and-real-time-olap
---

Apache Pinot came out of LinkedIn in 2013 and is built to serve tens of thousands of QPS with near-real-time ingestion. It organizes data into tables that break down into segments, which in turn hold records; the segments are immutable, columnar, and sized anywhere from a few hundred MB to a few GB.
