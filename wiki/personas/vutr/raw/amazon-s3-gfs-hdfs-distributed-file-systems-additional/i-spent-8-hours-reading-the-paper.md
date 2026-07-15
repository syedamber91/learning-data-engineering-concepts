---
title: "All you need to know about the Google File System"
channel: vutr
published: 2024-05-11
url: https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper
paid: false
topics: ["Data Engineering", "Streaming"]
tags: [master, chunk, file, https, auto, google]
---

# All you need to know about the Google File System

*How did Google build its large-scale file system?*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper)

## Topics

[[data-engineering|Data Engineering]] · [[streaming|Streaming]]

---

> *My name is Vu Trinh, and I am a data engineer.*
>
> *I’m trying to make my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!wAqm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69f439d1-b704-4900-b386-d4ad7feb2813_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!wAqm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69f439d1-b704-4900-b386-d4ad7feb2813_1400x1000.png)

Image created by the author.

---

***Before we move on**, I need your help. Besides Saturday blog posts, I’m planning to publish one more blog every Thursday, and I’m brainstorming the style of these blogs. It would help me a lot if you could spend 5 seconds doing the below poll for me:*

---

## Table of contents

* *Paper’s Introduction*
* *Design Overview*
* *System Interactions*
* *Master operation*
* *Fault Tolerance*

---

## Intro

