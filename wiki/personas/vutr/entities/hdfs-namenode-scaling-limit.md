---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: hdfs-namenode-scaling-limit
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Because the NameNode holds the whole namespace in RAM, HDFS starts to struggle once data exceeds 10 petabytes and gets materially worse beyond 50-100 petabytes. This memory ceiling is a big reason HDFS handed the data-lake crown to cloud object storage like S3 or GCS.

*See also: [[s3-strong-consistency]] · [[hdfs]] · [[prefix-as-folders]] · [[amazon-s3]] · [[gfs]] · [[gfs-record-append]]*
