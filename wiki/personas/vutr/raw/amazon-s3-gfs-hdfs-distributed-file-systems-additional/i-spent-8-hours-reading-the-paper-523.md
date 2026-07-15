---
title: "The Hadoop Distributed File System"
channel: vutr
author: "Vu Trinh"
published: 2024-05-18
url: https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper-523
paid: false
topics: ["Data Engineering", "Data Lake", "Lakehouse", "Streaming"]
tags: [block, https, namenode, hdfs, file, auto]
---

# The Hadoop Distributed File System

*Everything you need to know about the HDFS*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper-523)

## Topics

[[data-engineering|Data Engineering]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

> *Hi, I am Vu Trinh, a data engineer.*
>
> *Welcome to my knowledge hub, a place where I am excited to share the valuable insights and discoveries I've gained from my data engineering journey.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!aPaZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2303091-935b-4860-b650-8df7fd9fe019_1398x998.png)](https://substackcdn.com/image/fetch/$s_!aPaZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2303091-935b-4860-b650-8df7fd9fe019_1398x998.png)

Image created by the author.

---

## Table of contents

* *Paper’s Introduction*
* *HDFS’s architecture*
* *HDFS’s file I/O operations and replica management*
* *HDFS practice at Yahoo!*

---

## Intro

In the cloud era, cloud object storage is the first choice for data engineers when building a data lake solution. It can store anything you put in with theoretically unlimited scalability. The providers ensure the durability and availability of your data. If you [twist](https://vutr.substack.com/p/do-we-need-the-lakehouse-architecture) it, you can do the analytics on top of the cloud object storage.

But what if you were in the 2010s when cloud providers were not mature enough, and companies preferred to build solutions on their servers…

…what is your choice to build a scalable and reliable data lake?

Hadoop Distributed File System (HDFS) might be what you need.

To figure out how HDFS was so popular in the past, I spent a few hours reading the paper [The Hadoop Distributed File System](https://ieeexplore.ieee.org/document/5496972) at the weekend. This blog is all my notes after reading it.

---

## Paper’s Introduction

At Yahoo, Hadoop clusters span 25,000 servers and store 25 petabytes of data, with the largest cluster being 3500 servers. Hadoop is an Apache project; all components are available via the Apache open-source license. Yahoo! has contributed to 80% of the core of Hadoop (HDFS and MapReduce). HDFS is Hadoop’s file system component. Its interface is patterned after the UNIX file system. Like Google File System (GFS), HDFS separates the system metadata and data. It stores metadata on a dedicated NameNode server and data on other servers called DataNodes. All servers communicate with each other using TCP-based protocols.

HDFS replicates data on multiple DataNodes for reliability, similar to the GFS. This strategy ensures data durability and gives more opportunities for locating computation close to the needed data.

The following sections describe the HDFS’s architecture

## NameNode

The HDFS’s namespace is a hierarchy of files and directories. It represents files and directories on the NameNode by *inodes*, which contains permissions, modification and access times, namespace, and quotas. HDFS splits the content into large blocks (128 megabytes, but can be configurable by the user), and each block is independently replicated at multiple DataNodes (three at default).

[![](https://substackcdn.com/image/fetch/$s_!_cKl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8321d7f4-8e50-4990-a3c2-169c33106c5c_582x394.png)](https://substackcdn.com/image/fetch/$s_!_cKl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8321d7f4-8e50-4990-a3c2-169c33106c5c_582x394.png)

Block’s replication. Image created by the author.

The NameNode also maintains the namespace tree and the mapping of file blocks and DataNodes. If a client wants to read the data, it must first contact the NameNode for the blocks’ locations; after that, the client will read the block from the nearest DataNode. For the writing operations, the client asks the NameNode to nominate a set of three DataNodes to host the block replicas. It then writes data to these DataNodes in a pipeline fashion.

[![](https://substackcdn.com/image/fetch/$s_!WZk6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66897d26-4d36-4f5c-afa7-db9c5c588c4c_600x770.png)](https://substackcdn.com/image/fetch/$s_!WZk6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66897d26-4d36-4f5c-afa7-db9c5c588c4c_600x770.png)

A sketch of the inode, the image, and the checkpoint. Image created by the author.

HDFS keeps the entire namespace in RAM. The inode data and the blocks to each file mapping that have the metadata are called the *image*. HDFS persists the image’s record in the local file system, called *checkpoint*.

[![](https://substackcdn.com/image/fetch/$s_!HgBp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F511a2cfc-c235-43b2-9353-267aa4f4d051_624x464.png)](https://substackcdn.com/image/fetch/$s_!HgBp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F511a2cfc-c235-43b2-9353-267aa4f4d051_624x464.png)

A sketch on HDFS’s journal. Image created by the author.

The NameNode also stores the image’s modification log, called the *journal,* in the local file system. To improve the durability of the operations, HDFS replicates multiple copies of checkpoints and journals at other servers. On the other hand, HDFS does not persist in the block replicas’ locations because this information changes over time.

> *HDFS's log persists and replicates behavior similar to GFS’s operation log. You can find more about it in my previous GFS article [here](https://open.substack.com/pub/vutr/p/i-spent-8-hours-reading-the-paper?r=2rj6sg&utm_campaign=post&utm_medium=web).*

---

## DataNodes

Each block replica on a DataNode has two files in the local file system. The first one stores the data, and the second is the metadata, which includes the block data’s checksums and the block’s generation stamp. Each DataNode must connect to the NameNode during startup for the handshake protocol; this helps verify the namespace ID and the software version of the DataNode. If there is a mismatch with NameNode, the DataNode automatically shuts down.

[![](https://substackcdn.com/image/fetch/$s_!R1kD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28063a93-7390-44e4-b5ec-8878e5c5fa25_613x382.png)](https://substackcdn.com/image/fetch/$s_!R1kD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28063a93-7390-44e4-b5ec-8878e5c5fa25_613x382.png)

The handshake protocol between the DataNode and the NameNode. Image created by the author.

The namespace ID is assigned to the file system instance and persisted on all the cluster’s nodes. Nodes with a different namespace ID can’t join the cluster, thus protecting the file system’s integrity. Incompatible software versions may cause data corruption or loss; the handshake protocol ensures shutting down nodes that were not available during the upgrade.

After the handshaking, the DataNode registers with the NameNode and has a unique *storage ID.* This ID is used to identify the DataNode internally and will never change regarding the change of the DataNode’s IP. The DataNode sends a block report to the NameNode to inform its responsible block replicas. This report contains the block ID, the generation stamp, and each block replica’s length. DataNode will send the first report right after its registration, and the following reports will be sent every hour to keep the NameNode updated.

To prove they can operate normally, the DataNodes send heartbeats to the NameNode every three seconds at default. If the NameNode does not hear a heartbeat from a DataNode in ten minutes, the NameNode considers the DataNode down and its block replicas unavailable. In this case, the NameNode instructs the creation of new replicas of those blocks on other DataNodes. The heartbeat messages also have DataNode’s information, such as storage capacity, fraction of in-use storage, and the number of data transfers currently in progress. The NameNode uses this information for space allocation and load-balancing decisions.

The NameNode uses the heartbeat replies to instruct the DataNodes. The instructions include commands to:

* Blocks replication to other nodes
* Local block replicas removal
* The node re-registration or shutdown
* Immediate block report sending

---

## HDFS Client

Applications access the file system using the HDFS client. For file operations, HDFS supports reading, writing, and deleting; for the directories, it supports creating and deleting. When an application wants to execute read operations, the client first communicates the NameNode for the list of DataNodes that have replicas of the file’s blocks. Then, it contacts a DataNode to read the desired block.

[![](https://substackcdn.com/image/fetch/$s_!4sOW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F058dd3cb-f138-49f8-97a6-fe9e055bb637_545x392.png)](https://substackcdn.com/image/fetch/$s_!4sOW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F058dd3cb-f138-49f8-97a6-fe9e055bb637_545x392.png)

HDFS client's read request. Image created by the author.

With the write operations, the client first asks the NameNode to assign DataNodes to host replicas of the first file’s block. After getting the DataNode lists, the client organizes a data pipeline from node to node and sends the data. When the first block is finished written, the client asks the next DataNodes from the list to handle the next block’s replicas.

[![](https://substackcdn.com/image/fetch/$s_!954J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb46dbbe-7ea5-4c56-a1ae-ef6c8eda9e89_555x471.png)](https://substackcdn.com/image/fetch/$s_!954J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb46dbbe-7ea5-4c56-a1ae-ef6c8eda9e89_555x471.png)

HDFS client's write request. Image created by the author.

Moreover, HDFS supports an API that provides the locations of file blocks. This lets applications like the MapReduce framework schedule a task locally with the data, which can improve performance. HDFS also allows an application to configure the file’s replication factor, which is three by default. For critical files or files accessed often, having a higher replication factor will improve the data durability and increase the read bandwidth.

---

## Image and Journal

The image is the file system metadata that describes the organization of data. A persistent record of the image in a disk is called a checkpoint. The journal is a write-ahead commit log of changes to the file system. For each transaction, the change is recorded in the journal. The NameNode never changes the checkpoint file; it is entirely replaced when a new checkpoint is created during restart. When starting up, the NameNode initializes the namespace image using the checkpoint and replays any changes from the journal to make the image up-to-date. The namespace information will be corrupt if a checkpoint or journal is missing. So, HDFS can store the checkpoint and journal in multiple directories to prevent losing critical information.

---

## CheckpointNode

Besides serving client requests, the NameNode can act as a CheckpointNode or a BackupNode. HDFS assigns one of the two roles to the node at startup. For example, the cluster can have two NameNode, one for serving the client request and one for the CheckpointNode.

The CheckpointNode periodically merges the existing checkpoint and journal to produce a new checkpoint and an empty journal. It downloads the current checkpoint and journal from the NameNode and merges them locally. Finally, it returns the output checkpoint to the NameNode. This keeps the journal manageable. A large journal increases the chance of journal file loss or corruption. Moreover, it requires more time for the NameNode to restart when the journal is too large.

---

## BackupNode

Like a CheckpointNode, the BackupNode can create periodic checkpoints. What differentiates it from the CheckpointNode is that it maintains an in-memory, up-to-date file system namespace image that syncs with the NameNode’s state. Unlike CheckpointNode, the BackupNode does not need to download the checkpoints and journals from NameNode. It receives the journal stream of transactions from an active NameNode and stores them in its storage directories. The BackupNode then applies these transactions to its namespace image located in memory. If the NameNode fails, the BackupNode’s image in memory and the checkpoint on disk is a record of the latest namespace state. The BackupNode can be considered as a read-only NameNode. It contains all file system metadata information except block locations, which can only be retrieved by the block report from the DataNode sent to the NameNode.

---

## Snapshots

The snapshot mechanism allows saving the current state of the file system so that if the upgrade results in corruption, it can roll back the upgrade and return the HDFS state as it was at the time of the snapshot. If there is a request to create the snapshot, the NameNode merges the current checkpoint and journal files in memory. Then, it writes the new checkpoint and the empty journal in a new location.

During the handshake, the NameNode instructs the DataNode to create a local snapshot. The DataNode cannot take the snapshot by replicating the actual data files directories, which will cause double the storage required on every DataNode. Instead, each DataNode creates a copy of the storage directory and hard links with existing block files.

The administrator can rollback HDFS to the snapshot state when restarting the system. The NameNode recovers using the checkpoint saved when the snapshot was created. DataNodes restores the previously renamed directories and starts a background process to delete block replicas created after the snapshot’s creation time.

The following sections describe the HDFS’s file I/O operations and replica management.

## File Read and Write

### Write

When applications want to add data to HDFS, they create a new file and write the data to it. After the file is closed, the content cannot be changed or removed. HDFS only allows reopening the file for data append. HDFS implements a single-writer, multiple-reader model.

HDFS grants the file’s lease to the client who opens a file to write. Only the client with the lease can execute the write. During the process, the holding lease client periodically renews the lease by sending a heartbeat to the NameNode. HDFS revoked the lease when the file was closed.

A soft limit and a hard limit constrain the lease duration. The writer has exclusive access to the file until the soft limit expires. If it expires and the client fails to close the file or renew the lease, another client can take it. If, after the hard limit, the client fails to renew the lease, HDFS considers that the client has quit and will close the file on behalf of the writer. The lease only affects the write operation; a file can have multiple concurrent readers.

An HDFS file consists of blocks. If a new block is required, the NameNode allocates a block with a unique block ID and determines a list of DataNodes to host the block’s replicas. The DataNodes form a pipeline to minimize the total network distance from the client to the last DataNode. Bytes are pushed to the pipeline as a sequence of packets. The bytes that an application writes first buffer at the client side. The data are pushed to the pipeline after filling a packet buffer (typically 64 KB). The next packet can be moved to the pipeline before receiving the acknowledgment for the previous packets. After writing, HDFS only guarantees the data is visible to a new reader when the file is closed.

[![](https://substackcdn.com/image/fetch/$s_!Pcn8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83ac8102-144a-4201-b0fa-0fe52803eb60_1078x1056.png)](https://substackcdn.com/image/fetch/$s_!Pcn8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83ac8102-144a-4201-b0fa-0fe52803eb60_1078x1056.png)

The block construction process has three typical stages: pipeline setup, data streaming, and closing. Bytes are pushed to the pipeline as a sequence of packets. The next packet can be delivered before receiving the ACK for the previous packets. Figure 2. Data pipeline during block construction. The Hadoop Distributed File System (2010). [Source](https://pages.cs.wisc.edu/~akella/CS838/F16/838-CloudPapers/hdfs.pdf)

To prevent reading corrupt data, the HDFS can verify the checksums while reading to help detect any corruption. HDFS generates and stores checksums for each data block of an HDFS file. When creating an HDFS file, the client computes the checksum sequence for each block and sends it to a DataNode with the data. A DataNode stores checksums in a separate metadata. DataNode sends the block’s data and checksums to the client during the read process. The client then verifies that the newly computed checksums match the ones received. If not, the client informs the NameNode of the corruption and continues the process on a different block’s replica in another DataNode.

[![](https://substackcdn.com/image/fetch/$s_!exrN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f4290a1-be13-432f-9bc8-37cde94bf930_585x578.png)](https://substackcdn.com/image/fetch/$s_!exrN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f4290a1-be13-432f-9bc8-37cde94bf930_585x578.png)

When writing a file, the client computes the block’s checksum and sends it to a DataNode with the data. When reading a file, the client verifies the checksum to avoid corruption. Image created by the author.

### Read

When a client reads a file, it fetches the block replicas’ locations from the NameNode. The locations are ordered by their distance from the reader, which means the closest location will be prioritized for reading first. If the read fails, the client tries the next replica in the defined order. HDFS allows the client to read a file that is currently writing. In this case, the NameNode does not know the length of the last block still being written, so the client asks one of the replicas for the latest length before starting the read process.

---

## Block Placement

A common practice of networking management in large clusters is to spread the nodes across multiple racks. Rack nodes share a [switch](https://en.wikipedia.org/wiki/Network_switch), and one or more core switches connect rack [switches](https://www.ruijienetworks.com/support/tech-gallery/core-switches-and-access-switches). Communication between two nodes in different racks must go through multiple switches. Typically, the network bandwidth between nodes in the same rack is greater than between other racks.

The replica placement is essential to HDFS data reliability and read/write performance. The default HDFS block placement policy can be summarized as follows:

* *No Datanode contains more than one replica of any block.*
* *No rack contains more than two replicas of the same block, given there are sufficient racks on the cluster*

---

## Replication management

One of the NameNode's primary responsibilities is keeping each data block to achieve its desired number of replicas. The NameNode can check this information when receiving the block report from DataNodes. When there are more replicas than needed, the NameNode chooses to remove the replica based on these factors to balance storage utilization without reducing the block’s availability:

* *Not reducing the number of racks that host replicas.*
* *Preferring to remove a replica from the DataNode with the least available disk space.*

With fewer replicas than needed, the NameNode puts the block in the replication priority queue:

* *A block with only one replica has the highest priority.*
* *A block with several replicas greater than two-thirds of its desired replication has the lowest priority.*

A thread periodically scans the head of the replication queue in the background to decide where to place new replicas. Block replication has the same policy as new block placement:

* *If the number of existing replicas is one, HDFS places the next replica on a different rack.*
* *If the block has two existing replicas, if both existing replicas are on the same rack, the third replica is placed on a different rack; otherwise, the third replica is placed on a different node in the same rack as an existing replica.*

The NameNode must ensure that not all block replicas are located on one rack. Suppose this happens: The NameNode treats the block as under-replicated and replicates it to a different rack using the same block placement policy. After this, the block becomes over-replicated. The NameNode then removes an old replica because the over-replication policy prefers to keep the number of racks the same.

---

## Balancer

[![](https://substackcdn.com/image/fetch/$s_!oGJw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0487da90-959e-47c8-ba0f-7827b7f9d5f1_528x579.png)](https://substackcdn.com/image/fetch/$s_!oGJw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0487da90-959e-47c8-ba0f-7827b7f9d5f1_528x579.png)

The HDFS’s balancer. Image created by the author.

The balancer helps balance disk space usage on the HDFS cluster. It accepts a threshold value as an input parameter. The threshold is in the range of (0, 1). A cluster is in a balanced state if, for each DataNode, the node’s utilization (used space / total capacity) differs from the utilization of the whole cluster (used space / total capacity of the cluster) by no more than the threshold value.

Besides the threshold, the balancer also accepts the bandwidth limitation used by the rebalancing process as the second parameter; the higher the limit bandwidth, the faster a cluster can reach the balanced state. The lower the limit bandwidth, the less effect the rebalancing process will have on other operations (e.g., it will not take much bandwidth from the reads/writes)

The tool will move replicas from DataNodes with higher utilization to those with lower utilization. When choosing a replica to move and its destination, the balancer guarantees that the decision does not reduce the number of replicas or racks. The balancer minimizes rack-to-rack data copying. Suppose the balancer moves replica A to a different rack, and the destination rack has a replica B of the same block. In that case, the balancer will copy data from replica B instead of A.

---

## Block Scanner

[![](https://substackcdn.com/image/fetch/$s_!bVjV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6be366ed-a0ea-48fb-be66-acc85f858f6c_576x395.png)](https://substackcdn.com/image/fetch/$s_!bVjV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6be366ed-a0ea-48fb-be66-acc85f858f6c_576x395.png)

A brief on the Block Scanner. Image created by the author.

The DataNode periodically runs the block scanner to check if the block data matches the stored checksums. The system stores each block’s verified time in a human-readable log. When a read client or a block scanner detects block corruption, it informs the NameNode. The NameNode marks the replica as corrupt but does not delete the replica right away; instead, it executes the block replication from a valid block. Only when the valid replica count reaches the desired number of replications does the NameNode schedule for deletion of the corrupt replica.

---

## Decommissioning

The cluster administrator controls node membership by listing the host addresses of permitted (included list) and non-permitted nodes (excluded list). The administrator can ask the running system to re-evaluate these lists. The system marks a current joining node decommissioning when that node belongs to the excluded list. Once a DataNode is marked as decommissioning, the NameNode will leave out this node when it chooses the target for replica placement. The block’s replicas of this DataNode will be replicated to other nodes by NameNode. Once the NameNode is informed that all blocks on the decommissioning node are replicated, the node can be safely removed from the cluster without affecting the cluster’s operations.

---

## Inter-Cluster Data Copy

[![](https://substackcdn.com/image/fetch/$s_!iHJJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cd8f279-5809-41b1-963f-daad9cb3c315_577x345.png)](https://substackcdn.com/image/fetch/$s_!iHJJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cd8f279-5809-41b1-963f-daad9cb3c315_577x345.png)

A brief on HDFS DistCp. Image created by the author

HDFS provides a *DistCp* tool for large inter/intra-cluster parallel copying. Under the hood is a MapReduce job; each map task copies a set of the source data into the destination. The MapReduce framework handles the parallel task scheduling, error detection, and recovery of the copy job.

---

## Outro

We’ve gone through the design and architecture of HDFS, which I believe share many things in common with the Google File System. One of the essential reasons why HDFS was so popular is that it can operate on commodity machines with robust mechanisms and protocols to ensure data availability and reliability. I hope my work brings some value.

See you next time!

---

## **References**

[1] Konstantin Shvachko, Hairong Kuang, Sanjay Radia, Robert Chansler, [The Hadoop Distributed File System](https://ieeexplore.ieee.org/document/5496972) (2010).

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper-523/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
