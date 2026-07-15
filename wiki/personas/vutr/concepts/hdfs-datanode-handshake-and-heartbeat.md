---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper-523.md
last_updated: '2026-07-15'
qc: passed
slug: hdfs-datanode-handshake-and-heartbeat
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Every block replica a DataNode holds is backed by two local files: the data itself, and metadata carrying the block's checksums and generation stamp. Before any of that can matter, a DataNode has to prove it belongs to the cluster. At startup it performs a **handshake** with the NameNode, verifying its namespace ID (assigned to the whole file system instance and persisted on every node — a mismatched namespace ID means the node can't join, protecting the file system's integrity) and software version (an incompatible version could cause corruption or data loss, so the handshake shuts down nodes that weren't part of an upgrade). After a successful handshake, the DataNode registers and receives a **storage ID** — an internal identifier that, unlike an IP address, never changes, so the NameNode can recognize the same DataNode across network changes.

Once registered, the DataNode sends a **block report** — the block ID, generation stamp, and length for every replica it holds — immediately after registration, and again every hour after that, keeping the NameNode's live view of block placement up to date without ever persisting that placement info on disk (see [[hdfs-image-and-journal]]).

Ongoing liveness is tracked via **heartbeats**: every DataNode sends one to the NameNode every three seconds by default, carrying its storage capacity, fraction of storage in use, and number of in-flight data transfers — information the NameNode uses for space allocation and load-balancing decisions. If ten minutes pass with no heartbeat from a DataNode, the NameNode considers it down, treats its replicas as unavailable, and instructs new replicas of those blocks to be created elsewhere. The NameNode also rides on heartbeat *replies* to push instructions back to the DataNode: replicate specific blocks elsewhere, remove specific local replicas, re-register or shut down, or send an immediate (out-of-cycle) block report.

*See also: [[hdfs]] · [[hdfs-image-and-journal]] · [[hdfs-block-placement-and-replication-management]]*
