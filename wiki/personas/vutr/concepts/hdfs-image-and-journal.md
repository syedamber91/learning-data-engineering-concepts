---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper-523.md
last_updated: '2026-07-15'
qc: passed
slug: hdfs-image-and-journal
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

HDFS keeps its entire namespace in RAM on the NameNode, and splits that state's durability story into two parts, explicitly analogous to GFS's operation log (see [[gfs-metadata-and-operation-log]]). The **image** is the in-memory metadata itself — the inode data plus the file-to-block mapping. The **checkpoint** is a persistent, on-disk record of that image. The **journal** is a write-ahead commit log: every transaction that changes the file system is recorded there before it's considered durable. Crucially, the NameNode *never edits* the checkpoint file in place — a checkpoint is entirely replaced by a new one when a fresh checkpoint is created at restart, never patched.

On startup, the NameNode initializes its namespace image from the last checkpoint, then replays the journal's recorded changes on top of it to bring the image up to date. If either a checkpoint or its journal goes missing, the namespace information is corrupted — which is exactly why HDFS supports storing checkpoints and journals in multiple directories, so losing one copy doesn't mean losing the metadata. This mirrors GFS's own choice to replicate its operation log to remote machines for the same reason.

One deliberate omission, shared with GFS: HDFS does **not** persist the locations of block replicas, because that information changes constantly as DataNodes come and go — see [[hdfs-datanode-handshake-and-heartbeat]] for how the NameNode instead learns and maintains it live via block reports and heartbeats. Because an ever-growing journal both risks corruption/loss and slows down NameNode restart, HDFS offloads the job of periodically compacting it — see [[hdfs-checkpointnode-and-backupnode]].

*See also: [[hdfs]] · [[hdfs-checkpointnode-and-backupnode]] · [[gfs-metadata-and-operation-log]]*
