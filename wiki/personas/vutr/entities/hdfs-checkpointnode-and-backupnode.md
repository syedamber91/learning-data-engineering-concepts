---
persona: vutr
kind: entity
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper-523.md
last_updated: '2026-07-15'
qc: passed
slug: hdfs-checkpointnode-and-backupnode
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Besides serving client requests, an HDFS NameNode can additionally take on one of two auxiliary roles, assigned at startup — a cluster can run two NameNodes, one serving clients and one acting as the CheckpointNode or BackupNode. Both exist to solve the same problem described in [[hdfs-image-and-journal]]: an ever-growing journal increases the risk of journal loss/corruption and slows NameNode restart, so *something* has to periodically fold the journal back into a fresh checkpoint.

The **CheckpointNode** does this the "pull" way: it periodically downloads the current checkpoint and journal from the active NameNode, merges them locally into a new checkpoint plus an empty journal, and uploads the merged checkpoint back. The **BackupNode** does the equivalent job the "push" way and goes further: it maintains an in-memory, continuously up-to-date copy of the namespace image by receiving a live stream of journal transactions from the active NameNode and applying them as they arrive, rather than periodically downloading anything. That live-synced image plus its own on-disk checkpoint means a BackupNode is effectively a **read-only NameNode** — if the primary NameNode fails, the BackupNode's in-memory image and checkpoint together are a record of the latest namespace state. Its one gap is block *locations*, which — consistent with how HDFS treats chunk/block-location metadata generally — can only come from a live block report sent by DataNodes to a NameNode, not from the journal stream.

*See also: [[hdfs]] · [[hdfs-image-and-journal]] · [[hdfs-datanode-handshake-and-heartbeat]]*
