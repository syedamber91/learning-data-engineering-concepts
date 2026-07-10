---
title: "How do we run Kafka 100% on the object storage?"
channel: vutr
author: "Vu Trinh"
published: 2024-08-27
url: https://vutr.substack.com/p/how-do-we-run-kafka-100-on-the-object
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming"]
tags: [https, auto, automq, storage, image, cache]
---

# How do we run Kafka 100% on the object storage?

*Let's see how AutoMQ makes this dream come true.*

> Source: [Open post](https://vutr.substack.com/p/how-do-we-run-kafka-100-on-the-object)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!LwzR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96537f18-5941-4d86-a9dd-a691b553e2cb_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!LwzR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96537f18-5941-4d86-a9dd-a691b553e2cb_2000x1429.png)

Image created by the author.

---

## Intro

This week, I’m excited to explore AutoMQ, a cloud-native, Kafka-compatible streaming system developed by former Alibaba engineers. In this article, we’ll dive into one of AutoMQ’s standout technical features: running Kafka entirely on object storage.

---

## Overview

Before we move on, let’s revisit the Kafka design. The message system uses the OS filesystem for data storage and leverages the kernel page cache mechanism. Rather than trying to keep as much data in memory and flush it to the filesystem, the OS transfers all data to the page cache before flushing it to the disk. All the messages’ write and read operations must go through the page cache.

> *Modern OS systems usually borrow unused memory (RAM) portions for page cache. The frequently used disk data is populated to this cache, avoiding touching the disk directly too often, which lead to performance improvement*

[![](https://substackcdn.com/image/fetch/$s_!bWdn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2503f39-1ef7-43b1-9b17-83d5a339303b_1224x774.png)](https://substackcdn.com/image/fetch/$s_!bWdn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2503f39-1ef7-43b1-9b17-83d5a339303b_1224x774.png)

Apache Kakfa tightly-couped architecture. Image created by the author.

This design tightly couples computing and storage, meaning adding more machines is the only way to scale storage. If you need more disk space, you must add more CPU and RAM, which can lead to wasted resources.

[![](https://substackcdn.com/image/fetch/$s_!nxMy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4954ceee-fc2e-4811-8020-452bd960f194_743x780.png)](https://substackcdn.com/image/fetch/$s_!nxMy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4954ceee-fc2e-4811-8020-452bd960f194_743x780.png)

Apache Kafka tiered storage. Image created by the author.

After experiencing elasticity and resource utilization issues due to Kafka’s tight compute-storage design, Uber proposed Kafka Tiered Storage ([KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage)) to avoid the tight coupling design of Kafka. The main idea is that a broker will have two-tiered storage: local and remote. The first is the broker’s local disk, which receives the latest data, while the latter uses storage like HDFS/S3/GCS to persist historical data.

[![](https://substackcdn.com/image/fetch/$s_!i_wc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52c9dc64-98db-48e7-a178-b001781a460d_550x367.png)](https://substackcdn.com/image/fetch/$s_!i_wc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52c9dc64-98db-48e7-a178-b001781a460d_550x367.png)

The broker isn’t 100% stateless in the Kafka-tiered architecture. Image created by the author.

Although offloading historical data to remote storage can help Kafka broker computing and storage layers depend less on each other, the broker is not 100% stateless. The engineers at AutoMQ wondered, “Is there a way to store all of Kafka’s data in object storage while still maintaining high performance as if it were on a local disk?”

---

## AutoMQ Storage architecture

> *At the moment, AutoMQ can run on major cloud providers like AWS, GCS, and Azure, but I will use technology from AWS to describe its architecture to align with what I’ve learned from their blogs and documentation.*

The goal of AutoMQ is simple: to enhance Kafka's efficiency and elasticity by enabling it to write all messages to object storage without sacrificing performance.

They achieve this by reusing Apache Kafka code for the computation and protocol while introducing the shared storage architecture to replace the Kafka broker’s local disk. Unlike the tiered storage approach, which maintains local and remote storage, AutoMQ wants to make the system completely stateless.

From the 10,000-foot view, the AutoMQ broker writes messages into the memory cache. Before asynchronously writing this message into the object storage, the broker has to write the data into the WAL storage first to ensure the data durability.

[![](https://substackcdn.com/image/fetch/$s_!7g4K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F321524c8-1a1b-4178-b088-4de990d344dd_1134x748.png)](https://substackcdn.com/image/fetch/$s_!7g4K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F321524c8-1a1b-4178-b088-4de990d344dd_1134x748.png)

AutoMQ architecture overview. Image created by the author.

The following sub-sections go into the details of the AutoMQ storage layer.

### Cache

[![](https://substackcdn.com/image/fetch/$s_!CxyP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6876cace-4b1b-4e60-bf8d-697a42690fd0_786x398.png)](https://substackcdn.com/image/fetch/$s_!CxyP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6876cace-4b1b-4e60-bf8d-697a42690fd0_786x398.png)

Type of cache in AutoMQ. Image created by the author.

AutoMQ uses an off-heap cache memory layer to handle all message reads and writes, guaranteeing real-time performance. It manages two distinct caches for different needs: the log cache handles writes and hot reads (those requiring the most recent data), and the system uses the block cache for cold reads (those accessing historical data).

If data isn’t available in the log cache, it will be read from the block cache instead. The block cache improves the chances of hitting memory even for historical reads using techniques like prefetching and batch reading, which helps maintain performance during cold read operations.

> *[Prefetching](https://en.wikipedia.org/wiki/Prefetching) is a technique that loads expected to be needed data into memory ahead of time, so it’s ready when needed, reducing wait times. Batch reading is a technique that allows multiple pieces of data to be read in a single operation. This reduces the number of read requests and speeds up data retrieval.*

Each cache has a different data eviction policy. The Log Cache has a default max size (which is configurable). If it reaches the limit, the cache will evict data with a first-in-first-out (FIRO) policy to ensure its availability for new data. With the remaining cache type, AutoMQ uses the [Least Recently Used (LRU)](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU) strategy for the Block Cache to evict the block data.

The memory cache layer offers the lowest latency for read and write operations; however, it is capped by the amount of machine memory and is unreliable. If the broker machine crashes, the data in the cache will be gone. That’s why AutoMQ needs a way to make the data transfer more reliable.

### Write Ahead Log

Data is written from the log cache to raw EBS devices using Direct IO.

[![Panorama - How it Works](https://substackcdn.com/image/fetch/$s_!lSlT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc32dbd04-2b2b-4ada-8f18-f3e6fef20e5d_1180x413.png "Panorama - How it Works")](https://substackcdn.com/image/fetch/$s_!lSlT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc32dbd04-2b2b-4ada-8f18-f3e6fef20e5d_1180x413.png)

AWS Elastic Block Storage. [Source](https://aws.amazon.com/ebs/)

> *An [EBS](https://aws.amazon.com/ebs/) is a durable, block-level storage device that can be attached to EC2 instances. Amazon EBS offers various volume types, from SSD to HDD, allowing users to choose based on their needs. The EBS Multi-Attach feature lets you attach an EBS volume to multiple EC2 instances. We’ll revisit the Multi-Attach feature when exploring how AutoMQ recover from failure behind the scenes.*

The EBS storage acts as the [Write Ahead Log (WAL)](https://en.wikipedia.org/wiki/Write-ahead_logging), an append-only disk structure for crash and transaction recovery. Databases that use B-Trees for storage management usually include this data structure for recovery; every modification must go through the WAL before being applied to the data. When the machine returns from a crash, it can read the WAL to recover to the previous state.

[![](https://substackcdn.com/image/fetch/$s_!Nbs-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd847487-b0f1-4dca-9d1e-89f6cda65ab9_544x375.png)](https://substackcdn.com/image/fetch/$s_!Nbs-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd847487-b0f1-4dca-9d1e-89f6cda65ab9_544x375.png)

WAL in B-Tree Implementation Database. Image created by the author.

Similarly, AutoMQ treats the EBS device as the WAL for AutoMQ. The brokers must ensure the message is already in the WAL before writing to S3; when the broker receives the message, it writes to the memory cache and returns an “I got your message” response only when it persists in the EBS. AutoMQ uses the data in EBS for recovery in case of broker failure. We will get back to the recovery process in the upcoming section.

[![](https://substackcdn.com/image/fetch/$s_!6ZbA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a6d5fbd-0144-43c1-a88d-55692e5a17c1_559x358.png)](https://substackcdn.com/image/fetch/$s_!6ZbA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a6d5fbd-0144-43c1-a88d-55692e5a17c1_559x358.png)

WAL in AutoMQ. Image created by the author.

It’s essential to consider the high cost of EBS, especially with IOPS-optimized SSDs type. Since the EBS device in AutoMQ serves mainly as a WAL to ensure message durability, the system only needs a small amount of EBS volume. The AutoMQ default WAL size is set to 10GB.

### Object Storage

The object storage stores all AutoMQ data. Users can use services like AWS S3 or Google GCS for this layer. Cloud object service is famous for its extreme durability, scalability, and cost-efficiency. The broker writes the data to the object storage from the log cache asynchronously.

AutoMQ’s data files in the object storage have the following components: DataBlock, IndexBlock, and Footer, which store the actual data, index, and file metadata, respectively.

[![](https://substackcdn.com/image/fetch/$s_!vyx4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a39bb46-72ed-4fa7-84fb-bf75fbd10ae4_492x602.png)](https://substackcdn.com/image/fetch/$s_!vyx4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a39bb46-72ed-4fa7-84fb-bf75fbd10ae4_492x602.png)

Data file in object storage. Image created by the author.

* **DataBlocks** contain the actual data.
* The **IndexBlock** is a fixed 36-byte block made up of DataBlockIndex items. The number of items is associated with the number of DataBlocks in the file. Information within each DataIndexBlock helps to position the DataBlock location.
* The **Footer** is a fixed 48-byte block that contains the location and size of the IndexBlock, enabling quick access to index data.

The following sections will dive into the read/write operations of AutoMQ; along the way, we will understand more about how the system works under the hood.

## The write

From the user’s perspective, the writing process in AutoMQ is similar to Apache Kafka. It starts with creating a record that includes the message’s value and the destination topic. Then, the message is serialized and sent over the network in batches.

The critical difference lies in how the broker handles message persistence.

In Kafka, the broker writes the message to the page cache and then flushes it to the local disk. They don’t implement any memory cache and leave all the work to the OS system.

With AutoMQ, things got very different. Let’s take a look closer at the message-writing process:

[![](https://substackcdn.com/image/fetch/$s_!EoEx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d363648-7305-4a3f-859f-60ac1d2679a2_795x489.png)](https://substackcdn.com/image/fetch/$s_!EoEx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d363648-7305-4a3f-859f-60ac1d2679a2_795x489.png)

The overall message writing process of AutoMQ. Image created by the author.

* The producer sends the message to the broker and waits for the response.
* The broker places the received message into the log cache, an off-heap memory cache.

> *Off-heap memory in Java is managed outside the Java heap. Unlike heap memory, which the JVM handles and garbage collects, off-heap memory is not automatically managed. Developers must manually allocate and deallocate off-heap memory, which can be more complex and prone to memory leaks if not handled properly, since the JVM does not clean up off-heap memory automatically.*

* The message was then written to the WAL (the EBS) device using Direct I/O. Once the message is successfully written to the EBS, the broker sends a successful response back to the producer. (I will explain this process in the next section.)

> *Direct I/O is a method of bypassing the operating system’s file system cache by directly reading from or writing to disk, which can reduce latency and improve performance for large data transfers. Implementing Direct I/O often requires more complex application logic, as developers must manage data alignment, buffer allocation, and other low-level details*

* The message in the log cache is asynchronously written to the object storage after landing in the WAL.

In the following sub-section, we will go into the details of the two processes, cache-WAL and cache-object-storage.

### The journey from the cache to the WAL

The message is written from the log cache to the WAL using the `SlidingWindow` abstraction, which allocates the writing position for each record and manages the writing process. The SlidingWindow has several positions:

[![](https://substackcdn.com/image/fetch/$s_!EU_f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd47044a-e721-4b4a-b7c8-7e9e945f918f_2560x288.png)](https://substackcdn.com/image/fetch/$s_!EU_f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd47044a-e721-4b4a-b7c8-7e9e945f918f_2560x288.png)

Sliding Windows Position. [Source](https://www.automq.com/blog/principle-analysis-how-automq-implements-high-performance-wal-based-on-raw-devices)

* **Start Offset**: This offset marks the beginning of the sliding window; the system already writes records before this offset.
* **Next Offset**: The next unwritten position; new records start here. Data between the Start and Next Offsets has not yet been written entirely.
* **Max Offset**: This is the end of the sliding window; when the Next Offset reaches this point, it will try to expand the window.

To better understand, let’s check some new data structures from AutoMQ to facilitate the write-to-EBS process:

[![](https://substackcdn.com/image/fetch/$s_!dHYC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F651682e4-9616-46f1-9eb3-801cb5dee59c_2560x856.png)](https://substackcdn.com/image/fetch/$s_!dHYC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F651682e4-9616-46f1-9eb3-801cb5dee59c_2560x856.png)

Blocks Data Structure. [Source](https://www.automq.com/blog/principle-analysis-how-automq-implements-high-performance-wal-based-on-raw-devices)

* **block**: The smallest IO unit, containing one or more records, aligned to 4 KiB when written to disk.
* **writingBlocks**: A collection of blocks is currently being written; AutoMQ removes blocks once done writing them to disk.
* **pendingBlocks**: Blocks waiting to be written; new blocks go here when the IO thread pool is complete, moving to writingBlocks when space is available.
* **currentBlock**: The latest arrived log from the cache. Records that need to be written are placed in this block. New records are also allocated logical offsets here. When the currentBlock is full, all blocks are placed in pending blocks. At this time, the system will create a new current block.

After preparing all the prerequisite information, we will learn the process of data writing into EBS:

[![](https://substackcdn.com/image/fetch/$s_!hXDD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F933cbed7-245b-40ac-9370-a273e7fd8675_686x492.png)](https://substackcdn.com/image/fetch/$s_!hXDD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F933cbed7-245b-40ac-9370-a273e7fd8675_686x492.png)

The message’s journey from the cache to the WAL. Image created by the author.

* The process begins with an append request, passing in a record.
* The record is added to the currentBlock, assigned an offset, and asynchronously returned to the caller.
* If the currentBlock reaches a specific size or time limit, it moves all the blocks to the pendingBlocks. AutoMQ will create a new currentBlock.
* If there are fewer writingBlocks than the IO thread pool size, a block from pendingBlocks is moved to writingBlocks for writing.
* Once a block is written to disk, it’s removed from writingBlocks; the system restarts the Start Offset of the sliding window. One marks the append request as completed.

### The journey from the cache to the object storage

[![](https://substackcdn.com/image/fetch/$s_!DlGk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0eedbb84-f721-4ef6-81ce-59d07e9819af_682x484.png)](https://substackcdn.com/image/fetch/$s_!DlGk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0eedbb84-f721-4ef6-81ce-59d07e9819af_682x484.png)

The message’s journey from the cache to the object storage. Image created by the author.

When enough data accumulates in the log cache, AutoMQ triggers an upload to object storage. The data in the LogCache is sorted by streamId and startOffset. AutoMQ then writes the data from the cache to object storage in batches, with each batch uploaded in the same order.

As mentioned earlier, data files in object storage include DataBlock, IndexBlock, and the Footer.

After AutoMQ finishes writing the DataBlock, it constructs an IndexBlock using the information from the earlier writes. Since the position of each DataBlock within the object is already known, this data is used to create a DataBlockIndex for each DataBlock. The number of DataBlockIndexes in the IndexBlock corresponds to the number of DataBlocks.

Finally, the Footer metadata block records information related to the IndexBlock's data location.

---

## The read

AutoMQ Consumers start the consumption process just like with Apache Kafka. They issue an asynchronous pull request with the desired offset position.

After receiving the request, the broker searches for the message and returns it to the consumers. The consumers prepare the following request with the next offset position, calculated by the current offset position and its length.

> *next\_offset = current\_offset + current\_message\_length*

Things got different with the physical data reading path.

AutoMQ tries to serve as much data reading as possible from memory. Initially, Kafka read the data from the page cache. If the message is not there, the operating system will go to the disk and populate the required data to the page cache to serve the request.

[![](https://substackcdn.com/image/fetch/$s_!sNuV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe50657b-4d89-4a08-b992-1e34acf2ef77_858x590.png)](https://substackcdn.com/image/fetch/$s_!sNuV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe50657b-4d89-4a08-b992-1e34acf2ef77_858x590.png)

The overall message reading process of AutoMQ. Image created by the author.

Reading operations in AutoMQ follow the following paths: If the request requires recently written data, it reads from the log cache. It's important to note that only messages already written to the WAL are available to fulfill the request. If the data isn't in the log cache, the operation checks the block cache.

The block cache is filled by loading data from object storage. If the data is still not found there, AutoMQ attempts to prefetch it. Prefetching allows the system to load data that it anticipates will be needed soon. Since the consumer reads messages sequentially from a specific position, prefetching data can boost the cache hit ratio, improving read performance.

To speed up data lookup in object storage, the broker uses the file’s Footer to find the position of the IndexBlock. The data in the IndexBlock is sorted by (streamId, startOffset), allowing for quick identification of the correct DataBlock through binary search.

Once the DataBlock is located, the broker can efficiently find the required data by traversing all the record batches in the DataBlock.

The number of record batches in a DataBlock can affect the retrieval time for a specific offset. To address this, all data from the same stream is divided into 1MB segments during upload, ensuring that the number of record batches in each DataBlock doesn’t slow down retrieval speed.

---

## Recovery

As mentioned earlier, the role of the EBS storage is the AutoMQ’s Write Ahead Log, which helps the process of writing messages from memory to object storage more reliable. Let’s imagine a situation when an AutoMQ cluster has two brokers, A and B, each with two associated EBS storage; let’s see how AutoMQ achieves reliable message transfer:

[![](https://substackcdn.com/image/fetch/$s_!19j5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c32fc7a-f015-4fea-9bb5-e5a56263bc7d_900x897.png)](https://substackcdn.com/image/fetch/$s_!19j5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c32fc7a-f015-4fea-9bb5-e5a56263bc7d_900x897.png)

How does AutoMQ achieve reliable message transfer? Image created by the author.

* As mentioned, a message is considered successfully received once the broker confirms it has landed in the WAL (EBS).
* So, what if one of the brokers, says broker A, crashed? What happened with that broker's EBS storage device? How about the EBS data that had not been written to object storage?
* AutoMQ leverages the AWS EBS multi-attach feature to deal with this situation. After broker A is down, EBS device A will be attached to broker B. When broker B has two EBS volumes, it will know which one is attached from the idle state by tags. Broker B will flush the data of EBS storage A to S3 and then delete the volume. Moreover, when attaching the orphan EBS volume to Broker B, AutoMQ leverages the NVME reservation to prevent unexpected data writing to this volume. These strategies significantly speed up the failover process.
* The newly created broker will have new EBS storage.

---

## Metadata management

> *We'll wrap up this article by exploring how AutoMQ manages cluster metadata. It reuses Kafka’s KRaft mechanism. I didn’t dive deeply into KRaft when writing the Kafka series, so this is a great opportunity to learn more about this metadata management model.* 😊

AutoMQ leverages the latest metadata management architecture based on [Kafka's Kraft mode](https://developer.confluent.io/learn/kraft/).

> *Traditional Kafka relies on a separate ZooKeeper servers for cluster metadata management, but KRaft eliminates ZooKeeper, simplifying Kafka and enhancing resilience. In KRaft mode, Kafka uses an internal Raft-based controller quorum—a group of brokers responsible for maintaining and ensuring metadata consistency. The Raft consensus algorithm is used to elect a leader and replicate metadata changes across the quorum. Each broker in KRaft mode keeps a local copy of the metadata, while the Controller Quorum leader manages updates and replicates them to all brokers, reducing operational complexity and potential failure points.*

[![](https://substackcdn.com/image/fetch/$s_!yOmo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c5ac367-57b0-4ec5-9c39-439139bff2f2_1314x860.jpeg)](https://substackcdn.com/image/fetch/$s_!yOmo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c5ac367-57b0-4ec5-9c39-439139bff2f2_1314x860.jpeg)

Zookeeper Mode vs Kraft Mode. [Source](https://developer.confluent.io/learn/kraft/)

AutoMQ also has a controller quorum that determines the controller leader. The cluster metadata, which includes mapping between topic/partition and data, mapping between partitions and brokers, etc., is stored in the leader. Only the leader can modify this metadata; if a broker wants to change it, it must communicate with the leader. The metadata is replicated to every broker; any change in the metadata is propagated to every broker by the controller.

---

## Outro

In this article, we’ve explored how AutoMQ creatively leverages cloud services to meet a critical goal: storing all Kafka messages in virtually limitless object storage while maintaining Kafka’s original performance and compatibility.

Thank you for reading this far. See you in the following article.

---

## **References**

*[1] AutoMQ Blog, [How to implement high-performance WAL based on raw devices?](https://www.automq.com/blog/principle-analysis-how-automq-implements-high-performance-wal-based-on-raw-devices) (2024)*

*[2] AutoMQ Blog, [Challenges of Custom Cache Implementation in Netty-Based Streaming Systems: Memory Fragmentation and OOM Issues](https://www.automq.com/blog/netty-based-streaming-systems-memory-fragmentation-and-oom-issues#automq-cache-design) (2024)*

*[3] AutoMQ Blog, [Parsing the file storage format in AutoMQ object storage](https://www.automq.com/blog/parsing-the-file-storage-format-in-automq-object-storage) (2024)*

*[4] [AutoMQ Github Repo](https://github.com/AutoMQ/automq)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/how-do-we-run-kafka-100-on-the-object/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
