---
title: "I spent 5 hours understanding more about the Delta Lake table format"
channel: vutr
author: "Vu Trinh"
published: 2024-05-04
url: https://vutr.substack.com/p/i-spent-5-hours-to-understand-more
paid: false
topics: ["Data Engineering", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming"]
tags: [delta, object, https, table, objects, lake]
---

# I spent 5 hours understanding more about the Delta Lake table format

*All insights from the paper: Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores*

> Source: [Open post](https://vutr.substack.com/p/i-spent-5-hours-to-understand-more)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!Zctr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a996301-764e-4ddf-811b-31eff8e5ba7f_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!Zctr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a996301-764e-4ddf-811b-31eff8e5ba7f_1400x1000.png)

Image created by the author.

---

## Table of contents:

* *Context*
* *Motivation*
* *Delta Lake Storage Format*
* *Access Protocols*
* *Higher-level data management features*
* *Observations from Performance Experiments*

---

## Intro

Thanks to [my effort to check if “Lakehouse“ is just a marketing term](https://open.substack.com/pub/vutr/p/do-we-need-the-lakehouse-architecture?r=2rj6sg&utm_campaign=post&utm_medium=web), I learned about the metadata layer on top of the Data Lake, which aims to bring the management feature from the Data Warehouse directly into the [lake](https://en.wikipedia.org/wiki/Data_lake). Delta Lake, Apache Iceberg, and Apache Hudi are big players in this field. This week, we will deep-dive into the general principle design of one of the popular formats right now: Delta Lake.

> ***Note**: this week’s blog is my note on [Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf) in 2020, so it might not cover Delta Lake’s new features recently or try to compare any table formats. Please give me feedback if you think I missed something in this blog. One more thing to note is that I’ve never used any of these Lakehouse formats in my daily tasks, so this is my first experience researching a table format; correct me if I’m too naive at some point. :d*

---

## Context

In the rise of the cloud era, cloud object storage like Amazon S3 or Google Cloud Storage started to replace the HDFS file for the Data Lake implementation. Its advantages include theoretically unlimited scale, pay-as-you-go billing, durability, and reliability. As a result, many organizations now use cloud object stores to manage large structured datasets in data warehouses and data lakes. Popular open-source systems, including Apache Spark or Presto, support reading and writing to cloud object stores using file formats such as Apache Parquet and ORC. Cloud services, including Google BigQuery and Redshift Spectrum, can also query directly against these systems and these open file formats.

Still, object storage has shortcomings when putting it into the Lakehouse context, which requires data warehouse capabilities right on top of the Datalake. Most cloud object storages are implemented as key-value stores, making achieving ACID transactions and high performance challenging: operations such as listing objects are expensive, and consistency guarantees are limited.

Assume we store relational data natively in the cloud object storage. We logically considered each table to be stored as a set of Parquet file objects; this approach creates correctness and performance challenges for more complex workloads:

* There is no isolation between queries: if a query needs to update multiple objects in the table, consumers will see partial updates as the query updates each object individually.
* If an update query fails in the middle, the table is corrupted.
* Metadata operations are expensive in large tables with millions of objects. (e.g., list)

To address these challenges, Databricks designed [Delta Lake](https://delta.io/), an ACID table storage layer on cloud object storage that was served to their customers in 2017 and open-sourced in 2019. The core idea of Delta Lake is straightforward:

> *Maintain information about which objects belong to a Delta table in an ACID manner, using a write-ahead log in the cloud object store. The objects are encoded in Parquet, making it easy to write connectors from engines that can process Parquet.*

This design allows clients to update multiple objects simultaneously, replace a set of objects with another, etc., in a [serializable](https://en.wikipedia.org/wiki/Serialization) manner while still achieving high read and write performance as reading raw Parquet. The log also contains metadata such as min/max statistics for each data file, enabling faster metadata search operations than traditional object listing operations. Delta Lake’s transactional design enables Databricks to other features unsupported in traditional cloud data lakes, such as Time Travel, UPSERT, DELETE and MERGE operations, Caching, Layout optimization, Schema Evolution, and audit logging. All of these improve the data management and query performance of working with data in the cloud object storages; this allows for the more efficient Lakehouse architecture, which combines the key features of data lake and warehouse. Databricks’s customers could replace the architecture that separates data lakes, data warehouses, and streaming storage systems with Delta tables that provide appropriate features for all these use cases.

[![](https://substackcdn.com/image/fetch/$s_!toj7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa91de3d6-799f-486b-9e36-aaab6942c5cf_1147x1076.png)](https://substackcdn.com/image/fetch/$s_!toj7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa91de3d6-799f-486b-9e36-aaab6942c5cf_1147x1076.png)

Image created by the author.

In the following section, we will learn Databricks’s motivation behind developing the Delta Lake format.

---

## Motivation

We will examine the cloud object storage API and performance based on Databricks' observations to understand why implementing efficient ***table*** storage using existing cloud object storage can be challenging.

### Object Store APIs

Cloud object stores implement a key-value store aiming for excellent scalability. They allow users to create buckets that store multiple objects; each is a [binary blob](https://en.wikipedia.org/wiki/Binary_blob). The system uses a string key to identify the object. Object storages do not have the directory abstraction like file systems; the object’s path you see, for example, “/data/country=us/date=2024-04-27/object\_name,” is just the whole key to identify the object. The system also provides metadata APIs, such as [S3’s LIST](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) operation, that can list the objects in a bucket by lexicographic order of key, given a start key; this makes it possible to list the objects in a “directory” by starting a LIST request at the key that represents that directory prefix (e.g., “/data/country=us”). These APIs are typically expensive and have high latency: following the paper, S3’s LIST only returns up to 1000 keys per call, and each call takes tens to hundreds of milliseconds, so it can take minutes to list a table that contains millions of objects.

### Consistency Properties

The major cloud object stores support eventual consistency for each object’s key but not across keys. This characteristic raises some challenges when handling a table consisting of multiple objects. It is customary in these systems that after a client operates on an object (load, update), other clients are not guaranteed to see the result in LIST or read operations immediately.

> ***Note**: Because of the object’s immutability, an update in the object storage requires creating a whole new object*

The consistency model differs by the cloud provider. For example, Google Cloud Storage provides [strong global consistency](https://cloud.google.com/storage/docs/consistency) for the following operations: read-after-write, Read-after-metadata-update, Read-after-delete, Bucket listing, and Object listing. Different cloud object storages will offer various levels of consistency based on the operation, but all cloud storage systems lack support for atomic operations across keys.

### Performance

From the Databricks experiences, they found that achieving high throughput with object stores requires a balance of large sequential I/Os and parallelism:

* *For reads, each sequential read operation usually takes at least 5–10 ms of latency and can read data at roughly 50–100 MB/s. Hence, it must read at least several hundred kilobytes to achieve at least half the peak throughput for sequential reads and multiple megabytes to approach the peak throughput. Moreover, on typical Cloud Virtual Machine configurations, applications must run multiple reads in parallel to maximize throughput because it have higher network bandwidth.*
* *LIST operations also require significant parallelism to list large sets of objects quickly. For example, S3’s LIST operations can only return up to 1000 objects per request and take tens to hundreds of milliseconds, so clients need to request hundreds of LISTs in parallel to list large buckets or “directories.” Databricks sometimes parallelize LIST operations over the worker nodes in the Spark cluster and threads in the driver node to make the operations faster.*
* *Write operations must replace a whole object. This means that if a table is expected and updates in the future, its objects should be small to avoid expensive large file rewriting operations.*

Because of these characteristics, analytics workloads that are stored in cloud object storage should consider the following points:

* *Organizing data sequentially close to each other. The columnar format can help with this.*
* *Making objects large enough. Too large objects make updating data too expensive.*
* *Avoiding LIST operations. If there are cases that need these operations, make them request lexicographic key ranges.*

### Existing Approaches

Three popular approaches are used to handle relational data in the object storage at the time of paper writing:

* **Directories of Files:** Storing the table as a collection of objects using a columnar format like Parquet. The objects are organized into partition directories, for example, */data/country=us/date=2024-04-27/object\_name* for data in the 2024-04-27 partition. This logical partition reduces the cost of LIST operations and reads for queries requiring only a few partitions’s data. The approach originated in [Apache Hive](https://hive.apache.org/) on HDFS. Despite the simplicity, the approach has challenges, such as no atomicity across multiple objects, poor performance, and no warehouse management feature.
* **Custom Storage Engines:** This approach manages objects' metadata in a strongly consistent service. Cloud data warehouses like Snowflake or Google BigQuery employ this approach. These storage engines treat object storage as a dumb block device and implement standard techniques for efficient metadata operations over cloud objects. This approach is tied to service providers like Snowflake or BigQuery.
* **Metadata in Object Stores**. Delta Lake’s approach is to store the transaction log and metadata directly in the cloud object store and use a set of protocols over object store operations to achieve serializability. It stores table data in Parquet format, making it convenient to access from any software that supports Parquet.

After understanding Databricks's motivation behind Delta Lake, the following sections will describe its storage format, access protocols, and transaction isolation levels in detail.

## Delta Lake Storage Format

A Delta Lake table is the cloud object storage directory or file system that consists of the table’s data objects and a log of transaction operations.

[![](https://substackcdn.com/image/fetch/$s_!_rIK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87846ac4-9488-44f0-bc41-897afae27764_1502x1020.png)](https://substackcdn.com/image/fetch/$s_!_rIK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87846ac4-9488-44f0-bc41-897afae27764_1502x1020.png)

Objects stored in a sample Delta table. Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores (2020). [Source](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf)

### Data Object

The data in a table is stored in Apache Parquet objects, which can be organized into directories using [Hive’s partition](https://delta.io/blog/pros-cons-hive-style-partionining/) convention. Parquet is one of the most famous columnar formats currently available. It supports various compression schemes and can handle nested data types for semi-structured data. Moreover, the format has already been integrated with many engines, simplifying the connector development process for Databricks. Delta Lake identifies which object belongs to which table’s version using the transaction log.

### Transaction Log

The Delta table directory has a sub-directory called `_delta_log` to the transaction log. The log is a sequence of JSON objects with increasing, zero-padded numerical IDs (e.g., 000003) to store the log records and checkpoints for summarizing the log up to that point in Parquet format. Each log record object has a series of actions to apply to the previous version of the table to generate the next one. The available actions are:

* ***Change metadata**: The* `metaData` *action changes the table's current metadata. The first version of the table must contain a* `metaData` *action. Subsequent* `metaData` *actions completely overwrite the current metadata. The metadata is a data structure containing the schema, partition column names, the data files’ format, and other configuration options.*
* ***Add or Remove Files:** The* `add` *and remove actions modify the data in a table by adding or removing individual data objects. The table’s objects are determined as the number of all added objects that have not been removed. The client can use* `add` *action to include data statistics such as per-column min/max values or null counts. The action will replace any previous statistic version with the latest version. The removal action contains a timestamp to indicate when it occurred. The data objects are deleted after a retention time threshold. A* `remove` *action remains in the log, and any log checkpoints are a tombstone until the deletion of the underlying data objects.*
* ***Protocol Evolution**: The protocol action is used to increase the version of the Delta protocol.*
* ***Add Provenance Information**.: Each log record object can include provenance information in a* `commitInfo` *action.*
* ***Update Application Transaction IDs**: Delta Lake also provides a way for an application to ingest its data inside log records, which can help implement end-to-end transactional applications. For example, if the streaming job fails, it must know its previous writes in the table to replay the process starting at the correct stream’s offset. Delta Lake allows applications to write a custom* `txn` *action with* `appId` *and version fields in the log record objects that can track application information, such as the offset in the input stream in the example.*

### Log Checkpoints

Delta Lakes compresses the log periodically into the Parquet checkpoint files to achieve better performance. Checkpoints store all the non-redundant actions up to a specific log ID. Some sets of actions are redundant and can be discarded:

* `Add` *actions are followed by* `remove` *actions for the same data object. The* `add` *can be removed because the data object is no longer part of the table. The* `remove` *actions should be kept as tombstones according to the table’s data retention configuration.*

* *Multiple adds for the same object can be replaced by the last one.*
* *Multiple* `txn` *actions from the same* `appId` *can be replaced by the latest one, which contains its latest version field.*
* *The* `changeMetadata` *and protocol actions can also be merged to keep only the latest metadata.*

In the end, the checkpoints are the Parquet, which contains `add` records for objects still in the table and `remove` records for objects marked deleted but kept until the retention period expired. There are also a few records of actions like `txn`, protocol, and changeMetadata. This Parquet file is ideal for querying a table’s metadata. Databricks observed that using a Delta Lake checkpoint to find the objects is always faster than LIST operations. One more thing to note is that clients must efficiently find the last checkpoint without looping through all the objects in the `_delta_log` directory. To deal with this, Checkpoint writers write their new checkpoint ID in the `_delta_log/_last_checkpoint`.

---

## Access Protocols

Despite the object store’s eventual consistency guarantees, Delta Lake’s access protocols let clients achieve serializable transactions using only operations on the object store.

### Reading from Tables

[![](https://substackcdn.com/image/fetch/$s_!Unbf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14b82908-0951-4c72-83d6-aa614bf4721f_566x783.png)](https://substackcdn.com/image/fetch/$s_!Unbf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14b82908-0951-4c72-83d6-aa614bf4721f_566x783.png)

Image created by the author.

The read-only transactions have five steps:

* Read the `_last_checkpoint` object in the table’s log directory.
* It issues a LIST operation to find newer JSON and parquet files in the log directory. The start key for the operation is the last checkpoint if it exists or zero in case it is not present. This provides a file list that can reconstruct the table’s state starting from a recent checkpoint.
* Use the checkpoint and subsequent log records identified in the previous step to reconstruct the state of the table, which is the set of data objects and their associated data statistics. Databricks designed the Delta Lake format for parallel runs; for example, a Spark connector reads the checkpoint Parquet file and logs using Spark jobs.
* Identifying data objects needed for the read query using the statistics.
* Reading the necessary data objects in parallel. Due to the cloud object stores’ eventual consistency, some worker nodes may not query objects that the query planner found in the log; this can be handled by simply retrying after a short time.

Databricks noted that this protocol is designed to ensure consistency at each step. For example, if a client reads a stale version of the \_last\_checkpoint file, it can still find newer log files in the subsequent LIST operation and reconstruct the most recent table’s snapshot.

### Write Transactions

[![](https://substackcdn.com/image/fetch/$s_!5N3a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d211c33-7255-4414-9ba3-1fe61a92a506_577x780.png)](https://substackcdn.com/image/fetch/$s_!5N3a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d211c33-7255-4414-9ba3-1fe61a92a506_577x780.png)

Image created by the author.

The data write transactions generally have up to five steps:

* Identifying a recent log record ID using steps 1–2 of the read protocol. For convenience, we call this *current\_version.*
* Reading the data at *current\_version.*
* Write new data objects into the correct data directories, generating the object names using GUIDs. This step can be processed in parallel.
* If no other client has written this object, it attempts to write the transaction’s log record for the newly added objects into the *current\_version + 1* log object. This process needs to be atomic. If the step fails, the transaction can be retried.
* Optionally writing a new checkpoint for log record *current\_version + 1*. Then, after this write is complete, update the \_last\_checkpoint file to point to checkpoint r + 1.

As mentioned, the adding log record step (step 4) needs to be atomic; only one client should succeed in creating the object with that name. Databricks were able to implement this step for different storage systems:

* They use existing atomic put-if-absent operations from Google Cloud Storage and Azure Blob Store.
* On distributed filesystems such as HDFS, they use atomic renames to rename a temporary file to the target name or fail if it already exists.
* With Amazon S3, Databricks uses a separate coordination service to ensure that only one client can add a record with each log ID. This service is only needed for log write operations, so the workload is not too enormous. For example, the open-source connector for Apache Spark ensures the writes from the same Spark driver program will have different log record IDs using in-memory state, which means the users can make concurrent operations on a Delta table in a single Spark cluster. Moreover, they provide an API for the LogStore class customization. This lets users use other coordination mechanisms if they require.

### Available Isolation Levels

At the time of the paper's writing, Delta Lake only supported transactions in one table. All the write transactions are serializable, leading to a serial schedule that increases the order of log IDs. Read transactions can achieve snapshot isolation or serializability. The read protocol described above only reads a snapshot of the table; clients using this protocol will achieve snapshot isolation. Clients requiring serializable reading can issue a read-write transaction that performs a dummy write to accomplish this. In practice, Delta Lake connector implementations cache the latest accessed log record IDs for each table in memory, so clients will “read their own writes” even if they use snapshot isolation for reads.

### Transaction Rates

Delta Lake’s write transaction rate is constrained by the latency of the put-if-absent operations described in step 4 of the write protocol above. In practice, the latency of writes to object stores can be tens to hundreds of milliseconds, limiting the write transaction rate to several transactions per second. Databricks found that this rate is sufficient for all current Delta Lake applications: highly parallel stream ingestion jobs (e.g., Spark Streaming jobs) for the write processes that can batch many new data objects into a transaction. Databricks allows for LogStore class customization that could provide significantly faster commit times in cases that require higher rates. Read transactions at the snapshot isolation level create no contention because they only read objects in the object store, so any number of these can run concurrently.

The following sections describe higher-level data management features, similar to many traditional analytical DBMSs.

## Time Travel and Rollbacks

[![](https://substackcdn.com/image/fetch/$s_!nc4R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdba86212-629f-44cf-ac35-6c9d221d904f_784x469.png)](https://substackcdn.com/image/fetch/$s_!nc4R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdba86212-629f-44cf-ac35-6c9d221d904f_784x469.png)

Image created by the author.

Because of Delta Lake’s data objects and log immutability, it’s easy to query a snapshot of the data in the past with the MVCC implementations. A client reads the table state using an older log record ID. Delta Lake lets users configure a data retention interval for each table to facilitate time travel. It supports reading table snapshots using timestamp or commit\_id. Clients can also find which commit ID they read or wrote through Delta Lake’s API. Besides that, [Databricks also developed the CLONE command to create a copy of an existing Delta Lake table at a specific version.](https://docs.databricks.com/en/delta/clone.html)

## Efficient UPSERT, DELETE and MERGE

[![](https://substackcdn.com/image/fetch/$s_!a5sL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6078c4c-d11a-4f9d-a3ad-2e014066ed89_553x567.png)](https://substackcdn.com/image/fetch/$s_!a5sL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6078c4c-d11a-4f9d-a3ad-2e014066ed89_553x567.png)

Image created by the author.

Originally, updating Parquet files on S3 without blocking concurrent readers was difficult. The system must also process updated jobs carefully because a failure will leave the table partially updated. With Delta Lake, all these operations can be executed transactionally; the `add` and `remove` records in the log files will reflect the table’s updating. Delta Lake supports standard SQL UPSERT, DELETE, and MERGE syntax.

## Streaming Ingest and Consumption

[![](https://substackcdn.com/image/fetch/$s_!fgIf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ea52b0c-d9e3-4a26-9e88-9420499721b6_1171x570.png)](https://substackcdn.com/image/fetch/$s_!fgIf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ea52b0c-d9e3-4a26-9e88-9420499721b6_1171x570.png)

Image created by the author.

The system can treat the Delta Lake log as the message queue. This removes the need for the dedicated message buses in many cases. The log supports the streaming pipelines with the following features:

* **Write Compaction**: Streaming producers typically write data into small objects for faster ingest performance. Still, the small files slow down the consumer side because they need to process too many small objects. Delta Lake lets users run a background process that compacts small data objects transactionally without affecting readers.
* **Exactly-Once Streaming Writes:** As described in the “Write Transactions” section, writers can leverage the `txn` action to track which data was written into a Delta Lake table to implement “exactly-once” writes.
* **Efficient Log Tailing:** Delta Lake effectively allows users to query new-arrival data; the naming convention of the .json log objects with lexicographically increasing IDs is the key here. It makes the consumers efficiently run the LIST operations starting at the last log record ID to discover new logs. It is also easy for a streaming application to stop and restart at the same log record in a Delta Lake table by remembering the last record ID it finished processing.

## Data Layout Optimization

[![](https://substackcdn.com/image/fetch/$s_!GLV_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f2e1329-b9d6-476c-93f0-27e572661997_907x574.png)](https://substackcdn.com/image/fetch/$s_!GLV_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f2e1329-b9d6-476c-93f0-27e572661997_907x574.png)

Image created by the author.

Delta Lake can support a variety of layout optimizations without affecting concurrent operations because it updates the data structures that represent a table transactionally. From this advantage, Databricks implements various physical layout optimization:

* **OPTIMIZE command:** Users can leverage the [OPTIMIZE command](https://docs.databricks.com/en/sql/language-manual/delta-optimize.html) on a table to compact small objects without affecting executing transactions. This operation will make each data object 1 GB in size by default, and Databricks allows users to customize this target size.
* **Z-Ordering by Multiple Attributes:** [Delta Lake supports reorganizing](https://docs.databricks.com/en/delta/data-skipping.html#what-is-z-ordering) the records in a table in [Z-order](https://en.wikipedia.org/wiki/Z-order) for a given set of attributes to achieve locality along multiple dimensions (related data stored close together). Z-ordering works with data statistics to make the queries read less data. For more detail, Z-ordering will tend to make each data object contain a small range of the possible values in each chosen attribute so that the scanning data process can skip more data objects.
* **Auto Optimize:** Users can set the AUTO OPTIMIZE property on the table to have Databricks’s cloud service automatically handle the compact process for newly written data.

## Caching

[![](https://substackcdn.com/image/fetch/$s_!JtaK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08780e4f-ba83-48e8-a0ba-4091afbf7a60_979x572.png)](https://substackcdn.com/image/fetch/$s_!JtaK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08780e4f-ba83-48e8-a0ba-4091afbf7a60_979x572.png)

Image created by the author.

Databricks built a feature to cache Delta Lake data and log objects on clusters, accelerating tables’ data and metadata operations. Caching is safe because the data and log objects are immutable.

## Audit Logging

Delta Lake’s transaction logs can be used for audit logging based on `commitInfo` records. Users can view the history of a Delta Lake table using the [DESCRIBE HISTORY command](https://docs.databricks.com/en/sql/language-manual/delta-describe-history.html).

## Schema Evolution and Enforcement

Delta Lake can perform schema changes transactionally and update the physical objects to follow the schema change if needed (e.g., delete a column that no longer needs to be retained). Keeping a history of schema updates in the transaction log can also allow using older objects without rewriting them for specific schema changes. Moreover, Delta clients ensure that newly written data follows the table’s schema.

---

## Observations from Performance Experiments

> *This section will present Databricks’s observations of some of their Delta Lake performance experiments; the details of the experiments are in section 6 of the paper.*

* ***Impact of Many Objects or Partitions:** Databricks Runtime with Delta Lake significantly outperforms the other systems. Hive takes more than an hour to find the objects in a table with only 10,000 partitions, while Presto takes more than an hour to deal with 100,000 partitions. Databricks Runtime listing Parquet files completes in 450 seconds with 100,000 partitions, mainly because they have optimized it to run LIST requests in parallel across the cluster.*
* ***Impact of Z-Ordering:** Z-ordering by all four columns allows skipping at least 43% of the Parquet objects for queries in each dimension and 54% on average if we assume that queries in each dimension are equally likely.*
* ***TPC-DS Performance:** To evaluate Delta Lake's end-to-end performance on a standard DBMS benchmark, Databricks ran the TPC-DS power test Databricks Runtime with Delta Lake and Parquet file formats and on the Spark and Presto implementations in a popular cloud service. They see that Databricks Runtime with Delta Lake outperforms all the other configurations.*
* ***Write Performance:** They observed that Spark’s performance writing to Delta Lake is similar to writing to Parquet, showing that statistics collection does not add a significant overhead over the other data loading work.*

---

## Outro

If you had asked me one year ago what an open table format like Delta Lake was used for, I would have shrugged and replied, “I don’t know. “ But after learning a little bit about the Delta Lake format, I have to say it’s a fascinating tool that not only offers the capability to gap the two worlds of lake and warehouse but also has valuable technical knowledge derived from its implementation and design. This makes me curious about other table formats like Iceberg or Hudi. Should I write a blog about one of them?

Now, it’s time to say goodbye, see you next week.

---

## **References**

[1] Databricks, [Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf), (2020)

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-5-hours-to-understand-more/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
