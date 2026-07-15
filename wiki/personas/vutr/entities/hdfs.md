---
persona: vutr
kind: entity
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper-523.md
last_updated: '2026-07-15'
qc: passed
slug: hdfs
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

The Hadoop Distributed File System (HDFS), described in a 2010 paper, was Yahoo's answer to building a scalable, reliable data lake in an era (the 2010s) before cloud object storage was mature — Vu frames the whole post around that "what if you had to build this on your own servers" premise. At the scale Yahoo actually ran it: Hadoop clusters spanning 25,000 servers storing 25 petabytes, with the largest single cluster at 3,500 servers; Yahoo contributed roughly 80% of HDFS and MapReduce's core. HDFS's interface is patterned after the UNIX file system, and — like GFS, whose design it closely mirrors — it separates metadata from data across two server roles.

The **NameNode** is a dedicated server holding the HDFS namespace: a hierarchy of files and directories represented internally as *inodes* carrying permissions, modification/access times, and quotas. HDFS splits file content into blocks — 128MB by default, user-configurable — each replicated independently across three **DataNodes** by default. The NameNode keeps the entire namespace in RAM and maintains the file-to-block-to-DataNode mapping; unlike GFS, it does *not* persist block-replica locations on disk (see [[hdfs-image-and-journal]]) — that information is asked of the DataNodes directly. Because the namespace lives in memory, HDFS's practical scale is bounded by the NameNode's RAM — the same ceiling a sibling raw group (`raw/uber-data-infrastructure-case-studies`) documents concretely as [[hdfs-namenode-scaling-limit|struggling past 10PB and worsening beyond 50-100PB]].

For reads, a client asks the NameNode for block locations, then reads from the nearest DataNode. For writes, the client asks the NameNode to nominate three DataNodes to host the new block's replicas, then writes to them in a pipeline. HDFS also exposes an API returning file-block locations so frameworks like MapReduce can schedule tasks local to the data, and lets applications configure a per-file replication factor above the default three for files that are especially critical or heavily read (see [[hdfs-client-read-write-and-lease]] and [[hdfs-block-placement-and-replication-management]]). DataNode membership and health are tracked through a handshake-and-heartbeat protocol described in [[hdfs-datanode-handshake-and-heartbeat]], and the NameNode's own metadata durability rests on the image/journal/checkpoint machinery in [[hdfs-image-and-journal]], which can be delegated to a [[hdfs-checkpointnode-and-backupnode|CheckpointNode or BackupNode]].

*See also: [[gfs]] · [[hdfs-image-and-journal]] · [[hdfs-checkpointnode-and-backupnode]] · [[hdfs-datanode-handshake-and-heartbeat]] · [[hdfs-client-read-write-and-lease]] · [[hdfs-block-placement-and-replication-management]]*
