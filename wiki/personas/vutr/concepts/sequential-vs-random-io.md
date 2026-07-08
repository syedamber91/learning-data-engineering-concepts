---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: sequential-vs-random-io
topics:
- lsm-tree-storage-engines
---

The whole point of the LSM-tree is that it converts random writes into sequential disk I/O, at the cost of potentially higher read and write amplification. This matters because RAM access is measured in nanoseconds whereas an HDD seek can take milliseconds — a difference of four to five orders of magnitude, so avoiding random seeks is enormously valuable.
