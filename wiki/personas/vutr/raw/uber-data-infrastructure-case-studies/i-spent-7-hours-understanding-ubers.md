---
title: "How does Uber build real-time infrastructure to handle petabytes of data every day?"
channel: vutr
author: "Vu Trinh"
published: 2024-03-23
url: https://vutr.substack.com/p/i-spent-7-hours-understanding-ubers
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Flink", "Streaming"]
tags: [https, uber, auto, pinot, image, kafka]
---

# How does Uber build real-time infrastructure to handle petabytes of data every day?

*All insights from the paper: Real-time data Infrastructure at Uber.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-7-hours-understanding-ubers)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=142351678)

[![](https://substackcdn.com/image/fetch/$s_!Bxw2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbce475-f7ba-44f3-91f8-07b53b1c996d_1398x999.png)](https://substackcdn.com/image/fetch/$s_!Bxw2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbce475-f7ba-44f3-91f8-07b53b1c996d_1398x999.png)

Image created by the author.

---

## Table of contents:

* *Context*
* *Requirement*
* *Logical building blocks*
* *Deep dive into open-source solutions at Uber: Apache Kafka, Apache Flink, Apache Pinot, HDFS, Presto*
* *Use cases*
* *Uber’s lessons learned*

---

## Intro

[Uber](https://www.uber.com/) is the tech company that transformed the taxi market in the early 2010s when it launched an app that allows easy connection between drivers and riders. In 2023, [137 million people use Uber or Uber Eats once a month. Also, in 2023, Uber drivers completed 9.44 billion trips](https://www.businessofapps.com/data/uber-statistics/). To support the business, Uber aggressively leverages data analytics and machine learning models for operation. From the [dynamic pricing for Uber rides](https://www.uber.com/en-GB/blog/uber-dynamic-pricing/) to the [UberEats Restaurant Manager dashboard](https://merchants.ubereats.com/us/en/technology/simplify-operations/overview/), all must efficiently operate with real-time data. In this blog post, let’s jump on the boat with me to see how Uber manages its behind-the-scenes infrastructure that supports many real-time applications.

> ***Note**: This blog is my note after reading the paper: [Real-time Data Infrastructure at Uber](https://arxiv.org/pdf/2104.00087.pdf)*

---

## Context

[![](https://substackcdn.com/image/fetch/$s_!CHwB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5acf43d0-2c29-4357-8da9-e60b0a19d229_915x732.png)](https://substackcdn.com/image/fetch/$s_!CHwB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5acf43d0-2c29-4357-8da9-e60b0a19d229_915x732.png)

The high-level data flow at Uber infrastructure. Image created by the author with [reference](https://arxiv.org/pdf/2104.00087.pdf).

Uber’s business is highly real-time in nature. Data is continuously collected from many sources: drivers, riders, restaurants, eaters, or backend services. Uber processes this data to extract valuable information to make real-time decisions for many use cases like customer incentives, fraud detection, and machine learning model prediction. Real-time data processing plays a vital role in Uber’s business. The company relies on open-source solutions with in-house improvement to build the real-time infrastructure.

At a high level, real-time data processing in Uber consists of three broad areas:

* **Messaging platform** that allows communication between producers and subscribers.
* **Stream processing** that allows applying processing logic on top of the message streams.
* **Online Analytical Processing (OLAP)** that enables analytical queries over all the data in near real-time.

Each area has three fundamental scaling challenges:

* **Scaling data**: The total incoming real-time data volume has grown exponentially. In addition, Uber's infrastructure lies in several geographical regions to achieve high availability, which means the system has to handle the increase in data volume while maintaining data freshness, end-to-end latency, and availability SLA.
* **Scaling use cases**: As Uber’s business grows, new use cases emerge with varying requirements between different parts of the organization.
* **Scaling users**: The diverse users interacting with the real-time data system have different technical skill levels, from business users with no engineering background to advanced users who need to develop complex real-time data pipelines.

---

## Requirements for the infrastructure

Uber’s real-time infrastructure requires the following points:

* **Consistency**: Critical applications require data consistency across all regions.
* **Availability**: The infrastructure must be highly available with a 99.99 percentile guarantee.
* **Freshness**: Most use cases require second-level freshness. This means the user can process or query a given event or log seconds after it has been produced. This ensures the ability to respond to specific events, such as security incidents.
* **Latency**: Some use cases need to execute queries on the raw data and require the [p99](https://www.linkedin.com/pulse/day-5-mastering-latency-metrics-understanding-p90-p95-nguyen-duc/) query latency to be under 1 second.
* **Scalability**: The system can scale with the ever-growing data volume.
* **Cost**: Uber needs low data processing and serving costs to ensure high operational efficiency.
* **Flexibility**: Uber needs to provide a programmatic and declarative (SQL alike) interface for expressing computational logic to serve diverse user categories.

---

## The building blocks

In this section, we take a look at the main logical building blocks of Uber’s infrastructure:

[![](https://substackcdn.com/image/fetch/$s_!f6zf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd90d3207-d03a-4069-aa43-f40c37cc8bcb_1318x717.png)](https://substackcdn.com/image/fetch/$s_!f6zf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd90d3207-d03a-4069-aa43-f40c37cc8bcb_1318x717.png)

Image created by the author.

* **Storage**: This layer provides the object or blob storage for other layers with a [read-after-write consistency guarantee](https://arpitbhayani.me/blogs/read-your-write-consistency/). It is used for long-term storage and should be optimized for a high write rate. Uber also uses this layer to backfill or bootstrap data into the stream or OLAP table.
* **Stream**: This layer provides a pub-sub interface and should be optimized for low latency for both reads and writes. It requires partitioning the data and guaranteeing [at least once semantic](https://blog.bytebytego.com/i/51197752/𝐀𝐭-𝐥𝐞𝐚𝐬𝐭-𝐨𝐧𝐜𝐞).
* **Compute**: This layer provides computation over the stream and the storage layer. The layer also requires at least one semantics between the source and sink.
* **OLAP**: This layer provides limited SQL capability over data from stream or storage. It should be optimized to serve analytical queries. It requires at least once semantic while ingesting data from different sources. Some use cases require data to be ingestion [exactly once](https://blog.bytebytego.com/p/at-most-once-at-least-once-exactly#%C2%A7%F0%9D%90%84%F0%9D%90%B1%F0%9D%90%9A%F0%9D%90%9C%F0%9D%90%AD%F0%9D%90%A5%F0%9D%90%B2-%F0%9D%90%A8%F0%9D%90%A7%F0%9D%90%9C%F0%9D%90%9E)) based on a primary key.
* **SQL**: This is the query layer on the compute and OLAP layers. The SQL statement is compiled into a compute function, which can be applied to the stream or storage. When used with the OLAP layer, it will enhance the OLAP layer's SQL limit capability.
* **API**: Programmatic way for the higher layer applications to access the stream or compute function.
* **Metadata**: The simple interfaces to manage all kinds of metadata from all the layers. This layer requires metadata versioning and backward compatibility across versions.

The following sections will introduce the open-source system Uber has adopted for the corresponding building block.

## Apache Kafka

> *The streaming storage*

[![](https://substackcdn.com/image/fetch/$s_!7SYJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c89c36c-7841-4923-8c42-2611b3d83acd_1318x717.png)](https://substackcdn.com/image/fetch/$s_!7SYJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c89c36c-7841-4923-8c42-2611b3d83acd_1318x717.png)

Image created by the author.

[Apache Kafka](https://kafka.apache.org/) is a popular open-source event streaming system widely adopted in the industry. It was initially developed at LinkedIn and subsequently open-sourced in early 2011. Besides performance, several other factors for Kafka adoption include simplicity, ecosystem maturity, and open-source community.

In Uber, they have one of the largest deployments of Apache Kafka: trillions of messages and petabytes of data per day. Kafka at Uber backs many workflows: propagating event data from the rider and driver apps, enabling the streaming analytics platform, or database change logs to the downstream subscribers. Because of Uber's unique scale characteristics, they customized Kafka with the following enhancements:

### Cluster federation

> *Logical clusters*

[![](https://substackcdn.com/image/fetch/$s_!W7Y1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47da3de5-562a-43e3-bae1-f05399cd7c58_1072x801.png)](https://substackcdn.com/image/fetch/$s_!W7Y1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47da3de5-562a-43e3-bae1-f05399cd7c58_1072x801.png)

Image created by the author.

Uber developed a federated Kafka cluster setup that hides the cluster details from producers and consumers.

* They expose the "logical Kafka clusters" to the user. The user doesn't need to know which cluster a topic is located in.
* A dedicated server centralizes all the metadata of the clusters and topics to route the client’s request to the physical cluster.
* Moreover, cluster federation helps improve scalability. When a cluster is fully utilized, the Kafka service can scale horizontally by adding more clusters. New topics are seamlessly created on the newly added clusters.
* Cluster federation also simplifies topic management. Due to the large number of applications and clients, migrating a live topic between Kafka clusters is difficult. In most cases, the process requires manual configuration to route the traffic to the new cluster, which causes the consumer to restart. Cluster federation helps redirect traffic to another physical cluster without restarting the application.

### Dead letter queue

> *The queue for “bad“ messages*

[![](https://substackcdn.com/image/fetch/$s_!2UiP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90bb875c-eeaf-4cb3-80ea-b6799fe3c20e_962x426.png)](https://substackcdn.com/image/fetch/$s_!2UiP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90bb875c-eeaf-4cb3-80ea-b6799fe3c20e_962x426.png)

Image created by the author.

There are scenarios in which downstream systems fail to process the messages (e.g., message corruption or unexpected behavior). Initially, two options in Kafka can handle this situation:

* Drop those messages.
* Indefinitely retry, which blocks the processing of the subsequent messages.

However, Uber has many scenarios that demand neither data loss nor blocked processing. To resolve such use cases, Uber builds the [Dead Letter Queues (DLQ)](https://www.uber.com/en-VN/blog/chaperone-audit-kafka-messages/) strategy on top of Kafka: If the consumer cannot process a message after retries, it will publish that message to the DLQ. This way, unprocessed messages will be handled separately, not affecting other messages.

### Consumer Proxy

> *The middle layer*

[![](https://substackcdn.com/image/fetch/$s_!siMN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F943ea2f5-82d2-4349-b825-83353c652931_987x923.png)](https://substackcdn.com/image/fetch/$s_!siMN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F943ea2f5-82d2-4349-b825-83353c652931_987x923.png)

Image created by the author.

With tens of thousands of Kafka-running applications, Uber struggles to debug them and upgrade the client library. Users also use many programming languages inside organizations to interact with Kafka, which makes it challenging to provide multi-language support when the clients are complex.

Uber built a consumer proxy layer to address the challenges; the proxy reads messages from Kafka and routes them to a gRPC service endpoint. It handles the complexities of the consumer library, and the applications only need to adopt a light gRPC client. When the downstream service fails to receive or process some messages, the proxy can retry the routing and send them to the DLQ after several retries fail. The proxy also changes the delivery mechanism in Kafka from message polling to push-based message dispatching. This improves the consumption throughput and allows more concurrent application processing opportunities.

### Cross-cluster replication

> *Efficiently topics replication between clusters*

Because of the large scale of the business, Uber uses multiple Kafka clusters in different data centers. With this deployment, Uber needs the cross-cluster data replication of Kafka for two reasons:

* Getting a global view of the data for various use cases. For example, they must consolidate and analyze data from all data centers to compute trip metrics.
* Uber replicates Kafka deployment to achieve redundancy in case of failures.

Uber built and open-sourced a reliable solution called [uReplicator](https://github.com/uber/uReplicator) for Kafka replication purposes. The replicator has a rebalanced algorithm that keeps the number of the affected topic partitions as low as possible during rebalancing. Moreover, it can redistribute the load to the standby workers at runtime in case of a traffic burst. I’ve researched a little bit about the high-level architecture of the uReplicator, and here’s what I found:

[![](https://substackcdn.com/image/fetch/$s_!M5ml!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ae04366-557b-4550-8106-a0964ba4b34f_1362x697.png)](https://substackcdn.com/image/fetch/$s_!M5ml!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ae04366-557b-4550-8106-a0964ba4b34f_1362x697.png)

Image created by the author with [reference](https://www.youtube.com/watch?v=T2RDH0v3pzs).

* Uber uses [Apache Helix](https://helix.apache.org/) for uReplicator cluster management.
* The Helix controller is responsible for distributing topic partitions to the worker, handling the addition/deletion of topics/partitions, detecting node failures, and redistributing those specific topic partitions.
* After receiving the request for topics/partitions replication, the Helix controller updates the mapping between topic/partitions and the in-charge active worker to the [Zookeeper](https://zookeeper.apache.org/) service, which acts like the central state management service.
* The Helix agents in the worker will get notified when the mapping changes.
* [DynamicKafkaConsumer](https://www.confluent.io/blog/dynamic-vs-static-kafka-consumer-rebalancing/) instances in which the workers will carry the replicated tasks.

Uber also developed and open-sourced another service called [Chaperone](https://github.com/uber-archive/chaperone) to ensure no data loss from cross-cluster replication. It collects critical statistics, like the number of unique messages from every replication stage. Then, the Chaperone compares the statistics and generates alerts when there is a mismatch.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=142351678)

---

## Apache Flink

> *The stream processing*

[![](https://substackcdn.com/image/fetch/$s_!x7wx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd455fe82-8979-4508-a175-d381bdd144d1_1318x717.png)](https://substackcdn.com/image/fetch/$s_!x7wx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd455fe82-8979-4508-a175-d381bdd144d1_1318x717.png)

Image created by the author.

Uber uses [Apache Flink](https://flink.apache.org/) to build the stream processing platform that processes all the real-time data from Kafka. Flink delivers a distributed stream processing framework with a high throughput and low latency. Uber adopted Apache Flink for these reasons:

* Its robustness supports many workloads with native state management and checkpointing features for failure recovery.
* It is easy to scale and can handle back pressure efficiently.
* Flink has a large and active open-source community and a rich ecosystem of integrations.

Uber made the following contributions and improvements to Apache Flink:

### FlinkSQL

> *Building streaming analytical applications with SQL.*

[![](https://substackcdn.com/image/fetch/$s_!f9fM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d4f78ee-5712-44b2-a5f2-83dddf0ef53c_928x390.png)](https://substackcdn.com/image/fetch/$s_!f9fM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d4f78ee-5712-44b2-a5f2-83dddf0ef53c_928x390.png)

Image created by the author.

Uber contributes a layer on top of Flink called the FlinkSQL. It can transform [Apache Calcite](https://calcite.apache.org/) [SQL inputs](https://calcite.apache.org/docs/reference.html) into Flink jobs. The processor compiles the query into a distributed Flink application and manages its entire lifecycle, allowing users to focus on the process logic. Behind the scenes, the system will convert the SQL input into the logical plan, then it goes through the optimizer and forms the physical plan. Finally, the plan is translated into the Flink job using [Flink API](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/rest_api/).

However, hiding the complexity from the user adds the operational overhead for the infrastructure team to manage the production jobs. Uber had to deal with these challenges:

* **Resource estimation and auto-scaling**: Uber uses analysis to find the correlation between the common job types and the resource requirements. The platform team also observed that the workload may vary during peak and off-peak hours, so they continuously monitor the workload to achieve better cluster utilization and perform auto-scaling on demand.
* **Job monitoring and automatic failure recovery**: Since the user does not know what happens behind the scenes of the Flink job, the platform must handle job failures automatically. Uber built a rule-based engine for this purpose. The component compares the job’s metrics and then takes corresponding actions, such as restarting the job.

> ***Note**: FlinkSQL is a stream processing engine with unbounded input and output. Its semantics differ from batch-processing SQL systems, such as Presto, which will be discussed later.*

### A unified architecture for deployment, management, and operation.

[![](https://substackcdn.com/image/fetch/$s_!7s3v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5b5e757-7897-47cf-a537-a2cce9d3f691_800x995.png)](https://substackcdn.com/image/fetch/$s_!7s3v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5b5e757-7897-47cf-a537-a2cce9d3f691_800x995.png)

Image created by the author.

Uber's Flink unified platform resulted in a layered architecture for better extensibility and scalability.

* **The platform layer** organizes the business logic and integration with other platforms, such as machine learning, workflow management, or SQL compilation. The layer transforms business logic into a standard Flink job definition and passes it to the next layer.
* **The Job management layer** handles the Flink job's lifecycle: validation, deployment, monitoring, and failure recovery. It stores the job information: the state checkpoints and the metadata. The layer also serves as the proxy that routes the jobs to the physical clusters based on the job’s information. The layer also has a shared component that continuously monitors the health of all jobs and automatically recovers the failed jobs. It exposes a set of API abstractions for the platform layer.
* **The bottom layer** consists of the compute clusters and storage backend. It provides an abstraction of the physical resources regardless of on-premise or cloud infrastructure. For example, the storage backend can use [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html), [Amazon S3](https://aws.amazon.com/s3/?gclid=CjwKCAiA6KWvBhAREiwAFPZM7iITWNolRCYCSAt5gXHgR4luTOzzorZ7kvNOIZW968FmHEU0vbeNqBoC0MUQAvD_BwE&trk=f10cddca-7917-4465-9801-28c9cc57f288&sc_channel=ps&ef_id=CjwKCAiA6KWvBhAREiwAFPZM7iITWNolRCYCSAt5gXHgR4luTOzzorZ7kvNOIZW968FmHEU0vbeNqBoC0MUQAvD_BwE:G:s&s_kwcid=AL!4422!3!589846469979!e!!g!!amazon%20s3!16178327440!136912444927), or [Google Cloud Storage (GCS)](https://cloud.google.com/storage?hl=en) for the Flink job’s checkpoints.

Thanks to these improvements, Flink has become Uber's central processing platform, responsible for thousands of jobs. Now, let's move on to the next open-source system for the OLAP building block: Apache Pinot.

---

## Apache Pinot

> *The OLAP system*

[![](https://substackcdn.com/image/fetch/$s_!BCVO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F763fd2d6-a099-49da-9c97-97faa0f5871b_1318x718.png)](https://substackcdn.com/image/fetch/$s_!BCVO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F763fd2d6-a099-49da-9c97-97faa0f5871b_1318x718.png)

Image created by the author.

[Apache Pinot](https://pinot.apache.org/) is an open-source, distributed OLAP system for performing low-latency analytical queries. It was created on LinkedIn ["after the engineering staff determined that there were no off-the-shelf solutions that met the social networking site's requirements.”](https://en.wikipedia.org/wiki/Apache_Pinot) Pinot has a [lambda architecture](https://en.wikipedia.org/wiki/Lambda_architecture) that presents a unified view between online (real-time) and offline (historical) data.

In the two years since Uber introduced Pinot, its data footprint has grown from a few GB to several hundreds of TB of data. With time, the query workload has increased from a few hundred QPS (Queries Per Second) to tens of thousands of QPS.

Pinot supports several indexing techniques to answer low-latency OLAP queries, such as [inverted](https://docs.pinot.apache.org/basics/indexing/inverted-index), [range](https://docs.pinot.apache.org/basics/indexing/range-index), or [star tree index](https://www.google.com/search?q=star+tree+index+pinot&oq=star+tree+index+pinot&gs_lcrp=EgZjaHJvbWUqCQgAEAAYExiABDIJCAAQABgTGIAEMgYIARBFGDwyBggCEEUYQdIBCDExNjNqMGo5qAIAsAIA&sourceid=chrome&ie=UTF-8). Pinot takes a [scatter-gather-merge](https://www.youtube.com/watch?v=SnnGargfSOA) approach to query large tables in a distributed manner. It divides data by time boundary and groups it into segments while the query plan executes them in parallel. Here are why Uber decided to use Pinot as their OLAP solution:

> * *In 2018, the available options were [Elasticsearch](https://www.elastic.co/elasticsearch) and [Apache Druid](https://druid.apache.org/), but their following evaluation shows that Pinot has a smaller memory and disk footprint and supports significantly lower query latency SLAs.*
> * *For **ElasticSearch**: Give the same amount of data ingested into Elasticsearch, and Pinot Elasitcsearch’s memory usage was 4x higher, and disk usage was 8x higher than Pinot. In addition, Elasticsearch’s query latency was 2x-4x higher than Pinot's, benchmarked with a combination of filters, aggregation, and group by/order by queries.*
> * *For **Apache Druid**: Pinot is similar in architecture to Apache Druid but has incorporated optimized data structures, such as bit-compressed forward indices, for lowering the data footprint. It also uses specialized indices for faster query execution, such as star tree index, sorted, and range indices, which could result in an order of magnitude difference in query latency.*

At Uber, users leverage Pinot for many real-time analytics use cases. The main requirements for such use cases are data freshness and query latency. Uber has contributed the following features to Apache Pinot to handle Uber’s unique requirements:

### Upsert

The upsert operation combines the insert and update operations. It allows the user to update the existing record and insert a new one if the record doesn't exist in the database. Upsert is a common requirement in Uber's many use cases, such as correcting ride fares or updating delivery status.

[![](https://substackcdn.com/image/fetch/$s_!eQSJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2121c6bd-6f1c-4d90-820f-4a898746672b_784x715.png)](https://substackcdn.com/image/fetch/$s_!eQSJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2121c6bd-6f1c-4d90-820f-4a898746672b_784x715.png)

Image created by the author.

The main challenge for Upsert is finding the locations of the desired records. To overcome this, Uber split the input stream into multiple partitions using the primary key and distributed each partition to a node for processing. This means the same node will handle all the records with the same primary key. Uber also developed a routing strategy that routes subqueries over the segments of the same partition to the same node.

### Full SQL support

Pinot initially lacks important SQL features like subqueries and joins. Uber has integrated Pinot with Presto to enable standard PrestoSQL queries on top of Pinot.

### Integration with the rest of the data ecosystem

Uber has [invested a lot of effort](https://www.uber.com/en-VN/blog/operating-apache-pinot/) into integrating Pinot with the rest of the data ecosystem to ensure a good user experience.

> *For example, Pinot integrates with Uber’s schema service to infer the schema from the input Kafka topic and estimate the data's cardinality. Pinot also integrates with FlinkSQL as a data sink so customers can build an SQL transformation query and push the output messages to Pinot.*

---

## HDFS

> *The archival store*

[![](https://substackcdn.com/image/fetch/$s_!UASf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F502ab4ce-4902-481e-8f9c-5e3358705554_1327x717.png)](https://substackcdn.com/image/fetch/$s_!UASf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F502ab4ce-4902-481e-8f9c-5e3358705554_1327x717.png)

Image created by the author.

Uber uses [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) for storing long-term data. Most data from Kafka in Avro format are stored at HDFS as raw logs. The compact process merges the logs into Parquet format, then available through processing engines like [Hive](https://hive.apache.org/), [Presto](https://prestodb.io/), or [Spark](https://spark.apache.org/). This dataset acts as the source of truth for all analytical purposes. Uber also uses this for data backfilling in Kafka and Pinot. In addition, other platforms use HDFS for their particular purposes. For example:

* Apache Flink uses HDFS for the job checkpoints.
* Apache Pinot uses HDFS for long-term segment archival.

---

## Presto

> *The interactive query layer*

[![](https://substackcdn.com/image/fetch/$s_!hwsz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fad9235-b7eb-461e-8ca7-8d1ba8967fc0_1318x717.png)](https://substackcdn.com/image/fetch/$s_!hwsz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fad9235-b7eb-461e-8ca7-8d1ba8967fc0_1318x717.png)

Image created by the author.

Uber adopted Presto as its interactive query engine solution. [Presto is an open-source, distributed query engine developed at Facebook](https://research.facebook.com/publications/presto-sql-on-everything/). It was designed for fast analytical queries against large-scale datasets by employing a [Massively Parallel Processing (MPP)](https://www.youtube.com/watch?v=SnnGargfSOA) engine and performing all computations in memory, thus avoiding writing intermediate results to disk.

Presto provides a Connector API with a high-performance I/O interface that allows connections to multiple data sources: Hadoop data warehouses, RDBMSs, and NoSQL systems. Uber built a Pinot connector for Presto to satisfy real-time exploration needs. This way, users can execute standard [PrestoSQL](https://prestodb.io/docs/current/sql.html) on top of Apache Pinot.

The Pinot connector needs to decide which parts of the physical plan can be pushed down to the Pinot layer. Due to the API’s limitation, the first version of this connector only included a [predicate pushdown](https://airbyte.com/data-engineering-resources/predicate-pushdown#:~:text=Predicate%20pushdown%20is%20a%20query,of%20data%20transmitted%20and%20processed). Uber improved Presto’s query planner and extended the Connector API to push as many operators down to the Pinot layer as possible, such as [projection](https://www.ibm.com/docs/en/informix-servers/14.10?topic=concepts-selection-projection), aggregation, and limit. This helps lower query latency and leverage Pinot’s indexing.

The following sections introduce some real-time use cases in Uber production and show how Uber uses different systems to achieve its goals.

## Analytical Application: Surge Pricing

The surge pricing use case is a dynamic pricing mechanism in Uber that balances the supply of available drivers with the demand for rides. The overall design of the use case:

* Streaming data is ingested from Kafka.
* The pipeline runs a complex machine-learning-based algorithm in Flink and stores the result in a key-value store for quick result lookup.
* The surge pricing prioritizes data freshness and availability to meet the latency SLA requirement over data consistency because late-arriving messages don't contribute to the computation.
* This trade-off results in the Kafka cluster's configuration for higher throughput but not for lossless guarantee.

## Dashboards: UberEats Restaurant Manager

The Uber Eats restaurant manager dashboard allows the Restaurant owner to run [slice-and-dice queries](https://www.dremio.com/wiki/slice-and-dice-analysis/) to view insights from Uber Eats orders, such as customer satisfaction, popular menu items, and service quality analysis. The overall design of the use case:

* The use case requires fresh data and low query latency, but it does not require too much flexibility because the query’s patterns are fixed.
* Uber uses Pinot with start-tree indexes to reduce the serving time.
* Uber leverages Flink to execute tasks like filtering, aggregating, and roll-ups to help Pinot reduce processing time.
* Uber also observes the tradeoff between transformation time (Flink) and query time (Pinot). The transformation process results in optimized indices (in Pinot) and reduces the data for serving. In return, it reduces the query flexibility on the serving layer because the system has already turned the data into "fixed shapes."

## Machine Learning: Real-time Prediction Monitoring

Machine learning plays a crucial role in Uber, and to ensure the quality of the mode, it's vital to monitor the model's prediction to ensure it outputs accurate data. The overall design of the use case:

* The solution requires scalability due to the high volume and high cardinality of data: thousands of deployed models, each with hundreds of features.
* It leverages Flink's horizontal scalability. Uber deployed a large streaming job to aggregate the metrics and detect prediction abnormalities.
* Flink job creates pre-aggregation as Pinot tables to improve query performance.

## Ad-hoc Exploration: UberEats Ops Automation

The UberEats team needed to execute ad hoc analytical queries on real-time data from couriers, restaurants, and eaters. These insights will be used in a rule-based automation framework. The framework especially helps the ops team during COVID-19 in operating the business with regulations and safety rules. The overall design of the use case:

* The underlying system must be highly reliable and scalable, as this decision-making process is critical to the business.
* The User uses Presto on top of real-time data managed by Pinot to retrieve relevant metrics and then input them into the automation framework.
* The framework uses Pinot to aggregate needed statistics for a given location in the past few minutes and then generates alerts and notifications to the couriers and restaurants accordingly.
* Pinot, Presto, and Flink scaled quickly with the data growth and performed reliably during peak hours.

The following sections will deliver Uber’s all-active strategy, how Uber manages data-backfilling, and lessons learned from Uber.

## All-active strategy

> *This section will show how Uber provides business resilience and continuity.*

Uber relies on a multi-region strategy, ensuring services are operated with backup in geographically distributed data centers so that if one service in one region is unavailable, it can still be up and running in other regions. The foundation of this approach is a multi-region Kafka setup that provides data redundancy and traffic continuation.

[![](https://substackcdn.com/image/fetch/$s_!gtNQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51207906-2462-43ff-ae65-cc679caa6a1c_1163x643.png)](https://substackcdn.com/image/fetch/$s_!gtNQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51207906-2462-43ff-ae65-cc679caa6a1c_1163x643.png)

Image created by the author.

Here is an example of the active-active setup for the dynamic pricing application:

* All the trip events are sent to the Kafka regional cluster and then aggregated into the aggregate clusters for the global view.
* The Flink job will compute the pricing for different areas in each region.
* Each region has an update serviceinstance***,*** and an all-active coordinating service marks one of them as primary.
* The update service from the primary region stores the pricing result in an active/active database for fast lookup.
* When an outage happens in the primary region, the active-active service assigns another region as the primary, and the calculation fails over to another region.
* The computation state of the Flink job is too large to be synchronously replicated between regions, so its state must be computed independently.

→ This approach is compute-intensive because Uber needs to manage redundant pipelines in each region.

---

## Data Backfilling

Uber needs to go back in time and reprocess the data stream for several reasons:

* A new data pipeline often needs to test against the existing data.
* The machine learning model must be trained with a few months of data.
* A change or bug in the stream processing pipeline requires reprocessing old data.

Uber built a solution for stream processing backfilling using Flink, which has two modes of operation:

* **SQL-based**: This mode allows users to execute the same SQL query on both real-time (Kafka) and offline datasets (Hive).
* **API-based**: The Kappa+ architecture allows the stream processing logic to be reused directly on the batch data.

---

## Uber’s Lessons Learned

### Open source adoption

Uber builds most of the real-time analytics stack on open-source components. The main reason behind this is that Uber needs to iterate quickly. Relying on open source gives Uber a strong foundation. Still, this encounters some challenges:

* In their experience, most open-source technologies were built for a specific purpose.
* Uber had to do a lot of work to make the open-source solutions work for a broad spectrum of use cases and programming languages.

### Rapid system development and evolution

For a large company like Uber, it’s common to see multiple driving factors in the architecture’s evolution, such as new business requirements or industrial trends. As a result, Uber learned the importance of enabling rapid software development so that each system can evolve quickly:

* Interface standardization is critical for a clean service boundary. Uber leverages [Monorepo](https://en.wikipedia.org/wiki/Monorepo) to manage all projects in a single code repository.
* Uber always favors [thin clients](https://en.wikipedia.org/wiki/Thin_client) to reduce the frequency of client upgrades. Before the thin Kafka client was introduced, upgrading a Kafka client took several months.
* Uber employs a language consolidation strategy to reduce the number of ways to communicate with the system. Uber supports only [Java](https://www.java.com/en/) and [Golang](https://go.dev/) for programming languages and [PrestoSQL](https://prestodb.io/docs/current/sql.html) for declarative SQL languages.
* The platform team integrated all the infrastructure components with its proprietary CI/CD framework to continuously test and deploy open-source software updates or feature development in the staging environment. Moreover, this also minimizes issues and bugs in the production environment.

### Ease of operation and monitoring

* **Operation**: Uber invested in declarative frameworks to manage system deployments. After users define high-level intentions for operations like cluster up/down, resource reallocation, or traffic rebalancing, the frameworks will handle the instructions without engineer intervention.
* **Monitoring**: Uber built real-time automated dashboards and alerts for each specific use case using Kafka, Flink, or Pinot.

### Ease of user onboarding and debugging

Uber makes efforts in the following aspects to solve the user scaling challenge:

* **Data discovery**: Uber's centralized metadata repository, which acts as the source of truth for schemas across systems such as Kafka, Pinot, and Hive, makes it very convenient for users to search for the required datasets. The system also records the data lineage of the data flow across these components.
* **Data auditing**: Applications' events are audited from end to end. Kafka clients attribute additional metadata to individual events, such as a unique identifier, application timestamp, service name, and tier. The system uses this metadata to track data loss and duplication for every stage of the data ecosystem, helping users detect data issues efficiently.
* **Seamless onboarding**: The system automatically provisions the application log’s Kafka topics for the corresponding service deployed in the production environment. Users can also create Flink and Pinot pipelines using a drag-and-drop UI, which hides the complexity of infrastructure provisioning.

---

## Outro

The Uber paper contains valuable lessons on real-time infrastructure, system designs, and how the company improves and tunes open-source solutions like Kafka, Pinot, or Presto to meet its unique scaling requirements.

I plan to extend my writing topic to other areas like system design and data architecture, especially how big tech companies manage and develop their big data tech stacks, so stay tuned for my future writings ;)

Now it’s time to say goodbye, see you next week.

---

***References**: [Real-time Data Infrastructure at Uber](https://arxiv.org/pdf/2104.00087.pdf)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-7-hours-understanding-ubers/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
