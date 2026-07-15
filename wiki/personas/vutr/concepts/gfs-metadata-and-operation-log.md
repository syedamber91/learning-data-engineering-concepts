---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-metadata-and-operation-log
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

The GFS master tracks three kinds of metadata: the file and chunk namespaces, the mapping from files to chunks, and each chunk's replica locations. All of it lives in memory, which is what lets the master scan its entire state in the background — the basis for chunk garbage collection, re-replication, and migration. Google's own justification for the memory bound, quoted directly in Vu's notes: the cost of adding more RAM to the master is an insignificant trade against the simplicity, reliability, and performance gained by keeping metadata in memory.

One deliberate asymmetry: **chunk location metadata is not persisted on the master at all.** Instead, the master polls each chunkserver for its chunk list at master startup and whenever a new chunkserver joins. Because the master already controls all chunk placement and monitors chunkservers via HeartBeat, it can stay current without ever needing to keep itself and every chunkserver in sync across membership changes — polling on join/startup is enough.

The **namespace and file-to-chunk mapping**, by contrast, must survive a master crash, so GFS makes it durable via an **operation log**: every mutation is logged to the master's local disk and replicated to remote machines, and a client operation is only acknowledged after the log record has been flushed both locally and remotely. Recovery replays this log to rebuild master state. To keep the log itself small — and thus keep restart time low — the master periodically writes a checkpoint (a B-tree-like structure that can be mapped directly into memory) once the log passes a size threshold; recovery then only needs to load the latest *complete* checkpoint plus whatever log records follow it, and older checkpoints/logs can be discarded. Checkpoint creation is designed not to block incoming mutations: the master switches to a new log file and builds the new checkpoint in a separate thread, so a crash mid-checkpoint just means recovery detects and skips the incomplete one.

*See also: [[gfs]] · [[gfs-consistency-model]] · [[hdfs-image-and-journal]]*
