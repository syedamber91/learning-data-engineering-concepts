---
title: "I spent 5 hours learning how Google lets us build a Lakehouse."
channel: vutr
author: "Vu Trinh"
published: 2024-09-24
url: https://vutr.substack.com/p/i-spent-5-hours-learning-how-google
paid: false
topics: ["Data Engineering", "Apache Spark", "Apache Iceberg", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming"]
tags: [https, auto, bigquery, storage, image, biglake]
---

# I spent 5 hours learning how Google lets us build a Lakehouse.

*The Google Cloud BigLake*

> Source: [Open post](https://vutr.substack.com/p/i-spent-5-hours-learning-how-google)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!FCeF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53bd18cc-a186-4adb-bc70-d6aa689ae3da_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!FCeF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53bd18cc-a186-4adb-bc70-d6aa689ae3da_2000x1429.png)

Image created by the author.

---

## Intro

As I recently discussed on LinkedIn, large-scale cloud OLAP is steadily converging toward the lakehouse paradigm. Regardless of your cloud data warehouse solution, it’s now possible to query data directly from object storage. However, the support of format and governance features depends on our solution.

This week, we will explore how BigQuery — the enterprise data warehouse solution- evolved into a uniform lakehouse solution.

First, let’s revisit the overall architecture of BigQuery.

---

## BigQuery architecture

[![](https://substackcdn.com/image/fetch/$s_!RsmB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4b872d4-2c4d-45c1-9f3d-85711297b933_1390x1078.png)](https://substackcdn.com/image/fetch/$s_!RsmB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4b872d4-2c4d-45c1-9f3d-85711297b933_1390x1078.png)

Image created by the auhor.

BigQuery separates computing, storage, and shuffle, allowing each system component to be scaled and enhanced independently.

This architecture makes it easier for BigQuery to adapt to customers’ needs, especially with the Lakehouse solution, which requires bringing the query engine closer to the data storage. BigQuery’s processing engine—Dremel—was designed to be operated on remote storage (Colossus); thus, this flexibility is a powerful advantage when Google Cloud embarks on the Lakehouse journey.

In addition, to offer more interoperability for the user, Google developed BigQuery’s managed storage so that not only their proprietary engine can access the data, but third-party engines like Spark and Trino can access the managed storage via Google’s performant Read and Write API.

We will explore these APIs in the following section.

---

## Storage API

At first, users need to load data into BigQuery’s managed storage before it can be used for queries. The data is then stored in Google’s proprietary format, Capacitor. In other direction, when users need to use their chosen query engine (e.g., Spark, Trino) over these data, they must export the data into GCS so that this engine can read and process it.

[![](https://substackcdn.com/image/fetch/$s_!y8tc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F476f21a1-99b6-459b-866a-d198c216dd2b_456x442.png)](https://substackcdn.com/image/fetch/$s_!y8tc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F476f21a1-99b6-459b-866a-d198c216dd2b_456x442.png)

Image created by the author.

Google developed the Storage API for BigQuery to remove these limitations and let external query engines, such as BigQuery’s internal query engine, Dremel, access data in the managed storage. This API includes two services: Read API and Write API.

### Read API

[![](https://substackcdn.com/image/fetch/$s_!L67x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6073eb95-a5eb-43ab-b7f8-bc171c4cf4ab_244x204.png)](https://substackcdn.com/image/fetch/$s_!L67x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6073eb95-a5eb-43ab-b7f8-bc171c4cf4ab_244x204.png)

Image created by the author.

This API offers a powerful way to access BigQuery-managed storage and BigLake tables (covered later). Built on a gRPC-based protocol, it uses efficient binary serialization. It supports multiple streams for parallel data reads, which is ideal for external analytics engines like Apache Spark or Trino. It also includes a governance layer with column- and row-level access control, filter pushdown, and column projection for efficient data reads.

[![](https://substackcdn.com/image/fetch/$s_!W31N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe47bee88-1ec1-44f8-9c94-9427f8572c31_488x369.png)](https://substackcdn.com/image/fetch/$s_!W31N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe47bee88-1ec1-44f8-9c94-9427f8572c31_488x369.png)

Image created by the author.

The Read API process begins by creating a read session through. Users specify the number of streams, snapshot time, columns to return, and a filter predicate in the request. The response includes stream identifiers, a reference schema, and an expiration time of at least 6 hours. The data is split across multiple streams, requiring the user to read from all streams to capture the entire dataset.

Each stream transmits blocks of serialized row data. Reading can be resumed from a specific row offset if an error occurs. The API also supports dynamic work rebalancing by splitting streams into child streams, ensuring more flexible data processing.

Row blocks received from the API must be deserialized using either Apache Avro or Apache Arrow formats. A reference schema provided at session creation ensures consistency across streams, allowing for long-lived decoders that can be reused throughout the session. Sessions expire automatically and don’t require manual cleanup.

The Read API integrates Superluminal, a high-performance C++ library that executes GoogleSQL expressions and operators using vectorized processing.

> ***Superluminal** is the evalutaion engine of Procella, the OLAP system behind YoutTube. I’ve already writen an arcticle about Procella, you can find it here:*

This enables efficient columnar scans, applies user predicates and security filters, and handles data masking. The results are transcoded into Apache Arrow, allowing fast query execution and interoperability across different engines.

### Write API

[![](https://substackcdn.com/image/fetch/$s_!LH3E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48dd4b25-4eb7-4eb7-b440-cf8552e0dc40_236x200.png)](https://substackcdn.com/image/fetch/$s_!LH3E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48dd4b25-4eb7-4eb7-b440-cf8552e0dc40_236x200.png)

Image created by the author.

This API provides scalable, high-speed, high-volume streaming data ingestion into BigQuery-managed storage with support for multiple streams, “exactly once” delivery semantics, stream-level, cross-stream transactions, and a gRPC-based wire protocol. It offers different writing modes to accommodate desired processing semantics (real-time streaming or batch commit) and commit guarantees.

[![](https://substackcdn.com/image/fetch/$s_!I7OZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1bff9f-d600-4e53-8d87-79911414ba83_506x106.png)](https://substackcdn.com/image/fetch/$s_!I7OZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc1bff9f-d600-4e53-8d87-79911414ba83_506x106.png)

Image created by the author.

The core abstraction in the Write API is the stream, which allows data to be written to a table. Multiple streams can write to the same table concurrently.

Next, we’ll explore the BigLake table, an enhancement to BigQuery that offers first-class support for managing tables in formats like Parquet and Apache Iceberg.

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## BigLake

[![](https://substackcdn.com/image/fetch/$s_!7_4F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbde1538c-db0a-4032-a2c4-04605e90e9b5_928x562.png)](https://substackcdn.com/image/fetch/$s_!7_4F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbde1538c-db0a-4032-a2c4-04605e90e9b5_928x562.png)

Image created by the author.

In the past, BigQuery-supported querying data on object storage was implemented via read-only external tables. As customers demand the lakehouse solution, Google introduced the BigLake table in 2022. This feature ensures the following requirements:

* The deployments should offer the same enterprise data management capabilities as BigQuery, regardless of where the data is stored.
* These features should be accessible to other data lake analytics engines like Spark and Presto/Trino.
* Customers seek a unified platform that solves complex data management issues across different storage (e.g., BigQuery storage, object storage) and analytics tools (e.g., BigQuery engine, Spark, Trino)

BigLake is added to the list of BigQuery’s components to provide the managed lakehouse solution. Two key ideas behind BigLake tables are: First, they made external open-source data lake tables first-class concerns in BigQuery, leveraging the internal BigQuery catalog as the source of truth instead of those metadata files from Iceberg of Parquet. Second, these tables offer enterprise functionality to the broader analytics engine through the Read/Write APIs

### Access Model

In general, when reading data in object storage, the query engines must forward user credentials to the object store for access authorization, but this approach doesn't work for BigLake tables.

* First, credential forwarding gives users direct access to raw data, bypassing fine-grained controls from BigQuery like data masking or row-level security.

* Second, BigLake tables also need access to storage other than the object storage to perform operations like metadata cache refreshes or data reclustering.

[![](https://substackcdn.com/image/fetch/$s_!uV99!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdde16074-69ac-4833-b2fa-945b1422f5f1_762x302.png)](https://substackcdn.com/image/fetch/$s_!uV99!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdde16074-69ac-4833-b2fa-945b1422f5f1_762x302.png)

Image created by the author.

Instead, BigLake uses a delegated access model, where users associate a connection object with each table. This object includes a service account credential with read-only permission from the object store. The connection will handle queries and background maintenance. Users can reuse the same connection object for multiple tables, often one per data lake.

### Security

BigLake tables provide fine-grained access controls independent of storage or query engines:

* The delegated access model lets Google enforce column security, data masking, and row-level filtering using the same implementation for data in object stores or BigQuery-managed storage.
* Furthermore, BigLake offers a robust security model where the Read API establishes a security trust boundary and applies fine-grained access controls before data is returned to the query engine, with zero trust granted to the query engine.

### Performance Boost

BigLake tables support metadata caching to accelerate query performance. Google uses the internal metadata management system called BigMetdata for BigLake. BigQuery also leverages this system to manage all metadata for its native table.

With the help of Big Metadata, BigLake tables cache file names, partitioning information, and physical metadata from data files, such as physical size, row counts, and per-file column-level statistics in a **columnar** cache.

Regarding metadata granularity, the cache tracks metadata in more detail than other systems like Hive Metastore. The metadata collected in the metadata management layer enables BigQuery or other engines, such as Apache Spark, to build optimized high-performance query plans. (The more detail the metadata, the more opportunity for optimization)

[![](https://substackcdn.com/image/fetch/$s_!pMLS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc54d75d7-e7f5-44b9-98ee-ead212dda1e1_1046x720.png)](https://substackcdn.com/image/fetch/$s_!pMLS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc54d75d7-e7f5-44b9-98ee-ead212dda1e1_1046x720.png)

Figure 3: Performance acceleration for open-source data lake tables. [BigLake: BigQuery’s Evolution toward a Multi-Cloud Lakehouse](https://storage.googleapis.com/gweb-research2023-media/pubtools/7808.pdf) (2024)

**An important point to note**: BigLake tables still rely on the metadata management mechanism of open table formats like Iceberg, which stores metadata alongside the data in object storage. BigLake only supports caching (after it first reads the metadata from the object storage) and centralizing this metadata, reducing the need for BigQuery or Storage APIs to list files excessively from the object storage.

### Accelerating Spark Performance over Storage APIs

Based on Google's observation, many BigQuery customers use Spark besides the BigQuery engine. Thanks to the Storage API, the Spark engine can read and write BigLake tables in the most performant way.

The open-source Spark BigQuery Connector integrates the storage APIs with Spark [DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html) using Spark’s DataSourceV2 interface.

The Spark driver creates the read API session during query planning to get a list of read streams. During execution, Spark executors perform a parallel read of the streams. The read API returns the rows in the Apache Arrow columnar data, and Spark’s native support for Apache Arrow minimizes memory copies.

[![](https://substackcdn.com/image/fetch/$s_!y_vo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a68ddd-6f75-4826-991d-ef22dfce14c9_1114x906.png)](https://substackcdn.com/image/fetch/$s_!y_vo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a68ddd-6f75-4826-991d-ef22dfce14c9_1114x906.png)

Image created by the author.

Their ultimate goal was for customers using Spark against BigLake tables to get similar price performance compared to the process using Spark directly on the Parquet data from GCS.

Google's initial implementation of Parquet scans in the read API reused Dremel's row-oriented Parquet reader, translating the rows into Superluminal's columnar in-memory format. This process was inefficient because Parquet columns needed to be pivoted into rows and back into Arrow columnar batches.

To solve this, Google developed a vectorized Parquet reader that directly outputs Superluminal columnar batches from Parquet files. Since Superluminal can work directly with the dictionary and run-length encoded data, reading from Parquet files is much more efficient.

### BigLake Managed Tables

Unlike the BigLake table, which lets the open table format like Iceberg or Delta Lake control the metadata, BigLake managed tables (BLMTs) manage 100% of the metadata. Data is stored in Parquet, while metadata is stored and managed using Big Metadata.

[![](https://substackcdn.com/image/fetch/$s_!zvle!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e0acd03-c885-4fb7-9d74-a6b2e2adedee_1102x566.png)](https://substackcdn.com/image/fetch/$s_!zvle!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e0acd03-c885-4fb7-9d74-a6b2e2adedee_1102x566.png)

Image created by the author

BLMTs support DML, high-throughput data ingestion through the Write API, and behind-the-scenes storage optimizations such as adaptive file sizing, reclustering, or garbage collection.

BLMT differs from open table formats such as Iceberg and Delta Lake in some aspects:

* Committing metadata atomically to an object store does not limit them. However, since object stores can only update or replace an object a few times per second, this limits the number of mutations we can perform per second.
* The transaction log is stored alongside the data in open table formats, allowing a malicious writer to manipulate it and rewrite its history.

Instead, BLMT uses Big Metadata as the metadata source-of-truth. This offers several advantages:

* **Write throughput:** BigMetadata is powered by a stateful service that caches the tail of the transaction log in memory. BigMetadata periodically converts the transaction log to a columnar layout for read efficiency. During queries, Dremel, the BigQuery engine, reads the columnar data and reconciles them with the tail. Combining in-memory state and columnar baselines allows table mutations at a rate much higher than possible with open table formats without sacrificing read performance.

> *Regarding BigMetadata, I've already written an article about this metadata management, you can find it here:*

* **Multi-table transactions:** Using Big Metadata enables BLMT to support multi-table transactions, which are currently unsupported in open table formats.
* **Robust security model**: Since writers cannot directly mutate the transaction log, the table metadata has a reliable audit history.

---

## Outro

Thank you for reading this far! In this article, we explored how Google provides customers with approaches to building a Lakehouse solution, from BigLake tables and extended support for open formats like Iceberg to the Storage API that allows other analytics engines to access data in BigQuery's native storage or BigLake tables. Finally, we got to dive into BigLake Managed Tables, which offer the fully managed experience of BigQuery tables for data stored in object storage."

Now, see you in the next article.

---

## Reference

*[1] Google, [BigLake: BigQuery’s Evolution toward a Multi-Cloud Lakehouse](https://research.google/pubs/biglake-bigquerys-evolution-toward-a-multi-cloud-lakehouse/) (2024)*

*[2] BigQuery Official Document, [Use the BigQuery Storage Read API to read table data](https://cloud.google.com/bigquery/docs/reference/storage)*

*[3] BigQuery Official Document, [Introduction to the BigQuery Storage Write API](https://cloud.google.com/bigquery/docs/write-api)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-5-hours-learning-how-google/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
