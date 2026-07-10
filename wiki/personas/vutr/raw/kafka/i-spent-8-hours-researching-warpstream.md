---
title: "I spent 8 hours researching WarpStream"
channel: vutr
published: 2024-10-05
url: https://vutr.substack.com/p/i-spent-8-hours-researching-warpstream
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming", "Change Data Capture"]
tags: [warpstream, https, auto, kafka, image, storage]
---

# I spent 8 hours researching WarpStream

*Rewriting Kafka protocol in Go and running 100% on object storage*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-researching-warpstream)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]]

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

[![](https://substackcdn.com/image/fetch/$s_!zaxQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04fdf49d-5bbe-4fde-ad40-cb096c07f4b2_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!zaxQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04fdf49d-5bbe-4fde-ad40-cb096c07f4b2_2000x1429.png)

Image created by the author.

---

## Intro

After writing an article on AutoMQ not long ago, I planned to write about other messaging systems like Redpanda, Pulsar, and especially WarpStream, the solution that was just announced in 2023 as a robust alternative solution to Kafka that can run efficiently on the cloud.

Despite the planning, I didn’t want to write about WarpStream while looking for a topic for this article. However, on September 10th, Confluent announced that it acquired WarpStream and offered customers a [Bring Your Own Cloud (BYOC)](https://jack-vanlightly.com/blog/2024/9/11/byoc-not-the-future-of-cloud-services-but-a-pillar-of-an-everywhere-platform) model. This news made me want to write about WarpStream sooner than planned.

> *Read until the end to check out some of my personal observations on WarpStream.*

---

## Motivation

Before diving into Kafka, let’s understand the WarpStream founder’s WarpStream motivation.

* The challenges arise for those managing Kafka’s infrastructure. Generally, a dedicated team is needed to manage and handle all the operational complexities of Kafka.
* Suppose the users want to perform a basic operation, such as adding more nodes to our Kafka cluster. In that case, they must add broker machines, rebalance all topic partitions, and then wait for data replication. If the cluster is already at a high utilization rate, expanding it will add a significant load, potentially making things worse before they get better. Shrinking the cluster is also complex, as the users have to move data around, wait for data to be replicated, and remove brokers without disrupting partition leadership.
* Networking costs can be very high when lifting and shifting Kafka deployment to the cloud. For instance, if the user deploys a Kafka cluster across three availability zones, the data will be transferred across network boundaries multiple times, which is costly because cloud providers charge for data transfer across zones.
* In addition, durable storage like EBS (Elastic Block Store) in AWS is quite expensive in the cloud. Kafka’s replication factor can increase the storage bill.
* The inability to scale storage independently can waste cloud resources when adding more machines (CPUs, RAMs, and disks) just to expand the storage layer.

That’s why the founders of WarpStream decided to build a whole new system from the ground up in Go, designed to speak Kafka’s protocol.

---

## Overview

Customers must deploy WarpStream using a BYOC model. WarpStream replaces the need for a traditional Kafka cluster with a stateless binary known as the WarpStream agents, which are deployed in the customer account. WarpStream stores message data in object storage, such as Amazon S3 or Google Cloud Storage. The data are also guaranteed never to leave out the customer’s VPC. Agents’ local disks are only used to cache data from object storage (more on this later)

[![](https://substackcdn.com/image/fetch/$s_!SPgZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde80f684-7028-4d87-a44b-497a21f4930e_1286x814.png)](https://substackcdn.com/image/fetch/$s_!SPgZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde80f684-7028-4d87-a44b-497a21f4930e_1286x814.png)

Image created by the author.

> *[Jack Vanlightly](https://jack-vanlightly.com/home), a Staff Technologist at Confluent, has an excellent analysis of WarpStream’s BOYC model. I highly recommend checking out [his article](https://jack-vanlightly.com/blog/2024/9/11/byoc-not-the-future-of-cloud-services-but-a-pillar-of-an-everywhere-platform).*

To manage metadata, WarpStream replaces Zookeeper or KRaft with remote cloud services that run on WarpStream cloud.

---

## Agents

[![](https://substackcdn.com/image/fetch/$s_!rlm9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24907f97-913a-43ba-97f6-c509857e1b45_1518x848.png)](https://substackcdn.com/image/fetch/$s_!rlm9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24907f97-913a-43ba-97f6-c509857e1b45_1518x848.png)

Image created by the author.

The stateless design allows WarpStream agents to scale without caring about the beneath data (data rebalancing). The agents operate within the customer’s VPC, ensuring data privacy; only metadata is transmitted back to the WarpStream cloud service.

---

## WarpStream cloud

WarpStream architecture separates the data plane and control plane. The data plane is a pool of agents. The control plane runs in the WarpStream cloud, where it decides which agents will compact data files for optimal performance, which agents will participate in the data cache, and which agents will delete object storage files that have past retention.

[![](https://substackcdn.com/image/fetch/$s_!tIuO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59e165fa-f381-492a-9fef-4014aa2460fd_1566x926.png)](https://substackcdn.com/image/fetch/$s_!tIuO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59e165fa-f381-492a-9fef-4014aa2460fd_1566x926.png)

Image created by the author.

The control plane empowers WarpStream to fulfill its promise as an Apache Kafka-compatible streaming system by offloading consensus and coordination tasks onto a fully managed control plane. This approach makes the customer’s life easier while keeping all data securely within their VPC.

Additionally, WarpStream manages the cluster’s metadata separately from the data. Instead of leveraging Zookeeper or KRaft, WarpStream manages metadata via the private metadata store on the WarpStream Cloud. This store is a combination of the strongly consistent database and object storage that run in the WarpStream cloud account:

* In AWS, they run [DynamoDB](https://aws.amazon.com/pm/dynamodb/) and [S3](https://aws.amazon.com/s3/).
* In GCP, they run [Cloud Spanner](https://cloud.google.com/spanner?hl=en) and [Google Cloud Storage](https://cloud.google.com/storage?hl=en).
* In Azure, they run [Cosmos DB](https://azure.microsoft.com/en-us/products/cosmos-db) and [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs).

[The vast majority of data in the metadata store are the pointers to batches of data in the object storage.](https://youtu.be/DHravjus3Lw?t=2035) WarpStream metadata store is the leader for all topic partitions and is also in charge of guaranteeing message ordering in WarpStreams. It is involved in both message writing and reading processes; more on this later.

---

## Service Discovery

In Kafka, clients are typically set up with a list of bootstrap brokers via URLs or IPs. They then issue the metadata requests to identify brokers, their availability zones (AZs), and topic partition leaders.

[![](https://substackcdn.com/image/fetch/$s_!3nqc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee10235b-5c6b-4417-bae6-f2102dd4cb00_1696x854.png)](https://substackcdn.com/image/fetch/$s_!3nqc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee10235b-5c6b-4417-bae6-f2102dd4cb00_1696x854.png)

Image created by the author.

The client uses this metadata to establish connections with all the necessary brokers within the cluster. When producing data, the client always attempts to communicate with the leader of a given topic partition. Depending on its configuration, it may connect to one of the replicas when consuming data.

In contrast, thanks to WarpStream’s agents stateless, they can handle any request. When deployed, the agents discover their availability zone in the VPC and send this information and their internal IP address to the service discovery system in the WarpStream Cloud.

Instead of setting the list of bootstrap servers like in Kafka, WarpStream clients only need to be set up with a WarpStream bootstrap URL. The client will use DNS to resolve the WarpStream bootstrap URL to an IP address. Then, the WarpStream DNS server will return any available WarpStream agent IP address.

[![](https://substackcdn.com/image/fetch/$s_!sloR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F602a9e5a-2d71-4bcd-b8fd-61a5bc191b72_1050x678.png)](https://substackcdn.com/image/fetch/$s_!sloR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F602a9e5a-2d71-4bcd-b8fd-61a5bc191b72_1050x678.png)

Image created by the author.

Next, the client issues a metadata request to the agent identified in the previous step. The agent proxies the metadata request to the WarpStream discovery service, which returns the IP of a specific agent in the same AZ as the client.

In Apache Kafka, specific brokers serve as "leaders" for individual topic partitions. With WarpStream, no single agent is the designated leader for any topic partition. Instead, any WarpStream agent can read or write records for any topic partition at a time. However, because clients expect information about partition leaders in the Kafka protocol, WarpStream must still provide them with this information.

The control plane must [make the clients believe](https://www.youtube.com/watch?v=DHravjus3Lw&t=1243s) that the assigned agents are the leaders to align with the Kafka protocol. This approach ensures that the client always communicates with a single agent, minimizing the number of connections in the cluster and making load balancing easier.

WarpStream uses round-robin to load-balance connections across all agents, ensuring an even load distribution. [WarpStream takes a different approach from Kafka when the open-source Kafka solution tries to rebalance partitions across nodes. Instead, WarpStream rebalances the connections across agents.](https://www.youtube.com/watch?v=DHravjus3Lw&t=1280s)

---

## Write

Let’s take a look at how WarpStream carries the message write requests:

[![](https://substackcdn.com/image/fetch/$s_!i5bc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F104ea70b-3955-4f77-95f2-4ed4c481a871_1722x1096.png)](https://substackcdn.com/image/fetch/$s_!i5bc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F104ea70b-3955-4f77-95f2-4ed4c481a871_1722x1096.png)

Image created by the author.

* After the service discovery process described above, producers know which agents they need to communicate with.
* The clients (producers) will send the messages to the agents in batches over the network.

* When receiving write requests from the producers, WarpStream agents buffer requests from multiple producer clients and then write these records in batches to object storage.

  > *By default, the agents will buffer data for 250ms or until 8 MiB of accumulated data. Users can adjust the buffer time to optimize between cost and latency: a higher buffer time reduces costs but increases latency (reduces object storage write requests), while a lower buffer time (increases the write request) has the opposite effect.*
* After the file is written to object storage, the agent commits the metadata to the WarpStream metadata store. At this stage, the ordering of messages is also defined.
* Only then does the agent acknowledge all the requests in the batch and send them back to the clients.

→ Because the agent has to do things like buffering, writing to object storage, and committing to the metadata store, this incurs more latency than the original Kafka solution.

---

## Cache

WarpStream distributes loads across agents by using a consistent hashing ring. This ring lets each agent be responsible for a subset of data within a topic. When an agent receives a Fetch() request from a client, it identifies the agent responsible for the required file and routes the request accordingly.

> *[FetchRequest](https://github.com/apache/kafka/blob/2.2/clients/src/main/java/org/apache/kafka/common/requests/FetchRequest.java) is the request that the consumer sends to a Kafka broker in order to pull data from it.*

Once the request reaches the right agent, it loads the file chunk into memory, creating an in-memory cache. Each chunk of data in the cache is around 16 megabytes. This cache is then used to serve future Fetch() requests, improving efficiency.

A separate cache is maintained for each AZ. This ensures that Fetch() requests don’t need to cross zonal boundaries, avoiding additional latency and cross-AZ data transfer fees.

For historical reads or large data scans (4 megabytes or larger), the agents read data directly from the object store, as the cost of a direct read is more efficient in these cases.

---

## Read

Let’s explore the processes behind the data read path in WarpStream:

[![](https://substackcdn.com/image/fetch/$s_!ZFD2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b84c0a4-457f-4e3b-9b48-a714f7af2eae_1292x1048.png)](https://substackcdn.com/image/fetch/$s_!ZFD2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b84c0a4-457f-4e3b-9b48-a714f7af2eae_1292x1048.png)

Image created by the author.

* When an agent—let's say, agent A—receives a Fetch() request from the consumer, it routes the request to the agent responsible for the required data; let’s call this agent B.
* Agent B will contact the remote metadata store on the WarpStream cloud to retrieve information on which file contains the required data and in which order the files should be read.
* If agent B agent doesn’t have the required data in the memory, it loads the file chunk from object storage into memory, creating an in-memory cache that can serve future requests.
* Data is returned from the memory to the consumers.
* Once a file is cached, subsequent client requests are served directly from memory, reducing the need for repeated object storage access.

---

## Message Ordering

In Kafka, messages are guaranteed to be consumed in sequential order as if they were written. Determining message ordering is straightforward because all the message writing must be done by the leaders.

However, WarpStream allows multiple agents (any of which can be a leader) to write concurrently to any topic partition, resulting in data for a particular partition being scattered across many files without a specific order. How does WarpStream ensure message ordering for the consumers?

WarpStream defines the order of the messages when agents commit metadata to the metadata store after writing files to object storage. At this stage, the metadata store will determine the ordering of the messages in the object storage files.

When reading data from a given offset, the agent queries the metadata store for the file(s) and batches containing the offset. The metadata Store returns an ordered list of files and batches the agent should read, ensuring that the clients are served data correctly.

---

## Compaction

In the background, WarpStream’s compaction process runs automatically within the agents. It consolidates recently written small files or those with significantly different sizes into larger, more uniform files.

[![](https://substackcdn.com/image/fetch/$s_!w3cs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42c745f-3e91-40ff-854b-ff581d54037b_438x334.png)](https://substackcdn.com/image/fetch/$s_!w3cs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42c745f-3e91-40ff-854b-ff581d54037b_438x334.png)

Image created by the author.

The primary goals are standardizing file sizes and optimizing the process of reading historical data. This compaction ensures that data within the same partition is stored close together physically. When workloads need to replay historical data or catch up after falling behind, this organization enables high-throughput sequential reads from object storage, allowing efficient access to large amounts of data.

---

## Agent Roles

[![](https://substackcdn.com/image/fetch/$s_!U2MT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2de3289-4ee2-43f5-be4c-9bae4b12a794_1528x1176.png)](https://substackcdn.com/image/fetch/$s_!U2MT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2de3289-4ee2-43f5-be4c-9bae4b12a794_1528x1176.png)

Image created by the author.

One of WarpStream’s architectural benefits is its flexibility. Users can isolate workloads by deploying separate sets of agents with different roles, such as proxy-produce (handling only requests for pushing data), proxy-consume (handling only requests for reading data), or jobs (dedicated to running background tasks like compaction).

---

## Outro

Throughout this article, we delve into the technical details of WarpStream to understand why, despite being announced only in 2023, it quickly gained significant attention and was ultimately acquired by Confluent.

Drawing from their experience building Husky—a scalable data store at Datadog—the founders of WarpStream developed a superior streaming platform designed to replace and run Kafka in the cloud efficiently. WarpStream provides a highly cost-effective Kafka alternative, managing all complexities and operational overhead (which is extremely valuable to many customers) while allowing customers to keep their data within their private VPC. The cost advantages primarily arise from two key factors: avoiding cross-AZ data transfers and utilizing 100% object storage for data persistence.

That said, WarpStream isn’t without its drawbacks. While it aims to offer Kafka compatibility, it’s not 100%. Some Kafka features, like transactions, are not currently supported (though they promise to add them soon). Beyond the existing feature gaps, WarpStream may also take some time to catch up with future Kafka features that users might expect it to support.

Last but not least, let’s talk about latency. According to WarpStream’s founders, when designing the system, they sacrificed a bit of latency for cost-effectiveness. When a client produces a message, the agent buffers the data, writes it to object storage, and commits metadata to a remote store. Only after these steps are completed does the agent acknowledge the produce requests back to the client. This results in the system having a P99 latency of approximately 400ms for produce requests. Additionally, WarpStream’s end-to-end P99 latency from producer to consumer is around 1 second. Here is a quote from one of the founders:

> *If your workload can tolerate a P99 of ~1s of producer-to-consumer latency, then WarpStream can reduce your total data streaming costs by 5-10x per GiB, with almost zero operational overhead. — [Source](https://www.warpstream.com/blog/kafka-is-dead-long-live-kafka) —*

As mentioned above, users can reduce the latency in the following ways:

* Users can adjust the buffer time in the writing path; this reduces the latency, but in return, the cost will be higher due to more frequent PUT requests to the object storage.
* Use Amazon S3 Express One, which costs more than standard S3.

However, this drawback will surely not be a hurdle for customers with use cases that are not too sensitive to latency, such as Change Data Capture.

---

I think that’s all for my article on WarpStream. If I missed anything, please let me know. Any Feedback or discussion is welcome in the comments.

Thank you for staying with me until the end. See you in my next piece!

---

## **References**

*[1] Richard Artoul, [Kafka is dead, long live Kafka](https://www.warpstream.com/blog/kafka-is-dead-long-live-kafka) (2023)*

*[2] [WarpStream official documentation](https://docs.warpstream.com/warpstream)*

*[3] Yaroslav Tkachenko, [Streaming Platforms in the Cloud Era](https://streamingdata.substack.com/p/streaming-platforms-in-the-cloud-era) (2024)*

*[4] The Geek Narrator, [WarpStream: A drop-in replacement for Kafka](https://www.youtube.com/watch?v=DHravjus3Lw) (2024)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-8-hours-researching-warpstream/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
