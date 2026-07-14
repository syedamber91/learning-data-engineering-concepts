---
title: "The company that created Kafka is replacing it with a new solution"
channel: vutr
author: "Vu Trinh"
published: 2025-07-03
url: https://vutr.substack.com/p/the-company-that-created-kafka-is
paid: false
topics: ["Apache Kafka", "Apache Spark", "Data Lake", "Streaming"]
tags: [https, auto, kafka, good, substackcdn, image]
---

# The company that created Kafka is replacing it with a new solution

*How did LinkedIn build Northguard, the new scalable log storage*

> Source: [Open post](https://vutr.substack.com/p/the-company-that-created-kafka-is)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[data-lake|Data Lake]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=167187704)

[![](https://substackcdn.com/image/fetch/$s_!ZeWD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ea94ea8-b0e4-4295-9ffa-02faaf368e8d_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!ZeWD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ea94ea8-b0e4-4295-9ffa-02faaf368e8d_2000x1429.png)

---

## Intro

Fifteen years ago, LinkedIn built Kafka to meet their growing log processing demands. They open-sourced it, and the rest is history. Over time, the software that was named after the author [Franz Kafka](https://en.wikipedia.org/wiki/Franz_Kafka) has become the de facto standard for distributed messaging.

For LinkedIn, Kafka has been the backbone of their infrastructure, from collecting user activity, stream processing, database replication, to data lake ingestion. However, with the growing demand for their planet-scale business, they found it challenging to operate Kafka.

LinkedIn introduced a new solution to replace it.

This article will delve into their motivation, what the new solution looks like, and how they migrate away from Kafka.

> *All these technical details are credited to the LinkedIn Engineering team, particularly the two authors of the article [Introducing Northguard and Xinfra: scalable log storage at LinkedIn](https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra).*

---

## Overview

As LinkedIn shared, in 2025, they had over 1.2 billion users. The business's massive growth presented challenges for its Kafka infrastructure, which comprises 150 clusters containing 10,000 machines that serve 400,000 topics with 17PB of data daily.

Due to the tightly coupled architecture of Kafka, scaling traffic requires adding more machines to handle the increased load.

[![](https://substackcdn.com/image/fetch/$s_!LTWs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadf02028-c2bc-4114-ac88-ca5bfce2eef9_452x332.png)](https://substackcdn.com/image/fetch/$s_!LTWs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadf02028-c2bc-4114-ac88-ca5bfce2eef9_452x332.png)

Additionally, Kafka must replicate partitions to ensure data durability; a single leader will accept the write and replicate the data to its followers.

[![](https://substackcdn.com/image/fetch/$s_!YWYP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5561a927-0b59-4206-bac6-3c28fcff2ec0_922x864.png)](https://substackcdn.com/image/fetch/$s_!YWYP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5561a927-0b59-4206-bac6-3c28fcff2ec0_922x864.png)

When membership of the cluster changes, the data must be redistributed to balance the load, affecting the availability of the clusters.

[![](https://substackcdn.com/image/fetch/$s_!Mt88!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3421c5bf-f8f0-4573-8fdd-76aa788242a2_862x562.png)](https://substackcdn.com/image/fetch/$s_!Mt88!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3421c5bf-f8f0-4573-8fdd-76aa788242a2_862x562.png)

These problems are amplified when operating Kafka at LinkedIn’s scale.

They need a new solution with higher scalability. It must be more efficient in terms of load distribution. LinkedIn also requires strong consistency in both our data and metadata, without sacrificing high throughput, low latency, high availability, and high durability from Kafka.

So, they built Northguard, the log storage system. It breaks the data and metadata into smaller chunks and distributes them across nodes evenly by design.

At a high level, Northguard shares some similarities with Kafka, as it also operates as a cluster of brokers. However, the way it is organized and replicates data is different from Kafka.

[![](https://substackcdn.com/image/fetch/$s_!CaBG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F925c8cd5-f955-4b76-9edb-abb195dd5288_622x286.png)](https://substackcdn.com/image/fetch/$s_!CaBG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F925c8cd5-f955-4b76-9edb-abb195dd5288_622x286.png)

---

## Data Model

A record is the smallest unit of data in Northguard. Like Kafka’s message, a record is a sequence of bytes that has a key, a value, and optional user-defined headers.

[![](https://substackcdn.com/image/fetch/$s_!mHvd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2168cc65-61cc-4a67-83c6-4f73c248beba_374x362.png)](https://substackcdn.com/image/fetch/$s_!mHvd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2168cc65-61cc-4a67-83c6-4f73c248beba_374x362.png)

Records are stored sequentially in a segment. Like Kafka, a segment is associated with a file of 1GB. An active segment is the one that accepts record appending. When the segment reaches its maximum size, is active for more than 1 hour, or fails to replicate, it is sealed.

[![](https://substackcdn.com/image/fetch/$s_!O4yV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69a39fe6-b20f-4380-bb62-568ca2c8b972_936x538.png)](https://substackcdn.com/image/fetch/$s_!O4yV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69a39fe6-b20f-4380-bb62-568ca2c8b972_936x538.png)

Here is an interesting point: the segment is Northguard’s replication unit, rather than a partition like Kafka. We will revisit this point later.

In Kafka, partitions act as the logical logs. LinkedIn introduced the concept of range, which is the Northguard’s log abstraction.

[![](https://substackcdn.com/image/fetch/$s_!ywKt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F512a9413-e4dd-4146-ae44-372ceafc6a23_1072x578.png)](https://substackcdn.com/image/fetch/$s_!ywKt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F512a9413-e4dd-4146-ae44-372ceafc6a23_1072x578.png)

It's a chain of segments with a contiguous range of keys (e.g., A→D, D→M, M→Q). Like segments, ranges can be either active or sealed.

Northguard also has the concept of a topic, which is the collection of ranges that cover the entire keyspace (e.g., A→Z).

[![](https://substackcdn.com/image/fetch/$s_!X_Tc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F772e9854-1d94-4115-9033-fdbacec3ecee_1132x388.png)](https://substackcdn.com/image/fetch/$s_!X_Tc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F772e9854-1d94-4115-9033-fdbacec3ecee_1132x388.png)

Northguard can merge or split topic ranges.

* Splitting will seal the source range and create two new ranges.
* Merging will seal the two source ranges and create a new range.

A topic can be sealed or deleted. The process will occur across all the topic ranges.

The Northguard cluster’s admins can set the storage policy for a topic. A policy has a name, a retention period that defines when segments should be deleted, and some specified constraints.

Each broker in the Northguard cluster is deployed with encoded information, such as the rack or data center. When defining the policy for the topic, users can express the constraints to help determine which brokers are available to be chosen as the segment’s replica (the broker that holds one of the copies of the segment).

[![](https://substackcdn.com/image/fetch/$s_!9oZp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91c2fe70-7c1e-4138-9456-54cc5ca155ee_602x248.png)](https://substackcdn.com/image/fetch/$s_!9oZp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91c2fe70-7c1e-4138-9456-54cc5ca155ee_602x248.png)

This approach helps LinkedIn achieve rack-aware replica assignment for Northguard.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=167187704)

---

## Data replication

As mentioned above, the unit of data replication in Northguard is the segment. It is more fine-grained compared to Kafka’s partition.

LinkedIn observed that the Kafka approach can be inefficient when handling data skew, because each replica has to store the entire copy of the whole partition, which causes some problems:

* In Kafka, when you add a new broker to the clusters, the partitions are not automatically load-balanced to the new broker. The new broker will remain idle and underutilized until the user either creates new topics or partitions or manually rebalances them. However, creating topics or partitions is typically not done often, and manually moving the data is ineffective.

  [![](https://substackcdn.com/image/fetch/$s_!KxEs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F425c39b9-bb82-4f8d-9d27-f89f70204b29_828x676.png)](https://substackcdn.com/image/fetch/$s_!KxEs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F425c39b9-bb82-4f8d-9d27-f89f70204b29_828x676.png)
* A broker might be overloaded if it has hot partitions (e.g., intensive data ingestion). This requires data re-partition.

Northguard chooses to replicate segments instead of using log abstraction (partitioning in Kafka).

[![](https://substackcdn.com/image/fetch/$s_!P7Y2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F126a79d2-7793-465a-9ab5-b4cd48b6cd56_838x376.png)](https://substackcdn.com/image/fetch/$s_!P7Y2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F126a79d2-7793-465a-9ab5-b4cd48b6cd56_838x376.png)

The key here is that the segment is created more frequently than the log. Suppose a broker receives numerous write requests and is under considerable pressure.

[![](https://substackcdn.com/image/fetch/$s_!Jtx0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc31f2680-d6ae-4707-a3fc-24b56303c9fd_1294x984.png)](https://substackcdn.com/image/fetch/$s_!Jtx0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc31f2680-d6ae-4707-a3fc-24b56303c9fd_1294x984.png)

Northguard adds the new broker to share the workload, but here's the interesting thing: it doesn’t need to move the partition from the existing brokers to the new one like Kafka does; the system only assigns a new active segment to the new broker. The ingest workload would be routed to the new broker, relieving the struggling one.

Additionally, because segments are smaller than Kafka’s partitions, moving data around is less intensive than in Kafka.

---

## Metadata

The Northguard manages metadata for:

* Topics: When the topic is sealed or deleted, when its range is merged or split.
* Ranges: Its states (active/sealed/deleting), which topic it belongs to, the creation time, and the retention
* Segments: The segment’s replica, the state (active/sealed/reassigned), start offset, the segment’s length, and its creation and seal time.

Northguard uses [Raft](https://en.wikipedia.org/wiki/Raft_(algorithm))-backed [replicated state machines](https://www.geeksforgeeks.org/system-design/replicated-state-machines-in-distributed-systems/), distributed across vnodes, to manage metadata. A Northguard cluster will have one or more vnodes (my best guess for vnodes is a process in a broker), each of which stores a piece of topic, range, and segment metadata.

[![](https://substackcdn.com/image/fetch/$s_!UXRa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe58b74a5-0eb9-40bb-99c3-649e3ea6b413_488x428.png)](https://substackcdn.com/image/fetch/$s_!UXRa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe58b74a5-0eb9-40bb-99c3-649e3ea6b413_488x428.png)

Northguard uses consistent hashing to distribute metadata across the vnodes. Topic metadata is hashed by topic name, while range and segment metadata are hashed by range ID.

[![](https://substackcdn.com/image/fetch/$s_!isZ6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9ce5cb7-e99b-4e59-95cd-8c00bc117938_1122x450.png)](https://substackcdn.com/image/fetch/$s_!isZ6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9ce5cb7-e99b-4e59-95cd-8c00bc117938_1122x450.png)

By sharding metadata and utilizing decentralized coordination, Northguard eliminates Kafka’s controller bottlenecks, offering strong consistency and high availability.

---

## The protocol

Unsurprisingly, due to the difference in how Northguard organizes metadata and data compared to Kafka, its protocol differs.

Metadata operations follow the request-response model, where clients can send requests to any broker. This broker will check the local copy of the global state to identify which vnode can serve the request and route it to the right vnode.

[![](https://substackcdn.com/image/fetch/$s_!In8t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb0e44e2-ff98-4548-a4de-7df073d0ab61_750x514.png)](https://substackcdn.com/image/fetch/$s_!In8t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb0e44e2-ff98-4548-a4de-7df073d0ab61_750x514.png)

Data-related operations, such as producer, consumer, or replication, are performed via sessionized streaming protocols.

Like Kafka, the data-producing process is carried out through communication with the leader. The client starts the handshake with the active segment leader and will be informed about the window size accepted by the broker.

[![](https://substackcdn.com/image/fetch/$s_!tPIs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd67f6e16-dfba-4496-b452-13cbc8600a54_898x400.png)](https://substackcdn.com/image/fetch/$s_!tPIs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd67f6e16-dfba-4496-b452-13cbc8600a54_898x400.png)

The producer sends multiple requests to append data to the segment as long as the records do not exceed the window. The broker only sends the ACK back to the producer when the records are committed (all replicas are persistent).

The consumption process is similar to the production process, but with data flowing in the reverse direction, and the client determines the amount of data it can accept. Then, the broker will push data as long as the records do not exceed the predefined amount. This is in contrast to Kafka, where consumers pull data from the brokers.

[![](https://substackcdn.com/image/fetch/$s_!Pwwo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8609e068-5db8-445c-b3ea-be8d62fd3201_844x334.png)](https://substackcdn.com/image/fetch/$s_!Pwwo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8609e068-5db8-445c-b3ea-be8d62fd3201_844x334.png)

Segment replication also works quite similarly to the producing process; the difference is that the interaction is between the active segment leader and the segment followers.

---

## The storage layer

Northguard storage is pluggable. The default implementation has a Write Ahead Log (WAL) which is created per segment. This implementation leverages Direct I/O and keeps a sparse index in RocksDB.

[![](https://substackcdn.com/image/fetch/$s_!XsVr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e53494a-1575-468f-b269-e9843da90afb_908x478.png)](https://substackcdn.com/image/fetch/$s_!XsVr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e53494a-1575-468f-b269-e9843da90afb_908x478.png)

Write requests are batched until one of those conditions is met:

* A defined amount of time has passed
* The batch’s size reaches a configurable limit.
* The number of write requests reaches a configurable limit.

The batch is then written synchronously to the WAL, appended to segment files, fsynced these files, and the index is updated.

While Kafka excels at zero-copy reads, writes still require data to be transferred from the application buffer to the OS page cache and then to disk. Direct I/O can optimize write paths by eliminating the need for an intermediate OS page cache copy. In addition, Northguard utilizes application-level caching to leverage the information about its consumed data to fill the cache.

---

## How Kafka clients work with it

Given the protocol difference between Kafka and Northguard and the intensive use of Kafka at LinkedIn, migration is highly challenging.

LinkedIn introduces Xinfra, a virtualized Pub/Sub layer supporting both Northguard and Kafka for this purpose. Xinfra abstracts away physical clusters and provides a unified experience for both Kafka and Northguard clients.

[![](https://substackcdn.com/image/fetch/$s_!fUDV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487e290f-06c2-4da7-a14d-cb85f6fa1225_442x434.png)](https://substackcdn.com/image/fetch/$s_!fUDV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F487e290f-06c2-4da7-a14d-cb85f6fa1225_442x434.png)

Xinfra leverages dual-write approaches to facilitate the migration of user topics. Producers are migrated first, followed by consumers.

During the migration period, producers perform writes into both Kafka and Northguard to allow for a safe fallback in case of migration failures. Producers and consumers continue to operate normally during the migration. At the end of the process, the dual writes will be turned off.

---

## My thoughts

Despite the widespread adoption, Kafka has limitations that cause organizations trouble when managing at a large scale, especially in the cloud era. Many alternative solutions are introduced to solve the problems, most of which share some common characteristics:

[![](https://substackcdn.com/image/fetch/$s_!7lJT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20b2ef37-14cd-49b6-a6a2-a7689fa7b7c9_608x270.png)](https://substackcdn.com/image/fetch/$s_!7lJT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20b2ef37-14cd-49b6-a6a2-a7689fa7b7c9_608x270.png)

* They believe most of the use cases don’t require ultra-low latency, thus using a cheaper storage medium like object storage is acceptable.
* Besides the cheaper price, object storage also handles the data durability and availability for Kafka.
* Keeping the Kafka compatibility is non-negotiable.

However, we observed that the organization that created Kafka approaches building a Kafka alternative solution differently. They still want to keep the high throughput and low latency of Kafka while improving the scalability and operability. And it seems that they have concluded the Kafka protocol can’t help them achieve that.

[![](https://substackcdn.com/image/fetch/$s_!mWYv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b66064e-d9d3-4d36-90d3-f476cf5b0fd0_332x230.png)](https://substackcdn.com/image/fetch/$s_!mWYv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b66064e-d9d3-4d36-90d3-f476cf5b0fd0_332x230.png)

They developed the new solution using a different protocol and a distinct approach to organizing data and metadata. The most obvious difference compared to Kafka is the unit of data replication when Northguard replicates segments between brokers, rather than partitions. This clearly helps them achieve better load balancing and limit the number of clients affected by the rebalancing process compared to Kafka. However, they must put more effort into the migration process due to the huge differences between Kafka and the new system.

LinkedIn has its reasons and substantial resources for approaching it this way, rather than maintaining the Kafka protocol and attempting to replace the storage layer with object storage. Although users can utilize object storage for the Northguard storage layer (in theory, as the storage is pluggable), LinkedIn initially designed Northguard for local disk, as their primary focus is on low latency.

According to InfoQ, LinkedIn will explore the possibility of open-sourcing Northguard after finalizing the internal development of this system. However, I don’t see a solution that speaks a different language than Kafka’s will replace Kafka, as many organizations rely on this protocol. In addition, Northguard and Xinfra are built for the scale of LinkedIn, and not every company has the same requirements for latency and throughput as that.

However, I am still looking forward to the open-source release of these solutions. A pluggable storage layer is a good starting point for choosing the storage medium that best suits the organization's needs (e.g., object storage when low latency is acceptable but the cost must be significantly reduced).

If LinkedIn can somehow wrap a lightweight layer on top of Northguard, making it Kafka-compatible to some extent, things will be exciting, as the solution from Kafka’s parent is going to compete with all other Kafka alternative solutions out there.

---

## Outro

Thank you for reading this far.

In this article, we learned LinkedIn’s motivation behind building a new solution to replace Kafka called Northguard. Then, we explore Northguard’s data model, how it manages metadata, how the protocol differs from Kafka, and how it can help LinkedIn. Finally, I have some thoughts on the emerging trend of using object storage for Kafka vs Northguard.

See you in my next articles.

P.S. I read every comment. Your feedback helps me improve, so feel free to share your thoughts below.

---

## Reference

*[1] Onur Karaman and Xiongqi Wu, [Introducing Northguard and Xinfra: scalable log storage at LinkedIn](https://www.linkedin.com/blog/engineering/infrastructure/introducing-northguard-and-xinfra) (2025)*

*[2] Eran Stiller, [LinkedIn, Announces Northguard and Xinfra: Scaling beyond Kafka for Log Storage and Pub/Sub](https://www.infoq.com/news/2025/06/linkedin-northguard-xinfra/) (2025)*
