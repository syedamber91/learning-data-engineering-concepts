---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: s3-strong-consistency
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

S3's consistency guarantee changed shape over its history. Initially it offered read-after-write consistency only for *new* objects (a freshly uploaded object was immediately visible to other readers), but only *eventual* consistency for overwrites and deletes — a small window, typically milliseconds to a few seconds, during which a read could still return the old version or a list operation could still show a deleted object. Today, Amazon S3 offers strong read-after-write consistency for all operations, matching what Google Cloud Storage also provides.

The reason the eventual-consistency window existed in the first place is a metadata cache: S3 was designed so that repeated requests for the same object don't have to hit the persistent metadata layer every time. That cache is what let stale reads happen — a PUT or DELETE's effect on metadata hadn't yet propagated into the cache when a subsequent request checked it. To close that gap, Amazon added a component that checks whether a cached metadata value is stale before serving it: if it isn't stale, S3 answers from cache as before; if it is, S3 reads from the persistence layer and refreshes the cache, and only then answers the request. That one addition is what converted S3 from eventually consistent to strongly consistent, without giving up the performance benefit of caching metadata in the common case.

*See also: [[amazon-s3]] · [[object-storage-durability-erasure-coding]] · [[s3-atomicity-and-conditional-writes]]*
