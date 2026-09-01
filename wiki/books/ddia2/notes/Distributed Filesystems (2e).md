---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing in Distributed Systems
type: subtopic
tags: [ddia2, hdfs, dfs, namenode, erasure-coding, fuse, nfs]
sources:
  - raw/ch11.md
---
# Distributed Filesystems
> Every layer of your local filesystem has a distributed counterpart. Bigger blocks, data nodes instead of block devices, a metadata service instead of inodes, and a protocol instead of the VFS.

## The Idea
**A local filesystem has four layers:** **block device drivers** speaking directly to the disk; a **page cache** keeping recently accessed blocks in memory; a **filesystem layer** (ext4, XFS) breaking files into blocks and tracking inodes, directories, and files; and the **virtual filesystem (VFS)**, the common API that lets applications read and write in a standard way regardless of the underlying filesystem.

**Distributed filesystems work in much the same way.**

## How It Works
**Blocks.** **Files are broken into blocks distributed across many machines**, and **DFS blocks are typically much larger than local blocks**: **HDFS defaults to 128 MB**, while **JuiceFS and many object stores use 4 MB** — **much larger than ext4's 4,096 bytes.** **Larger blocks mean less metadata to track, which makes a big difference on petabyte-sized datasets, and they lower the overhead of seeking to a block relative to reading it.**

**Most physical storage devices can't write partial blocks, so operating systems require writes to use an entire block even if the data doesn't fill it.** **Since DFS blocks are larger and usually implemented on top of OS filesystems, they don't have this requirement** — **a 900 MB file with 128 MB blocks would have seven full blocks and one 4 MB block.**

**Data nodes.** **Blocks are read by making network requests to the machine storing them.** **Each machine runs a daemon exposing an API that lets remote processes read and write blocks as files on its local filesystem** — **HDFS calls these DataNodes, GlusterFS calls them `glusterfsd` processes**; the book calls them **data nodes**.

**Caching.** **Since DFS blocks are stored as files on data nodes, reads and writes go through each node's operating system, including its in-memory page cache** — **keeping frequently read blocks in memory.** **Some distributed filesystems implement more caching tiers**, such as **JuiceFS's client-side and local disk caching.**

**Metadata.** ext4 and XFS track free space, block locations, directory structures, and permissions; **distributed filesystems need to track file locations across machines too.** **Hadoop has a NameNode service maintaining cluster metadata; DeepSeek's 3FS has a metadata service persisting to a key-value store such as FoundationDB.**

**Protocols — the VFS analogue.** **A DFS must expose a protocol or interface so batch systems can read and write files.** **This acts as a pluggable interface: any DFS may be used so long as it implements the protocol.** **Amazon S3's API has been widely adopted by MinIO, Cloudflare's R2, Tigris, Backblaze's B2, and many others** — **so batch systems with S3 support can use any of them.**

**Some DFSs implement POSIX-compliant filesystems that appear to the VFS like any other filesystem**, using **FUSE** or **NFS** to integrate. **NFS is perhaps the most well-known distributed filesystem protocol**, originally developed to let multiple clients read and write on a single server; **more recently Amazon EFS and Archil provide NFS-compatible distributed implementations that are far more scalable** — **NFS clients still connect to one endpoint, but underneath these systems talk to distributed metadata services and data nodes.**

## Trade-offs & Pitfalls
> **Distributed filesystems and network storage.** **DFSs are based on the shared-nothing principle**, in contrast to the **shared-disk approach of NAS and SAN.** **Shared-disk storage is implemented by a centralized storage appliance, often with custom hardware and special network infrastructure such as Fibre Channel** — **the shared-nothing approach requires no special hardware, only computers connected by a conventional datacenter network.**

- **Many DFSs are built on commodity hardware, which is less expensive but has higher failure rates.** **To tolerate machine and disk failures, file blocks are replicated on multiple machines** — **which also lets schedulers distribute workloads more evenly, since they can execute a task on any node holding a replica of its input data.**
- **Replication may mean keeping several full copies, or using an erasure coding scheme such as Reed–Solomon codes, which allows lost data to be recovered with lower storage overhead than full replication.** **The techniques are similar to RAID; the difference is that in a DFS, file access and replication happen over a conventional datacenter network without special hardware.**

## Examples & Systems
HDFS (128 MB blocks, DataNodes, NameNode); GlusterFS, CephFS, JuiceFS, DeepSeek 3FS; MinIO, R2, Tigris, B2 as S3-API implementations; FUSE and NFS; Amazon EFS and Archil.

## Since the 1st Edition
The 1st edition covered HDFS inside [[MapReduce and Distributed Filesystems]], including NameNodes, block replication, erasure coding, and the shared-nothing-versus-NAS/SAN contrast. **The 2nd edition promotes it to its own subtopic and restructures it around the four-layer local-filesystem analogy** — block devices, page cache, filesystem, VFS — which is new. **Also new:** JuiceFS, DeepSeek 3FS, the S3 API as a de facto pluggable protocol with its five implementations, and FUSE/NFS integration including Amazon EFS and Archil.

## Related
- up: [[Batch Processing in Distributed Systems (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Object Stores (2e)]] — the increasingly common alternative
- [[Shared-Memory, Shared-Disk, and Shared-Nothing Architectures (2e)]] — the architectural contrast
- 1st edition: [[MapReduce and Distributed Filesystems]] — where HDFS was covered
