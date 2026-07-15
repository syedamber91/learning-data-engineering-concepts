---
title: "I spent 4 hours learning the architecture of BigQuery's storage engine"
channel: vutr
author: "Vu Trinh"
published: 2024-11-23
url: https://vutr.substack.com/p/i-spent-4-hours-learning-the-architecture
paid: false
topics: ["Data Engineering", "Apache Kafka", "BigQuery", "Data Warehouse", "Streaming", "ETL"]
tags: [https, stream, auto, image, vortex, substackcdn]
---

# I spent 4 hours learning the architecture of BigQuery's storage engine

*Vortex: The BigQuery's Stream-Oriented Storage Engine (Part 1)*

> Source: [Open post](https://vutr.substack.com/p/i-spent-4-hours-learning-the-architecture)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[etl|ETL]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!SbNq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F785b7a66-de4c-4e8d-b2a3-e1bf174c5ac3_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!SbNq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F785b7a66-de4c-4e8d-b2a3-e1bf174c5ac3_2000x1429.png)

Image created by the author.

---

## Intro

This week, I decided to return to my biased cloud data warehouse—Google BigQuery. (It's simply because I've never used any cloud warehouse longer than BigQuery.)

We'll explore some cool stuff about BigQuery's storage engine from Google's recent paper, [Vortex: A Stream-oriented Storage Engine For Big Data Analytics.](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/)

The paper offers numerous insights, so I'll divide them into two articles. You're reading the first part; the second part will be released next Tuesday.

---

## Overview

The overall BigQuery architecture includes independent components for query execution, storage, a container management system, and a shuffler service:

* **Colossus**: A distributed storage system that holds and stores data.
* **Dremel**: The distributed query engine.
* **Borg is** Google’s large-scale cluster management system that can reliably manage and orchestrate compute resources. ([Borg is the predecessor of Kubernetes.](https://kubernetes.io/blog/2015/04/borg-predecessor-to-kubernetes/)) We will return to Borg when discussing the Vortex architecture.
* **Dedicate shuffle service**: Dremel was inspired by the map-reduce paradigm to operate and manage the data shuffle between stages efficiently; Google built a separate shuffle service on top of disaggregated distributed memory. This service backs BigQuery and supports other services, such as [Google Dataflow](https://cloud.google.com/products/dataflow?hl=en).

Recently, Google released a paper introducing us to the storage engine behind the Google BigQuery.

> *According to [Wikipedia](https://en.wikipedia.org/wiki/Database_engine), a storage engine is a database management system software component that creates, reads, updates, and deletes data from a database*.

[![](https://substackcdn.com/image/fetch/$s_!89Jq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f045947-c488-4c16-ab9e-5394af75c65f_514x662.png)](https://substackcdn.com/image/fetch/$s_!89Jq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f045947-c488-4c16-ab9e-5394af75c65f_514x662.png)

Image created by the author.

The paper presented Vortex, a storage engine Google built to support [real-time analytics in BigQuery](https://cloud.google.com/blog/products/data-analytics/bigquery-continuous-queries-makes-data-analysis-real-time). It is a storage system that supports streaming and batch data analytics. Instead of using infrastructure built for batch data to work with streaming, Google observe that it is better to create a storage system for streaming and then use it for batch. Vortex provides a highly distributed, synchronously replicated storage engine optimized for append-focused data ingestion. (*This reminds me of [ClickHouse MergeTree Storage Engine](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-the-clickhouse?r=2rj6sg&utm_campaign=post&utm_medium=web).)*

I will dive into the Vortext concepts and architecture in the upcoming sections.

---

## The Stream

[![](https://substackcdn.com/image/fetch/$s_!ydel!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c12601f-44b9-403f-be64-fc75e87a114f_668x526.png)](https://substackcdn.com/image/fetch/$s_!ydel!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c12601f-44b9-403f-be64-fc75e87a114f_668x526.png)

Image created by the author.

In Vortex, a stream is an entity to which rows can be appended to the end. The stream identifier and its offset identify every row in. A table is an unordered set of streams. The clients can read a single stream concurrently at different offsets for the read operations. For the write operations, tens of thousands of clients can write to a table concurrently, each using their own stream.

---

## Stream type

Vortex supports the following stream types:

* **UNBUFFERED**: The system will return the successful response to the data append request only if the input data is durably committed to Vortex. Subsequent reads of this table are guaranteed to see these rows.
* **BUFFERED**: The system will return the successful response when the input rows have been written to Vortex but haven’t been committed. Subsequent reads will not be able to see these rows until they are flushed.
* **PENDING**: The input rows are not visible until the Stream is committed.

By providing different types of streams, Vortex unifies batch and stream data ingestion. With **PENDING** mode, Vortex guarantees ACID semantics on large transactions, which is common in batch ETL processes. With **BUFFERED** mode, Vortex guarantees the atomicity for smaller transactions, which is suitable for stream ingestion.

---

## Typical process of writing data using the stream.

[![](https://substackcdn.com/image/fetch/$s_!Ssz0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f0aaeb2-4f03-49cb-9425-97dda402abe3_1478x864.png)](https://substackcdn.com/image/fetch/$s_!Ssz0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f0aaeb2-4f03-49cb-9425-97dda402abe3_1478x864.png)

Image created by the author.

The first step for the client is to create a stream, which requires specifying the desired stream type.

After creating a stream, the clients will get the stream object, including the destination table schema. The clients then use this schema to serialize input data to a binary format (Vortex supports various data formats such as Protocol buffers or Avro). The clients can also input the row\_offset here to specify the offset to which the input data is being appended.

The row\_offet can ensure exactly-once semantics when more than one client tries to append to the same offset; only one will succeed. Clients can prioritize low latency over this guarantee by omitting the row\_offset; the input data will only be written at the end of the stream (the default behavior.)

If the clients use the **BUFFERED**type, the data must be flushed. If the flush process returns success, it implies that all stream rows up to and including the row at row\_offset have been committed.

[![](https://substackcdn.com/image/fetch/$s_!2eUt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0a6a646-ae8f-46de-8de1-9d9986a10988_678x608.png)](https://substackcdn.com/image/fetch/$s_!2eUt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0a6a646-ae8f-46de-8de1-9d9986a10988_678x608.png)

Image created by the author.

With the **PENDING** type, data written to a stream remains invisible until the stream is committed. This mode is mainly used for batch data writing. The scenario involves multiple workers independently writing to the table concurrently. Each creates a PENDING stream, writes all its data to the stream, and reports completion to a coordinator node. Once the coordinator receives success confirmations from all workers, it issues a batch commit request to Vortex to commit all the streams atomically. This ensures the data in these streams becomes atomically visible to readers.

[![](https://substackcdn.com/image/fetch/$s_!x7jz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cd5dc7c-f30b-47cc-8948-c51595a481d3_776x604.png)](https://substackcdn.com/image/fetch/$s_!x7jz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cd5dc7c-f30b-47cc-8948-c51595a481d3_776x604.png)

Image created by the author.

The final step is to finalize a stream. If the clients are done writing the data to the stream, they need to finalize the stream to prevent further appends.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Data Mutation

To implement data mutation in Vortex, the storage engine defines a virtual column called \_CHANGE\_TYPE in the table schema. The column specifies the type of ingested content in the stream. It can have three values associated with three actions: INSERT, UPSERT, and DELETE.

* **INSERT** indicates that the row was appended to the table.
* **UPSERT** indicates the row was updated if the row with the same existed or was inserted otherwise. (using a set of keys in the DML statement to check existed row)
* **DELETE** indicates that all rows that match the set of keys in the DML statement will be deleted.

> ***Note**: While Google supports primary key(s) for BigQuery, it does not enforce uniqueness.*

---

## Concepts

Before moving to the Vortex architecture, let’s learn some metadata concepts:

[![](https://substackcdn.com/image/fetch/$s_!riR9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca810bb-d064-4bcd-8ed8-1386d37935a6_760x440.png)](https://substackcdn.com/image/fetch/$s_!riR9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca810bb-d064-4bcd-8ed8-1386d37935a6_760x440.png)

Image created by the author.

* **Streamlets**: A stream is divided into contiguous slices of rows called Streamlets, and a Stream is an ordered list of one or more Streamlets. To ensure data durability, each Streamlet is replicated within the region. Every Streamlet is stored in at least two Borg clusters in a BigQuery region. A Stream can only have one writable Streamlet at any given time, which is always the last Streamlet in the Stream.
* **Fragments**: Each Streamlet is further split into contiguous blocks of rows called Fragments. Fragments typically are a range of rows inside a log file. Vortex stores log files in Colossus.

> *When reading about Streamlet and Fragment, I was remined of the [Kafka internal](https://open.substack.com/pub/vutr/p/apache-kafka-part-1-overview?r=2rj6sg&utm_campaign=post&utm_medium=web) in which topic is devide into paritions and each partition is replicated between broker, similar to the Vortex’ streamlet. Each Kafka partition of a topic corresponds to a logical log, which is implemented as a set of approximately same size segment files, similar to the Vortex’s Fragment.*

* **Data formats**: Vortex operates in two different data formats to optimize for two workloads. The write-optimized storage format (WOS) is the format in which data is written. The read-optimized storage format (ROS) is the format in which data is optimized for data reading. BigQuery tables use the Capacitor file format as ROS. Data is first written to the Vortex in the WOS format and later converted into the ROS by a dedicated service.

[![](https://substackcdn.com/image/fetch/$s_!S-mP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8683f981-b5df-4c4d-a9b1-9bd0833c3add_1292x522.png)](https://substackcdn.com/image/fetch/$s_!S-mP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8683f981-b5df-4c4d-a9b1-9bd0833c3add_1292x522.png)

Image created by the author.

> *Based on my past research, using two different formats is somewhat similar to [Hudi](https://open.substack.com/pub/vutr/p/i-spent-5-hours-exploring-the-story?r=2rj6sg&utm_campaign=post&utm_medium=web), which uses a row-oriented format (Avro) to achieve high-throughput data ingestion and later writes that data into a column-oriented format (Parquet) to achieve efficient data reading.*

Now, let’s move on to the Vortex architecture.

---

## Control Plane

The Vortex’s Control Plane is the Stream Metadata Server(s) (SMS). It handles the physical metadata of Streams, Streamlets, and Fragments. Google Cloud Spanner backs the SMS and stores the table’s logical metadata, such as the schema and parition/clustering information.

[![](https://substackcdn.com/image/fetch/$s_!HRch!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f097a75-4942-4efd-b8bc-1f512f9c7feb_950x728.png)](https://substackcdn.com/image/fetch/$s_!HRch!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f097a75-4942-4efd-b8bc-1f512f9c7feb_950x728.png)

Image created by the author.

As described above, Vortex Stream provides an entry point for the client to append data to the table. More than one client can append to the table concurrently, and each client can append to its stream.

In most cases, a stream contains a single writable Streamlet. Still, Vortex creates an additional Streamlet whenever a Streamlet is closed due to moving the table to a new Borg cluster or Stream Server restarting.

> *Stream Server is the Vortex Data Plane and will be explore in the next section.*

The SMS assigns a Streamlet to a specific Stream Server, which maintains a set of fragments for the Streamlet. When a Vortex client sends a request to append to a table, the SMS finds an available Stream (which has not been assigned to any client).

[![](https://substackcdn.com/image/fetch/$s_!C9HJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F195cb141-651c-4a6c-b1b9-2b83a3a624fe_1112x806.png)](https://substackcdn.com/image/fetch/$s_!C9HJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F195cb141-651c-4a6c-b1b9-2b83a3a624fe_1112x806.png)

Image created by the author.

If no stream is available, Vortex creates a new stream and assigns it to a Stream Server. It then instructs the server to create the Streamlet. The SMS then responds to the client request with the Streamlet ID and the address of the Stream Server with the writable Streamlet. The client creates a long-lived connection to the Stream Server to append batches of rows to the Streamlet.

> *The seperation of metadata and data request reminded me of the architecture of [HDFS](https://vutr.substack.com/p/i-spent-8-hours-reading-the-paper-523?utm_source=publication-search).*

Each BigQuery table is managed by a single SMS. When the SMS becomes unavailable, the system will redistribute the load by assigning the table to a new SMS.

[![](https://substackcdn.com/image/fetch/$s_!0eT_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeb33543-c715-4148-bab3-783d3b1c95bf_934x562.png)](https://substackcdn.com/image/fetch/$s_!0eT_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeb33543-c715-4148-bab3-783d3b1c95bf_934x562.png)

Image created by the author.

---

## Data Plane

The vortex data plane is the Stream Servers. A single server is responsible for a set of Streams and creates Fragments for those Streams. Besides the metadata from the SMS, the Stream Server has in-memory metadata about its Streams and Fragments. It persists the metadata by writing to a transaction log and periodically checkpointing it. The Stream Server stores Fragments, checkpoints, and transaction logs separately in Colossus. After creating a checkpoint, old logs and checkpoints are cleaned to free up space.

[![](https://substackcdn.com/image/fetch/$s_!610o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ce1689-0d42-4b8c-a5be-c24ec9d231ad_556x540.png)](https://substackcdn.com/image/fetch/$s_!610o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ce1689-0d42-4b8c-a5be-c24ec9d231ad_556x540.png)

Image created by the author.

For each Fragment, the Stream Server’s in-memory metadata holds information like which Streamlet it belongs to, its size, its minimum and maximum record timestamp, whether it was finalized, its schema, and partition/clustering columns.

Each Borg cluster can have hundreds of Stream Servers. A specific Stream Server in a cluster can host Streamlets for any table that uses the cluster as its primary.

> *Stream data is replicated across two Borg clusters within a region. This leads to the bigger picture: a specific BigQuery table is managed by two Borg clusters in the same region. The first cluster serves as the primary, while the second acts as the secondary, to which failover occurs if the primary cluster becomes unavailable.*

As mentioned above, the SMS assigns the Streamlet to the Stream Server. The SMS’s decision aims to balance CPU, memory, and network traffic load between the Stream Server. When the Stream Server gets the request to create a Streamlet from the SMS, it stores the Streamlet information in the metadata and tells the client that this Streamlet is ready to accept the append. Then, the client can send batches of append rows to the Stream Server.

[![](https://substackcdn.com/image/fetch/$s_!w3Nw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F134be13c-40cf-4ece-b401-eb3debea90f2_686x610.png)](https://substackcdn.com/image/fetch/$s_!w3Nw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F134be13c-40cf-4ece-b401-eb3debea90f2_686x610.png)

Image created by the author.

Upon receiving the data row, the Stream Server appends it to the Streamlet’s latest Fragment. When the current Segment reaches a specific size, the Stream Server finalizes the Fragment and creates a new one. The Fragment’s max size needs to be carefully considered here. The reason is that the Fragment is the WOS-ROS conversion unit; its size is chosen to be small enough that the WOS-ROS conversion happens frequently (by the Storage Optimization Service), but if it is too small, the SS will need to manage a lot of Fragments metadata.

If the issue arises during the fragment writing process, the Stream Server finalizes the current fragment and retries to append it to the following fragment. If the following retries fail, the Stream Server finalizes the current Streamlet and marks the append request as failed. At this time, the client will request the SMS for a new Streamlet, which will most likely be placed on a different Stream Server to avoid a scenario when something weird happens with the previous Stream Server.

For the reading operation, the client can choose to read desired Fragments in a specific Streamlet because the Stream Server provides an API that returns the list of Streamlet’s Fragments and the the valid bytes to read from each Fragment.

---

## Outro

Through this article, we’ve explored the overview and architecture of Vortex, BigQuery’s storage engine. See you in the second part of my series on Vortex, where I’ll dive deeper into how it handles data-related and system operations.

---

## **References**

*[1] Google,* [Vortex: A Stream-oriented Storage Engine For Big Data Analytics](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/)

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-4-hours-learning-the-architecture/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
