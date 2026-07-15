---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-replica-management-and-fault-tolerance
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS's replica placement policy serves two goals at once: maximize data reliability/availability, and maximize network bandwidth utilization. The concrete mechanism is spreading a chunk's replicas across **racks** rather than just across machines — reads then get to use the aggregate bandwidth of multiple racks, while writes must cross multiple racks, a bandwidth cost Google explicitly accepts as the trade for surviving a whole-rack failure.

The master creates new replicas for three distinct reasons — chunk creation, re-replication, and rebalancing — and applies the same placement logic each time: prefer chunkservers with below-average disk utilization, cap how many "recent" creations land on one chunkserver, and keep replicas of a chunk spread across racks. Re-replication kicks in whenever a chunk's replica count falls below its target (a chunkserver going down being the common cause), and the master *prioritizes* which under-replicated chunk to fix first: chunks further from their replication goal (lost two replicas beats lost one), live files before deleted ones, and chunks actively blocking a client's progress. To avoid cloning traffic drowning out real client traffic, the master limits the total number of active clone operations cluster-wide and per chunkserver, and each chunkserver throttles its own read bandwidth spent serving clone sources. Rebalancing runs on a separate, periodic cadence, checking the current replica distribution and moving replicas to even out disk usage and load, including filling newly added chunkservers.

**Garbage collection** in GFS is lazy by design: deleting a file doesn't reclaim storage immediately. The master logs the deletion like any other mutation, then renames the file to a hidden name carrying a deletion timestamp; during regular namespace scans, any hidden file older than three days (configurable) is actually removed and its in-memory metadata erased — until then it can still be read under its hidden name or undeleted by renaming it back. Orphaned *chunks* (chunks no chunkserver report references) are found the same way: chunkservers report a subset of their chunks, the master replies with which of those it doesn't recognize, and the chunkserver is free to delete its local replica.

**Stale replica detection** uses a per-chunk version number: whenever a new lease is granted, the master bumps the version and informs up-to-date replicas, both of which persist it. A chunkserver that was down during that bump keeps its old version number, so when it returns and reports its chunks the master can spot the mismatch, exclude that replica from serving reads or accepting mutations, and garbage-collect it in the next regular sweep. Clients also receive the version number from the master and can verify it themselves before operating, as a second line of defense against reading stale data.

For **high availability** broadly, GFS layers three strategies: fast recovery (both master and chunkservers restart in seconds, and Google doesn't even distinguish normal shutdown from a killed process — routine termination is just how servers get restarted); chunk replication at a configurable level per part of the namespace, with the master cloning replicas whenever a chunkserver goes offline or a checksum fails; and master replication, where the operation log and checkpoints are copied to multiple machines, and monitoring infrastructure outside GFS starts a fresh master elsewhere from the replicated log if the active one fails.

For **data integrity**, each chunk is broken into 64KB blocks, each with its own 32-bit checksum, kept in memory and persisted via logging. On every read, the chunkserver verifies the relevant blocks' checksums before returning data — a mismatch triggers an error back to the requestor (who reads a different replica instead) and a report to the master, which clones a fresh replica from a valid source and then tells the corrupted chunkserver to delete its bad copy. Chunkservers also scan rarely touched chunks during idle time to catch corruption that an active read wouldn't otherwise surface, specifically so an inactive-but-corrupted replica can't fool the master into believing all replicas are healthy.

*See also: [[gfs]] · [[gfs-lease-and-write-pipeline]] · [[object-storage-durability-erasure-coding]] · [[hdfs-block-placement-and-replication-management]]*
