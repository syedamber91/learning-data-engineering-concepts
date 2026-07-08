---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: data-lake
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

The data lake is schema-on-read: you dump data in its native format onto HDFS or cloud object storage and impose structure only when you query. Without ACID, DML, discovery, and quality controls, though, it kept degrading into a 'data swamp.'

*See also: [[data-warehouse]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*
