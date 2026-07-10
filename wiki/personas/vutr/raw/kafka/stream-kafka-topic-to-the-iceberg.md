---
title: "Stream Kafka Topic to the Iceberg Tables with Zero-ETL"
channel: vutr
author: "Vu Trinh"
published: 2025-06-19
url: https://vutr.substack.com/p/stream-kafka-topic-to-the-iceberg
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming", "Data Quality", "ETL"]
tags: [https, auto, kafka, table, substackcdn, image]
---

# Stream Kafka Topic to the Iceberg Tables with Zero-ETL

*A solution from AutoMQ: open-sourced + no need for ETL pipeline maintenance*

> Source: [Open post](https://vutr.substack.com/p/stream-kafka-topic-to-the-iceberg)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *My ultimate goal is to help you break into the data engineering field and become a more impactful data engineer. I'm excited to introduce a paid membership option to take this a step further and dedicate even more time to creating in-depth, practical content.*
>
> *This will allow me to produce even higher-quality articles, diving deeper into the topics that matter most for your growth and making this whole endeavor more sustainable.*
>
> *To celebrate this new milestone, I’m offering a limited-time **50% discount** on the annual plan.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!qqim!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b3b71eb-f194-41e5-a871-85dd9cb817ea_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!qqim!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b3b71eb-f194-41e5-a871-85dd9cb817ea_2000x1429.png)

---

## Intro

For a long time, Kafka has been the standard for distributed messaging. It is heavily used in operational services where a service doesn’t have to communicate directly with hundreds of other services.

“I note things I want to say in a Kafka topic. If you guys want to read, consume them from Kafka. “

Many companies rely on the Kafka protocol. People also use Kafka to ingest data into an analytics repository, which can be a data warehouse, a data lake, or a lakehouse. Suppose we want to build an analytics dashboard from Kafka messages, we must build a pipeline with Kafka Connect, Spark, or Flink to consume messages from the Kafka topic, write them into files, and push these files to the data lake.

We have to handle everything from managing the pipeline to ensuring the files’ optimal physical layout.

Besides the emergence of using object storage for Kafka, ongoing efforts are being made to help organizations streamline the process of converting Kafka’s topic messages to Iceberg tables.

