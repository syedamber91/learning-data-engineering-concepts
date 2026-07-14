---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: lambda-architecture
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
- flink
---

The Lambda Architecture gives a low-latency estimate from a streaming path, then promises correctness later from a batch path. It does not actually solve completeness — it just papers over the gap by re-computing with batch.

*See also: [[data-lake]] · [[data-warehouse]] · [[kappa-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's fuller account of the same dual-path pattern (stream for fast approximate views, batch for corrected exact views) and its costs: duplicated logic, hard-to-merge joins, expensive reprocessing.
