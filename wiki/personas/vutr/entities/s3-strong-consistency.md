---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: s3-strong-consistency
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

S3 initially gave you only eventual consistency for overwrites and deletes, but since December 2020 it provides strong read-after-write consistency via a new staleness-check component. This is a quiet but important shift — it removes a whole class of correctness workarounds data engineers used to bake in.

*See also: [[hdfs-namenode-scaling-limit]] · [[hdfs]] · [[prefix-as-folders]] · [[amazon-s3]] · [[gfs]] · [[gfs-record-append]]*
