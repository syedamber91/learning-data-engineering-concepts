---
title: "I spent 6 hours learning how Google serves analytics applications "
channel: vutr
author: "Vu Trinh"
published: 2025-04-30
url: https://vutr.substack.com/p/i-spent-6-hours-learn-how-google
paid: false
topics: ["Data Engineering", "Snowflake", "Databricks", "BigQuery", "Data Warehouse"]
tags: [https, auto, napa, media, good, substackcdn]
---

# I spent 6 hours learning how Google serves analytics applications 

*10GBs/ s throughput and sub-milliseconds query latency*

> Source: [Open post](https://vutr.substack.com/p/i-spent-6-hours-learn-how-google)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]]

---

> *I’m making my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned. Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!lXHb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9248d129-4c43-4dc0-9ffd-c30d35db1af4_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!lXHb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9248d129-4c43-4dc0-9ffd-c30d35db1af4_2000x1428.png)

---

## Intro

When it comes to “big data”, it’s hard not to mention Google.

From [MapReduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf), [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf), to [BigTable](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf).

As the business evolves, Google must continuously innovate to adapt to more data requirements. They built [Spanner](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) for transactional workload and [Dremel](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf) for analytics workload. The latter is the core component of Google BigQuery, the service you might be more familiar with.

Google operates multiple services with more than a billion users worldwide. They extract insights from data produced by these services to provide better user experiences and improve quality.

