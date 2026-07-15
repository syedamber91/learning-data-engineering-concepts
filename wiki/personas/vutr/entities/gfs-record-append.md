---
persona: vutr
kind: entity
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-record-append
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Record append is GFS's atomic append operation: the client supplies only the data, and GFS appends it to the file **at least once atomically** at an offset of GFS's own choosing, then returns that offset to the client. This is the primitive behind GFS's producer-consumer-queue use case, where many writers concurrently append to the same file without needing a lock to coordinate who writes where.

The "at least once" qualifier is the deliberate trade Vu calls out: GFS accepts the possibility of duplicate or padded fragments in the file in exchange for letting concurrent appends proceed without serialization overhead. Per [[gfs-consistency-model]], a region written this way ends up *consistent* (all clients see the same bytes) but not necessarily *defined* if there were concurrent appenders — client-side self-validating records (checksums per record) are how applications cope with the resulting duplicates and padding, since GFS itself won't deduplicate for you.

*See also: [[gfs]] · [[gfs-consistency-model]] · [[gfs-lease-and-write-pipeline]]*
