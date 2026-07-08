---
persona: vutr
kind: entity
sources:
- substack/vutr/kafka-tiered-storage
last_updated: '2026-07-09'
qc: passed
slug: tiered-storage
topics:
- kafka
---

Tiered storage (KIP-405) offloads older log segments to cheaper object storage, decoupling retention from broker disk for cold data.
