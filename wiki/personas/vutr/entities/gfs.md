---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: gfs
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Google File System uses a 64MB chunk size with three replicas by default, and its master keeps all metadata in memory, persisting it via an operation log and B-tree-like checkpoints. Notably, chunk location metadata is NOT stored on the master — it's polled from chunkservers at startup — and the master grants a 60-second lease to a primary replica, separating control flow from data flow.
