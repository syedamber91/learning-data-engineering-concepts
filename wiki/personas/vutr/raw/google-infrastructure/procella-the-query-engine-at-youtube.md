---
title: "Procella - The query engine at YouTube"
channel: vutr
author: "Vu Trinh"
published: 2024-06-29
url: https://vutr.substack.com/p/procella-the-query-engine-at-youtube
paid: false
topics: ["Data Engineering", "BigQuery", "Streaming", "ETL"]
tags: [https, procella, query, server, auto, metadata]
---

# Procella - The query engine at YouTube

*Everything at once*

> Source: [Open post](https://vutr.substack.com/p/procella-the-query-engine-at-youtube)

## Topics

[[data-engineering|Data Engineering]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!6ST0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47808dd-158f-4d50-87ae-784c257f38b9_1399x996.png)](https://substackcdn.com/image/fetch/$s_!6ST0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47808dd-158f-4d50-87ae-784c257f38b9_1399x996.png)

Image created by the author.

---

## Table of contents

* *Context*
* *Architecture*
* *Optimization Techniques*

---

## Intro

When seeking OLAP systems to research, I found Procella, the query engine that powers the analytics demand behind YouTube. Without further ado, let’s deep dive into this engine; it will be a pretty long post.

> *This blog post is my note after reading the paper [Procella: Unifying serving and analytical data at YouTube](https://research.google/pubs/procella-unifying-serving-and-analytical-data-at-youtube/).*

---

### Context

There was increasing demand for data-driven applications at YouTube: reports and dashboards, embedded statistics in pages (no of views, likes,…), time-series monitoring, and ad-hoc analysis. Instead of building dedicated infrastructure for each use case, engineers at YouTube built a new SQL query engine – Procella. The engine is designed to address all of the four use cases above. At the time of paper writing, Procella served hundreds of billions of daily queries on YouTube.

Initially, YouTube leveraged different technologies for data processing: [Dremel](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf) for ad-hoc analytics, [Bigtable](https://cloud.google.com/bigtable?hl=en) for customer-facing dashboards, [Monarch](https://research.google/pubs/monarch-googles-planet-scale-in-memory-time-series-database/) for site health monitoring, and [Vitess](https://github.com/vitessio/vitess) for embedded statistics. However, using a dedicated tool for specific demands raises some challenges:

* There are too many ETL processes to load data to multiple systems.
* Each system has a different interface, which increases learning code and reduces usability.
* Some systems have performance and scalability issues when dealing with YouTube data.

To solve these pain points, YouTube built Procella, a new distributed query engine with a set of compelling features:

* **Rich API**: Procella supports a nearly complete implementation of standard SQL.
* **High Scalability**: Procella can achieve scalability more efficiently by separating computing and storage.
* **High Performance**: Procella uses state-of-the-art query execution techniques.
* **Data Freshness**: It supports high throughput and low latency data ingestion in batch and streaming.

The following sections describe the Procella’s architecture.

## The engine was designed to run on Google Infrastructure.

[![](https://substackcdn.com/image/fetch/$s_!-3Ko!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6b09e37-3878-432d-b28b-48b50ea0a71f_1344x960.gif)](https://substackcdn.com/image/fetch/$s_!-3Ko!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6b09e37-3878-432d-b28b-48b50ea0a71f_1344x960.gif)

Image created by the author.

### The storage

All data is stored in [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system), Google’s scalable file system. The storage has some differences when compared to the local disk:

* Data is immutable.
* Metadata operations such as listing files have higher latency than local file systems because they must communicate with Colossus’s metadata servers.
* All Colossus read or write operations can only be executed via [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call), which leads to higher cost and latency when there are many small operations.

### The compute

YouTube runs all Procella’s servers on [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/), Google’s cluster manager (imagine [Kubernetes](https://kubernetes.io/docs/concepts/overview/) here, but Borg is the internal technology at Google). Running on Borg means there are some implications:

* Borg master can often tear down machines for maintenance, upgrades, …
* A Borg cluster will have thousands of commodity machines with different hardware configurations, each with a different set of tasks with incomplete isolation. Thus, the task performance can be unpredictable. This implies that a system running on Borg must have fault-tolerance capability.

## The Data

### Data Storage

As mentioned above, the data in Procella is stored separately in Colossus. Logically, Procella organizes into tables. Each table has multiple files, which are also referred to as tablets or partitions. The engine has its columnar format, Artus, but it also supports other formats, like Capacitor (the [Dremel](https://research.google/pubs/dremel-a-decade-of-interactive-sql-analysis-at-web-scale/) query engine format).

### Metadata Storage

Procella uses lightweight secondary structures such as zone maps, bitmaps, bloom filters, partition, and sort keys. The metadata server provides this information for the root server during the query planning phase. These secondary structures are retrieved from the data file headers. Most metadata is stored in metadata stores such as [BigTable](https://cloud.google.com/bigtable?hl=en).

### Table management

Table management is achieved by sending standard DDL commands (CREATE, ALTER, etc.) to the registration server (which will be covered in upcoming sections). The user can define information like column names, data types, partitioning, sorting information, etc. Users can specify expiration time or data compact configuration with the real-time tables.

### Batch ingestion

[![](https://substackcdn.com/image/fetch/$s_!nh5F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3493d6-744c-4d12-83ec-9055bfdcda39_864x672.gif)](https://substackcdn.com/image/fetch/$s_!nh5F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe3493d6-744c-4d12-83ec-9055bfdcda39_864x672.gif)

Image created by the author.

The typical approach for processing batch data for users in Procella is using offline batch processes (e.g., MapReduce) and then registering the data by making a DDL RPC to the register server.

During the data registration phase, the register server extracts the table-to-file mapping secondary structures from file headers. Moreover, Procella also leverages data servers (covered in the upcoming sections) to generate secondary structures if the required information is not in the file headers. The register servers are also responsible for sanity checks during the data registration phase. It validates schemas’s backward compatibility, prunes, and compacts schemas…

### Realtime ingestion

[![](https://substackcdn.com/image/fetch/$s_!KmZT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff19c0db8-97e3-41eb-b4f7-e55ea6e19d46_864x672.gif)](https://substackcdn.com/image/fetch/$s_!KmZT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff19c0db8-97e3-41eb-b4f7-e55ea6e19d46_864x672.gif)

Image created by the author.

In Procella, the ingestion server is in charge of real-time data ingestion. Users can stream data into it using RPC or [PubSub](https://cloud.google.com/pubsub?utm_source=google&utm_medium=cpc&utm_campaign=japac-SG-all-en-dr-SKWS-all-all-trial-DSA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_655856181323-ADGP_Hybrid+%7C+SKWS+-+BRO+%7C+DSA+-All+Webpages-KWID_39700076131766622-aud-970366092687:dsa-1456167871416&userloc_1028581-network_g&utm_term=KW_&gad_source=1&gclid=CjwKCAjw1K-zBhBIEiwAWeCOF8oP9zyJbDKC9dK-RQnIx0qCfjrRN-pTc6_VNSZwKN5LGmEbvXx09hoCixkQAvD_BwE&gclsrc=aw.ds&hl=en). When receiving the data, the ingestion server can apply some transform to align it with the table’s structure and append it to the [write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging) in Colossus. They also send the data in parallel to the data server for real-time queries based on the data partitioning scheme. The data servers temporarily store data in the memory buffer for query processing.

Having the data flow in two parallel paths allows the data to be available to queries in near real-time while eventually being consistent with slower, durable ingestion. The queries can combine data from in-memory buffers and the on-disk tablets. Moreover, the querying-from-buffer can be turned off to ensure consistency with the trade-off of higher query latency.

### Compaction

To make data more efficient for serving, the compaction server periodically compacts and repartitions the logs written by the ingestion servers into larger partitioned columnar files. The compaction server can apply user-defined SQL-based logic specified during table registration to reduce the data size by filtering, aggregating, or keeping only the latest value.

## The Query Lifecycle

> *Let's see how the internal query flows in Procella.*

[![](https://substackcdn.com/image/fetch/$s_!uNgY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0478a685-913d-4c70-bf06-93502959e275_864x768.gif)](https://substackcdn.com/image/fetch/$s_!uNgY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0478a685-913d-4c70-bf06-93502959e275_864x768.gif)

Image created by the author.

* Clients send the SQL queries to the Root Server (RS).
* The RS performs query rewrites, parsing, planning, and optimizations to generate the execution plan.
* The RS uses metadata such as partitioning and index information from the Metadata Server (MDS) to filter out unnecessary data files.
* The RS orchestrates the query execution through the different stages.
* The RS builds the query plan as a tree composed of query blocks as nodes and data streams as edges.
* The Data Servers (DS) are responsible for physical data processing. After receiving the execution plan from the RS or another DS, the DS executes the according query plan and sends the results back to the requestor (RS or DS)
* The plan starts with the lowest DS reading source data from Colosuss or the DS’s memory buffer. The query is carried out following the plan until it is finished.
* Once the RS receives the final results, it sends the response back to the client.

The following sections describe some optimizations that are being applied to Procella.

## Caching

Procella employs multiple cache strategies to mitigate networking latency due to the separation of computing and storage:

* **Colossus metadata caching**: The file handles contain the mapping between the data blocks and the Colossus servers. Data Servers cache these handles to avoid too many file open calls to the Colossus.
* **Header caching:** The data servers cache the header information (e.g., column size and column’s min-max values) in the dedicated LRU cache.
* **Data caching:** The DS caches columnar data in a separate cache.The format Artus lets the data have the exact representation in memory and on disk, which makes it convenient to populate the cache.
* **Metadata caching:** To avoid bottlenecks due to remote calls to the metadata storage, the metadata servers cache the metadata in a local LRU cache.
* **Affinity scheduling**: Procella implements affinity scheduling to the data and metadata servers to ensure that the same data/metadata operations go to the same server. An important note is that the affinity is flexible; the request can be routed to a different server when the desired server is down. In this case, the cache hit is lower, but the query is guaranteed to be processed successfully. This property is important for high availability in Procella.

The caching strategies are designed so that when there is sufficient memory, Procella becomes an in-memory database.

## Data format

The first version of Procella used the Capacitor data format, primarily aimed at large scans typical in analysis workloads. Since Procella is designed to cover several other use cases requiring fast lookups and range scans, YouTube decided to build a new format called Artus; let's see some features of the format:

* It uses custom encoding to seek single rows without decompressing data efficiently. This makes the format more suitable for small-point lookups and range scans.
* Doing multi-pass adaptive encoding; e.g., it first passes over the data to collect lightweight information (e.g., distinct values, min, and max, etc.) and uses this information to determine the optimal encoding scheme. Besides that, Artus uses various methods to encode data, such as dictionary encoding, run-length, delta, etc.
* Artus chooses encodings that allow binary search for sorted columns, allowing fast lookups in O (logN) time.
* Instead of using representation for nested and repeated data types adopted by Capacitor and [Parquet](https://parquet.apache.org/), Artus visualizes a table’s schema as a tree of fields and stores a separate column on disk for each field.
* Artus also implements many common filtering operations inside its API, which allows computation to be pushed down to the data format, leading to significant performance gain.
* Apart from the data schema, Artus also encodes encoding information, bloom filters, and min-max values to make many standard pruning operations possible without reading the actual data.
* Artus also supports [inverted indexes](https://en.wikipedia.org/wiki/Inverted_index).

## Evaluation Engine

Many modern analytical use LLVM to compile the execution plan for native to achieve high evaluation performance. However, Procella needs to serve both analytical and high QPS demands, and for the latter, the compilation time can often affect the latency requirement. Thus, the Procella evaluation engine, Superluminal, takes a different approach:

* Using C++ template [metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming) for code generation.
* Processing data in blocks to use vectorized computation and CPU cache-aware algorithms.
* Operating directly on encoding data.
* Processing structured data in an entirely columnar fashion.
* Pushing filters down the execution plan to the scan node, allowing the system only to scan the rows required for each column independently.

> *🤓 **Fact**: Superluminal powers the [Google BigQuery BI](https://cloud.google.com/blog/products/data-analytics/demystifying-bigquery-bi-engine) and [Google BigLake](https://cloud.google.com/biglake?hl=en) processing engines.*

## Partitioning and Indexing

Procella supports multi-level partitioning and clustering. Most fact tables are partitioned by date and clustered by multiple dimensions. Dimension tables would generally be partitioned and sorted by the dimension key. This enables Procella to prune tablets that do not need to be scanned and perform co-partitioned joins, avoiding moving data around.

The metadata server is responsible for storing and retrieving partition and index information. For high scalability, MDS is implemented as a distributed service. The in-memory structures are transformed from Bigtable (the metadata store) using various encoding schemes such as prefixes, delta, or run-length encoding. This ensures that Procella can deal with a vast amount of metadata in memory efficiently.

After filtering out the unwanted tablets, the data server uses bloom filters, min/max values, and other file-level metadata to minimize disk access based on the query filters. The data servers will cache this information on the LRU cache.

## Distributed operations

### Distributed Joins

Procella has several join strategies that can be configured using hints or implicitly by the optimizer based on the layout and size of the data:

* **Broadcast**: One table side in the join operation is small enough to be loaded into the memory of each data server running the query.
* **Co-partitioned:** When fact and dimension tables are partitioned on the same join key, the data server only needs to load a small subset of the data to operate the join.
* **Shuffle**: When both tables of the join operations are large, data is shuffled on the join key to a set of intermediate servers.
* **Pipelined:** When the right side of the join is a complex query but has a high chance that it will result in a small data set, the right-size query will be executed first, and the result is sent to the servers in charge of the left-side query. In the end, this results in a broadcast-like join
* **Remote lookup:** In many cases, the dimension table is partitioned on the join key; however, the fact table is not. In such cases, the data server sends remote RPCs to the server in charge of dimension tablets to get the required keys and values for the joins.

### Addressing Tail Latency

[![](https://substackcdn.com/image/fetch/$s_!_xdE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F768cc04b-bbd8-442f-9958-0fe2f56fbdf2_984x485.png)](https://substackcdn.com/image/fetch/$s_!_xdE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F768cc04b-bbd8-442f-9958-0fe2f56fbdf2_984x485.png)

Image created by the author.

Operating on commodity-shared hardware, individual machine failures are not rare. This makes achieving low tail latency difficult. Procella has some techniques to deal with this problem:

* The root server maintains data server response latency statistics while executing a query. If a request takes longer than the median, it asks the secondary data server to come and be in charge of the request. This can be achieved thanks to the fact that data is stored in Colossus, which makes the data available for every data servers
* The root server limits the requests to the data servers currently handling heavy queries to avoid putting more burden on these servers.
* The root server decorates the priority information for each request to the data servers. Generally, smaller queries will have higher priority, and larger ones will have lower priority. The data servers maintain separate threads for high and low-priority requests. This ensures small queries respond faster, and the large query cannot slow down other queries.

### Intermediate Merging

The final aggregation often becomes the bottleneck for queries with heavy aggregations as it needs to process large amounts of data in a single node. Thus, they add an intermediate operator right before the final aggregator, which acts as a data buffer. The operator can dynamically bring additional CPU threads to perform aggregations if the final aggregator cannot keep up the data in the buffer.

## Query Optimization

### Virtual Tables

Procella supports materialized views with some additional features to ensure optimal query performance:

* **Index-aware aggregate selection:** the materialized view in Procella chooses the suitable tables based on physical data organization, such as clustering and partitioning.
* **Stitched queries**: the materialized view combines multiple tables to extract different metrics from each one using UNION ALL if they all have the dimensions in the query.
* **Lambda architecture awareness:** the materialized view combines multiple tables from batch and real-time flow using UNION ALL.
* **Join awareness**: the materialized view understands the joins and can automatically insert them in the query.

### Query Optimizer

Procella's query optimizer uses static and adaptive query optimization techniques. During the query compilation phase, they use a rule-based optimizer. At query execution time, they use adaptive techniques (dynamically changing the plan properties such as the workers needed) to optimize physical operators based on statistics of the data used in the query.

Adaptive techniques simplify the Procella system, as they do not have to collect and maintain statistics on the data beforehand, especially when Procella is ingested at a very high rate. The adaptive techniques can be applied to aggregation, join, and sorting operations.

## Serving Embedded Statistics

[![](https://substackcdn.com/image/fetch/$s_!pBT7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fe23116-8890-43cf-b767-6cdb546dfc2c_672x672.gif)](https://substackcdn.com/image/fetch/$s_!pBT7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fe23116-8890-43cf-b767-6cdb546dfc2c_672x672.gif)

Image created by the author.

Procella powers various embedded statistical counters, such as views or likes, on high-traffic pages such as YouTube channel pages. The query for these use cases is straightforward: e.g., SELECT SUM(views) FROM Table WHERE video id = X, and the data volumes are relatively small.

However, each Procella instance needs to be able to serve over a million queries per second with millisecond latency for each query. Moreover, the user-facing statistical values are being rapidly updated (view increase, the user subscribes), so the query result must be updated in near real-time. Procella solves this problem by running these instances in “stats serving” mode:

* When new data is registered, the registration server will notify the data servers so that they can load them into memory immediately.
* Instead of operating as a separate instance, the metadata server’s functionality is compiled into the Root Server to reduce the RPC communication overheads between the root and metadata server.
* The servers pre-load all metadata and asynchronously update it to avoid remotely accessing metadata at query time, which incurs higher tail latencies.
* Query plans are cached to eliminate parsing and planning overhead.
* The root server batches requests for the same key and sends them to a single pair of primary and secondary data servers. This minimizes the number of RPCs required to serve simple queries.
* The root and data server tasks are monitored so that Procella can move these tasks to other machines if there is a problem with the running machine.
* Expensive optimizations and operations are turned off to avoid overheads.

---

## Outro

Thank you for reading this far; I hope my work helps you learn more about another (real-time) OLAP system. If you are interested in systems that have some similar characteristics to Procella, you can check out my two previous articles on Apache Pinot and Apache Druid:

---

## **References**

*[1] Google, [Procella: Unifying serving and analytical data at YouTube](https://research.google/pubs/procella-unifying-serving-and-analytical-data-at-youtube/) (2019)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/procella-the-query-engine-at-youtube/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
