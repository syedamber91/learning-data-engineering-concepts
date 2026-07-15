---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-snapshot-and-namespace-locking
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS's snapshot operation copies a file or directory tree cheaply, and "cheaply" is the operative word: creating a snapshot does not copy chunk data up front. When the master gets a snapshot request, it first revokes any outstanding leases on chunks belonging to the files involved — forcing subsequent writes to those chunks to go back through the master to find the (new) leaseholder — logs the snapshot operation to disk, and then duplicates the source file/directory's metadata in memory. The resulting snapshot file's chunks simply *point at the same underlying chunks* as the source file; no data has moved yet.

The actual copy-on-write happens lazily, the first time either the source or the snapshot tries to mutate a shared chunk. The client contacts the master as usual to find the leaseholder; the master notices the chunk's reference count is greater than one (both source and snapshot point to it) and instructs each chunkserver holding a replica to create a local copy of the chunk under a new chunk handle — done locally on the same chunkservers to avoid a network copy. Only after that new chunk exists does the master proceed normally: it grants a lease on the new chunk to one of its replicas and replies to the client, which can then write as if nothing special happened.

Separately, GFS's **namespace locking** exists to let the master avoid serializing all its (sometimes long-running) operations behind one another. The namespace is represented as a lookup table mapping full pathnames to metadata, and every node in that namespace tree — each absolute file or directory name — carries its own read-write lock. An operation touching a path like `/d1/d2/...` acquires read-locks on each ancestor directory (`/d1`, `/d1/d2`, ...) before proceeding, which lets unrelated operations on different parts of the tree run concurrently while still serializing conflicting operations on the same path.

*See also: [[gfs]] · [[gfs-metadata-and-operation-log]] · [[hdfs-checkpointnode-and-backupnode]]*
