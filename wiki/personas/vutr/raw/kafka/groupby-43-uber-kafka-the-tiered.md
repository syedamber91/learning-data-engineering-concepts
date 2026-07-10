---
title: "GroupBy #43: Uber | Kafka - The Tiered Storage"
channel: vutr
author: "Vu Trinh"
published: 2024-07-09
url: https://vutr.substack.com/p/groupby-43-uber-kafka-the-tiered
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Data Modeling", "Data Lake", "ETL"]
tags: [storage, https, kafka, local, remote, tiered]
---

# GroupBy #43: Uber | Kafka - The Tiered Storage

*Plus: Notion’s data lake - Building and Scaling*

> Source: [Open post](https://vutr.substack.com/p/groupby-43-uber-kafka-the-tiered)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[data-modeling|Data Modeling]] · [[data-lake|Data Lake]] · [[etl|ETL]]

---

*This is **GroupBy**, the weekly compiled resources for data engineers.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I share my lesson and excellent resources to read in this newsletter.*
>
> *Hope this issue finds you well.*

[![](https://substackcdn.com/image/fetch/$s_!CKi-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4dbc9812-a96c-40c4-b747-0a817b03c59e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!CKi-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4dbc9812-a96c-40c4-b747-0a817b03c59e_2000x1429.png)

Image created by the author.

---

# **Kafka Tiered Storage at Uber**

## Intro

Last week, Uber released an article introducing Kafka Tiered Storage; the following texts will cover some insights from that article.

> *You can find the original article from Uber [here](https://www.uber.com/en-SG/blog/kafka-tiered-storage/).*

## The Kafka original

At first, Kafka stores the messages in segment files on the broker’s file system. The only way to scale the storage capacity is by adding more machines. Due to Kafka's compute-storage coupling, we must add unused memory and CPUs when we only need more storage.

## De-coupling effort

Uber proposed Kafka Tiered Storage ([KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)) to de-couple the Kafka storage and processing power. The proposal suggests that instead of having one storage system, Kafka will have two storage tiers: local (as the initial design) and remote.

## **Architecture**

A Kafka cluster with tiered storage uses two tiers: local and remote. The local tier consists of the broker's current local storage, while the remote tier extends to storage like HDFS/S3/GCS/Azure. Each tier has its own retention configurations based on size and time. The local tier's retention can be reduced to hours, whereas the remote tier can retain data for days or months. Latency-sensitive applications perform reads from the local tier, leveraging efficient page cache. In contrast, applications needing older data, such as backfill or failure recovery, access the remote tier.

This brings some advantages:

* Allowing Kafka’s storage capacity to scale independently.
* Reducing the local storage burden on brokers, minimizing data transfer during recovery and rebalancing.
* Consumers can access messages on remote storage directly without loading data back to the broker.
* Allowing for longer data retention.

Tiered storage divides a topic partition’s log into two components: local log and remote log. The first consists of local log segments, while the latter consists of remote log segments. The remote log subsystem copies eligible segments from local storage to remote storage. A segment becomes eligible for copying when its end offset is less than the partition's [LastStableOffset](https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#isolation-level).

> *The last stable offset (LSO) is the offset in a user partition such that all lower offsets have been decided and are always present - [Source](https://strimzi.io/blog/2023/05/03/kafka-transactions/).*

## Copying to the remote storage

The leader broker for a topic partition will process the copying of the eligible log segments to the remote storage. It copies the log segments from the earliest to the latest in a sequence.

[![Image](https://substackcdn.com/image/fetch/$s_!bhma!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbda7948e-292d-404b-be7e-5158eafb705a_899x333.jpeg "Image")](https://substackcdn.com/image/fetch/$s_!bhma!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbda7948e-292d-404b-be7e-5158eafb705a_899x333.jpeg)

Some local segments before the “300” were deleted based on the local retention configuration, but those segments are available remotely because they were copied to the remote storage. [Source](https://www.uber.com/en-SG/blog/kafka-tiered-storage/)

## **Fetching from remote storage**

When a consumer fetch request targets data in remote storage, it is handled by a dedicated thread pool. If the requested offset is available in the broker’s local storage, it is served using the local fetch mechanism. This ensures that local and remote reads do not block each other.

## **Follower Replication**

With tiered storage, followers replicate segments from the leader's local storage and must build auxiliary data (e.g., leader epoch state, producer-ID snapshots) before fetching messages. The follower fetch protocol ensures message consistency and order across replicas, even during cluster changes like broker replacements or failures.

## **Outro**

Speaking of Kafka, I’m currently writing a series of articles about my Kafka learning journey; you can find the first article [here](https://vutr.substack.com/p/apache-kafka-part-1-overview?r=2rj6sg). This article is an overview of Kafka and its use on LinkedIn. The following article will be about some of Kafka’s important designs and will be released this Saturday.

---

# 📋 The list

────────

[Building and scaling Notion’s data lake](https://www.notion.so/blog/building-and-scaling-notions-data-lake) — 12 mins, by Notion Blog

> *In the past three years, Notion's data has expanded 10x due to user and content growth, with a doubling rate of 6-12 months. Managing this rapid growth while meeting the ever-increasing data demands of critical product and analytics use cases, especially our recent Notion AI features, meant building and scaling Notion’s data lake. Here’s how we did it.*

────────

[Canva | Unlocking Efficiency and Performance: Navigating the Spark 3 and EMR 6 Upgrade Journey at Slack](https://slack.engineering/unlocking-efficiency-and-performance-navigating-the-spark-3-and-emr-6-upgrade-journey-at-slack/) — 10 mins, by Slack Engineering Blog

> *Slack Data Engineering recently underwent data workload migration from [AWS](https://aws.amazon.com/emr/) [EMR 5](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-5x.html) (Spark 2/[Hive 2](https://hive.apache.org/) processing engine) to [EMR 6](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-6x.html) ([Spark 3](https://spark.apache.org/news/spark-3-0-0-released.html) processing engine). In this blog, we will share our migration journey, challenges, and the performance gains we observed in the process. This blog aims to assist Data Engineers, Data Infrastructure Engineers, and Product Managers who may be considering migrating to EMR 6/Spark 3.*

────────

[Demystifying Data Flow: ETL and ELT Explained Simply](https://datagibberish.com/p/etl-elt-basics) — 8 mins, by

> *I'll explain ETL and ELT in a clear and understandable way. By the end of this article, you'll have a clear grasp of these essential data processing methods and know precisely when to use each one.*

────────

[Data pipelines and SCDs](https://juhache.substack.com/p/data-pipelines-and-scds) — 4 mins, by

> *The recommended approach for backfilling is not to write ad-hoc SQL but to re-run the pipeline over a specified interval. This is done by designing a pipeline with idempotent transformation code. But what about SCDs?*

────────

[Data Modelling Using Complex Data Types](https://www.junaideffendi.com/p/data-modelling-using-complex-data) — 6 mins, by

> *Complex data types like struct, array, map in modern warehouses are game changer, learn the useful aspects from a Data Engineer.*

────────

[SQL or Python for Data Transformations?](https://www.startdataengineering.com/post/sql-v-python/) - 9 mins, by Start Data Engineering

> *By the end of this post, you will understand how the underlying execution engine impacts your pipeline performance. You will have a list of criteria to consider when using Python or SQL for a data processing task. With this checklist, you can use each tool to its benefit.*

---

## 😉 Previously on Dimension

> *Dimension is my sub-newsletter, where I note down things I learn from people smarter than me in the data engineering field. Here is the latest article*

Let me hear your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-43-uber-kafka-the-tiered/comments)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
