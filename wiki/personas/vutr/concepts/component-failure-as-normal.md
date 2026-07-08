---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: component-failure-as-normal
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

In these systems component failure is no longer treated as unexpected — hardware faults (disk, memory, power) and software faults (bugs, human errors) are assumed to happen constantly. That assumption is what forces monitoring, error detection, fault tolerance, and automatic recovery into the core design rather than bolting them on.
