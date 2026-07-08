---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: hdfs
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

HDFS keeps the entire namespace in RAM on the NameNode, uses a 128MB default block size with 3 replicas, and has DataNodes send heartbeats every 3 seconds — if none arrives for 10 minutes the DataNode is considered down and its replicas unavailable. Its block placement rule ensures no DataNode holds more than one replica and no rack more than two (given enough racks), and DistCp handles large inter-cluster parallel copies.

*See also: [[s3-strong-consistency]] · [[hdfs-namenode-scaling-limit]] · [[prefix-as-folders]] · [[amazon-s3]] · [[gfs]] · [[gfs-record-append]]*
