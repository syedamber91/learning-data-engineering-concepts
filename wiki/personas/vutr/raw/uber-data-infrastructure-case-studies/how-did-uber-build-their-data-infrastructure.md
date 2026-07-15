---
title: "How did Uber build their data infrastructure to serve 137 million monthly active users"
channel: vutr
author: "Vu Trinh"
published: 2025-06-12
url: https://vutr.substack.com/p/how-did-uber-build-their-data-infrastructure
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Delta Lake", "Data Modeling", "Data Lake", "Streaming", "Batch Processing", "ETL"]
tags: [https, auto, uber, kafka, substackcdn, image]
---

# How did Uber build their data infrastructure to serve 137 million monthly active users

*With the help of Kafka, HDFS, Hudi, Spark, Flink, Pinot, and Presto*

> Source: [Open post](https://vutr.substack.com/p/how-did-uber-build-their-data-infrastructure)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[delta-lake|Delta Lake]] · [[data-modeling|Data Modeling]] · [[data-lake|Data Lake]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=165604105)

[![](https://substackcdn.com/image/fetch/$s_!wTEK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04735244-91c9-4ac6-a96f-5ff2ef9abc68_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!wTEK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04735244-91c9-4ac6-a96f-5ff2ef9abc68_2000x1429.png)

---

## Intro

This week, we will explore Uber’s data infrastructure, which was built with open-sourced solutions like Kafka, Spark, Flink, Hudi, Pinot, and Presto.

**Note**: I read and compiled many resources from Uber to write this article. Those resources vary in both details and release time; it’s sure that this article might not entirely reflect the current status of Uber’s data infrastructure. Feel free to reach out if you find something that needs to be corrected. All the technical details in this post are credited to the Uber engineering teams.

---

## High-level architecture

[Straight from their homepage](https://www.uber.com/us/en/about/), Uber's mission is to power the movement, from the place we want to go to the meals we want to eat.

They promise to do it worldwide.

In real time.

From a [talk](https://opensourcedatasummit.com/ubers-data-infrastructure/), they shared that they currently serve 137 million monthly active users across 10,000 cities with 25 million trips daily.

Uber relies heavily on data to support its business.

The data is not only used for common analytic cases; Uber also uses data to power critical functions of their services and applications, such as rider safety, ETA predictions, or fraud detection.

To efficiently collect, store, manage, and serve data, Uber has constantly built and improved its lambda-architecture, with open-source solutions as the backbone.

From the 10,000-foot view, Uber’s data architecture has:

[![](https://substackcdn.com/image/fetch/$s_!qRM2!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd719498f-4e20-4110-bad4-b778efa69ff2_1900x1074.png)](https://substackcdn.com/image/fetch/$s_!qRM2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd719498f-4e20-4110-bad4-b778efa69ff2_1900x1074.png)

* **The stream**: Flink consumes data from Kafka. After processing the data in real time, Flink sinks data to Pinot to serve real-time analytics. Users can interact with Pinot via a custom SQL built on Presto.
* **The batch**: Spark consumes data from Kafka and writes to the data lake, which is backed by HDFS, Apache Hudi, and Apache Hive. The data is transformed to fit the lake's predefined data model before serving analytics demand via Presto.

## Kafka

[Apache Kafka](https://kafka.apache.org/) is a popular open-source event streaming system that has been widely adopted in the industry. It was initially developed at LinkedIn and subsequently open-sourced in early 2011.

Uber has one of the largest deployments of Apache Kafka: trillions of messages and petabytes of data per day.

Kafka at Uber backs many workflows: propagating event data from the rider and driver apps, enabling the streaming analytics platform, or database change logs to the downstream subscribers.

Because of Uber's unique scale characteristics, they customized Kafka with the following enhancements:

### **Cluster federation**

Uber developed a federated Kafka cluster setup that hides the cluster details from producers and consumers.

[![](https://substackcdn.com/image/fetch/$s_!-B4J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7730d19c-1d3a-4687-b86e-623721cfc3cb_1508x752.png)](https://substackcdn.com/image/fetch/$s_!-B4J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7730d19c-1d3a-4687-b86e-623721cfc3cb_1508x752.png)

* They expose the "logical Kafka clusters" to the user. The users don’t need to know which cluster a topic is in.
* A dedicated server centralizes all the metadata of the clusters and topics to route the client’s request to the physical cluster.
* This design improves scalability. When a cluster is fully utilized, the Kafka service can scale horizontally by adding more clusters. New topics are seamlessly created on the newly added clusters.
* Cluster federation also simplifies topic management. Due to the large number of applications and clients, migrating a live topic between Kafka clusters is difficult. The process typically requires manual configuration to route the traffic to the new cluster, which causes the consumer to restart. The design helps redirect traffic to another physical cluster without restarting the application.

### **Dead letter queue**

There are scenarios in which downstream systems fail to process the messages. Originally, two options in Kafka can handle this situation:

* Drop those messages.
* Indefinitely retry, which blocks the processing of the subsequent messages.

However, Uber has many scenarios that demand neither data loss nor blocked processing. To deal with these use cases, Uber builds the [Dead Letter Queues (DLQ)](https://www.uber.com/en-VN/blog/chaperone-audit-kafka-messages/) strategy on top of Kafka.

[![](https://substackcdn.com/image/fetch/$s_!1Axj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F858ffec2-eed3-49a5-9d40-92bedd69e35f_672x312.png)](https://substackcdn.com/image/fetch/$s_!1Axj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F858ffec2-eed3-49a5-9d40-92bedd69e35f_672x312.png)

If the consumer cannot process a message after retries, it will publish it to the DLQ. This way, unprocessed messages will be handled separately, not affecting other messages.

### **Consumer Proxy**

With tens of thousands of Kafka-running applications, Uber struggles to debug them and upgrade the client library. Users also use many programming languages inside organizations to interact with Kafka, which makes it challenging to provide multi-language support when the clients are complex.

They built a consumer proxy layer to address the challenges. The proxy reads messages from Kafka and routes them to a gRPC service endpoint. It handles the complexities of the consumer library, and applications only need to adopt a light gRPC client.

[![](https://substackcdn.com/image/fetch/$s_!4nJH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36001c8f-1791-433a-b145-60f598b6674f_600x582.png)](https://substackcdn.com/image/fetch/$s_!4nJH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36001c8f-1791-433a-b145-60f598b6674f_600x582.png)

When the downstream service fails to receive or process some messages, the proxy can retry the routing and send them to the DLQ after several retries fail.

The proxy also changes the delivery mechanism in Kafka from message polling to push-based message dispatching. This improves the consumption throughput and allows more concurrent application processing opportunities.

### **Cross-cluster replication**

Because of the large scale of the business, Uber uses multiple Kafka clusters in different data centers. With this deployment, Uber needs the cross-cluster data replication of Kafka for two reasons:

* Getting a global view of the data for various use cases. For example, they must consolidate and analyze data from all data centers to compute trip metrics.
* Uber replicates Kafka deployment to achieve redundancy in case of failures.

Uber built and open-sourced a reliable solution called [uReplicator](https://github.com/uber/uReplicator) for Kafka replication purposes. The replicator has an algorithm that keeps the number of affected topic partitions as low as possible during rebalancing. Moreover, it can redistribute the load to the standby workers at runtime in case of a traffic burst.

### Tiered storage

Kafka was designed with tightly coupled compute and storage, a common approach back then, given that the network was not as fast as it is today. Scaling storage requires adding more machines, leading to inefficient resource usage.

Uber proposed Kafka Tiered Storage ([KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage)), introducing a two-tiered storage system:

[![](https://substackcdn.com/image/fetch/$s_!9A90!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d560d63-3c51-4643-bb4c-6637b245895f_1010x426.png)](https://substackcdn.com/image/fetch/$s_!9A90!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d560d63-3c51-4643-bb4c-6637b245895f_1010x426.png)

* Local storage (broker disk) stores the most recent data.
* Remote storage (HDFS/S3/GCS) stores historical data.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=165604105)

---

## HDFS

Uber uses [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) for the data lake. Apache Spark consumes and processes the data from Kafka. The Spark jobs then write the data to HDFS using the Parquet file format, plus the Apache Hudi metadata.

Inside the Lake, Uber leverages Apache Hive to transform landing data into well-organized data based on the data modeling.

[In 2024, Uber shared](https://www.uber.com/en-VN/blog/modernizing-ubers-data-infrastructure-with-gcp/) that it was migrating their infrastructure to the Google Cloud, and HDFS was incrementally replaced with object storage.

## Hudi

At first, Uber leveraged only native Parquet files and HDFS for its data lake. However, it showed limitations over time. It lacks efficient support for updates and deletes. Many use cases at Uber require data to be processed incrementally; they need to process only the changed/affected data to ensure freshness.

Imagine Uber had a dataset containing daily driver earnings for every driver. A rider can tip the driver hours after a trip is completed. A driver earned $10 for the trip on Monday night and got an extra 1$ tip on Tuesday morning.

[![](https://substackcdn.com/image/fetch/$s_!VZGY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44ef386d-f37c-4b7d-bf0a-33fe27edab5b_476x328.png)](https://substackcdn.com/image/fetch/$s_!VZGY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44ef386d-f37c-4b7d-bf0a-33fe27edab5b_476x328.png)

With batch processing, Uber doesn’t know if the driver’s earning data will be changed. They must assume that “Data was changed in the last X days“ and reprocess all X data partitions to update the driver earnings. A small change can cost them a lot of resources to re-process the data,

[![](https://substackcdn.com/image/fetch/$s_!OYIP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61ea3802-19a6-4246-a7e7-48d010619f8f_410x438.png)](https://substackcdn.com/image/fetch/$s_!OYIP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61ea3802-19a6-4246-a7e7-48d010619f8f_410x438.png)

What if they could extract only the update (e.g., the event where the rider tipped $1$) and apply it to the target table?

To bring the incremental processing capability to the data lake, Uber developed the Apache Hudi table format. You can check out the details of Apache Hudi from my previous article:

In short, Hudi has a very special design compared to the Iceberg or Delta Lake format. The ultimate goal is to process data incrementally. To achieve this, there are Hudi’s characteristics that we need to be aware of:

* **Two file formats**: The **base files** store the table’s records. To optimize data reading, Hudi uses a columnar-oriented file format (e.g., Parquet) for the Base Files. The **log files** capture changes to records on top of their associated Base File. Hudi uses a row-oriented file format (e.g., Avro) for Log Files to optimize data writing.

[![](https://substackcdn.com/image/fetch/$s_!8j5l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26fddf5a-45df-49bf-94f6-ab736e57a299_430x406.png)](https://substackcdn.com/image/fetch/$s_!8j5l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26fddf5a-45df-49bf-94f6-ab736e57a299_430x406.png)

* **Timeline**: Hudi Timeline records all actions performed on the table at different times, which helps provide instantaneous views of the table while also efficiently supporting data retrieval in the order of arrival.

[![](https://substackcdn.com/image/fetch/$s_!RYDn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc14ab00c-314d-48ff-baa2-1a635f436f47_564x236.png)](https://substackcdn.com/image/fetch/$s_!RYDn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc14ab00c-314d-48ff-baa2-1a635f436f47_564x236.png)

* **Primary key**: Each record in a Hudi table has a unique identifier called a primary key, consisting of a pair of record keys and the partition's location to which the record belongs. Using primary keys, Hudi ensures no duplicate records across partitions and enables fast updates and deletes on records. Hudi maintains an index to allow quick record lookups.

[![](https://substackcdn.com/image/fetch/$s_!dErX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8576c88e-62bb-45f3-86ff-c777843cf508_436x310.png)](https://substackcdn.com/image/fetch/$s_!dErX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8576c88e-62bb-45f3-86ff-c777843cf508_436x310.png)

## Spark

[In 2023, Uber](https://www.uber.com/en-VN/blog/sparkle-modular-etl/) migrated all batch workloads to Apache Spark, using 20,000+ critical pipelines and datasets to power the batch workloads.

Uber developed the [Sparkle framework](https://www.uber.com/en-VN/blog/sparkle-modular-etl/) on top of Apache Spark to streamline Spark pipeline development and testing. Sparkle lets users express business logic as modules. Each module in a Sparkle framework is a unit of transformation. This approach improves reusability and testability. Users can create test suites for each module or end-to-end pipelines.

It offers various source and sink integrations so users can focus on writing the business logic using SQL or procedural language such as Java, Scala, or Python.

Uber used Spark to consume data from Kafka and write it to Hudi tables. To simplify this process, the framework was also integrated with a tool called DeltaStreamer. They initially contributed to [DeltaStreamer](https://github.com/apache/hudi/tree/master/hudi-utilities/src/main/java/org/apache/hudi/utilities/deltastreamer), and many organizations have used it to streamline incremental data processing with Hudi. [In more detail](https://hudi.apache.org/docs/hoodie_streaming_ingestion/#hudi-streamer), the tool provides ways to ingest from different sources, such as Kafka.

With the Kafka-Spark-Hudi pipeline, users only need to provide these inputs:

[![](https://substackcdn.com/image/fetch/$s_!fhcB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba0dc2ca-23a0-4d0b-b7ee-86e222f18a3d_432x506.png)](https://substackcdn.com/image/fetch/$s_!fhcB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba0dc2ca-23a0-4d0b-b7ee-86e222f18a3d_432x506.png)

* **Table definition**: A DDL definition file with the table’s schema information and Apache Hudi format.
* **DeltaStreamer YAML configs:** This file will provide a list of configurations expected by the Apache Spark DeltaStreamer application. One important one is the Hudi tables’ primary key, which declares the target table’s primary key. Hudi uses this key to deduplicate data.
* **Transformation logic**: The user will provide a file with the SQL transformation logic. The DeltaStreamer will execute this logic using Spark SQL. For more advanced use cases, users can express the transformation logic using Spark Scala/Java.

## Flink

Uber uses [Apache Flink](https://flink.apache.org/) to build the stream processing platform that processes all the real-time data from Kafka. Flink delivers a distributed stream processing framework with high throughput and low latency. Uber adopted Apache Flink for these reasons:

* Supports many workloads with native state management and checkpointing features for failure recovery.
* It is easy to scale and can handle back pressure efficiently.
* Flink has an active open-source community and a rich ecosystem of integrations.

Uber made the following improvements to Apache Flink:

### FlinkSQL

[![](https://substackcdn.com/image/fetch/$s_!XNvr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f60425d-00b9-4469-877f-f69d1c11bd89_1014x438.png)](https://substackcdn.com/image/fetch/$s_!XNvr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f60425d-00b9-4469-877f-f69d1c11bd89_1014x438.png)

It can transform [Apache Calcite](https://calcite.apache.org/) [SQL inputs](https://calcite.apache.org/docs/reference.html) into Flink jobs. The system converts the SQL input into the logical plan, which then passes through the optimizer and forms the physical plan. Finally, the plan is translated into the Flink job using the [Flink API](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/rest_api/).

### A unified architecture for deployment, management, and operation.

Uber's Flink unified platform resulted in a layered architecture for better extensibility and scalability.

[![](https://substackcdn.com/image/fetch/$s_!pHdZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58153a63-7aa5-4d4b-ae17-ef16940805be_522x634.png)](https://substackcdn.com/image/fetch/$s_!pHdZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58153a63-7aa5-4d4b-ae17-ef16940805be_522x634.png)

* **The platform layer** organizes the business logic and integration with other platforms, such as machine learning or workflow management. This layer transforms business logic into a standard Flink job definition and passes it to the next layer.
* **The Job management layer** handles the Flink job's lifecycle: validation, deployment, monitoring, and failure recovery. It stores the job information, such as the state checkpoints and the metadata. The layer also serves as the proxy that routes the jobs to the physical clusters based on the job’s information. It continuously monitors the health of all jobs and automatically recovers the failed ones. It exposes a set of API abstractions for the platform layer.
* **The bottom layer** consists of the compute clusters and storage backend. It provides an abstraction of the physical resources regardless of on-premise or cloud infrastructure. For example, the storage backend can use [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html), [Amazon S3](https://aws.amazon.com/s3/?gclid=CjwKCAiA6KWvBhAREiwAFPZM7iITWNolRCYCSAt5gXHgR4luTOzzorZ7kvNOIZW968FmHEU0vbeNqBoC0MUQAvD_BwE&trk=f10cddca-7917-4465-9801-28c9cc57f288&sc_channel=ps&ef_id=CjwKCAiA6KWvBhAREiwAFPZM7iITWNolRCYCSAt5gXHgR4luTOzzorZ7kvNOIZW968FmHEU0vbeNqBoC0MUQAvD_BwE:G:s&s_kwcid=AL!4422!3!589846469979!e!!g!!amazon%20s3!16178327440!136912444927), or [Google Cloud Storage (GCS)](https://cloud.google.com/storage?hl=en) for the Flink job’s checkpoints.

## Pinot

At Uber, users leverage [Pinot](https://pinot.apache.org/) for many real-time analytics use cases. The main requirements for such use cases are data freshness and query latency. Pinot is an open-source, distributed OLAP system for performing low-latency analytical queries. Pinot has a lambda architecture that presents a unified view of online (real-time) and offline (historical) data.

In the two years since Uber introduced Pinot, its data footprint has grown from a few GB to several hundred TB of data. With time, the query workload has increased from a few hundred QPS (Queries Per Second) to tens of thousands of QPS.

Pinot supports several indexing techniques, such as inverted, range, or star tree index, to answer low-latency OLAP queries. It divides data by time boundary and groups it into segments, while the query plan executes them in parallel.

## Presto

Uber adopted Presto, an open-source, distributed query engine developed by Facebook, as the primary query interface.

[At Uber, Presto currently processes](https://www.uber.com/en-VN/blog/speed-up-presto-with-alluxio-local-cache/) 500K queries daily, handles over 50 PB of data, and serves 9,000 active users daily. The Presto deployment has 20 clusters with 7,000 nodes.

To manage Presto at scale, besides the Presto clusters, Uber built some more components:

* **The client layer:** This layer includes internal dashboards and other tools. Uber also has backend services that use JDBC to communicate with Presto.
* **The routing layer:** This layer routes queries to different Presto clusters based on statistics from each cluster, such as resource utilization and the number of queries. It acts as the load balancer.

A Presto cluster has a coordinator node and a set of worker nodes:

[![](https://substackcdn.com/image/fetch/$s_!ZYvh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9efd9d76-cab4-432d-95c7-f6e0a1385ca8_1106x892.png)](https://substackcdn.com/image/fetch/$s_!ZYvh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9efd9d76-cab4-432d-95c7-f6e0a1385ca8_1106x892.png)

* The coordinator parses, plans, and orchestrates queries.
* The workers execute the query.

The coordinator parses and analyzes the SQL. It then creates and optimizes the execution plan and sends it to the workers. Workers start executing the tasks, operating chunks of data in an external storage system.

To improve Presto's performance, Uber implements SSD-based cache for each worker node. When calling external systems like HDFS, the worker looks at the cache to see if the data it needs exists.

[![](https://substackcdn.com/image/fetch/$s_!YK8q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5a24e86-87b3-4432-9e84-5e5e7fa60e00_692x350.png)](https://substackcdn.com/image/fetch/$s_!YK8q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5a24e86-87b3-4432-9e84-5e5e7fa60e00_692x350.png)

If yes, it will read from the local SSD. If no, they make the remote call to the remote storage and cache this data for subsequent reads.

—

In addition, Uber tried to unify the SQL usage by introducing CommonSQL, which lets users define SQL in a unified syntax. They built an internal SQL editor to help users build SQL queries. To refine the queries, the editor interacts with the Presto system (via the Client layer). When satisfied with the SQL query, users push it into production.

These refined Presto SQL queries can run on Pinot or Presto. They can also be converted into Flink and Spark jobs.

## Outro

In this article, we explore Uber’s data architecture from a high level and then dive into more details of how Uber leverages open-source tools like Kafka, HDFS, Hudi, Flink, Spark, Pinot, and Presto to efficiently store, process, and serve analytics demand at a very large scale.

Thank you for reading this far. See you in my next posts.

---

## Reference

[1] Girish Baliga, Director of Engineering @Uber, [Session: Diving into Uber's cutting-edge data infrastructure](https://opensourcedatasummit.com/ubers-data-infrastructure/)

*[2] Yupeng Fu, Chinmay Soman, [Real-time Data Infrastructure at Uber](https://arxiv.org/pdf/2104.00087)*

*[3] Uber Engineering team, [Sparkle: Standardizing Modular ETL at Uber](https://www.uber.com/en-VN/blog/sparkle-modular-etl/) (2024)*

*[4] Uber Engineering team, [Speed Up Presto at Uber with Alluxio Local Cache](https://www.uber.com/en-VN/blog/speed-up-presto-with-alluxio-local-cache/) (2022)*