This article will explore the evolution of Kafka’s architecture from its original shared-nothing to the shared-data architecture. Then, we move on to the background and implementation principles behind the development of the Table Topic, the completely open-sourced feature from [AutoMQ](https://github.com/AutoMQ/automq?utm_source=vu_table_topic) that helps users manage the end-to-end Kafka-Iceberg pipeline without user inference.

---

## Original Kafka

LinkedIn generated vast amounts of log data, from user activity events (like logins, page views, and clicks) to operational metrics (service call latency, errors, or system resource utilization).

Traditionally used for tracking user engagement and system performance, this log data now enhances production features such as search relevance, recommendations, and ad targeting.

To deal with LinkedIn’s demands for log processing, a team led by Jay Kreps built a messaging system called [Kafka](https://kafka.apache.org/). The system combines the benefits of traditional log aggregators and publish/subscribe messaging systems. It was designed to offer high throughput and scalability. Kafka provides an API similar to a messaging system, allowing applications to consume real-time log events.

Kafka was designed with tightly coupled compute and storage, a common approach back then, given that the network was not as fast as it is today. It achieves high throughput by leveraging the page cache and the sequential disk access pattern. Modern OS systems usually borrow unused memory (RAM) portions for the page cache. This cache populates frequently used disk data, avoiding touching the disk directly too often. Thus, the system is much faster, mitigating the latency of disk seeks.

[![](https://substackcdn.com/image/fetch/$s_!nc8C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7389d3fe-aff5-4477-82e6-b36ca80cd8fb_472x484.png)](https://substackcdn.com/image/fetch/$s_!nc8C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7389d3fe-aff5-4477-82e6-b36ca80cd8fb_472x484.png)

Kafka is designed to make writing (the producers write data) and reading (the consumers consume data) happen sequentially. There is no doubt that with random access, the disk will be slower than RAM, but it can outperform memory slightly when it comes to sequential access.

However, the initial design of Kafka soon showed limitations.

---

## Uber’s Tiered Storage

This tightly coupled design means that scaling storage requires adding more machines, leading to inefficient resource usage.

[![](https://substackcdn.com/image/fetch/$s_!prmU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbf5a71c-2da4-4cd7-91dc-82b5af39e2a0_844x394.png)](https://substackcdn.com/image/fetch/$s_!prmU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbf5a71c-2da4-4cd7-91dc-82b5af39e2a0_844x394.png)

Kafka's design also relies on replication for message durability. Each partition has a single leader and followers (those storing replicas). All writes must go to the partition’s leader, and reads can be served by a leader or the partition's followers.

[![](https://substackcdn.com/image/fetch/$s_!kpyG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd96fcff6-2e38-440b-9976-7fb1f066179b_986x568.png)](https://substackcdn.com/image/fetch/$s_!kpyG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd96fcff6-2e38-440b-9976-7fb1f066179b_986x568.png)

When the leader receives messages from producers, the leader replicates them to the followers. This ensures data durability and availability. Because Kafka storage and compute are tightly coupled, any change in cluster membership forces data to move around the network.

The challenges get amplified when companies operate Kafka on the cloud:

* It can’t fully leverage the cloud's pay-as-you-go pricing model, as computing and storage cannot be scaled independently.
* It can incur significant cross-availability-zone (AZ) data transfer fees because messages are replicated across different AZs.

To address these limitations, Uber proposed Kafka Tiered Storage ([KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage)), introducing a two-tiered storage system:

[![](https://substackcdn.com/image/fetch/$s_!Xui8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F825afb27-1a58-46d8-b739-5084a5072c36_512x290.png)](https://substackcdn.com/image/fetch/$s_!Xui8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F825afb27-1a58-46d8-b739-5084a5072c36_512x290.png)

* Local storage (broker disk) stores the most recent data.
* Remote storage (HDFS/S3/GCS) stores historical data.

However, the problem was not completely solved. The broker is still stateful.

---

## The trend of shared storage

The year 2023 witnessed the emergence of building Kafka on object storage. At least five vendors have introduced a solution like that since 2023. We had WarpStream and AutoMQ in 2023, Confluent Freight Clusters, Bufstream, or Redpanda Cloud Topics in 2024.

[![](https://substackcdn.com/image/fetch/$s_!2_wB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8fb5703-d909-4410-875e-6a7cc6110775_642x300.png)](https://substackcdn.com/image/fetch/$s_!2_wB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8fb5703-d909-4410-875e-6a7cc6110775_642x300.png)

These new systems promise to offer alternatives to Kafka that:

* Would be cheaper
* Would be way easier to maintain and operate.

Each vendor did this with their approach. At the high level, these systems try to speak the Kafka protocol and store complete data in the object storage. Bufstream and Warpstream rewrite the Kafka protocol from scratch. AutoMQ takes a very different approach, leveraging Kafka’s code for the protocol layer to ensure 100% Kafka compatibility while re-implementing the storage layer so the broker can write data to the object storage without sacrificing the latency due to the introduction of the write-ahead log.

[![](https://substackcdn.com/image/fetch/$s_!uhMA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a976859-1c9c-434d-99a6-4fffc909a9b3_912x588.png)](https://substackcdn.com/image/fetch/$s_!uhMA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a976859-1c9c-434d-99a6-4fffc909a9b3_912x588.png)

AutoMQ leverages Kafka’s code for the protocol. It introduces the Stream abstraction over the segments to facilitate data offloading to object storage.

Of course, building a Kafka-compatible solution on object storage was not easy. Ensuring Kafka compatibility is challenging because the protocol is centered around an essential technical design: it relies on local disks to store data. This includes appending messages to the physical logs, dividing the topic into partitions, replicating them among brokers, load balancing, asking for leader information to produce messages, serving consumers by locating the offset in the segment files, and more.

Thus, switching to a different storage medium (object storage) is hard. Besides that, there are many things to consider, from latency, metadata management, throughput, to cache management.

If you're curious, I wrote a dedicated article on diving into all the potential challenges of building a solution like AutoMQ or WarpStream here:

---

## Shared data

Data is the new oil.

Every company wants the ability to capture, store, process, and serve data to drive business decisions. Data engineers consolidate data from multiple sources, store it, transform it, and serve it through a central repository.

In the past, a data warehouse was the no-brainer choice for organizations when building this analytics repository. However, an alternative approach has emerged recently, [thanks to the evolution of modern table formats](https://vutr.substack.com/p/why-do-we-need-open-table-formats?r=2rj6sg). People call it the “lakehouse.“

[![](https://substackcdn.com/image/fetch/$s_!Wklo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8cd5de1d-5629-4e50-89d1-5e608f1e646f_558x210.png)](https://substackcdn.com/image/fetch/$s_!Wklo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8cd5de1d-5629-4e50-89d1-5e608f1e646f_558x210.png)

Lakehouse offers a simple idea: a giant storage (object storage) that can store your data infinitely (except for your budget), and you can bring any query engine to the party. You will have more control over the data and the flexibility to choose the query engine. It combines the best from both the lake and the warehouse.

However, bringing the data warehouse features, such as ACID semantics or time travel, to the data lake is difficult. The two systems operate with different abstractions; users see tables in the data warehouse, while the lake manages the data as files.

[![](https://substackcdn.com/image/fetch/$s_!R_ej!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356d9418-5946-420c-a5bb-a81ca4f03fe7_918x252.png)](https://substackcdn.com/image/fetch/$s_!R_ej!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356d9418-5946-420c-a5bb-a81ca4f03fe7_918x252.png)

We need a metadata layer to bring table abstraction to the data lake. That’s the value of table formats like Delta Lake, Hudi, or Iceberg.

[![](https://substackcdn.com/image/fetch/$s_!Azhl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2699aba0-ad9e-40e7-a512-03e290d701c7_496x400.png)](https://substackcdn.com/image/fetch/$s_!Azhl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2699aba0-ad9e-40e7-a512-03e290d701c7_496x400.png)

They bring ACID semantics and enable many data warehouse features such as schema evolution, data versioning, time travel, or performance-optimized techniques.

> *If you want to learn more about the rise of these open table formats, check out [this article](https://vutr.substack.com/p/why-do-we-need-open-table-formats?r=2rj6sg).*

Iceberg is getting more attention thanks to its ability to work well with many systems; vendors like Google, Amazon, Databricks, and Snowflake natively support interacting with Iceberg tables.

> *If you want to learn more about Iceberg, check out [this article](https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into).*

A company that uses Kafka likely uses it to stream data to the analytics repository. Plus, with the rise of the lakehouse, the demand for consuming Kafka’s messages and writing them to Iceberg tables increases.

[![](https://substackcdn.com/image/fetch/$s_!oGNH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F102fd773-4ea3-4b84-b0db-609071a3c0f3_498x238.png)](https://substackcdn.com/image/fetch/$s_!oGNH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F102fd773-4ea3-4b84-b0db-609071a3c0f3_498x238.png)

However, managing the Kafka-Iceberg pipelines is not simple. Users must handle everything from defining logic using Flink, Spark, or Kafka Connect to operating these systems and ensuring optimal physical layout of the Iceberg table.

[![](https://substackcdn.com/image/fetch/$s_!xXdE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2b98dc9-10f9-4a66-8c51-7d60c2ac2002_462x308.png)](https://substackcdn.com/image/fetch/$s_!xXdE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2b98dc9-10f9-4a66-8c51-7d60c2ac2002_462x308.png)

That’s why more and more Kafka alternatives offer the feature of writing Kafka’s topic messages to Iceberg tables.

[![](https://substackcdn.com/image/fetch/$s_!wMa7!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F786ff9fc-4b2a-4bbb-9a74-02e815d98027_2134x860.png)](https://substackcdn.com/image/fetch/$s_!wMa7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F786ff9fc-4b2a-4bbb-9a74-02e815d98027_2134x860.png)

From the original shared-nothing architecture, we’ve seen the evolution of Kafka from tiered storage, where the broker still holds a minority of the data, to shared storage, where the data is offloaded 100% to object storage. Now, we might see the new stage of evolution, the shared-data architecture, where the data is available via Kafka’s API and served as Iceberg tables.

Few know that [AutoMQ was the first one in the industry](https://www.automq.com/blog/automq-table-topic-seamless-integration-with-s3-tables-and-iceberg?utm_source=vu_table_topic) to publicly propose the shared-data architecture.

---

## AutoMQ’s approach of Kafka → Iceberg

When the [S3 TABLE](https://aws.amazon.com/s3/features/tables/) is first introduced, AutoMQ simultaneously releases the Table Topic feature, which automatically converts Kafka Topics to Iceberg Tables with the help of S3 TABLE.

At first, this feature was only available in the enterprise version. Recently, AutoMQ officially brought the Table Topic capability to the open source version ([PR-2513](https://github.com/AutoMQ/automq/pull/2513?utm_source=vu_table_topic)). They believed the stream-to-table capability is Kafka’s next big thing.

### Motivation

AutoMQ observed two things when working with their customers.

**First**, there is a real pain point of using Kafka to ingest data into the lakehouse, including the ETL pipelines and data management.

[![](https://substackcdn.com/image/fetch/$s_!e0rB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d1d166c-894e-4a1e-9361-ea1827a38eed_1040x382.png)](https://substackcdn.com/image/fetch/$s_!e0rB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d1d166c-894e-4a1e-9361-ea1827a38eed_1040x382.png)

Every Kafka topic requires an ETL pipeline to consume and transform the data into an open table format. Many topics will result in numerous Spark/Flink job tasks. Managing, monitoring, operating, and governing them is not easy. Data management is also a challenge. How do we handle dirty or corrupted data and manage schema changes?

In addition to the resources for ETL pipelines, each table requires a dedicated resource to manage data on object storage: from cleaning obsolete data/metadata to compacting small files to optimized read performance.

**Second,** there is a demand for data sharing within enterprises, requiring data to be shared and understood between APIs and services. Kafka has been doing very well in operational data sharing, where microservices use the Kafka protocol to exchange data.

[![](https://substackcdn.com/image/fetch/$s_!c1yv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1b89caf-8ba3-4947-89c2-c6879e3ef83a_914x578.png)](https://substackcdn.com/image/fetch/$s_!c1yv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1b89caf-8ba3-4947-89c2-c6879e3ef83a_914x578.png)

However, with the demand for analytics, it needs more than that. Apache Kafka sees your messages as an array of bytes; it does not perceive data schema and semantics. People must somehow transform the Kafka data into a more analytics-friendly representation, and Iceberg is a strong candidate given its ubiquity.

### The overview

The user only needs to set the `automq.table.topic.enable` to use the Kafka-Iceberg feature.

[![](https://substackcdn.com/image/fetch/$s_!N5N_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf6a5c76-23c9-4f66-a4d7-e939e39d7a39_372x264.png)](https://substackcdn.com/image/fetch/$s_!N5N_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf6a5c76-23c9-4f66-a4d7-e939e39d7a39_372x264.png)

After enabling it, the producers still use the Kafka protocol to write data for AutoMQ. The brokers first write the data to the Kafka topic, then convert the data into the Iceberg table after batch accumulation in the background. From this time, the query engine can consume this table to serve analytics demands.

AutoMQ will take care of everything from retrieving the schema to committing the writes to the Iceberg catalog. Users no longer need to maintain complex ETL tasks; they only need to use the Kafka API to produce the data, and AutoMQ will seamlessly convert it into Iceberg tables.

Currently, AutoMQ only supports the Table Topic on AWS with [different catalogs such as REST, Glue, Nessie, or Hive Metastore](https://www.automq.com/docs/automq/table-topic/table-topic-configuration#supported-catalog-types-and-configuration?utm_source=vu_table_topic). They’re working to expand the support for this feature to other cloud vendors.

### Auto Schema management

AutoMQ uses Kafka's native Schema Registry as a data quality gate. When the producers send data it will check whether the data follows the schema retrieved from the schema registry . If not, the producer won’t accept the messages.

[![](https://substackcdn.com/image/fetch/$s_!g9N6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cd1322-fbf7-463d-b5a2-e901426ed2d4_1124x522.png)](https://substackcdn.com/image/fetch/$s_!g9N6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cd1322-fbf7-463d-b5a2-e901426ed2d4_1124x522.png)

In case of schema changes, AutoMQ can use the schema version from the Kafka messages to retrieve the new schema information from the schema registry. It then updates the schema from the Iceberg table to maintain continuous data writing without interruption. This can be achieved because table formats like Iceberg native support schema evolution over time, such as adding new columns, dropping existing ones, or changing data types, without requiring the complete rewriting of the entire dataset or disrupting downstream applications.

Unlike the approach of hardcoding table schema in the Flink/Spark jobs, AutoMQ centralizes the schema definitions that were previously scattered in multiple places into a single source of truth, with the help of the Kafka Schema Registry. This reduces the workload of metadata maintenance and ensures the schema consistency of real-time access (Kafka API )to the lake warehouse storage (Iceberg table).

### Iceberg Partitioning

> ***Note**: This partition concept describes how physical data is organized in an Iceberg table; it does not refer to Kafka’s partition.*

In OLAP systems, the most common way to optimize performance is to limit the data scan as much as possible. Data partitioning is widely recommended for this purpose. Given a table with 6 years of data, if users only need to query data for the last month, it would be efficient to read data for that month instead of doing a full table scan.

Partitioning can help; you configure the table to be partitioned on a specific column, such as the `month` column, and the system will split the table into different parts and store them separately. This helps the query engine to retrieve only the desired partitions based on the user’s filter.

[![](https://substackcdn.com/image/fetch/$s_!lzqh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd03d96b5-7d5b-4859-9ace-171f94bdeabd_410x392.png)](https://substackcdn.com/image/fetch/$s_!lzqh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd03d96b5-7d5b-4859-9ace-171f94bdeabd_410x392.png)

The user can define the Iceberg table partition scheme with multiple columns in AutoMQ so that it will write Kafka’s topic data to Iceberg in associated partitions. Users can configure the partition strategy with the setting `automq.table.topic.partition.by`, for example, `automq.table.topic.partition.by=[month(date)]`.

### Efficient Upsert

AutoMQ also supports the Upsert operation, which lets users specify the key(s). The brokers will use the key to insert, delete, and modify. Iceberg's efficient support for data modification plays a vital role here.

Thanks to Iceberg, this process is efficient. Data modification in Iceberg could be achieved by writing delta files that contain the data change instead of rewriting the whole table.

### No management overhead

To handle this feature, AutoMQ was developed with some more components:

[![](https://substackcdn.com/image/fetch/$s_!kmH9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3319d39-6b4c-4df5-8e00-f2477b8113cc_732x354.png)](https://substackcdn.com/image/fetch/$s_!kmH9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3319d39-6b4c-4df5-8e00-f2477b8113cc_732x354.png)

* The Coordinator manages the synchronization progress and the table’s committing. Each Table Topic has a dedicated Coordinator, which is bound to partition 0 of the Topic. Its role is to limit table committing conflicts and metadata inflation caused by each worker's independent committing.
* The Workers are responsible for the writing process: converting Kafka records into Parquet data files, uploading them to object storage S3, and committing the metadata to the Iceberg catalog. When enabling the tabla topic, each AutoMQ’s partition has a corresponding Worker within the same process.

Users do not need to handle Spark, Flink, or Kafka Connect tasks.

### Cost efficient

By binding the worker to a specific AutoMQ partition, they ensure that Iceberg table read/write operations will happen in the same availability zone (AZ), thus saving cross-AZ costs.

[![](https://substackcdn.com/image/fetch/$s_!v2YW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F000e9309-c586-4e45-af90-e2d855650638_498x386.png)](https://substackcdn.com/image/fetch/$s_!v2YW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F000e9309-c586-4e45-af90-e2d855650638_498x386.png)

Initially, when consuming data from Kafka and writing to the Iceberg table, the data engineers have to manage two storage layers, one for Kafka’s topic and one for the lakehouse’s data. With AutoMQ data, after being transformed to an Iceberg table, the broker can serve this data to both AutoMQ consumers via the Kafka API and analytics query engines.

[![](https://substackcdn.com/image/fetch/$s_!898i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6a4536b-8687-4d51-a172-91caee9911f1_1102x460.png)](https://substackcdn.com/image/fetch/$s_!898i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6a4536b-8687-4d51-a172-91caee9911f1_1102x460.png)

---

## Outro

In this article, we learn about the evolution of Kafka, from its original shared-nothing architecture, tiered-storage, shared-storage, and the most recent paradigm change: the shared data, which we explore why the data lakehouse is an attractive option with the help of open-source formats like Delta Lake, Apache Hudi, and especially the one that seems dominant in the field: Apache Iceberg. Kafka plays a vital role here, as it is the common method to stream the data to the lakehouse. The Kafka-Iceberg pipeline is getting more attention. Many Kafka alternative vendors are trying to offer this feature.

We then explore AutoMQ’s motivation behind the shared data architecture, how it enhanced the broker's ability to write Kafka data to the Iceberg table, and the benefits of this new architecture.

Thank you for reading this far. See you in my next articles.

---

## Reference

*[1] [AutoMQ | Streaming from Kafka Topic to Iceberg® Table](https://www.automq.com/solutions/table-topic?utm_source=vu_table_topic)*

*[2] Jack Vanlightly, [Tableflow: the stream/table, Kafka/Iceberg duality](https://jack-vanlightly.com/blog/2024/3/19/tableflow-the-stream-table-kafka-iceberg-duality) (2024)*
