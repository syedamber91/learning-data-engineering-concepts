---
title: "How does Meta move terabytes of data per second?"
channel: vutr
author: "Vu Trinh"
published: 2025-09-25
url: https://vutr.substack.com/p/how-did-meta-move-terabytes-of-data
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming", "Change Data Capture"]
tags: [https, auto, fetch, substackcdn, image, good]
---

# How does Meta move terabytes of data per second?

*Meta has built an internal message queue system over the last 18 years, capable of ingesting over 15TB/s and serving over 110TB/s to its consumers.*

> Source: [Open post](https://vutr.substack.com/p/how-did-meta-move-terabytes-of-data)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!oiYn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa69acfb-12f8-41dc-9b4c-2f6b334f567d_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!oiYn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa69acfb-12f8-41dc-9b4c-2f6b334f567d_2000x1428.png)

---

## Intro

Apache Kafka is ubiquitous. It’s the number one choice for distributed messaging, serving many companies worldwide for various use cases, including messaging, log aggregation, and stream processing.

Many companies use it, including big techs like PayPal, Uber, and LinkedIn. However, not everyone uses Kafka; they use other available solutions or … built their own system. In today's article, we will explore Scribe, a message queue service that Meta built to support the global scale of traffic.

---

## Terminology

Before moving on, we first explore some Scribe concepts:

First is the **Category**. It exposes the concept of a logical stream to the users.

[![](https://substackcdn.com/image/fetch/$s_!D4sb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbe22909-3ce0-4082-9ce6-47b72aa3c2a0_522x262.png)](https://substackcdn.com/image/fetch/$s_!D4sb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbe22909-3ce0-4082-9ce6-47b72aa3c2a0_522x262.png)

Like Kafka, the clients that write and read data to and from the category are also referred to as producers and consumers. Both are implemented as libraries. An application could have many producer and consumer instances as required.

[![](https://substackcdn.com/image/fetch/$s_!AHjc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd709dc75-1f41-49e3-b99d-023da376271e_662x270.png)](https://substackcdn.com/image/fetch/$s_!AHjc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd709dc75-1f41-49e3-b99d-023da376271e_662x270.png)

For consuming messages, a group of consumers could together handle messages from a category. The data can be split into logical shards based on the message key or value. A consumer can read only the messages from a logical shard. Scribe allows the whole traffic to be distributed among the consumer groups arbitrarily, without the sharding scheme.

[![](https://substackcdn.com/image/fetch/$s_!gpTx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F865abdc7-b918-4822-9b9b-b47da333fa02_632x262.png)](https://substackcdn.com/image/fetch/$s_!gpTx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F865abdc7-b918-4822-9b9b-b47da333fa02_632x262.png)

There is also a concept of physical shards, which are log files that contain metadata associated with the message payloads (such as the pointer to the payload). We will explore in more detail later.

---

## The high-level architecture

From the write path, producer instances accept messages from users, batch them, and send them to the ScribeD. At this stage, a batch can have messages from different categories. The ScribeD then sends these batches to the Write Proxy.

Messages are then split so that ones from the same category will belong to the same batch. Write Proxy, then route those batches to the Batch Service. The Batch Service persists these batches and commits their metadata.

[![](https://substackcdn.com/image/fetch/$s_!gTMQ!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ba0958f-6bf3-4de5-8b7d-f05f34ac13f7_1214x498.png)](https://substackcdn.com/image/fetch/$s_!gTMQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ba0958f-6bf3-4de5-8b7d-f05f34ac13f7_1214x498.png)

For the read path, the consumer instances contact the Read Stream Service to retrieve metadata from the metadata store. Then, the consumers use the information from the metadata (e.g., where to read the metadata) to form requests to the Read Proxy. This proxy manages all related data access operations.

Next, we delve into more details of the write/read operations, as well as how the data is stored.

## Write

The producer lib is the entry point. A number of the producer instances can be initiated across multiple hosts. When applications make a write request to the Producer library, they will get an object that contains the result of the write operation.

[![](https://substackcdn.com/image/fetch/$s_!OqD-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54f12196-61a2-4322-a3c5-04ef673d4a31_652x306.png)](https://substackcdn.com/image/fetch/$s_!OqD-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54f12196-61a2-4322-a3c5-04ef673d4a31_652x306.png)

To save the memory footprint, the Producer batches messages from multiple categories together in memory. The Producer will flush the message batch to the ScribeD, a local daemon that accepts messages from all the Producer instances on a host, and eventually sends them to the Write Proxy.

[![](https://substackcdn.com/image/fetch/$s_!peS1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3a9cebe-b670-4da7-ab72-388a3c9205f0_566x264.png)](https://substackcdn.com/image/fetch/$s_!peS1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3a9cebe-b670-4da7-ab72-388a3c9205f0_566x264.png)

The main goal of ScribeD is to ensure fault tolerance for the messages flushed from the Producer (in memory) by buffering them on disk. This approach prevents data loss in the event of a failure when writing to durable storage.

[![](https://substackcdn.com/image/fetch/$s_!MuHQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c5df11d-4c15-4a9f-8c53-6aca1473ecc2_1016x274.png)](https://substackcdn.com/image/fetch/$s_!MuHQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c5df11d-4c15-4a9f-8c53-6aca1473ecc2_1016x274.png)

After accepting a message batch, Write Proxy first performs admission control checks with these messages and then splits the messages from the same category into the same batch. These batches are routed to the Batch Service.

[![](https://substackcdn.com/image/fetch/$s_!LyQG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe547f0e6-4d94-458b-9694-2bb40b2a59dc_788x374.png)](https://substackcdn.com/image/fetch/$s_!LyQG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe547f0e6-4d94-458b-9694-2bb40b2a59dc_788x374.png)

The Batch Service compresses and flushes batches of the ephemeral data store (for caching) and durable payload store (for long-term retention). After that, the Batch Service writes the metadata about these batches, including the pointer to the batch data, to log-based metadata storage. This metadata will help Scribe provide the sequential, stream abstraction read patterns for the consumer.

## Storage

As mentioned, Meta separated the metadata and data. The message metadata is stored in LogDevice, a log-based storage system optimized for sequential data read and write operations.

### Metadata store

For each category, the [LogDevice](https://engineering.fb.com/2017/08/31/core-infra/logdevice-a-distributed-data-store-for-logs/) appends the metadata of each data batch to a file called `log`. Each log is a physical shard of the category. Each record in the log file has a monotonically increasing sequence number.

[![](https://substackcdn.com/image/fetch/$s_!MA8V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5224833b-dd5f-48a0-bed3-a0bd34c6aebf_638x336.png)](https://substackcdn.com/image/fetch/$s_!MA8V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5224833b-dd5f-48a0-bed3-a0bd34c6aebf_638x336.png)

Meta stores millions of logs in a LogDevice cluster. Each LogDevice cluster comprises storage nodes. Each record can be replicated across any of a subset of these nodes, ensuring data redundancy.

### Durable Data Store (DDS)

All the message payloads are stored in [Tectonic](https://www.usenix.org/system/files/fast21-pan.pdf), a distributed filesystem Meta built to replace HDFS. This file system is also the backbone of the other systems, such as Meta’s warehouse.

Rather than fully replicate the payload based on a factor (e.g., three replicas), Tectonic supports erasure coding to ensure data reliability. (Read more [here](https://vutr.substack.com/i/169994133/store-data-on-multiple-devices)). The storage footprint will be lower compared to naive replication; however, the approach will require more resources in the event of data reconstruction in the case of failures.

[![](https://substackcdn.com/image/fetch/$s_!NASS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa5c40fc-36bc-437f-8081-390ef1ed288f_638x450.png)](https://substackcdn.com/image/fetch/$s_!NASS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa5c40fc-36bc-437f-8081-390ef1ed288f_638x450.png)

To keep the number of data blocks under control, Scribe can store data from multiple categories in the same block. The Write Proxy accumulates blocks in the order of 10s of megabytes, then performs a flush operation to the Tectonic storage node’s disk. In a block, data from the same category is also accumulated to serve read operations more efficiently, up to 2 megabytes.

### Ephemeral Data Store (EDS)

Besides the durable storage, message payloads also exist in the regional ephemeral data store, which is essentially a cache with two tiers: the local and the remote ones.

This is important because the DDS could reside in a different region than the read users. A category typically receives input data records from producers that run globally. This leads to the fact that when a Consumer issues a read request, it reads most of the data from the different regions.

The EDS comes to the rescue here, as it allows users to access the DDS from a different region. The goal is to minimize access to the remote storage containing the actual payload data.

Besides reducing latency and avoiding pressure on the Tectonic, other interesting EDS responsibilities will be discussed later in this article.

[![](https://substackcdn.com/image/fetch/$s_!TgP9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0a61f97-2672-4cba-8ac1-dc01fa134b06_632x486.png)](https://substackcdn.com/image/fetch/$s_!TgP9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0a61f97-2672-4cba-8ac1-dc01fa134b06_632x486.png)

For the remote tier, Meta utilizes [Memcached](https://github.com/memcached/memcached) to store message payloads for a period of 1-2 hours. Meta believes this period is sufficient for users who want to consume data considered ‘warm’. For the hotter data, Meta uses [Cachelib](https://cachelib.org/) to manage the cache, which utilizes the spare memory resources of Read Proxy hosts. We will explore the EDS more in depth when we discuss the read path.

## Read

The entry point for the read path is also a library called Consumers. An application usually starts a group of Consumer instances to read the data from a category. When the user starts an instance of a Consumer, a stateful connection to the Read Stream service is spawned.

Meta attempts to establish the connection in a manner that ensures the Consumer instance and the Read Stream service are located in the same region. This Read Stream service is in charge of providing the stream abstraction for the users (with the help of the metadata)

An instance of the service has a pool of connections to LogDevice clusters. When it receives a Consumer request, it identifies all the required LogDevice clusters, physical shards, and the shard’s offer to read based on the input from the Consumer.

[![](https://substackcdn.com/image/fetch/$s_!T3oj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5327c054-49c9-42fb-80f6-bc2e656cd680_1052x398.png)](https://substackcdn.com/image/fetch/$s_!T3oj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5327c054-49c9-42fb-80f6-bc2e656cd680_1052x398.png)

A different instance (called the reader) will handle the actual data reading from the LogDevice cluster. This Read Stream instance merges results from the reader to provide a single metadata stream for the Customer.

The Consumer uses this metadata (including the data pointer) to issue RPC requests to the Read Proxy for the payloads. The Read Proxy’s main job is to take care of everything related to accessing the payload storage.

[![](https://substackcdn.com/image/fetch/$s_!HEfk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9414e244-c95a-4909-9171-f34c28909976_672x364.png)](https://substackcdn.com/image/fetch/$s_!HEfk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9414e244-c95a-4909-9171-f34c28909976_672x364.png)

When receiving the request from the consumer, the Read Proxy tries to fetch data from a regional ephemeral Data Store. The data could exist in the in-memory cache of the Memcached instance.

In the case of the Read Proxy, it must reach the durable data storage (DDS); the request is then routed to the Read Proxy located in the same region as the payload stored in the DDS.

* If a Read Proxy instance in region A needs the payload stored in region B, it routes the request to the instance living in region B. The data is then populated in the EDS in region B. After that, a request from a

  [![](https://substackcdn.com/image/fetch/$s_!Tsvg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71f61db7-a9da-4aca-a5af-de7d69b764dc_1058x428.png)](https://substackcdn.com/image/fetch/$s_!Tsvg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71f61db7-a9da-4aca-a5af-de7d69b764dc_1058x428.png)
* Read Proxy instance in region C for the same data will be served by the EDS in region B. Although it still needs to communicate across regions, the latency is slower compared to reading directly from the DDS in region B.

If the customer specifies any filtering or serialization option, the Read Proxy will apply them to the accessed messages.

[![](https://substackcdn.com/image/fetch/$s_!-Nug!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b220af9-84ca-492b-bd70-11439d162e6a_482x314.png)](https://substackcdn.com/image/fetch/$s_!-Nug!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b220af9-84ca-492b-bd70-11439d162e6a_482x314.png)

* Meta designed the Read Proxy to act as a data staging area. When populating the data into the EDS, the Read Proxy transforms the category’s payloads from their original format (row) to columnar format to help consuming applications avoid this expensive process, especially when they need the data for an analytics workload.
* Read Proxy can also apply the pushdown of the consume application filter; it can evaluate a subset of SQL queries.

## How metadata is managed

Metadata is the heart of Scribe. Many components require access to the metadata store to support both write and read operations. Although the LogDevice is a transactional, highly available database, millions of clients trying to query the metadata is another story.

To solve this problem, Meta built a caching and distribution layer on top of the metadata store. There is a background job that scans the entire metadata database and populates the contents into a [configuration distribution system](https://scontent.fsgn6-2.fna.fbcdn.net/v/t39.8562-6/240878090_886902905538621_3270513309519299878_n.pdf?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=qy6bc-qvNIsQ7kNvwHFwplQ&_nc_oc=Adm1-Yt4J1SJNjN8AbGZm5pxAVlj7pCcD42zAF7Ck3A8DxyiYdWHqg7ootvoYrDkoEs&_nc_zt=14&_nc_ht=scontent.fsgn6-2.fna&_nc_gid=9qeuFDil0RoliXUR_8WfkQ&oh=00_AfYz8ebtpn1y_EuPtIYiYL_fzD3u1UaSBoh2cZ8ajGT4MQ&oe=68D0A4D9). Clients can read the metadata from here.

[![](https://substackcdn.com/image/fetch/$s_!aisC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26fe4909-fd20-4d80-87d5-9b020c60b70f_554x332.png)](https://substackcdn.com/image/fetch/$s_!aisC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26fe4909-fd20-4d80-87d5-9b020c60b70f_554x332.png)

For more detailed metadata, such as the physical shards that contain pointers to the required data (Read Stream Service needs this to stream the metadata back to the Consumers), a periodic job polls the LogDevice clusters to retrieve the latest mapping between cluster, categories, and physical shards, and exposes the mapping in a highly replicated database.

[![](https://substackcdn.com/image/fetch/$s_!a0nG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff69f8e32-d239-4682-87ea-4058bde6adfa_724x272.png)](https://substackcdn.com/image/fetch/$s_!a0nG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff69f8e32-d239-4682-87ea-4058bde6adfa_724x272.png)

For a request from the consumer, the Read Stream Service instance subscribes to the relevant mapping. The mapping could be changed when a physical shard is added or removed at runtime. Based on this information, the service can start or stop the reader instances accordingly.

## How traffic is managed

To address the global scale of traffic, Scribe utilizes a multi-layered traffic management system at various levels.

**Intra-cluster traffic shaping:** Scribe dynamically adjusts its internal resources to handle traffic within a single LogDevice cluster. When a specific category sees a traffic surge, a service automatically splits its existing physical shards (log files) into smaller ones to ensure horizontal scalability for the category. When traffic drops, the system gradually removes excess shards once they are past their retention period.

[![](https://substackcdn.com/image/fetch/$s_!pROZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6ff7f51-dc22-4bc8-9edb-242a354957d6_624x530.png)](https://substackcdn.com/image/fetch/$s_!pROZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6ff7f51-dc22-4bc8-9edb-242a354957d6_624x530.png)

**Inter-cluster traffic shaping:** The control plane continuously monitors each LogDevice cluster’s write and read workload to adjust the incoming write workload limitation, ensuring the cluster is not overwhelmed.

[![](https://substackcdn.com/image/fetch/$s_!0vF3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72eee5ca-2c94-48a2-bc39-365eeae83743_480x304.png)](https://substackcdn.com/image/fetch/$s_!0vF3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72eee5ca-2c94-48a2-bc39-365eeae83743_480x304.png)

When reaching the limitation, the Write Proxy can route the traffic to another LogDevice cluster in the same region (that still has write workload below the limitation). If the overload is happening globally, the [graceful degradation](https://www.usenix.org/conference/osdi23/presentation/meza) approach is used to protect the system.

**Host-level traffic shaping:** At the individual server level, Scribe uses Meta's service mesh to route traffic. The service mesh uses a host's exposed load metric (e.g., CPU utilization) to route requests to the least-loaded server.

[![](https://substackcdn.com/image/fetch/$s_!kgwB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf7dc300-c22a-427b-86dd-359b02281cb0_810x438.png)](https://substackcdn.com/image/fetch/$s_!kgwB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf7dc300-c22a-427b-86dd-359b02281cb0_810x438.png)

When a server accepts a request that will consume significant resources over a long period, it immediately **advertises a “fake“ high load metric**. This high value tells the rest of the system that the server is “reserved“ even though the actual resource usage hasn't started yet.

[![](https://substackcdn.com/image/fetch/$s_!BOGu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2a8fce9-4b0a-4467-b5f4-59feeaac13c2_764x430.png)](https://substackcdn.com/image/fetch/$s_!BOGu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2a8fce9-4b0a-4467-b5f4-59feeaac13c2_764x430.png)

The server then **exponentially decays** this load value. The load metric gradually decreases over time. By the time the request's actual resource consumption becomes apparent, the artificial value has decayed to the point where it reflects the actual load on the server.

This mechanism is crucial because it prevents the service mesh from routing too many requests to a server that is already handling a heavy workload. Without it, the service mesh would consider the host idle for the first few seconds of a long request and assume that the server is capable of handling new requests.

For specific tasks, Scribe uses **consistent hashing** to assign requests to particular hosts, which helps maximize efficiency. This is helpful in use cases such as the Write Proxy, which sends groups of messages for a specific data category to the same **Batch Service** host, or when the requests need to be routed to a particular **Read Proxy** host to benefit from the in-memory cache on that host.

## How ephemeral data is managed

As mentioned above, Scribe manages data replicas in the ephemeral data store to:

* Prevent reaching the durable storage too often, thus reducing the latency of the cross-region network traffic
* Represent the data in a more read-efficient format (columnar) for analytics applications

Scribe uses a **constraint satisfaction model** around the resource, such as durable storage IO or Memcached network utilization, to determine which replicas to create and where. The system's "control plane" makes these decisions based on several factors, aiming to maximize the benefit while working within resource limits. The key factors considered are:

* **Read fanout:** How many readers are accessing a specific data category?
* **Message freshness:** Are consumers primarily reading the newest messages or older ones?
* **Data filtering (selectivity factor):** Can a new replica in the ephemeral data store significantly reduce the amount of data that needs to be transferred?
* **Deserialization cost:** Does the Read Proxy need to perform costly data conversion to a different format? A replica in the ephemeral data store in the required format for the deserialization process.

Depending on a data center's specific resource limitations, Scribe will adopt different **caching policies** to make the most of what's available. For example, a region with limited Memcached outgoing traffic might use a Read Proxy in-memory replica as a "shield" to prevent too many requests from hitting the cache.

Scribe's control plane constantly recalculates these policies to adapt to fluctuating workloads.

## Guarantees support

Scribes support several message delivery guarantees: best effort, at least once, and at least once with repeatable reads.

### Best effort

The general idea of the best effort guarantee is that it prioritizes throughput and availability. It's a trade-off designed for high-volume, "fire-and-forget" data streams where getting most of the data through quickly is more important than ensuring every single message is delivered exactly once and in a strict, sequential order.

[![](https://substackcdn.com/image/fetch/$s_!AnSl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa60da891-0ab1-46bb-a7b0-2bdc8bc7ec9f_646x196.png)](https://substackcdn.com/image/fetch/$s_!AnSl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa60da891-0ab1-46bb-a7b0-2bdc8bc7ec9f_646x196.png)

From the write path**:**

* **Prioritizes Write Availability:** Scribe's primary goal in this guarantee is to persist massive amounts of data with minimal resource consumption.
* **Opportunistic Routing:** Messages are routed to the nearest or most available Write Proxy host and can even be routed to another data center if needed. This ensures that data continues to move, even if the path is congested.
* **Retries and Duplication:** If a write request fails, the client will retry the call. This can lead to the same message being successfully delivered more than once, resulting in **message duplication**. This is a known and accepted trade-off for maximizing availability.
* **Potential for Data Loss:** A customer must be prepared to tolerate a small degree of **data loss** if a write call fails and cannot be recovered.

From the read path:

* **Collecting:** Scribe's write path scatters messages for a single category across many physical shards. A consumer reading this data must collect messages from all these shards.
* **Embracing Disorder:** Enforcing a strict order across all these shards would introduce significant latency and reduce throughput. To avoid this, Meta introduced a configuration that allows users to balance latency and data ordering.

### At least once

The primary objective is to ensure that every message is successfully stored. Scribe achieves this by:

* **Storage Acknowledgments:** The client only considers a message sent once it receives a confirmation from the storage layer that the message has been successfully saved.

  [![](https://substackcdn.com/image/fetch/$s_!Omn_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ffc345c-2c1a-4fc2-a361-b6e79f593cd1_676x196.png)](https://substackcdn.com/image/fetch/$s_!Omn_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ffc345c-2c1a-4fc2-a361-b6e79f593cd1_676x196.png)
* **Aggressive Retries:** If a message doesn't receive an acknowledgment, it is resent. This process is repeated across every step of the write path until the message is confirmed to be saved.

  [![](https://substackcdn.com/image/fetch/$s_!JoDv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6460ded-2b4b-45ee-be55-36940cd3687e_1000x248.png)](https://substackcdn.com/image/fetch/$s_!JoDv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6460ded-2b4b-45ee-be55-36940cd3687e_1000x248.png)

However, aggressive retries might cause data deduplication. To minimize this, Scribe implements several optimizations:

* **Proactive Shard Initialization:** Scribe predicts and initializes physical shards ahead of time. This prevents retries from being delayed by the process of setting up a new shard (the delay could lead to the timeout → retry → potential duplicated data).
* **Graduated Timeouts:** Each step in the write path has a progressively longer timeout than the one before it. This ensures that a step doesn't prematurely give up and retry a request while the next step is still processing it, thus reducing unnecessary retries and duplication.
* **Conservative Batching:** For data requiring "at least once" delivery, Scribe sends messages in smaller batches. This means that if a retry happens, the potential duplication event involves a smaller number of messages.

### Repeatable reads

> ***Non-repeatable read:** During a transaction, if a transaction sees a piece of data with a different value at a different point in time, this behavior is referred to as a non-repeatable read.*

With **repeatable reads**, Scribe guarantees that a consumer reading a data stream will see the **same data in the same order** if it were to reread it. This is a stronger guarantee than the two guarantees above, and it is crucial for use cases that require strict data ordering and reliable processing, such as change data capture (CDC).

Scribe offers two distinct approaches to achieve this, each with its own trade-offs: the Write and Read Path Variant.

The write variant:

[![](https://substackcdn.com/image/fetch/$s_!vEh2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63d1029c-2ad4-4066-869c-b181ca1d8f70_1000x422.png)](https://substackcdn.com/image/fetch/$s_!vEh2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63d1029c-2ad4-4066-869c-b181ca1d8f70_1000x422.png)

* It ensures a logical shard's traffic is sent to a single, dedicated **physical shard**.
* However, this limits the maximum throughput to what a single physical shard can handle.

The read variant:

[![](https://substackcdn.com/image/fetch/$s_!i7_d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ff0edaf-ca65-43f2-9649-cc70342b6f59_904x470.png)](https://substackcdn.com/image/fetch/$s_!i7_d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ff0edaf-ca65-43f2-9649-cc70342b6f59_904x470.png)

* An internal service, called **Sequenced Shard Generator**, reads all the scattered metadata shards of a category.
* The generator then **reorders** the messages into a single, new **metadata shard** based on the batch size required by the downstream application.
* This provides a single, deterministic order for all messages in a category. It also allows the downstream application to define its own batch size.
* However, it adds an extra step to the data flow, which includes additional steps, thus introducing **latency** to the overall system.

## Outro

In this article, we first explore the terminology of Scribe, then delve into its architecture, which comprises many components with clear responsibilities on both the read and write paths. Scribe also separates metadata and data and introduces a cache tier to improve the read path.

We then take a closer look at how Scribe manages traffic, metadata, and data in the cache system. Finally, we conclude the article by examining several message delivery guarantees provided by Scribe.

Thank you for reading this far. See you in my next article.

## Reference

*[1] Meta, Scribe: [How Meta transports terabytes per second in real time](https://www.vldb.org/pvldb/vol18/p4817-karpathiotakis.pdf), (2025)*