[![](https://substackcdn.com/image/fetch/$s_!-wU7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2e764b1-b03d-4113-a541-c6e670cbd661_624x556.png)](https://substackcdn.com/image/fetch/$s_!-wU7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2e764b1-b03d-4113-a541-c6e670cbd661_624x556.png)

Services operating users interact with this data through analytical interfaces to gain insights. To answer the user's questions, the system must process vast amounts of data and provide the results within a rigorous time constraint. Some queries must even be returned in milliseconds.

In addition to internal analytics use, Google needs to serve user-facing analytics demands with intensive requirements in terms of performance and data freshness.

This article will explore Napa, the Google warehouse system behind these analytics use cases.

---

## Background

Before exploring Napa in detail, it would be helpful to understand the typical workloads the system is trying to serve. As mentioned, Napa doesn’t handle the same workloads you and I usually discuss when we discuss a data warehouse system.

Systems like Snowflake or Databricks usually receive batches of historical data from other systems, although these vendors support real-time ingestion. We typically expect a cloud data warehouse to help us extract insights by processing a large amount of data; we can tolerate the results provided after a few minutes and rarely need milliseconds of performance. Even if we need it, we can’t achieve it due to the characteristics of the workload: scanning a massive amount of data that needs to be aggregated and joined from many tables.

However, Napa typically serves a different type of workload. It is still analytical but less complicated (i.e, fewer joins, …), requires more high-throughput data ingestion, high data freshness, and lower response time. Data usually flows to Napa from Google services with billions of users, and the end users of Napa usually require fast analytics results to operate these services properly.

[![](https://substackcdn.com/image/fetch/$s_!ZPWI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F341bed4b-b0d2-41f9-bf4a-f42557c52449_736x310.png)](https://substackcdn.com/image/fetch/$s_!ZPWI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F341bed4b-b0d2-41f9-bf4a-f42557c52449_736x310.png)

In my opinion, Napa is closer to systems like [Apache Pinot](https://pinot.apache.org/) or [Apache Druid](https://druid.apache.org/), which are positioned as real-time OLAP.

---

## Requirement

Based on those typical workloads, it’s not a surprise that Napa must provide:

* **Robust Query Performance**: The queries must have low latency performance and low variance in latency regardless of the query and data ingestion load.
* **High-throughput Data Ingestion**: All Napa functions must handle heavy ingestion loads.

The third requirement is very exciting: **flexibility**. Google observed that Napa’s clients make a three-way tradeoff between data freshness, resource costs, and query performance. Some need data results to be highly fresh and are willing to pay more for that, while some clients can tolerate low query performance to save cost.

[![](https://substackcdn.com/image/fetch/$s_!Fs9B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0ec769b-23e8-452e-bf87-40dd0de84b6c_412x340.png)](https://substackcdn.com/image/fetch/$s_!Fs9B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0ec769b-23e8-452e-bf87-40dd0de84b6c_412x340.png)

To see how Napa can adapt to these requirements. Let’s explore its architecture.

---

## Architecture

The Napa conceptual design consists of three main blocks: ingestion, storage, and serving. Each was designed to handle its responsibility independently, which is essential for helping Napa adapt to clients’ flexible needs. We will revisit this point in the “Choose the trade-off sections.”

[![](https://substackcdn.com/image/fetch/$s_!NZq2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc0242ef-c743-4ed4-811e-f196a7f8a16d_1098x344.png)](https://substackcdn.com/image/fetch/$s_!NZq2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc0242ef-c743-4ed4-811e-f196a7f8a16d_1098x344.png)

Napa leverages existing Google infrastructure components. It uses [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system) to store data, [Spanner](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) for functions that require strict transaction semantics, such as metadata management, and [F1 Query](https://research.google/pubs/f1-query-declarative-querying-at-scale/) for data serving. Napa has a control plan to coordinate work among the sub-services.

To optimize for its primary workload, Napa uses materialized views as the main technique to maximize query performance.

[![](https://substackcdn.com/image/fetch/$s_!QJiP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13cdb705-2c90-42ed-9a42-5ead7eacf9bf_856x386.png)](https://substackcdn.com/image/fetch/$s_!QJiP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13cdb705-2c90-42ed-9a42-5ead7eacf9bf_856x386.png)

This is different from systems like Snowflake or Databricks, which rely on the ability to efficiently prune unnecessary data (e.g., using a min-max index like the one in Parquet). Napa’s materialized views are sorted, indexed, and range-partitioned by primary key(s).

Napa implements LSM-trees for its storage engine to achieve high data ingestion throughput.

We will discuss these technical designs in more detail in the following sections.

---

## Ingestion

The goal of the ingestion component is straightforward: insert large volumes of data into Napa’s storage. It accepts data, performs some lightweight transformation, and writes data (e.g., successfully writes to disk or replicates to other data centers).

[![](https://substackcdn.com/image/fetch/$s_!vC1y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b3d1b0a-1e1a-4a53-a95b-bf1bfeed4859_640x436.png)](https://substackcdn.com/image/fetch/$s_!vC1y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b3d1b0a-1e1a-4a53-a95b-bf1bfeed4859_640x436.png)

Napa allows users to increase or decrease the number of data ingestion workers.

---

## Storage

This block's main responsibility is to store the data, and because materialized views are used to boost query performance, it is also in charge of view maintenance.

[![](https://substackcdn.com/image/fetch/$s_!Nd4G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffd0c991-bdca-4c45-b626-62aec468d705_782x340.png)](https://substackcdn.com/image/fetch/$s_!Nd4G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffd0c991-bdca-4c45-b626-62aec468d705_782x340.png)

Google employed two important technical designs for storage. First, Napa used **two file formats**: The write-optimized (WO) format serves high-throughput data writing, and the read-optimized (RO) format is designed for efficient data reading.

Second, Napa uses the **LSM-tree** (Log-Structured Merge-Tree) paradigm to handle table and view maintenance.

[![](https://substackcdn.com/image/fetch/$s_!mDUe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f67c887-3dd9-44a1-b44e-0f94e315011c_936x592.png)](https://substackcdn.com/image/fetch/$s_!mDUe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f67c887-3dd9-44a1-b44e-0f94e315011c_936x592.png)

LSM-trees employ an *append-only* strategy optimized for write throughput; writes are buffered in an in-memory component (memtable) and periodically flushed to disk as immutable, sorted segments (SSTables). It relies on a background *compaction* process to merge these segments, reconcile updates/deletes, and maintain sorted order across levels, thus converting random writes into sequential disk I/O at the cost of potentially higher read amplification (checking multiple segments) and write amplification (during compaction).

The other paradigm you might be more familiar with is B-trees. These are mutable, page-oriented structures that perform updates in place, meaning writes (inserts, updates, deletes) navigate the tree to find the specific disk page containing the relevant key range and modify it directly. This often incurs random I/O, potentially triggering page splits or merges to maintain balance.

> *I will not deep dive into LSM-trees or B-trees here because those could require dedicated articles. So, see you in my future articles for these topics.*

Back in Napa, the data is ingested into the WO format. These files might not be immediately available for reading because they can impact the query performance. Later, the data in WO format will be converted into RO format. The RO format shares some characteristics with the PAX file format, which can be found in Parquet, BigQuery, or Snowflake’s file format. The WO-RO conversion or merging multiple small RO files process is implemented via the LSM trees compaction process.

The LSM tree relies heavily on the compaction process, which improves query performance and reduces storage consumption by

* Sorting records based on key(s) to allow binary search.
* Aggregating multiple updates to the duplicate rows to avoid jumping around to find all the updates. Because in LSM-tree, deletes and updates are treated as inserts, there is a high chance that updates for a single record are scattered across multiple files. This differs from B-tree, where data is updated in-place, so fragmentation is not a concern like in LSM-tree.

Because data is sorted in each segment, compaction is essentially merge sorting. Napa applies the compaction process for both table and materialized view updates. A note here is that the process of aggregating updates for records can also happen at the serving times if the LSM compaction process can not handle it before the query engine processes this data for the query.

---

## Serving

For many Napa clients, obtaining query results within milliseconds is critical for their business use cases. Google has employed many techniques for Napa to achieve this:

* As mentioned, Napa aggressively leverages materialized views. Napa uses views to answer a query whenever possible instead of the base tables.

  [![](https://substackcdn.com/image/fetch/$s_!cdZB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d6b1d6d-fd80-482d-bfe2-c20f4947c3f7_732x370.png)](https://substackcdn.com/image/fetch/$s_!cdZB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d6b1d6d-fd80-482d-bfe2-c20f4947c3f7_732x370.png)
* Filters are pushed down to the storage layer to minimize the data transferred via the network.

  [![](https://substackcdn.com/image/fetch/$s_!Aoip!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28d87d8d-7cb1-4800-8a51-5312c8be1c0d_508x194.png)](https://substackcdn.com/image/fetch/$s_!Aoip!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28d87d8d-7cb1-4800-8a51-5312c8be1c0d_508x194.png)
* Napa also relies on parallelism to reduce the data each subquery has to read. Each segment in the LSM-tree keeps a local index. Napa uses this index to partition an input query into thousands of subqueries that satisfy the filters.

  [![](https://substackcdn.com/image/fetch/$s_!Gm4P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F630b07fb-da09-4e68-8f47-924eead04375_774x394.png)](https://substackcdn.com/image/fetch/$s_!Gm4P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F630b07fb-da09-4e68-8f47-924eead04375_774x394.png)

* Napa maintains two cache layers to limit disk accesses: the first is the local RAM of the workers who process the query, and the second is the distributed caching layer, which can be shared between workers.

  [![](https://substackcdn.com/image/fetch/$s_!3up3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cd96585-8a89-4d09-8dec-62cc563b8ddc_484x456.png)](https://substackcdn.com/image/fetch/$s_!3up3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cd96585-8a89-4d09-8dec-62cc563b8ddc_484x456.png)
* Napa also prefetches data to reduce the number of disk accesses further.

  [![](https://substackcdn.com/image/fetch/$s_!4fpH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bf9849d-153d-496e-98e6-b94bc40f6887_488x328.png)](https://substackcdn.com/image/fetch/$s_!4fpH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bf9849d-153d-496e-98e6-b94bc40f6887_488x328.png)
* The systems combine small I/Os as much as possible to improve the efficiency.

  [![](https://substackcdn.com/image/fetch/$s_!GW7m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3e8dab6-40d7-4d4f-b99b-70cd0e6eb4bd_488x296.png)](https://substackcdn.com/image/fetch/$s_!GW7m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3e8dab6-40d7-4d4f-b99b-70cd0e6eb4bd_488x296.png)

---

## Choose the trade-off

As mentioned, Napa allows users to trade off one of performance, freshness, or cost to achieve the remaining two dimensions. Let's first understand how Napa could achieve each dimension:

* **High Freshness**: As mentioned above, data written in WO format is not available immediately. If users need fresher data, Napa must speed up the conversion/compacting of the newly written data to serve it faster. There are cases when the query requires files that should be merged during the background compaction process; however, for some reason (e.g., fewer resources for the compaction), these files are still not merged at the query time, and the merge must be executed at runtime instead to ensure the freshness requirement.
* **Higher Performance**: Napa maintains more views to speed up query performance. More views mean more workers are needed to update them. Another requirement is to optimize the data's physical layout; too many small files can harm performance. Also, the query performance would be degraded because the file merge process could be executed at runtime instead.
* **Low Cost**: The system's resources can be roughly categorized into these workloads: compaction process, View maintenance, and Data Ingestion. The less the resource is used, the lower the cost.

Giving the decouple architecture of Napa, tuning to optimize for two dimensions, and sacrificing the remaining is straightforward:

* If the client wants to **sacrifice data freshness** for **moderate** **query performance and cost**, Napa can maintain a moderate number of views and fewer files to merge at query execution time. It uses fewer workers and cheaper resources (like spot VM instances from AWS or GCP) for view maintenance to keep costs low. Thus, the view maintenance occurs more slowly; hence, the data is not so fresh. However, clients still get pretty good query performance and keep the resource cost down.

  [![](https://substackcdn.com/image/fetch/$s_!IdPI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87e437a1-621e-4750-8304-713ed60c4fd2_1060x310.png)](https://substackcdn.com/image/fetch/$s_!IdPI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87e437a1-621e-4750-8304-713ed60c4fd2_1060x310.png)
* If the client wants to **sacrifice query performance** for **high data freshness and low cost**, Napa can maintain fewer materialized views but allow more files to be merged during the query runtime. Napa coordinates more workers for the ingestion process because the view maintenance effort is low. That said, clients can get fresher data results with the trade-off for the query performance because the query engine has fewer materialized views for reference, plus it has to merge more files at execution time.

  [![](https://substackcdn.com/image/fetch/$s_!Vz_k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d98712a-7cad-4256-a107-a18e7e864258_678x226.png)](https://substackcdn.com/image/fetch/$s_!Vz_k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d98712a-7cad-4256-a107-a18e7e864258_678x226.png)
* If the client can tolerate **high resource cost**s for both **good query performance** and **high data freshness**, Napa can direct more workers to ingestion, data compaction, and the view maintenance process. The data will be ingested with higher throughput, data in the LSM-tree will be merged faster, and the materialized view will get updates more frequently, thus the clients will have the desired query performance and data freshness. In return, the resource cost will be relatively high.

  [![](https://substackcdn.com/image/fetch/$s_!7Qs4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2474cefc-09ac-45cf-8303-95e77dc690ab_838x366.png)](https://substackcdn.com/image/fetch/$s_!7Qs4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2474cefc-09ac-45cf-8303-95e77dc690ab_838x366.png)

---

## Outro

Thank you for reading this far.

In this article, we learn the motivation behind Napa and the requirements it must adapt to. We then explore the system's architecture and the technical designs that Google made to make Napa a highly scalable, high-throughput, robust, and extremely flexible system.

It’s not hard to point out the shared characteristics between Napa and other analytics systems:

* [Vortex, the BigQuery storage engine](https://open.substack.com/pub/vutr/p/how-does-vortex-the-bigquery-storage?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false), also has two file formats to serve data write and read separately. The system also uses LSM-tree to manage table data like Napa did.
* Clickhouse uses an [LSM-tree-like mechanism](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-the-clickhouse?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false) to achieve high throughput data for the MergeTreeEngine.
* [Apache Hudi](https://open.substack.com/pub/vutr/p/i-spent-5-hours-exploring-the-story?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false) also has two file formats.
* The new player table format, [Apache Paimon](https://paimon.apache.org/docs/master/primary-key-table/overview/#lsm-trees), adopts an LSM tree for the file storage.
* RisingWave with its LSM storage engine, [Hummock](https://risingwave.com/blog/hummock-a-storage-engine-designed-for-stream-processing/)
* …

All these systems are designed for high-throughput data writing and low-latency query performance. The case of Vortex is more special because Google decided to build Vortex for BigQuery after years of operation, when they wanted to offer real-time analytics for users, and concluded that the legacy batch storage engine couldn’t provide what they needed.

I think we will see more systems like this in the near future, given that real-time analytics data is getting more and more attention.

What do you think about this observation?

—

Now, see you in my next articles!

---

## Reference

*[1] Google, [Napa: Powering Scalable Data Warehousing with Robust Query Performance at Google](https://research.google/pubs/napa-powering-scalable-data-warehousing-with-robust-query-performance-at-google/) (2021)*

*[2] Jagan Sankaranarayanan, [Google Napa: Scalable Data Warehousing with Robust Query Performance](https://www.youtube.com/watch?v=dtWwUWB5JyQ) (2021)*