To expand my writing topic, I’ve recently decided to read papers other than those about the OLAP system. After searching for a while, I landed on this [excellent repo](https://github.com/DataExpert-io/data-engineer-handbook?tab=readme-ov-file) with valuable data engineering resources. Based on the recommendation of the repo, I chose to read the paper [The Google File System](https://research.google/pubs/the-google-file-system/). Despite being written in 2003, I realized the paper contained a lot of valuable insight and knowledge from Google when they built their distributed large-scale file system, so I decided to note down everything I learned after reading it in this blog.

> ***Note**: The paper was published in 2003, so some details may be changed or updated now; if you have any feedback or information that can supplement my blog, feel free to comment.*

---

## Paper’s Introduction

Google designed the Google File system (GFS) to adapt to the increasing demands of internal data processing workloads. The observations of Google application workloads and the technological environment drive the GFS design. Here are some key points:

* **Component failure is no longer unexpected behavior**: this includes hardware failure (disk, memory, power supplies…) or software failure (bugs, human errors,…). This implies the need for monitoring, error detection, fault tolerance, and automatic recovery.
* **Files are enormous by traditional standards:** Multi-GB files are regular. User internal workloads usually work with data sets of many TBs with billions of objects.
* **File mutations are done mainly by appending new data rather than overwriting existing data.** Random writes in a file are rare. After being written, the files are only read, and often only sequentially. Given this, appending becomes the focus of performance optimization and atomicity guarantees.

The following sections will describe the design of Google's File System.

## Assumptions

Google describes their assumptions when designing the GFS in more detail:

* *The system is built from many inexpensive commodity components that often fail.*
* *The system stores a modest number of large files. They expect a few million files, each typically 100 MB or larger.*
* *The read workloads typically consist of large streaming reads (subsequence operations read through a contiguous file region) and small random reads (read at specific file offset).*
* *The workloads have many large, sequential writes that append data to files.*
* *The system must efficiently implement semantics for multiple clients that append to the same file concurrently.*
* *High bandwidth is more important than low latency*

## Interface

Like other file systems, GFS provides a familiar interface but does not support standard APIs like [POSIX](https://vi.wikipedia.org/wiki/POSIX). It organizes files in directories and identifies them by pathnames. GFS supports operations to create, delete, open, close, read, and write files. GFS also implements snapshot and record append operations:

* *Snapshot creates a copy of a file or a directory tree cheaply.*
* *Record append allows multiple clients to append data to the same file concurrently while guaranteeing the atomicity of each client’s append.*

## Architecture

[![](https://substackcdn.com/image/fetch/$s_!6Opr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F323bf056-f3b4-48c7-9599-df9f4cde347f_1360x857.png)](https://substackcdn.com/image/fetch/$s_!6Opr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F323bf056-f3b4-48c7-9599-df9f4cde347f_1360x857.png)

GFS’s high-level architecture. Image created by the author.

A GFS cluster has a single master, multiple chunkservers, and multiple clients. GFS divides files into fixed-size chunks. The system identifies each chunk by an immutable and globally unique 64-bit chunk handle assigned by the master at the creation time. Chunkservers store chunks on local disks and read/write chunks using a chunk handle and byte range. GFS replicates chunks on multiple chunkservers (three replicas by default) for reliability.

The master handles all file system metadata, including the namespace, access control information, mapping from files to chunks, and chunk locations. It also controls chunk lease management, garbage collection, and chunk migration between chunkservers. The master communicates with each chunkserver periodically through *HeartBeat* messages.

> *Lease management and garbage collection operations will be covered in upcoming sections.*

The GFS client communicates with the master and chunkservers to read or write data. Clients interact with the master only for metadata operations; they communicate directly to the chunkservers for data-related operations.

## Single Master

Having a single master simplifies the GFS design and allows the master to make sophisticated decisions using global knowledge. To prevent the master from being the bottleneck, Google minimizes its involvement in reads and writes. A client never reads and writes file data through the master. Instead, it asks the master, " Hey, which chunkservers should I contact?” then the client caches this information and interacts with the chunkservers directly for subsequent operations.

[![](https://substackcdn.com/image/fetch/$s_!n2F-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28cb4bd0-d007-453b-83de-326643735bc3_777x895.png)](https://substackcdn.com/image/fetch/$s_!n2F-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28cb4bd0-d007-453b-83de-326643735bc3_777x895.png)

The interactions for a simple read. Image created by the author.

## Chunk Size

Google decided on a chunk size of 64 MB, which was more significant than most file system block sizes at the time. GFS stores each chunk replica as a plain Linux file on a chunkserver. A large chunk size has several advantages:

* *Reducing clients’ need to interact with the master because operations on the same chunk require only one initial request to the master for chunk location.*
* *Since a large chunk, the client is more likely to perform many operations on a given chunk, this can reduce network overhead by keeping a persistent TCP connection to the chunkserver.*
* *Reducing the size of the metadata stored on the master.*

Still, the large-size chunk approach has a disadvantage: with a small file consisting of a few chunks, the chunkservers storing those chunks may become hot spots if many clients access the same file.

[![](https://substackcdn.com/image/fetch/$s_!KuND!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03d250bf-53ac-4a6d-acfd-732721ff4cc9_499x472.png)](https://substackcdn.com/image/fetch/$s_!KuND!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03d250bf-53ac-4a6d-acfd-732721ff4cc9_499x472.png)

Image created by the author.

## Metadata

[![](https://substackcdn.com/image/fetch/$s_!Iyg0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff597e486-81f2-42ae-9190-e9d8d1e2473f_1183x877.png)](https://substackcdn.com/image/fetch/$s_!Iyg0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff597e486-81f2-42ae-9190-e9d8d1e2473f_1183x877.png)

There are three major types of metadata. Image created by the author.

The master stores three major types of metadata: the file and chunk namespaces, the files-to-chunks mapping, and the chunk’s replica locations. The master keeps the metadata in memory. It also persists the namespaces and file-to-chunk mapping metadata by logging the mutations to an operation log, which is stored on the master’s disk and replicated on remote machines. The log lets Google update the master state simply and reliably when a master crashes. For the chunk location metadata, instead of storing on the master itself, it asks for this information from the chunkserver at the time the master startup and whenever a new chunkserver joins the cluster.

### In-Memory Data Structures

Master operations are fast, thanks to the metadata stored in the memory. This allows the master to scan the entire state behind the scenes. Google uses this scanning to implement chunk garbage collection, re-replication, and chunk migration. However, storing all the metadata in the memory will be constrained to the amount of the master’s memory. Google states that *the cost of adding extra memory to the master is an insignificant tradeoff for the system's simplicity, reliability, and performance by storing the metadata in memory*.

### Chunk Locations

The master does not initially store the metadata of the chunk locations. It polls the chunkservers for this information at startup. The master can keep updated after that because it controls all chunk placement and monitors chunkservers with HeartBeat messages. This approach eliminated the need to keep the master and chunkservers in sync when chunkservers memberships change.

### Operation Log

The operation log contains a historical record of the metadata changes. It is the only persistent record of metadata (stored on the master’s local disks) and serves as a logical timeline that records the order of concurrent operations. Due to its importance, Google stores the log redundantly outside the master; they replicate the log on multiple remote machines and respond to a client operation only after flushing the corresponding log record to the master’s local disk and the remote machines’ disks.

The master recovers its state by replaying the operation log. Google keeps the log small to minimize the startup time. The master writes the checkpoints of its state whenever the log grows beyond a certain threshold. This helps the master recover by only loading the latest checkpoint from the disk and replaying for only a limited number of log records afterward. The checkpoint has a B-tree-like data structure that can be directly mapped into memory.

[![](https://substackcdn.com/image/fetch/$s_!wrYV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf0c1061-3a8e-4af6-bada-d40fff5ddf53_589x677.png)](https://substackcdn.com/image/fetch/$s_!wrYV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf0c1061-3a8e-4af6-bada-d40fff5ddf53_589x677.png)

The Operation Log. Image created by the author.

The master’s internal state is carefully structured so a new checkpoint can be created without affecting incoming metadata mutations. The master switches to a new log file and creates the new checkpoint in a separate thread. The new checkpoint has all mutations before the switch. When completed, it is written to disk both locally and remotely. Recovery needs only the latest ***complete*** checkpoint and subsequent log files. Older checkpoints and log files can be deleted. A failure during checkpointing does not affect the correctness because the recovery process detects and skips incomplete checkpoints.

## Consistency Model

GFS has a consistency model that well supports distributed applications but remains simple and efficient to implement

### Guarantees by GFS

The state of a file region after a mutation depends on whether it succeeds or fails and whether there are concurrent mutations.

[![](https://substackcdn.com/image/fetch/$s_!Fqgd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cedf5d1-7138-43d2-bd24-86c3824b7414_1044x350.png)](https://substackcdn.com/image/fetch/$s_!Fqgd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cedf5d1-7138-43d2-bd24-86c3824b7414_1044x350.png)

File Region State After Mutation. Table 1, The Google File System (2003). [Source](https://research.google/pubs/the-google-file-system/)

> ***Description***
>
> *- A file region is consistent if all clients see the same data, regardless of which replicas they read from.*
>
> *- If a file data mutation is consistent, a region is defined after it, and clients will see what the mutation writes in its entirety. → If the data is defined, it must be consistent first.*

When a mutation succeeds without concurrent writers, the affected region is defined (which means it is also consistent). Concurrent successful mutations leave the region consistent but undefined: all clients see the same data, but they may not reflect any mutation. Typically, it consists of mixed fragments from multiple mutations. A failed mutation makes the region inconsistent; clients see different data at different times.

Data mutations may be `writes` or `record appends`. The first writes the data at a specified file offset defined by the application. The later append records at an offset of GFS’s choosing atomically at least once, even if there are concurrent mutations. The system then returns the offset to the client and marks the beginning of a defined region. After a sequence of successful mutations, the mutated file region is guaranteed to be defined; GFS achieves this by:

* *Applying mutations to a chunk in the same order on all its replicas*
* *Using chunk version to detect any replica that had become stale due to mutations missing when its chunkserver was down. Stale replicas will not be involved in a mutation or given to clients asking the master for chunk locations. GFS garbage collects these replicas as soon as possible.*

Component failures can corrupt or destroy data after a successful mutation. GFS detects the failed chunkservers by regular handshakes between master and chunkservers and detects corruption by checksumming. GFS restores the data from a valid replica as soon as possible after the failures occur.

### Implications for Applications

The applications can adapt to the GFS’s consistency model with simple techniques: relying on appends rather than overwrites, checkpointing, and writing self-validating, self-identifying records.

In one typical use case, a writer creates a file from beginning to end. It renames the file to a permanent name after writing all the data or periodically checkpoints how much has been successfully written. Checkpoints may also be included in the application-level checksums. Readers will verify and process only the file region until the last checkpoint. Checkpointing allows writers to restart incrementally and keeps readers from processing successfully written files.

In the other use case, writers concurrently append to a file as a producer-consumer queue. GFS preserves each writer’s output. Concurrent writers will add extra information like checksums in each record so that readers can verify its validity. The checksums allow the reader to detect and discard extra padding and record fragments.

The following sections will describe how the client, master, and chunkservers interact with each other.

## Leases and mutation order

A mutation is an operation that changes the chunk's contents or metadata. GFS performs each mutation at all the chunk’s replicas. Google implements a lease mechanism to ensure consistent mutation order across replicas. The master grants a chunk lease to one of the replicas (the primary). The primary picks a serial order for all mutations to the chunk. All replicas must follow this order when mutations are applied. This way, the primary defines the global mutation order. This mechanism is designed to reduce the master management overhead. The lease has a default timeout of 60 seconds, but the primary can request the timeout extensions from the master. The master may sometimes try to revoke a lease before it expires in some scenarios, such as the master wanting to stop the mutations on a renamed file. The master can grant a new lease to another replica after the old lease expires if it loses communication with the primary. Let's visit an example of the leasing flow from the paper:

[![](https://substackcdn.com/image/fetch/$s_!vHE5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9eb255b-1a60-4021-9e44-0fe849d4720f_730x606.png)](https://substackcdn.com/image/fetch/$s_!vHE5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9eb255b-1a60-4021-9e44-0fe849d4720f_730x606.png)

Write Control and Data Flow. Figure 2, The Google File System (2003). [Source](https://research.google/pubs/the-google-file-system/)

* *Step 1: The client asks the master which chunkserver holds the current lease for the chunk and the replicas’ locations.*
* *Step 2: The master replies with the identity of the primary and the locations of the other (secondary) replicas.*
* *Step 3: The client pushes the data to all the replicas. A client can do so in any order.*

> ***Note**: As I understand, in step 3, despite the arrival of the data, all the replicas are not updated with any mutations until the write request from the primary is received in step 5.*

* *Step 4: Once all the replicas have acknowledged receiving the data, the client sends a write request to the primary.*
* *Step 5: The primary forwards the write request to all secondary replicas.*
* *Step 6: The secondaries all reply to the primary, indicating that they have completed the operation*
* *Step 7: The primary replies to the client*

GFS client code breaks the write process down into multiple write operations if the write is too large.

## Data flow

Google separates the control and data flow to use the network efficiently. The control flow from the client begins with the primary (the replica granted a lease) and then to all secondaries. On the other hand, data is linearly pushed along a chain of chunkservers in a pipelined fashion rather than using some network topology (e.g., tree).

## Atomic Record Appends

GFS supports an atomic append operation called record append. In a record append, the client specifies the data only. GFS appends it to the file at least once atomically at an offset chosen by GFS and returns that offset to the client.

[![](https://substackcdn.com/image/fetch/$s_!m1MZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b83100-28ba-4328-ad6d-16f9d6cd18fe_760x894.png)](https://substackcdn.com/image/fetch/$s_!m1MZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b83100-28ba-4328-ad6d-16f9d6cd18fe_760x894.png)

The Atomic Record Appends. Image created by the author.

## Snapshot

The snapshot operation makes a copy of a file or a directory tree while minimizing interruptions caused by ongoing mutations. When the master receives a snapshot request, it will revoke any leases on the chunks from files involved in the request. This ensures that subsequent writes to these chunks communicate with the master to find the leaseholder. This will allow the master to create a new chunk copy first. After revoking the lease, the master logs the operation to disk. It then applies this log record to its in-memory state by duplicating the metadata for the source file or directory tree. The newly created snapshot files point to the same chunks as the source files.

[![](https://substackcdn.com/image/fetch/$s_!mLbx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ea71e1c-d164-4c97-87ea-c444b592035f_683x788.png)](https://substackcdn.com/image/fetch/$s_!mLbx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ea71e1c-d164-4c97-87ea-c444b592035f_683x788.png)

The snapshot process. Image created by the author.

After the snapshot process, the first time the client wants to operate on chunk A from the snapshot, it contacts the master to find the leaseholder. The master notices that the reference count for chunk A is greater than one (both the source file and snapshot file point to this chunk). It asks each chunkserver with a replica of A to create a new chunk called A’. Creating the new chunk locally on the same chunkservers as the original chunk avoids copying data over the network. After the creation of chunk A’, the master handles the request as usual; it grants one of the replicas a lease on the new chunk A’ and replies to the client, who can operate normally.

The following sections will describe operations that the master handles.

## Namespace Management and Locking

Google doesn’t want to delay other GFS master operations while running, given that many operations can take a long time. Therefore, they allow multiple operations to be processed, and locks are used to ensure proper serialization. GFS logically represents the namespace as a lookup table mapping full pathnames to metadata. Each node in the namespace tree (an absolute file name or an absolute directory name) has an associated read-write lock. Each master operation acquires a set of locks before it operates; if it involves /d1/d2/..., it will acquire read-locks on the directory names /d1, /d1/d2, .…

## Replica Placement

The chunk replica placement policy has two purposes:

* Maximizing data reliability and availability
* Maximizing network bandwidth utilization.

GFS spreads chunk replicas across racks to ensure that some chunk replicas will survive and remain available even in case of the failure of an entire rack. For read operations, the traffic can leverage the aggregate bandwidth of multiple racks. In contrast, write traffic must flow through multiple racks, a trade-off that Google makes.

## Creation, Re-replication, Rebalancing

GFS creates chunk replicas for three reasons: chunk creation, re-replication, and rebalancing. The master considers some factors when creating the chunk:

* *Placing new replicas on chunkservers with below-average disk space utilization.*
* *Limit the number of “recent” creations on each chunkserver.*
* *Spreading replicas of a chunk across racks (mentioned in the Replica Placement section. )*

The master re-replicates a chunk right after the number of available replicas falls below a user-specified goal for various reasons, such as when a chunkserver becomes unavailable. Each chunk re-replication is prioritized based on several factors:

* How far is it from its replication goal? For example, a chunk that has lost two replicas has higher priority than a chunk that has lost only one.
* Live file chunks have higher priority than deleted file chunks.
* Chunks that are blocking client progress will have higher priority.

The master picks the highest priority one and clones it by telling some chunkserver to copy the chunk from an existing valid replica. To prevent cloning traffic from affecting client traffic, the master limits the number of active clone operations for the cluster and each chunkserver. Moreover, each chunkserver has its limit on the amount of bandwidth it spends on the clone operation by throttling its read requests to the source chunkserver.

For replica rebalancing, the master periodically checks the current replica distribution and moves replicas to improve disk space and load balancing. The rebalance process also involves filling up data for the new chunkservers.

## Garbage Collection

GFS does not immediately reclaim the deleted file's physical storage. It does this during regular garbage collection at both the file and chunk levels.

When a file is deleted, the master logs the deletion like any other changes. Then, the file is renamed to a hidden name that includes the deletion timestamp. During the master’s regular scan of the file system namespace, any hidden files are removed if they have existed for more than three days (the period is configurable). Until then, the file can still be read under the new, special name and undeleted by renaming it to normal. When the hidden file is removed from the namespace, its in-memory metadata is erased. For the chunk level, the master identifies orphaned chunks in the same regular scan and discards the metadata for these chunks. Chunkservers report a subset of its chunks, and the master replies with the identity of all chunks, not in its metadata. The chunkserver is free to delete its replicas of such chunks.

## Stale Replica Detection

Chunk replicas are stale if they miss the mutations while the chunkserver is down. The master maintains a chunk version number for each chunk to distinguish between up-to-date and stale replicas. Whenever a new lease is granted, the master increases the chunk version number and informs the up-to-date replicas. The master and these replicas all record the new version number in their persistent state. If one chunkserver fails, its replica version number will not be updated. The master will detect if the chunkserver has a stale replica when the chunkserver returns and reports its set of chunks and their version numbers. The master discards stale ones in the regular garbage collection. In addition, the master includes the version number when communicating with the clients. The client can verify the version number when it operates to ensure it always accesses up-to-date data.

The following sections describe how Google File System achieves high availability and data integrity.

## High Availability

GFS keeps the overall system highly available with two strategies: fast recovery and replication:

* ***Fast Recovery:** Both the master and the chunkserver can restore their state and start in seconds in case of terminating. Google does not distinguish between normal and abnormal termination; servers are routinely shut down by killing the process. Clients and other servers will experience a minor downtime on their outstanding requests during the restarting.*
* ***Chunk Replication**: Users can specify different replication levels for different parts of the file namespace. The master clones existing replicas to keep each chunk fully replicated when chunkservers go offline or detect corrupted replicas through checksum verification.*
* ***Master Replication**: The master’s log and checkpoints are replicated on multiple machines. A mutation is committed only after its log record has been flushed to disk locally and remotely. In case of the master failure, monitoring infrastructure outside GFS starts a new master process somewhere else with the replicated operation log.*

## Data Integrity

Chunkservers use checksumming to detect data corruption. A chunk is broken up into 64 KB blocks. Each has a corresponding 32-bit checksum. Checksums are kept in memory and stored persistently with logging. For reads, the chunkserver verifies the checksum of data blocks before returning any data to the client or another chunkserver. If a checksum mismatch occurs in a block, the chunkserver returns an error and reports this behavior to the master. In this case, the requestor will read from other replicas, while the master will clone the chunk from another replica. After a valid new replica is cloned, the master tells the chunkserver that reported the mismatch to delete the invalid replica.

Chunkservers can verify the contents during idle periods to detect corruption in rarely touched chunks. Once the corruption is detected, the master can create a new uncorrupted replica and delete the corrupted one. This prevents an inactive but corrupted replica from fooling the master into thinking it has all “healthy” replicas.

## Diagnostic Tools

GFS servers generate diagnostic logs that record significant events (such as chunkservers going up and down) and all RPC requests and replies. Google tries to keep these logs as long as there is enough space. The RPC logs include the exact requests and responses sent on the wire, except for the file data. By matching requests with replies and collating RPC records on different machines, they can reconstruct the entire interaction history to diagnose a problem. The logs also serve as traces for load testing and performance analysis.

The rest of the papers deliver Google observations from a few micro-benchmarks of the GFS system, but I won’t include them here. You can read it from the original paper.

## Outro

We have gone through all the insights from the Google File System paper. Despite being written in 2003, I believe all the lessons from the paper will never get old. This is not the first time I’ve written about a system that is not an OLAP, but the enormous amount of new things from this paper made me worry a little bit when I started writing about the Google File System. But in the end, I’m happy that I could finish this blog. I hope my work brings some value to you guys.

If you think my blog has some points that need to be corrected, please leave a comment.

It’s time to say goodbye; see you on the next blog.

---

## **References**

[1] Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, [The Google File System](https://research.google/pubs/the-google-file-system/) (2003).

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
