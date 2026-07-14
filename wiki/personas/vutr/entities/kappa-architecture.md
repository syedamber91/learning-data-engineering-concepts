---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: kappa-architecture
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Kappa collapses everything into a single streaming pipeline and handles historical reprocessing by replaying Kafka offsets. It kills Lambda's dual-codebase problem, but the price is that you now need real stream-system expertise.

*See also: [[data-lake]] · [[data-warehouse]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's "unification instead" alternative — replaying history through one stream-processing codebase via log replay and exactly-once semantics — describes the same idea this note names as Kappa.
