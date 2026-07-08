---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: conditional-writes
topics:
- iceberg
---

Object storage guarantees Durability but does not support multi-object atomic transactions, so all three formats lean on single-object conditional writes for Atomicity. Amazon S3 added conditional-writes support in August 2024, which is what Delta's put-if-absent and Hudi's .completed-file commit depend on.

*See also: [[iceberg-metadata-layer]] · [[hudi-index]] · [[apache-iceberg]] · [[hudi-timeline]] · [[open-table-formats]] · [[copy-on-write-vs-merge-on-read]]*
