---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: gfs-record-append
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS's record append operation guarantees atomicity at-least-once, which is the primitive that lets many clients concurrently append to the same file without a lock. It's a deliberate design trade — you accept possible duplicates in exchange for concurrent, atomic appends.

*See also: [[s3-strong-consistency]] · [[hdfs-namenode-scaling-limit]] · [[hdfs]] · [[prefix-as-folders]] · [[amazon-s3]] · [[gfs]]*
