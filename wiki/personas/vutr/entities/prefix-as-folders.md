---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: prefix-as-folders
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Cloud object storage has no real folders — objects are organized purely by a prefix that merely appears as folders to the user. It's a flat keyspace dressed up as a hierarchy, and understanding that flatness matters when you reason about how S3 partitions and scales.

*See also: [[s3-strong-consistency]] · [[hdfs-namenode-scaling-limit]] · [[hdfs]] · [[amazon-s3]] · [[gfs]] · [[gfs-record-append]]*
