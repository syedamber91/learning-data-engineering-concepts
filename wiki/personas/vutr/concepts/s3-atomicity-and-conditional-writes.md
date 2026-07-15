---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: s3-atomicity-and-conditional-writes
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Amazon S3 only guarantees atomicity at the level of a single object operation: if a PUT succeeds, the entire object plus its metadata is durably stored; if it fails, nothing is persisted. There is no multi-object atomic transaction — an operation touching several objects can succeed for some and fail for others. Google Cloud Storage makes the identical trade, supporting atomic operations only per individual object.

The feature that makes single-object atomicity usable for building higher-level guarantees is the **conditional write**: S3 (and GCS) can check a specified condition before executing a request, which prevents one writer from silently clobbering another writer's concurrent change. Vu draws a direct, explicit line from this primitive to table formats: Delta Lake and Apache Hudi rely heavily on conditional writes to perform lightweight atomic operations that create a new metadata object — that's how they get atomic table commits out of a storage layer that otherwise offers no cross-object transactions. (This is the same design tension traced from the table-format side in [[iceberg-branching-and-wap-implementation]] and the wider [[iceberg]] topic — the object store's durability is free, but its transactional semantics have to be built by the table format on top of exactly this conditional-write primitive.)

*See also: [[amazon-s3]] · [[s3-strong-consistency]] · [[object-storage-as-backbone]]*
