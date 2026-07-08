---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: apache-hudi
topics:
- iceberg
---

Hudi was created by Uber to bring incremental processing to the data lake, after Uber faced challenges with data updates and deletions over HDFS. It commits atomically by creating a .completed file via object-storage conditional writes, and prioritizes incremental and real-time processing over the wide adoption enjoyed by Iceberg and Delta Lake.
