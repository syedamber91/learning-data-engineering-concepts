---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: occ-on-object-storage
topics:
- iceberg
---

All three formats use Optimistic Concurrency Control for Isolation, and the genuinely hard parts of ACID are Isolation and Atomicity — Durability is essentially free via S3/GCS's eleven-nines durability. Hudi pushed past OCC's ceiling by introducing Non-Blocking Concurrency Control (NBCC) in v1.0 (2024).
