---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: cpu-bound-lakehouse
topics:
- parquet
---

Since Parquet was created, storage and network performance have improved significantly, but CPUs have not — so in the lakehouse paradigm with high-bandwidth object storage, I/O is no longer the bottleneck, the CPU is. This is why research now suggests skipping general-purpose compression, and why Parquet's poor random-access performance is being exposed by AI workloads.
