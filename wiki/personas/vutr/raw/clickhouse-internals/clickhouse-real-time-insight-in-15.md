---
title: "ClickHouse® -> Real-time insight in 15 minutes"
channel: vutr
author: "Vu Trinh"
published: 2026-03-19
url: https://vutr.substack.com/p/clickhouse-real-time-insight-in-15
paid: false
topics: ["Apache Kafka", "Apache Spark", "Snowflake", "BigQuery", "Data Warehouse", "Streaming"]
tags: [https, auto, tinybird, good, substackcdn, image]
---

# ClickHouse® -> Real-time insight in 15 minutes

*Tinybird: a complete, real-time platform built to work with open-source ClickHouse®*

> Source: [Open post](https://vutr.substack.com/p/clickhouse-real-time-insight-in-15)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]]

---

[![](https://substackcdn.com/image/fetch/$s_!D2el!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28b05579-285a-4e3a-b6c0-ffc897fb8064_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!D2el!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28b05579-285a-4e3a-b6c0-ffc897fb8064_2000x1429.png)

---

> *Neither VuTrinh newsletter nor Tinybird is affiliated, associated with, or sponsored by ClickHouse, Inc. ClickHouse® is a registered trademark of ClickHouse, Inc. This article references ClickHouse solely for descriptive and informational purposes.*

---

## Intro

In the 1980s, Bill Inmon introduced the concept of the data warehouse. Since then, companies have become more focused on using data to support business decisions.

In the 1990s, OLAP systems were still in the research phase. To optimize analytics workloads on OLTP databases, people started building data cubes as precomputed aggregations to speed up queries, which had to be specified in advance and refreshed periodically.

In the 2000s, with the internet’s explosion, companies generated more data than ever before. There was a huge need for a robust system to help companies extract insights from “big data”. We have witnessed the rise of OLAP systems since then: Hadoop, Spark, cloud data warehouses, and open-source OLAP databases.

Compared to 20 years ago, it is much easier to ingest TBs of data, clean it, select some fields, join it with other tables, and aggregate it however you want.

The ability to extract insight from data is commoditized.

However, we live in an era where insight alone is not enough. In some cases, we need insights immediately. The dashboard must be updated every 30 seconds; personalized recommendations must be delivered within 10 seconds; and user-facing analytics must be refreshed every 5 seconds.

[![](https://substackcdn.com/image/fetch/$s_!KIye!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09b5a02b-88d5-444d-80df-c1d60c4eee3e_384x388.png)](https://substackcdn.com/image/fetch/$s_!KIye!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09b5a02b-88d5-444d-80df-c1d60c4eee3e_384x388.png)

OLAP no longer handles historical data and daily reports. They’re required to handle a high-throughput ingested stream and provide real-time query capability. When these properties come up, it’s hard not to mention ClickHouse®. The famous open-source OLAP database was built for real-time analytics.

However, operating ClickHouse can require a strong understanding of the system, including cluster management and configuration tuning, depending on your needs and deployment model. Building a real-time analytics application on your own could therefore potentially take months.

What if you could build real-time analytics applications using ClickHouse in hours instead of months?

In this week’s article, we will dive into why ClickHouse has become a widely used database for real-time analytics workloads and discuss some of the challenges teams may encounter when self-managing ClickHouse deployments. From there, we explore Tinybird, a real-time analytics platform that can help you deliver a real-time analytics application that leverages ClickHouse-compatible infrastructure more quickly. We will learn about their robust ingestion, processing, and serving systems, as well as tooling for building, iterating on, and deploying data projects.

We will end this article with a quick demo and some of my thoughts on Tinybird.

---

## Clickhouse

### What makes it fast?

ClickHouse is an open-source, column-oriented, OLAP database designed for high-performance analytics workloads; for petabyte-scale data with exceptionally ***high ingestion rates***.

[![](https://substackcdn.com/image/fetch/$s_!nJ_q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb639737d-9e2f-488e-855c-0759eb5565ed_552x648.png)](https://substackcdn.com/image/fetch/$s_!nJ_q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb639737d-9e2f-488e-855c-0759eb5565ed_552x648.png)

The database was initially built by engineers from [Yandex Metrica](https://metrica.yandex.com/). They offered an analytics platform that let customers gain real-time insights from around 12 billion daily events in 2014. A single query might require scanning millions of rows within a few hundred milliseconds. The system was designed to support fast analytical queries over large volumes of non-aggregated data.

[![](https://substackcdn.com/image/fetch/$s_!sZF6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F883c7a5e-76d9-4f6f-8c15-c78421902206_1080x500.png)](https://substackcdn.com/image/fetch/$s_!sZF6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F883c7a5e-76d9-4f6f-8c15-c78421902206_1080x500.png)

If you want your dashboard to be updated in seconds or your end users to see fresh statistics (such as the “Who viewed my profile” feature on LinkedIn), ClickHouse is a strong candidate. The database was designed to address the real-time analytics challenges.

Its MergeTree storage engines allow users to index a table’s data by its primary key, which can be a set of columns or expressions.

[![](https://substackcdn.com/image/fetch/$s_!EoLm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8072693-77d4-4a4d-9a8e-709eecab84f2_510x730.png)](https://substackcdn.com/image/fetch/$s_!EoLm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8072693-77d4-4a4d-9a8e-709eecab84f2_510x730.png)

Inspired by the [LSM tree](https://open.substack.com/pub/vutr/p/i-spent-the-weekend-learning-about?utm_campaign=post-expanded-share&utm_medium=web), data in a MergeTree table is stored in horizontally partitioned “parts,” which are later merged in the background to larger ones. This allows ClickHouse to accept ***high-ingestion-rate*** streams, as data can arrive in small parts and be merged later to serve reads.

[![](https://substackcdn.com/image/fetch/$s_!Um3c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba8c8d57-e725-4464-90a1-1137ca322300_914x476.png)](https://substackcdn.com/image/fetch/$s_!Um3c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba8c8d57-e725-4464-90a1-1137ca322300_914x476.png)

ClickHouse stores each column of data independently, and values are sorted (based on the primary key or the sort key).

[![](https://substackcdn.com/image/fetch/$s_!J4_8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6d8762b-0fcf-4cae-8cb0-52d4759bc2ef_570x342.png)](https://substackcdn.com/image/fetch/$s_!J4_8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6d8762b-0fcf-4cae-8cb0-52d4759bc2ef_570x342.png)

Unlike an OLTP database, not every record has an associated index. Instead, the ClickHouse index will point to a range of data (a sparse index). By doing this, ClickHouse can leverage indexes to boost read performance (since data is sorted, the spare index allows ClickHouse to reduce the search space during binary search).

[![](https://substackcdn.com/image/fetch/$s_!Adz4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65876c9a-9b1d-4687-bfb8-cb4ee8db8812_1222x726.png)](https://substackcdn.com/image/fetch/$s_!Adz4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65876c9a-9b1d-4687-bfb8-cb4ee8db8812_1222x726.png)

The approach also prevents the indexing process from impacting the write performance (it would be super expensive if you ingest millions of records while maintaining an index for every record)

In addition to its storage engine, ClickHouse’s robustness also stems from its processing engine. ClickHouse uses a vectorized execution model (like DuckDB, BigQuery, or Snowflake) in combination with opportunistic code compilation.

[![](https://substackcdn.com/image/fetch/$s_!JskB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c2e6a79-4209-4c53-98fd-e8f6899fd4df_1420x850.png)](https://substackcdn.com/image/fetch/$s_!JskB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c2e6a79-4209-4c53-98fd-e8f6899fd4df_1420x850.png)

To process data efficiently, ClickHouse parallelizes queries across multiple levels, from distributing data across multiple nodes to processing batches of data in parallel using SIMD.

> *If you want to learn more about ClickHouse, you can read my two articles [here](https://open.substack.com/pub/vutr/p/i-spent-3-hours-learning-the-overview?utm_campaign=post-expanded-share&utm_medium=web) and [here](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-the-clickhouse?utm_campaign=post-expanded-share&utm_medium=web).*

All of that design makes ClickHouse a leader in real-time analytics.

However, that power comes with complexity.

### What do you need to do to get that power?

If your company wants to self-deploy and manage ClickHouse, here are “a few” things you need to consider:

* As ClickHouse is a distributed database, you need to manage the cluster of physical machines: how do you sure that they have enough resource, how do you coordinate them (ClickHouse Keeper or Zookeeper), how do you shard you data across nodes (as ClickHouse was initially design as share-nothing architecture), what happen when node membership change, such as a node down or you want to add new node, do you need to rebalancing the data?,…

  [![](https://substackcdn.com/image/fetch/$s_!5tLL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd16e88ac-9a02-4ecd-9c81-03eeffe382a6_774x638.png)](https://substackcdn.com/image/fetch/$s_!5tLL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd16e88ac-9a02-4ecd-9c81-03eeffe382a6_774x638.png)
* You have many configurations to adjust so ClickHouse can adapt to your needs: the preferred storage engine, the ingestion connector, the partition merge frequency, the in-memory write buffer, …

  [![](https://substackcdn.com/image/fetch/$s_!NBIi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb279897-0b1f-4729-b013-90ff523a7054_574x322.png)](https://substackcdn.com/image/fetch/$s_!NBIi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb279897-0b1f-4729-b013-90ff523a7054_574x322.png)

Self-managing ClickHouse requires engineers to have a deep understanding of the database. Depending on scale and operational requirements, production ClickHouse deployments may require dedicated engineering resources to manage infrastructure, configuration, and performance tuning.

[![](https://substackcdn.com/image/fetch/$s_!9aSJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ecc073d-9626-48d6-b41d-4a06e2b28e80_488x498.png)](https://substackcdn.com/image/fetch/$s_!9aSJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ecc073d-9626-48d6-b41d-4a06e2b28e80_488x498.png)

It would be a dream to have the power of ClickHouse at our fingertips without the burden of managing it.

# Tinybird

Tinybird comes to the rescue.

[![](https://substackcdn.com/image/fetch/$s_!mEru!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9c544b2-a616-43d8-981b-64e63236bc72_992x536.png)](https://substackcdn.com/image/fetch/$s_!mEru!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9c544b2-a616-43d8-981b-64e63236bc72_992x536.png)

Tinybird is a robust real-time analytics platform that uses ClickHouse-based infrastructure as part of its architecture. In addition to operating and abstracting the underlying infrastructure, the platform offers high-performance ingestion/serving systems and a set of tools to streamline the end-to-end lifecycle of a data project, from development and testing through production deployment.

In the next sections, we will dive into each feature of Tinybird and stick everything together with a simple demo.

## Managed ClickHouse

First, Tinybird provides a managed environment designed to simplify working with ClickHouse-based infrastructure.

The only thing the user needs to care about now is understanding the pricing model. Tinybird is designed to reduce some of the operational complexities commonly associated with running ClickHouse deployments, so users can focus on delivering value from real-time insights rather than spending time and resources on cluster management, tuning, and debugging.

[![](https://substackcdn.com/image/fetch/$s_!R5mI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5319fb09-66d0-480e-bd23-18fb948b33c4_1500x1106.png)](https://substackcdn.com/image/fetch/$s_!R5mI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5319fb09-66d0-480e-bd23-18fb948b33c4_1500x1106.png)

Tinybird manages user workloads across multiple replicas in a ClickHouse-based architecture. Instead of relying on a classic shared-nothing deployment pattern, where each replica holds a subset of data, Tinybird stores data in object storage such as S3 or GCS. Each replica has local SSDs for caching to boost performance.

> *At a high level, this approach is conceptually similar to architectures used by some cloud data platforms (for example, separating storage and compute).*

Stateless replicas mean Tinybird can scale the cluster horizontally. If the user needs more processing power (to serve both write and read), the platform can add more replicas. If the workload is reduced, Tinybird can save resources by scaling down the cluster. Nodes come and go without requiring a data rebalance process.

Tinybird also allows you to change the replica resource spec (vertical scaling). By combining both scale strategies, the platform can adapt to users’ diverse concurrency and latency requirements.

[![](https://substackcdn.com/image/fetch/$s_!CyQO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21e6cb7b-fdb4-43c8-8520-906492280521_1578x610.png)](https://substackcdn.com/image/fetch/$s_!CyQO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21e6cb7b-fdb4-43c8-8520-906492280521_1578x610.png)

As mentioned, scaling the ClickHouse cluster (up or down) and tuning the right configurations to reduce latency or increase concurrency is extremely challenging, especially if your team doesn’t have many resources and ClickHouse experience.

The approach of leveraging a platform like Tinybird to offload the ClickHouse operational burden so the team can deliver insights faster to business users (the ultimate goal of any data project) is far more reasonable to me.

## Ingestion

### Overview

In addition to operating the underlying database infrastructure, Tinybird offers robust connectors for data ingestion. Users ingest data from Kafka, object storage, or stream HTTP payloads through the [Events API](https://www.tinybird.co/docs/forward/get-data-in/events-api).

> *Ingestion in Tinybird is managed through the datasource concept, where each datasource contains the configuration, such as the schema, the ClickHouse storage engine, and the associated connection.*
>
> [![](https://substackcdn.com/image/fetch/$s_!KuvC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F437e75a0-c6a4-4ec8-8f3d-6c7b0824d1fa_710x438.png)](https://substackcdn.com/image/fetch/$s_!KuvC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F437e75a0-c6a4-4ec8-8f3d-6c7b0824d1fa_710x438.png)
>
> *Connection is another concept in Tinybird that helps users specify the information needed to work with a physical source. For example, the Kafka connection includes bootstrap servers, the key, the secret, and other configurations.*

To help improve ingestion resource efficiency in deployments, Tinybird provides ingestion flow-control mechanisms.

[![](https://substackcdn.com/image/fetch/$s_!dspB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F684d944b-5176-40e5-8638-1d218d7d50f1_516x600.png)](https://substackcdn.com/image/fetch/$s_!dspB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F684d944b-5176-40e5-8638-1d218d7d50f1_516x600.png)

It batches incoming insertions over a short period (the flush interval) before flushing them to reduce pressure on the cluster; however, this can increase data latency.

> *The interval depends on the billing plan.*

To ensure reliability, Tinybird prevents data loss and application interruptions by gracefully handling ingestion failures. If the errors are retriable, the affected data is stored in a staging area for later re-ingestion. For non-retriable ones, Tinybird keeps the data in a special quarantine table so users can investigate later (this is like the [dead-letter queue](https://aws.amazon.com/what-is/dead-letter-queue/) (DLQ) concept commonly used in streaming systems such as Kafka)

[![](https://substackcdn.com/image/fetch/$s_!cAOW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcafe461-efd8-4a5a-a1a3-f3f8e05c5576_1034x572.png)](https://substackcdn.com/image/fetch/$s_!cAOW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcafe461-efd8-4a5a-a1a3-f3f8e05c5576_1034x572.png)

Tinybird also has backpressure mechanisms to keep the “abnormal“ ingestion source from affecting others. When a source starts to consume more resources, Tinybird automatically applies backpressure in two phases.

[![](https://substackcdn.com/image/fetch/$s_!Vt41!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ebf63dd-a84a-4f2e-bc6f-8dab49c90153_1322x844.png)](https://substackcdn.com/image/fetch/$s_!Vt41!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ebf63dd-a84a-4f2e-bc6f-8dab49c90153_1322x844.png)

First, the system delayed ingesting that source until resource consumption returned to normal. During the delay, Tinybird continuously monitors the number of delayed insertions and the age of pending insertions; if these metrics exceed a predefined threshold, the system proceeds to the next phase of backpressure, which temporarily applies rate limits oningestion for that source.

### Kafka Connector

Discussing Tinybird’s ingestion system without mentioning their Kafka Connector would be incomplete.

The Connector is a Python service that deploys one Kubernetes cluster across multiple regions. Yeah, you read it right, it's written in Python, the programming language is not usually associated with high-performance applications.

[![](https://substackcdn.com/image/fetch/$s_!Ierk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf766e96-64d0-44a2-b56d-0c1a160e630c_1298x336.png)](https://substackcdn.com/image/fetch/$s_!Ierk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf766e96-64d0-44a2-b56d-0c1a160e630c_1298x336.png)

Tinybird chose Python mostly because they already chose this language for their other backend services. They also note that the Python Global Interpreter Lock (GIL) is not a problem, since most bottlenecks are network I/O and ClickHouse's ingestion capacity. For high-performance components, they prefer native libraries that bypass the GIL, such as the confluent\_kafka C++ bindings for Kafka communication.

[![](https://substackcdn.com/image/fetch/$s_!SFaf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9615b30-9971-49f6-9db6-97c208f56608_1248x868.png)](https://substackcdn.com/image/fetch/$s_!SFaf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9615b30-9971-49f6-9db6-97c208f56608_1248x868.png)

Tinybird implements the controller/worker model for the connection, where a controller manages multiple workers. One or many workers are assigned a Kafka topic. The connector scales based on the number of worker instances assigned to a Kafka topic.

## Transformation and Serving

### The pipes

[![](https://substackcdn.com/image/fetch/$s_!kv3g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a07e30-4dd3-434a-90c9-250e3ab25a3b_1502x812.png)](https://substackcdn.com/image/fetch/$s_!kv3g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a07e30-4dd3-434a-90c9-250e3ab25a3b_1502x812.png)

In Tinybird, users will use the pipe to transform, filter, join, or aggregate the data. You can think of a pipe as a data pipeline. A pipeline can be broken into smaller parts for call nodes. Each node is a SQL query. The user can combine nodes to build a complete pipeline.

### The sink

To export data, Tinybird supports Kafka and object storage sinks. A sink is built on top of the pipe and is managed completely by Tinybird.

### The API endpoint

In a traditional stack, exposing an analytical metric to a frontend application involves a multi-step process:

[![](https://substackcdn.com/image/fetch/$s_!ddOj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F965181fc-156e-4eee-8345-6adb76570446_1376x560.png)](https://substackcdn.com/image/fetch/$s_!ddOj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F965181fc-156e-4eee-8345-6adb76570446_1376x560.png)

* Building pipelines to move data into a warehouse.
* Whenever the front-end needs the data, it must communicate with the backend via API.
* The backend queries the warehouse and returns the data for the front end.

Successfully building a real-time pipeline to extract insights is only half the story; you also need a backend server to serve the insights to the frontend or other applications. However, this is not an easy task; your backend not only exposes the API interface but must also be carefully built to meet latency/concurrency requirements.

Tinybird sees this pain and solves it.

[![](https://substackcdn.com/image/fetch/$s_!eZX0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52f5cfc3-dd26-4d8c-83cb-13baeac78dcd_1198x706.png)](https://substackcdn.com/image/fetch/$s_!eZX0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52f5cfc3-dd26-4d8c-83cb-13baeac78dcd_1198x706.png)

Endpoints are the type of Tinybird pipe that exposes the APIs for other applications to call. An endpoint allows external applications to call and pass parameters for filtering, sorting, pagination, selecting specific columns, and more. (Just like you call a traditional API endpoint)

We will make this clearer in the demo below.

> **Note:** Tinybird connections, sources, pipes, endpoints, and other objects are defined in files using a custom domain-specific language (DSL). We will look at this in more detail in the demo section. Recently, Tinybird released the [TypeScript SDK](https://www.tinybird.co/blog/tinybird-now-in-typescript) that allows users to define all Tinybird objects in TypeScript, from sources and pipes to endpoints and connections.

## Build, iterate, and deploy

In addition to managing ClickHouse, the Tinybird platform offers a robust ingestion and sink system, along with a toolkit to help users build, iterate on, and deploy their data applications.

The toolkit includes:

[![](https://substackcdn.com/image/fetch/$s_!ArkM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0132cdfb-cd8b-411a-873b-34639af8d3cd_1540x442.png)](https://substackcdn.com/image/fetch/$s_!ArkM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0132cdfb-cd8b-411a-873b-34639af8d3cd_1540x442.png)

* Tinybird CLI: A command-line tool to manage the whole data project lifecycle. The CLI can be enabled in AI-powered mode to streamline the workflow.
* Tinybird Local: a Docker container that allows users to test what they have built locally.
* Tinybird Cloud: the web interface that manages the Tinybird deployment.

Tinybird simplifies local development and production deployment. The flow will look like this:

[![](https://substackcdn.com/image/fetch/$s_!NavR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3a6d9b0-61ba-4f17-93a7-474b6e0ebbc8_1262x996.png)](https://substackcdn.com/image/fetch/$s_!NavR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3a6d9b0-61ba-4f17-93a7-474b6e0ebbc8_1262x996.png)

* You initiate a git repository to version control your data project.
* You use the CLI to set up a Docker container locally (Tinybird Local) with related components running inside, including ClickHouse.
* You use the CLI to scaffold a project to help you organize all the related Tinybird objects (e.g., datasource, pipe, connection, …) along with required CI/CD templates.
* You define the connection and source, and create pipes to develop your application. (connection and source can be created via CLI)
* Then, you test your data application by deploying it on Tinybird Local and running the test suite if needed (via CLI as well)
* When you see it ready, you can deploy your application to the Tinybird Cloud via CI/CD pipeline

---

## Let’s build a simple data application

After diving into the Tinybird platform, let's get our hands dirty a bit by writing and deploying a simple real-time data application.

> *The term “real-time data application” might be “a bit” overkill here, as I only plan to stream a few records to the Kafka topic and see what the workflow looks like in Tinybird.*
>
> *The goal of the demo is to consume data from a Kafka topic, aggregate the data, and expose it via an API endpoint. The workflow is developed and built on both Tinybird Local and Cloud (free tier).*
>
> *You can follow along; the whole demo is free, and all you need is internet and a laptop with Docker installed.*

### Sign up for a free Tinybird account

To get started, let's [sign up for the](https://www.tinybird.co/) **[free-tier](https://www.tinybird.co/)** [Tinybird account](https://www.tinybird.co/). With only a few clicks, you are good to go. To give us a feel of what Tinybird CLI can do, there will be an interactive session right on the browser, so we can type the command and run it:

[![](https://substackcdn.com/image/fetch/$s_!GSRB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36c2bb4a-f7d6-4c80-bace-713d4ef50616_1334x1286.png)](https://substackcdn.com/image/fetch/$s_!GSRB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36c2bb4a-f7d6-4c80-bace-713d4ef50616_1334x1286.png)

### Set up locally

> *You can find all these steps [here](https://www.tinybird.co/docs/forward/get-started/quick-start).*

1. We need to install Tinybird CLI on our laptop:

```
curl https://tinybird.co | sh
```

2. We create a folder and enter that folder (for the rest of the demo)

```
mkdir tinybird_demo && cd tinybird_demo
```

3. We need to log in to Tinybird. This command will redirect to the Tinybird account site on the browser

```
tb login
```

4. We start the Tinybird Local, which is a Docker container that has multiple processes, including ClickHouse. The command requires a few minutes to complete

```
tb local start
```

5. We scaffold the Tinybird project structure:

```
tb create
```

After running this command, you will have a set of required folders and files that help you get ready for the first data application:

[![](https://substackcdn.com/image/fetch/$s_!zW_a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10a2a741-f49b-44a8-ac93-0b7f2fe4bc02_286x590.png)](https://substackcdn.com/image/fetch/$s_!zW_a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10a2a741-f49b-44a8-ac93-0b7f2fe4bc02_286x590.png)

You will have the GitHub/GitLab CI/CD files, a “connections” folder to store connections (e.g., Kafka host, key, and secret), a “datasources” folder to store source definitions, and a “pipe” folder to store pipe logic.

### Kafka set up on Aiven

1. For Kafka, I chose Aiven’s free tier for this demo because of its simplicity. You can sign up by clicking “start for free“ on the [Aiven website](https://aiven.io/free-kafka). The whole process from choosing your Google account for sign up to having a Kafka service running won’t take you more than 10 minutes.

[![](https://substackcdn.com/image/fetch/$s_!cHBK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3076c124-d93b-4603-a746-b0820bb650ae_882x234.png)](https://substackcdn.com/image/fetch/$s_!cHBK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3076c124-d93b-4603-a746-b0820bb650ae_882x234.png)

Here is my Aiven Kafka service after 9.7 minutes.

2. After you have your Kafka service, create a topic called “tinybird-demo“ in the “Topic“ panel.

   [![](https://substackcdn.com/image/fetch/$s_!LeEd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f86e86a-7c65-440c-9c38-eb2fe4d82121_458x166.png)](https://substackcdn.com/image/fetch/$s_!LeEd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f86e86a-7c65-440c-9c38-eb2fe4d82121_458x166.png)
3. For this demo, make sure you enable SASL authentication for your Kafka service as described in this [guide](https://aiven.io/docs/products/kafka/howto/kafka-sasl-auth#enable-sasl-authentication). After that, open “Connection Information” in your service’s “Overview” panel, and select SASL to get the required information for the following steps.

   [![](https://substackcdn.com/image/fetch/$s_!45LZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6d7ab46-15a9-4a59-8221-3a8b3bde024f_2282x1154.png)](https://substackcdn.com/image/fetch/$s_!45LZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6d7ab46-15a9-4a59-8221-3a8b3bde024f_2282x1154.png)
4. Next, send some messages to the topic.

   First:

   ```
   python3 -m pip install kafka-python
   ```

   Then copy this code and run it to send a message with user\_id, click\_count, and country fields to our Kafka topic “tinybird-demo”.

   ```
   import json
   import time
   from kafka import KafkaProducer

   TOPIC_NAME = "tinybird-demo"
   SASL_MECHANISM = 'SCRAM-SHA-256'

   producer = KafkaProducer(
       bootstrap_servers="Copy and paste the Service URI from Connection Information",
       sasl_mechanism = SASL_MECHANISM,
       sasl_plain_username = "Copy and paste the Username from Connection Information",
       sasl_plain_password = "Copy and paste the Password from Connection Information",
       security_protocol="SASL_SSL",
       ssl_cafile="ca.pem", # Download CA certificate from Connection Information
       value_serializer=lambda v: json.dumps(v).encode("utf-8")
   )

   data = [
       {'user_id': 1, 'click_count': 3, 'country': 'US'},
       {'user_id': 2, 'click_count': 1, 'country': 'DE'},
       {'user_id': 2, 'click_count': 1, 'country': 'DE'},
       {'user_id': 1, 'click_count': 2, 'country': 'US'},
       {'user_id': 3, 'click_count': 6, 'country': 'VN'},
       {'user_id': 3, 'click_count': 4, 'country': 'VN'},
       {'user_id': 2, 'click_count': 8, 'country': 'DE'},
       {'user_id': 2, 'click_count': 12, 'country': 'DE'},
   ]

   for d in data:
       producer.send(TOPIC_NAME, value=d)
       time.sleep(1)

   producer.close()
   ```

### Create a Kafka source on Tinybird Local

Now that the Kafka service is up and running, we are ready to create the Kafka source in Tinybird Local.

1. Create Kafka connection via Tinybird CLI:

```
tb connection create kafka
```

You need to enter:

* The connection name: Enter whatever name you want
* The bootstrap server: Copy and paste the “Service URI” from the “Connection Information.”
* The Kafka key: Copy and paste the “User” from the “Connection Information.”
* The Kafka secret: Copy and paste the “Password” from the “Connection Information.”

After that, you will have a <connection-name>.connection file in the connections folder.

2. Create Kafka source

```
tb datasource create --kafka
```

It also prompts you to answer some questions, such as the source name (enter whatever name you want) or the Kafka connection (use the Kafka connection name from the previous step)

After that, you have a <source-name>.datasource in the datasources folder. Here is mine.

[![](https://substackcdn.com/image/fetch/$s_!tzZ4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd85029e8-5245-4fb9-8fd5-2eb19da9bdc8_828x406.png)](https://substackcdn.com/image/fetch/$s_!tzZ4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd85029e8-5245-4fb9-8fd5-2eb19da9bdc8_828x406.png)

As you can see, Tinybird extracts the schema from the messages we previously sent to the topic. We can also see the ClickHouse storage engine (MergeTree) and the connection name (my\_kafka) used for this data source.

3. After setting up the source, you can preview the data from the source by:

```
tb sql "select * from <your-kafka-source-name>"
```

4. Finally, you need to deploy the source to the Tinybird local:

```
tb deploy
```

### Set up an API endpoint

To expose Kafka data via API endpoints for other applications to access, we need to create an endpoint pipeline.

1. Create a file called “kafka\_expose.pipe” in the “pipes” folder.
2. Copy this content into the file

```
TOKEN token READ
TAGS click_count

NODE result
SQL >
    %
    SELECT 
     user_id,
     sum(click_count) as click_counts
    FROM <your-kafka-source-name>
    WHERE country = {{ String(country, 'US')}}
    GROUP BY 1
TYPE ENDPOINT
```

We use the TYPE ENDPOINT here to signal to Tinybird that this is an Endpoint pipe, and we use the TOKEN to indicate to the caller that this endpoint requires a token.

This pipe has a single NODE called result. The query is defined in the “SQL” section; we calculate the total click\_count for each user\_id from our Kafka source. The country filter is filled by the query parameter passed by the external caller; if the caller doesn’t specify it, the ‘US‘ value will be used.

3. We deploy the pipe to Tinybird local:

```
tb deploy
```

4. Now we can call the API to get the data. But first, let's retrieve the token to call the endpoint:

```
tb endpoint token kafka_expose
```

5. Now we can make the API via Postman with this token. The URL should follow this format

```
http://localhost:7182/v0/pipes/<endpoint_name>.<format (csv | json) >?param=value
```

In case we want the return data to be filtered to the US only and in JSON format, the URL looks like this (don’t forget to pass the token in the header):

[![](https://substackcdn.com/image/fetch/$s_!WQML!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c4a9ed1-aa53-4fd1-93f0-fef770be5d35_1004x200.png)](https://substackcdn.com/image/fetch/$s_!WQML!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c4a9ed1-aa53-4fd1-93f0-fef770be5d35_1004x200.png)

And the returned data looks like this:

[![](https://substackcdn.com/image/fetch/$s_!hD8w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa42f9d89-eb85-4af4-a7a0-4b6ff66f0f8d_578x880.png)](https://substackcdn.com/image/fetch/$s_!hD8w!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa42f9d89-eb85-4af4-a7a0-4b6ff66f0f8d_578x880.png)

Here is a video of the whole process from creating the Kafka connection, source, endpoint, to finally calling the endpoint

6. We can also make the API call via Python and convert the result to a Pandas dataframe:

```
from io import StringIO
import requests
from urllib.parse import urlencode
import pandas as pd

host = 'localhost:7182'
endpoint_name = 'kafka_expose'
format = 'csv'
token = 'PASS YOUR TOKEN HERE'
country = 'DE'
 
s = requests.Session()
s.headers['Authorization'] = f'Bearer {token}'
 
URL = f'http://{host}/v0/pipes/{endpoint_name}.{format}'
params = {'country': country}
        
r = s.get(f"{URL}?{urlencode(params)}")
df = pd.read_csv(StringIO(r.text))
print(df)
```

### Deploying to the cloud

After done with local development, we can deploy our work to the cloud:

```
tb --cloud deploy
```

---

## My thoughts

One of the biggest lessons I learned over my ~7 years as a data engineer is that delivering insights is always the number one priority. No matter how hard you manage your 10-node cluster or spend 10 hours optimizing a Spark application, if you don’t deliver the insight the business users need, your work is useless.

This is even more true when your companies require real-time analytics. You set up a ClickHouse cluster for the data processing, the Kafka connector to route data to ClickHouse, and you develop a data project.

You’re done, but wait a minute, you need to test your logic before applying it to production data. So, you create another ClickHouse for testing. Now, you can test, but how you deploy your logic to the production cluster, you have to build a CI/CD pipeline. The whole flow might need a month to build.

The use case requires the dashboard to be refreshed every 2 minutes but you need a month to prepare the infrastructure. That is only the happy case. You might need more time to tune your ClickHouse cluster to meet your company’s requirements and data volume.

—

Based on my Tinybird research, I believe the flow Kafka → ClickHouse → Insight could take just a few days, in many scenarios, to have your first MVP. That’s a huge win, given the fact that you don’t need to operate, scale, and tune the ClickHouse clusters. (Don’t forget you have two clusters in dev and prod environments)

The speed also comes from Tinybird's investment in the developer experience. The convenient CLI commands cover the entire data project lifecycle, from scaffolding the project and starting the local instance to creating a Tinybird object to test and deploying to production. The CLI can be easily integrated into CI/CD pipelines to govern testing and deployment.

If you choose ClickHouse as your real-time analytics engine but want to focus on insight delivery and a seamless developer experience rather than the hard parts, I highly recommend you try Tinybird. (It has a free tier)

---

## Outro

In this article, we first explore what real-time analytics is, then dive into ClickHouse to see how it is built to handle high-throughput ingestion and low-latency query workloads. Then we discover that self-managing ClickHouse is not easy, as the database requires deep knowledge and substantial resources to prepare it for production.

From there, we start exploring Tinybird, the real-time analytics platform that offers a managed experience for ClickHouse-based deployments, which abstracts away all the complexity. In addition, Tinybird provides a robust managed ingestion system with a high-performance Kafka connector or the Event API to let users stream API payloads to Tinybird’s underlying ClickHouse deployment.

Next, we find that Tinybird also helps with the serving side, supporting exports to Kafka and object storage, and especially exposing data via API endpoints, helping companies save resources by not building backend servers, so front-end or other applications can consume ClickHouse data.

Tinybird focuses on developer experience by offering tools such as the CLI, a local Tinybird Docker container, and a cloud Tinybird. Users can apply software engineering best practices to build, test locally, and later deploy changes via a CI/CD pipeline.

Finally, we wrap up the article with a simple Kafka-Tinybird-API Endpoint demo and some of my personal thoughts on this awesome platform.

Thank you for reading this far. See you in my next article.

---

## Reference

*[1] Javi Santana, [How to scale a real-time data platform](https://www.tinybird.co/blog/how-tinybird-scales) (2025)*

*[2] Tinybird official documentation, [Ingestion protection](https://www.tinybird.co/docs/forward/get-data-in/ingestion-protection)*

[*3] Alberto Romeu, Jordi Vilaseca Corderroure, [How we built a production Kafka connector for ClickHouse](https://www.tinybird.co/blog/clickhouse-kafka-connector) (2026)*
