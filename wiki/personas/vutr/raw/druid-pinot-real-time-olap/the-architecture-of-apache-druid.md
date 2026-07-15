---
title: "The Architecture of Apache Druid"
channel: vutr
author: "Vu Trinh"
published: 2024-06-15
url: https://vutr.substack.com/p/the-architecture-of-apache-druid
paid: false
topics: ["Data Engineering", "Apache Kafka"]
tags: [nodes, https, time, druid, auto, real]
---

# The Architecture of Apache Druid

*When Hadoop can solve every problem*

> Source: [Open post](https://vutr.substack.com/p/the-architecture-of-apache-druid)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!hK3Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb18f60f6-d4e6-4aff-ad19-d6d09b9606c6_1399x999.png)](https://substackcdn.com/image/fetch/$s_!hK3Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb18f60f6-d4e6-4aff-ad19-d6d09b9606c6_1399x999.png)

Image created by the author.

---

## Table of contents

* *The beginning*
* *The architecture*
* *The real-time nodes*
* *The historical nodes*
* *The broker nodes*
* *The coordinator nodes*

---

## Intro

This week, we will dive deep into one of the most famous real-time OLAP systems: Apache Druid. Have you ever wondered how it works? This blog post is noted after reading the paper [Druid - A Real-time Analytical Data Store](http://static.druid.io/docs/druid.pdf).

***Note**: This paper was released in 2014, so some of Druid’s details have been changed/updated now.*

---

## The beginning

In 2004, Google published one of the most influential papers in the industry: [MapReduce: Simplified Data Processing on Large Clusters](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf). Google introduced MapReduce to achieve massive large-scale data processing using commodity computers. The Hadoop project followed not long after that; the HDFS and the MapReduce framework set the foundation for big data analytics for many companies over a decade. Despite enabling the storage and process of large-scale data, the Hadoop system has some drawbacks and can’t satisfy every requirement.

[Metamarket](https://metamarkets.com/) (now [Rill](https://www.rilldata.com/metamarkets)) is a company that focuses on helping make it easier for marketers to access, interact, and visualize marketing insights. Metamarkets products require guarantees around query performance and data availability in a highly concurrent environment. They soon realized Hadoop could not support what they needed. After researching many of the open-source solutions, they found that they needed more than the available solutions to help them. Thus, they created Druid, a data store for real-time analytics on large data sets.

In the early days of Metamarkets, they were focused on building a dashboard solution that let users explore event streams. The data beneath the dashboard needed to be processed and returned fast enough for users to have an interactive experience. In addition to the query latency, the system requires high availability (downtime can harm the business) and concurrency (many users use their product simultaneously). This is why Matamarket has to self-develop Druid.

---

## Architecture

[![](https://substackcdn.com/image/fetch/$s_!qmXO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F452a8493-bb0e-467f-b73e-014d79e6e2c1_1152x768.gif)](https://substackcdn.com/image/fetch/$s_!qmXO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F452a8493-bb0e-467f-b73e-014d79e6e2c1_1152x768.gif)

Image created by the author.

Druid has a share-nothing architecture. A Druid cluster has different types of nodes; each node type is in charge of a set of responsibilities. The following sub-sections will dive into the details of Druid’s node types.

> *This blog is based on the Druid technical paper from 2014, so it will describe the initial design of Druid and will not include some components from the [current official document](https://druid.apache.org/docs/latest/design/overlord), like Overlord nodes.*

### Real-time Nodes

The real-time nodes are in charge of ingesting and querying event streams. The nodes can make the events immediately available for querying. They will inform the Zookeeper (Druid’s state management component) of its state and its responsible data. The real-time nodes act like the row store for the event. These nodes maintain an in-memory index buffer for all incoming events; these indexes are incrementally created when events are ingested. The index can be queried directly.

Because of memory limitations, the real-time nodes will persist the in-memory index to disk in two ways: periodically or after the maximum row threshold. This process converts the row-storage format from memory to a column-oriented storage format. Then, the data on the disk will be stored immutably. The real-time node will schedule a background task that looks for all locally persisted data in the disk. The task merges these indexes and builds an immutable data block containing all the ingested events in a specific time range. Following the paper, this merged data is called “segment.” Later, the real-time nodes will upload this segment to remote storage (called deep storage in Druid), such as S3 or HDFS.

[![](https://substackcdn.com/image/fetch/$s_!9pTQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d4ab8f-d1df-4beb-9c61-ca0de34fce0b_768x384.gif)](https://substackcdn.com/image/fetch/$s_!9pTQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d4ab8f-d1df-4beb-9c61-ca0de34fce0b_768x384.gif)

Image created by the author.

Real-time nodes typically consume message buses like Kafka. The producer will send the data to the Kafka topic; then, the real-time node will ingest data by reading from the Kafka topics. There are advantages when there is a middle layer like Kafka:

* **Event buffer**: Kafka maintains event offsets to inform the real-time nodes of their current consumption position. The nodes update this offset every time they persist in their in-memory buffers on disk. If the disk is still available in case of failure, real-time nodes can use the offset saved in the disk to continue reading the topics from that committed offset. This helps reduce the recovery time.
* **Single data endpoint:**

  [![](https://substackcdn.com/image/fetch/$s_!SNc9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8e893d6-368a-4275-9c73-99e963a598d0_461x493.png)](https://substackcdn.com/image/fetch/$s_!SNc9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8e893d6-368a-4275-9c73-99e963a598d0_461x493.png)

  Image created by the author.

  + Redundant consumers: multiple real-time nodes can ingest the same set of events from the Kafka topics to create a redundant event stream; in case 1 real-time node fails, the other node will make sure the data is ingested.
  + Load balanced consumers: multiple real-time nodes each ingest a stream partition. Thus, the system can scale the ingestion throughput.

### Historical Nodes

Historical nodes load and serve the segments from real-time nodes. Segments (from real-time nodes) are stored remotely on storage like S3 or HDFS, and the node’s local disk is used for cache. Like real-time nodes, historical nodes announce their online state and the data they serve in Zookeeper. Druid will send the instructions for historical nodes on how to load and drop segments to the Zookeeper. The instructions also have information about where the segment is located in deep storage and how to decompress and process the segment.

[![](https://substackcdn.com/image/fetch/$s_!ULeZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd15c4278-a359-4738-8ff0-2f3d4d142d7e_960x480.gif)](https://substackcdn.com/image/fetch/$s_!ULeZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd15c4278-a359-4738-8ff0-2f3d4d142d7e_960x480.gif)

Image created by the author.

The historical node will download a specific segment from deep storage for data serving. Before downloading, it first checks the local cache. If the needed segments are not in the cache, they download from deep storage. After downloading it, they announce its status to the Zookeeper. Because they only deal with immutable data, Historical nodes can ensure consistency when executing reading on the segments. Immutability also lets Druid achieve parallelization more efficiently when it is not concerned about whether any process modifies the data.

[![](https://substackcdn.com/image/fetch/$s_!obml!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25488408-7234-4907-a01a-22d7f50453b0_961x464.png)](https://substackcdn.com/image/fetch/$s_!obml!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25488408-7234-4907-a01a-22d7f50453b0_961x464.png)

Image created by the author.

Historical nodes can be grouped into different tiers. Users can configure different performance and fault-tolerance parameters for each tier. The purpose of tiered nodes is to enable higher or lower-priority segments to be distributed according to their importance. For example, users can set up the “hot” tier of historical nodes with high CPUs and memory. The “hot” cluster will download more frequently accessed data. In addition, the “cold” one would only contain less frequently accessed segments.

### Broker Nodes

[![](https://substackcdn.com/image/fetch/$s_!HACJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb87f675-525d-4593-af0a-840694268f06_960x768.gif)](https://substackcdn.com/image/fetch/$s_!HACJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb87f675-525d-4593-af0a-840694268f06_960x768.gif)

Image created by the author.

The broker nodes route the “right” queries to historical and real-time nodes (to the nodes that have necessary data). Broker nodes read the metadata in Zookeeper to point out what segments are queryable and where those segments are located. When the queries need results from real-time and historical nodes, the broker merges results before returning them to the caller.

These nodes have cache implementation with a LRU strategy. The cache can use local heap memory or an external store such as Memcached. When a broker node receives a query, it maps the query to a set of segments. The query results may already exist in the cache, so re-processing them is unnecessary. For any results that do not exist in the cache, the broker node will forward the query to the correct nodes:

* For the results from the historical node, the broker will cache these results on a per-segment basis for future use.
* The broker never caches the results from the real-time nodes. This ensures the query is always processed by the real-time node, which guarantees the freshness of the result.

The broker nodes are critical to routing queries to the processing nodes. They must communicate with the Zookeeper for the segment-nodes mapping to do this. In the case of a Zookeeper failure, broker nodes use the cluster's latest known state (the last metadata from the previous successful Zookeeper communication). Broker nodes will assume that the cluster’s state is the same as before the failure.

### Coordinator Nodes

These nodes are in charge of data management and distribution on historical nodes. The coordinator nodes tell historical nodes to load new data, drop outdated data, replicate data, and move data to load balance. Coordinator nodes have a leader-election process to determine a node that runs the coordinator tasks; other nodes will act as redundant backups.

A coordinator node runs periodically to determine the current state of the cluster. It then makes decisions by comparing the expected state and the actual state of the cluster. (similar to [Kubernetes](https://kubernetes.io/), huh?). Like all the node types above, Coordinator nodes communicate with the Zookeeper for current cluster information. These nodes are also connected to a [MySQL](https://www.mysql.com/) database, which stores additional operational parameters and configurations. The MySQL database stores a rule table that controls how segments are created, destroyed, and replicated in the cluster.

The rule table contains rules. Rules control how historical segments are loaded and dropped from the cluster. Rules let the coordinator know:

* How segments should be assigned to different historical node tiers
* How many replicates of a segment should exist in each tier
* When to drop segments

The coordinator nodes also ensure the cluster’s balance by controlling the distribution of the segments. Furthermore, coordinator nodes can tell the historical nodes to load a copy of the same segment to increase and achieve better fault tolerance and availability; the number of replicas can be configurable.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Storage Format

Tables in Druid are collections of timestamped events and partitioned into segments, where each segment is typically 5–10 million rows. Segments are the fundamental storage unit; replication and distribution are done at a segment level. Every table always has the timestamp column, which Druid requires because Druid uses this column for data distribution and retention policies. Segments are identified by data source identifier, the interval of the data, and the version. Segments with later versions have fresher data. Read operations in Druid always read data in a particular time range from the segments with the latest version. Segments are stored in the remote storage in columnar format; this allows for more efficient CPU usage: only needed data is loaded. Druid has multiple column types to support many data formats. Druid will apply different compression schemes on different data types to compress data on the disk or memory more efficiently.

---

## Outro

That’s all for my notes after reading the paper Druid - A Real-time Analytical Data Store. I hope it brings some value. If you want to read about another real-time OLAP system, you can check out my article on Apache Pinot:

Now, see you on the next blog.

---

## **References**

[1] Fangjin Yang, Eric Tschetter, Xavier Léauté, Nelson Ray, Gian Merlino, Deep Ganguli, [Druid - A Real-time Analytical Data Store](http://static.druid.io/docs/druid.pdf)

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/the-architecture-of-apache-druid/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
