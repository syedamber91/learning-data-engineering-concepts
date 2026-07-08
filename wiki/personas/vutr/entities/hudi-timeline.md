---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: hudi-timeline
topics:
- iceberg
---

The Hudi Timeline records actions with an explicit state machine: REQUESTED then INFLIGHT then COMPLETED. This is how Hudi tracks the lifecycle of every action against a table.

*See also: [[iceberg-metadata-layer]] · [[hudi-index]] · [[apache-iceberg]] · [[conditional-writes]] · [[open-table-formats]] · [[copy-on-write-vs-merge-on-read]]*
