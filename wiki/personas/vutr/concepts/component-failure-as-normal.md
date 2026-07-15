---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: component-failure-as-normal
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS's design starts from a reframing, not a feature: component failure is "no longer unexpected behavior." That covers both hardware failure (disk, memory, power supply) and software failure (bugs, human error). Treating failure as the normal case rather than an edge case is what forces monitoring, error detection, fault tolerance, and automatic recovery into the *core* of the design rather than being bolted on afterward — a stance later mirrored, in different specifics, by S3's [[object-storage-durability-erasure-coding|erasure coding]] and by HDFS's own heartbeat/replication machinery.

That reframing sits alongside a small set of companion assumptions Google names explicitly: the system runs on many inexpensive commodity components that fail often; it stores a modest number of very large files (millions of files, typically 100MB or more each); read workloads split into large streaming reads and small random reads; write workloads are dominated by large, sequential appends; multiple clients need to append to the same file concurrently with correct semantics; and — the one that reorders GFS's whole set of engineering priorities — high bandwidth matters more than low latency. Every mechanism covered elsewhere in this topic (64MB chunks, record append, the lease-based write pipeline, replica placement across racks) is a consequence of taking these assumptions as given rather than negotiable.

*See also: [[gfs]] · [[gfs-metadata-and-operation-log]] · [[gfs-replica-management-and-fault-tolerance]]*
