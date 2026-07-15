---
persona: vutr
kind: entity
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

The Google File System (GFS), described in Google's 2003 paper, is a distributed file system Google built for its own internal data-processing workloads. Vu's notes on it are explicit that the paper's assumptions still generalize two decades on: [[component-failure-as-normal|component failure is treated as normal rather than exceptional]], files are multi-GB and workloads run into many TBs with billions of objects, mutations are dominated by appends rather than overwrites (random writes are rare, and files once written are mostly read sequentially), and high bandwidth matters more than low latency. GFS's interface resembles a familiar hierarchical file system (directories, pathnames, create/delete/open/close/read/write) without implementing POSIX, and adds two operations tailored to those assumptions: **snapshot** (cheap copy of a file or directory tree — [[gfs-snapshot-and-namespace-locking]]) and **record append** (concurrent atomic appends — [[gfs-record-append]]).

Architecturally, a GFS cluster has a single master, many chunkservers, and many clients. Files are divided into fixed-size **chunks** — Google settled on 64MB, larger than typical file-system block sizes at the time — each identified by an immutable, globally unique 64-bit chunk handle assigned by the master at creation. Chunkservers store chunks as plain Linux files on local disk; GFS replicates each chunk on three chunkservers by default for reliability. The master communicates with chunkservers via periodic **HeartBeat** messages, and it handles all filesystem metadata (namespace, access control, file-to-chunk mapping, chunk locations), plus lease management, garbage collection, and chunk migration — see [[gfs-metadata-and-operation-log]] and [[gfs-replica-management-and-fault-tolerance]].

The single-master design is deliberate rather than a limitation Google backed into: it simplifies the system and lets the master make sophisticated placement/scheduling decisions using global knowledge, while the master's *involvement* in reads and writes is deliberately minimized so it never becomes a bottleneck. A client asks the master only "which chunkservers should I contact?", caches the answer, and then talks to chunkservers directly for the actual data ([[gfs-lease-and-write-pipeline]]). The large 64MB chunk size reduces how often clients need to hit the master (one lookup often covers many operations on the same chunk), lets clients hold a persistent TCP connection to a chunkserver, and shrinks the metadata the master must track — at the cost of small files with only a few chunks becoming hot spots if many clients access them concurrently.

*See also: [[gfs-metadata-and-operation-log]] · [[gfs-consistency-model]] · [[gfs-lease-and-write-pipeline]] · [[gfs-record-append]] · [[gfs-replica-management-and-fault-tolerance]] · [[gfs-snapshot-and-namespace-locking]] · [[hdfs]]*
