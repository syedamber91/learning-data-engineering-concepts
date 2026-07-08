---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: amazon-s3
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Amazon S3, introduced in 2006, runs on 350+ microservices per AWS region and distributes load by partitioning object keys (prefixes) lexicographically, supporting at least 3,500 PUT or 5,500 GET requests per second per prefix. It leans on erasure coding to reach 99.999999999% (eleven 9s) durability, which is why I argue it's nearly impossible for an organization to match that guarantee in-house.

*See also: [[s3-strong-consistency]] · [[hdfs-namenode-scaling-limit]] · [[hdfs]] · [[prefix-as-folders]] · [[gfs]] · [[gfs-record-append]]*
