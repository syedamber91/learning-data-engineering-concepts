---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
last_updated: '2026-07-15'
qc: passed
slug: lambda-architecture
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
- flink
---

In Vu's telling, Lambda routes data down two parallel paths: a batch layer that processes data in large chunks (daily, weekly) and a stream layer that processes data as it arrives for low-latency updates. The two layers carry an explicit trade-off — batch is assumed to be more accurate but delayed, while the stream layer is faster but may sacrifice some accuracy — and their results are unified for users, who see fast (stream) insight first, corrected later by the batch layer if needed. Vu names the architecture's biggest disadvantage plainly: users must maintain two codebases and two systems doing conceptually the same job.

He classifies Lambda (along with [[kappa-architecture]]) as more of a pattern than an architecture in his own terms — see [[architecture-vs-pattern]] — because it provides a specific solution for data processing and serving rather than the full end-to-end blueprint of how data is ingested, stored, processed, and served.

*See also: [[data-lake]] · [[data-warehouse]] · [[kappa-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's fuller account of the same dual-path pattern (stream for fast approximate views, batch for corrected exact views) and its costs: duplicated logic, hard-to-merge joins, expensive reprocessing.
