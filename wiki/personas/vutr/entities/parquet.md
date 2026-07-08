---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: parquet
topics:
- storage-models-nsm-dsm-pax-and-column-store
- llms-ai-agents-and-vector-databases
---

Standard columnar formats like Parquet are problematic for vector workloads: they're bad for random access, and the wide columns of embeddings make row-group sizing difficult. So the columnar format that serves analytics well doesn't transfer cleanly to vector storage.
