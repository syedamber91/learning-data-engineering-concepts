---
title: "I spent 3 hours learning the overview of ClickHouse"
channel: vutr
author: "Vu Trinh"
published: 2024-10-29
url: https://vutr.substack.com/p/i-spent-3-hours-learning-the-overview
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Iceberg", "Snowflake", "BigQuery"]
tags: [https, clickhouse, auto, image, table, query]
---

# I spent 3 hours learning the overview of ClickHouse

*The overview architecture*

> Source: [Open post](https://vutr.substack.com/p/i-spent-3-hours-learning-the-overview)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!88VX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46febe27-a3e1-4aff-92f4-80bb6969cbe5_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!88VX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46febe27-a3e1-4aff-92f4-80bb6969cbe5_2000x1429.png)

Image created by the author.

---

## Intro

This week, we’ll explore one of the most renowned OLAP systems: ClickHouse. I plan to write a dedicated article on the ClickHouse MergeTree Storage engine and include a brief overview of ClickHouse.

While researching, I realized it might be better to start with a separate article that covers ClickHouse's overview before we dive deeper into its components.

> *I reference most of the material from their [paper released on last August](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) and Clickhouse’s official documetation.*

---

## Motivation

ClickHouse is a high-performance, column-oriented SQL OLAP system that is available as an open-source solution and a cloud service. It’s designed for high-performance analytics over petabyte-scale data with exceptionally ***high ingestion rates***.

The system was initially developed internally in 2009 to power the [Yandex Metrica](https://metrica.yandex.com/) analytics platform. Yandex Metrica enables customers to create customized reports, providing real-time insights based on user hits and sessions. This often involves building complex aggregates with near real-time data.

In April 2014, Yandex Metrica tracked around 12 billion events (page views and clicks) daily, all of which needed to be stored for custom report generation. A single query might scan millions of rows within a few hundred milliseconds. ClickHouse was designed to enable these custom reports to be generated on the fly directly from non-aggregated data.

ClickHouse was open-sourced in 2016 and has since evolved into a more robust and generalized OLAP system.

[![](https://substackcdn.com/image/fetch/$s_!Cynf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d690f6b-2773-4a54-8703-4154ab5237af_1812x292.png)](https://substackcdn.com/image/fetch/$s_!Cynf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d690f6b-2773-4a54-8703-4154ab5237af_1812x292.png)

ClickHouse Development Timeline, Figure 1, [ClickHouse - Lightning Fast Analytics for Everyone](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) (2024)

ClickHouse aims to address the key challenges of modern analytical data management:

* **High ingestion rates:** Data-driven applications like web analytics, finance, and e-commerce generate large amounts of data. Analytical databases need more efficient indexing, compression, and supporting data distribution across multiple nodes. Additionally, recent data often holds more value for real-time insights than historical data. This makes it essential for databases to ingest new data at high and consistent rates—even in bursts—while processing older data efficiently. This balance ensures reporting queries run smoothly, even as data scales up, without performance slowdowns.
* **Simultaneous queries with an expectation of low latencies:** Queries typically fall into two categories: ad-hoc, like exploratory data analysis, or recurring, such as regular dashboard queries. The more interactive a query is, the lower query latencies are expected, which introduces challenges in optimization and execution. Recurring queries, however, offer a chance to tailor the database’s physical layout to fit these workloads, making pruning techniques essential for efficient data processing. Moreover, databases must allocate shared resources—CPU, memory, disk, and network I/O—based on query priority. This ensures that each query receives fair or prioritized access even under high query loads, maintaining performance across simultaneous operations.
* **Adaptability:** Modern analytical databases must be highly adaptable, allowing seamless integration with existing data architectures. This means they should readily read and write external data across various systems, locations, and formats, ensuring flexibility and compatibility within diverse environments.
* **Deployment**: Given the unreliability of commodity hardware, databases must include data replication to remain resilient against node failures. They should also be versatile enough to run on any hardware, from outdated laptops to high-powered servers.

In the next section, we will learn the architecture of Clickhouse

---

## Architecture

[![](https://substackcdn.com/image/fetch/$s_!oqY2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F508077f4-282f-4dac-ad70-562fc42084a3_1096x1054.png)](https://substackcdn.com/image/fetch/$s_!oqY2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F508077f4-282f-4dac-ad70-562fc42084a3_1096x1054.png)

Clickhouse Overall Architecture. Image created by the author. [Reference](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf)

ClickHouse, developed in C++, is split into three primary layers: query processing, storage, and integration. Additionally, an access layer manages user sessions and enables communication through various protocols. Beyond these core layers, ClickHouse includes components for threading, caching, role-based access control, backups, and continuous monitoring.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

### Query Processing Layer

The query processing layer parses incoming queries, building and optimizing logical and physical query plans and execution. ClickHouse uses a vectorized execution model (like DuckDB, BigQuery, or Snowflake) in combination with opportunistic code compilation.

[![](https://substackcdn.com/image/fetch/$s_!BQTf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd8d55cf-fb11-4a82-b94e-841ee93b087e_1368x810.png)](https://substackcdn.com/image/fetch/$s_!BQTf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd8d55cf-fb11-4a82-b94e-841ee93b087e_1368x810.png)

Vectorized Model. Image created by the author.

ClickHouse parallelizes queries at many levels of data elements, data chunks, and table shards (if a table is sharded among multiple nodes).

[![](https://substackcdn.com/image/fetch/$s_!vsvd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0121502-b618-4f8a-a5da-85aa2cb9168a_1406x764.png)](https://substackcdn.com/image/fetch/$s_!vsvd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0121502-b618-4f8a-a5da-85aa2cb9168a_1406x764.png)

Image created by the author.

* **Table shard**: Multiple nodes can scan the shards at the same time. Thanks to this, all hardware resources are fully utilized, and query processing can be scaled by adding nodes and vertically by adding cores.
* **Data Chunks**: On a single node, the query engine executes operators simultaneously in multiple threads. ClickHouse uses the vectorization model for operators to produce, pass, and consume multiple rows (data chunks) instead of single rows to minimize the overhead of virtual function calls.
* **Data Elements**: Multiple data elements can be processed within operators at once using SIMD units in a single CPU core.

### Storage Layer

[![](https://substackcdn.com/image/fetch/$s_!2rjp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181b727b-b22c-42ec-ab55-aeb38377e8bf_1232x456.png)](https://substackcdn.com/image/fetch/$s_!2rjp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181b727b-b22c-42ec-ab55-aeb38377e8bf_1232x456.png)

Image created by the author.

Unlike most OLAP databases, ClickHouse’s storage layer includes various table engines, each designed to handle data for different use cases and requirements. Table engines fall into three categories:

* The first category is the **MergeTree family** of table engines, which is the primary engine in ClickHouse: based on the idea of LSM tree tables (but not 100% the same), the table is split into horizontal, sorted portions of data, which are later continuously merged by a background process. Each MergeTree engine differs in how it merges rows from its input portions. For example, rows can be aggregated (with **AggregatingMergeTree**) or replaced (with **ReplacingMergeTree**)

[![](https://substackcdn.com/image/fetch/$s_!PkVR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94cc50c1-51ef-40aa-9f46-77472df18674_1050x604.png)](https://substackcdn.com/image/fetch/$s_!PkVR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94cc50c1-51ef-40aa-9f46-77472df18674_1050x604.png)

Image created by the author.

> *I will cover the **MergeTree** engine layer in my next article.*

* The second category includes **special-purpose table engines** designed to speed up or distribute query execution. This category features in-memory key-value table engines called dictionaries, which cache the results of queries periodically executed against internal or external data sources.
* The third category is **virtual table engines** for data exchange with external systems such as relational databases (e.g., PostgreSQL, MySQL), publish/subscribe systems (e.g., Kafka), or key/value stores (e.g., Redis). These engines can also work with data with table formats (Iceberg, DeltaLake, or Hudi) or data in object storage (e.g., AWS S3, Google GCP).

ClickHouse supports sharding and replication of a table’s data across cluster nodes. Sharding will divide a table into a subset of shards using a sharding expression. A shard can be considered a separate table; users can interact with shards directly, i.e., treat them as separate tables or use a distributed special table engine to have a consolidated view of all shards. The ultimate goal of sharding is to process a table’s data that a single machine can not handle.

Another use of sharding is distributing the read-write load for a table over multiple nodes. Moreover, a shard can be replicated across nodes for fault tolerance. Clickhouse provides a corresponding **ReplicatedMergeTree engine** for each MergeTree table engine.

The ReplicatedMergeTree uses a multi-master coordination scheme based on the Raft consensus, implemented by ClickHouse Keeper (a C++ replacement for Apache Zookeeper), to ensure that each shard consistently maintains a configurable number of replicas.

### Integration Layer

There are two approaches to making external data available in an OLAP database: push-based and pull-based. In the push-based approach, a third-party component pushes data from external sources into the database. In the pull-based model, the database connects to remote data sources and pulls data into the system. ClickHouse uses the pull-based data integration method.

* **External Connectivity**: Clickhouse provides 50+ integration table functions and engines for connectivity with external systems and storage locations, including MySQL, PostgreSQL, Kafka, Hive, or S3/GCP/Azure object stores.
* **Data Format:** ClickHouse supports over 90 formats, including CSV, JSON, Parquet, Avro, ORC, Arrow, and Protobuf. Some analytics-oriented formats, like Parquet, are integrated with query processing so that the query optimizer can leverage embedded Parquet statistics, enabling filters to be evaluated directly on compressed data.
* **Compatibility interfaces**: Clients can interact with ClickHouse through MySQL- or PostgreSQL-compatible wire-protocol interfaces. This compatibility is useful for enabling access from applications where vendors have not yet implemented native ClickHouse connectivity.

---

## Outro

That's all for this week.

In this article, we've covered the motivation behind ClickHouse, its architecture, and an overview of the storage engine's query processing layer.

With this foundational knowledge in place, I'll see you in my next blog, where we'll explore the MergeTree Table Engine.

---

## Reference

*[1] Ryadh Dahimene, Alexey Milovidov, [ClickHouse - Lightning Fast Analytics for Everyone](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) (2024)*

*[2] [ClickHouse Official Documentation](https://clickhouse.com/docs/en/intro)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-3-hours-learning-the-overview/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
