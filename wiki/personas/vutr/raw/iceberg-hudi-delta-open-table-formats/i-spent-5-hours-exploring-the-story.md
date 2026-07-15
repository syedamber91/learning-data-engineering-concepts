---
title: "I spent 5 hours exploring the story behind Apache Hudi."
channel: vutr
author: "Vu Trinh"
published: 2024-10-08
url: https://vutr.substack.com/p/i-spent-5-hours-exploring-the-story
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Delta Lake", "Data Warehouse", "Data Lake", "Streaming", "Batch Processing", "ETL"]
tags: [https, hudi, auto, image, table, file]
---

# I spent 5 hours exploring the story behind Apache Hudi.

*Why did Uber create it back then? What makes Hudi different from Iceberg or Delta Lake?*

> Source: [Open post](https://vutr.substack.com/p/i-spent-5-hours-exploring-the-story)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[etl|ETL]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=149755728)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!XL_5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F580ba064-c120-4b4a-866f-c8da4c754c1c_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!XL_5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F580ba064-c120-4b4a-866f-c8da4c754c1c_2000x1429.png)

Image created by the author.

---

## Intro

After covering Iceberg and Delta Lake, I will begin learning about Hudi to gain a comprehensive view of the landscape of table formats.

This week, we'll explore the origin story and motivation behind Hudi. Why did Uber create Hudi, and what problems is it trying to solve?

---

## Why?

If you navigate to the “use case” section of Apache Hudi's official documentation, you'll find the first on the list is:

[![](https://substackcdn.com/image/fetch/$s_!W14K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67f5629c-1363-44d5-86f2-2a9a460545a7_1684x708.png)](https://substackcdn.com/image/fetch/$s_!W14K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67f5629c-1363-44d5-86f2-2a9a460545a7_1684x708.png)

Screenshot of [Apache Hudi official documentation](https://hudi.apache.org/docs/use_cases/).

Near real-time ingestion and incremental processing!

So, why was Apache Hudi designed to support these two use cases in the first place? No one can answer this better than Hudi’s creators — the engineers at Uber.

### Incremental

On their journey to build an internal data warehouse solution, Uber chose Hadoop as the core of their second-generation data platform. Unlike the first generation, where data was loaded directly into the Vertica data warehouse, raw data was now ingested into a Hadoop-based data lake.

This shift introduced a new paradigm for Uber’s Big Data platform, enabling the ingestion and storage of vast amounts of raw data from various sources without transformation during ingestion.

Doing so reduced the load on Uber’s source data stores, as data could be ingested into Hadoop in its native format without pre-processing. Once the data was in Hadoop, it could be transformed and analyzed using various tools.

However, Uber faces new challenges, including significantly high latency in data updates. Uber’s data frequently requires updates—ranging from minor adjustments (like fare changes) to more extensive backfills or revisions that span weeks or even months.

[![](https://substackcdn.com/image/fetch/$s_!HFcZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93e9ca25-ee0c-4226-9fc8-c40d3d5ae129_1568x500.png)](https://substackcdn.com/image/fetch/$s_!HFcZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93e9ca25-ee0c-4226-9fc8-c40d3d5ae129_1568x500.png)

Image created by the author.

However, since HDFS and Parquet don't natively support data updates, the data ingestion process must recreate a new snapshot and convert the entire dataset into columnar Parquet files each time. Engineers must ingest a fresh copy of the source data every 24 hours, which could take over 20 hours using 1,000+ Spark executors.

In 2015, while only around 100 gigabytes of new data were added daily per table, the ingestion job still had to process over 100 terabytes for each table, converting the entire dataset. However, as the need for fresher data grew, supporting update and delete operations on large-scale HDFS became crucial.

Similarly, ETL and modeling jobs followed a snapshot-based approach, rebuilding derived tables in every run. To reduce data latency, ETL jobs required an incremental approach—pulling only changed data from the raw source table and updating the derived output table instead of repeatedly rebuilding it every few hours.

### Near-realtime analytics

Lambda architecture separates data processing into two pipelines: batch and streaming. The batch layer periodically computes an accurate business state and updates the serving layer in bulk, while the streaming layer provides a low-latency, real-time approximation. Due to slight discrepancies between batch and streaming states, separate serving layers are required.

Kappa architecture simplifies this by using a single stream processing pipeline, where the streaming layer manages batch processing by replaying computations over the data stream. However, it still faces the challenge of managing two distinct serving layers.

Real-time serving systems are optimized for record-level updates in a row-oriented format, focusing on speed. However, most designs are unsuitable for analytical scans, which benefit from a columnar-oriented format.

[![](https://substackcdn.com/image/fetch/$s_!utGn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F023dc614-07db-4e3b-8d2a-93d25b294349_1256x792.png)](https://substackcdn.com/image/fetch/$s_!utGn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F023dc614-07db-4e3b-8d2a-93d25b294349_1256x792.png)

Figure 4: The distribution of use cases across different latencies and completeness levels at Uber. [Source](https://www.uber.com/en-SG/blog/hoodie/)

Consequently, Uber typically offloads analytics on historical data to batch query engines like Spark or Trino on HDFS, where latency is less of a concern. However, for workloads tolerating latencies of around 10 minutes, a separate “speed” serving layer is unnecessary if data ingestion and preparation in HDFS are efficient. This approach unifies the serving layer, reducing overall complexity and resource usage.

All these requirements and challenges led Uber to design Hudi, a Hadoop Upsert, Delete, and Incremental framework.

In the following sections, we will take a glimpse into Apache Hudi.

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=149755728)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

## Metadata

### hoodie.properties

Metadata files are stored in `<base_path>/.hoodie/` directory. Here, a file called hoodie.properties contains Hudi table configurations, such as table name, version, partition scheme, file format, or table type.

[![](https://substackcdn.com/image/fetch/$s_!ZRrS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17d9715b-f55a-4610-983e-57f9aad15110_1460x946.png)](https://substackcdn.com/image/fetch/$s_!ZRrS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17d9715b-f55a-4610-983e-57f9aad15110_1460x946.png)

Screenshot of the hoodie.properties

Besides hoodie.properties, metadata files record transactional actions on the table, constructing the table's Timeline.

[![](https://substackcdn.com/image/fetch/$s_!Cdb-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffac3770a-e22f-43a0-8b60-712f8ebae607_622x136.png)](https://substackcdn.com/image/fetch/$s_!Cdb-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffac3770a-e22f-43a0-8b60-712f8ebae607_622x136.png)

Screenshot of the Hudi transactional metadata files.

### Timeline

Hudi Timeline records all actions performed on the table at different `instants` of time which helps provide instantaneous views of the table while also efficiently supporting retrieval of data in the order of arrival.

[![](https://substackcdn.com/image/fetch/$s_!tVIv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa942fe10-04b8-479e-b8c1-a12a9fed4b2d_1470x614.png)](https://substackcdn.com/image/fetch/$s_!tVIv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa942fe10-04b8-479e-b8c1-a12a9fed4b2d_1470x614.png)

Image created by the author.

A Hudi instant consists of the following components. Each transactional metadata file is associated with a `instants`. The file has the following pattern:

<instant timestamp>.<instant action>[.<instant state>]

* **Instant timestamp**: Instant time is typically a timestamp (e.g., 20241004000131320 from the screenshot), which monotonically increases in the order of the instant action’s beginning time.
* I**nstant action**: Type of actions that can be performed on the table. **COMMITS** refer to an atomic write of a batch of records. **CLEANS** are background tasks that remove outdated file versions. **DELTA\_COMMIT** involves atomic writes to a MergeOnRead table, with data written to delta logs. **COMPACTION** is a background process reconciling data structures, such as converting updates from row-based logs to columnar formats, appearing as a special commit. **ROLLBACK** occurs when a commit fails, removing any partial files. Lastly, **SAVEPOINT** marks specific file groups as preserved for potential recovery, preventing their deletion by cleaners.
* **State**: At any given moment, instant action can be in one of three states: **REQUESTED**, indicating an action has been scheduled but not yet started; **INFLIGHT**, showing the action is currently in progress; and **COMPLETED**, marking the action as finished. Note: The metadata file associated with the **COMPLETED** state will have no state suffix.[​](https://hudi.apache.org/cn/docs/timeline/#active-and-archived-timeline)

Hudi manages timelines as active and archived timelines. The active timeline serves valid data files, ensuring that read requests don’t experience unnecessary latencies as the timeline grows. It is bounded by the instants (metadata files) it can serve.

[![](https://substackcdn.com/image/fetch/$s_!QW_0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F619f7620-3ffa-4724-b341-670b18e13885_1838x512.png)](https://substackcdn.com/image/fetch/$s_!QW_0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F619f7620-3ffa-4724-b341-670b18e13885_1838x512.png)

Image created by the author.

To maintain this, Hudi moves older timeline events to the archived timeline after certain thresholds. Generally, the archived timeline is not used for regular table operations but is kept for bookkeeping and debugging purposes. Any instances under the ".hoodie" directory refer to active timelines, while archived events are moved to the ".hoodie/archived" folder.

---

## Data

Hudi stores data files under partition paths for partitioned tables (like Hive) or under the base path for non-partitioned tables. These data files are categorized as Base and Log Files:

[![](https://substackcdn.com/image/fetch/$s_!-jBt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0552e5d5-3b87-49f7-827a-80d328dee5e3_1426x674.png)](https://substackcdn.com/image/fetch/$s_!-jBt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0552e5d5-3b87-49f7-827a-80d328dee5e3_1426x674.png)

Image created by the author.

* **Base Files** store the table’s records. Hudi uses a columnar-oriented file format (e.g., Parquet) for Base Files to optimize data reading.
* **Log Files** capture changes to records on top of their associated Base File. Hudi uses a row-oriented file format (e.g., Avro) for Log Files to optimize data writing.

A Hudi table is divided into multiple file groups, similar to database sharding, where each group contains a subset of the table’s data. A File Group is uniquely identified by a `fileId`, and each group contains File Slices. Each slice has a single Base File (Parquet/ORC) and associated Log Files (Avro). A slice represents a version of the group at a specific time.

[![](https://substackcdn.com/image/fetch/$s_!WzDj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83864e19-3bfb-48c0-b649-b4dd99d698dc_1306x528.png)](https://substackcdn.com/image/fetch/$s_!WzDj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83864e19-3bfb-48c0-b649-b4dd99d698dc_1306x528.png)

Image created by the author.

Hudi adopts Multiversion Concurrency Control (MVCC), where [compaction](https://hudi.apache.org/docs/next/compaction) action merges logs and base files to produce new file slices, and [cleaning](https://hudi.apache.org/docs/next/hoodie_cleaner) action removes unused/older file slices to reclaim space on the file system.

With this design, Hudi achieves:

* **Read and write efficiency**: The Base File format efficiently supports large data scans, while the row-based Log File format provides high performance for data writing.
* **Data versioning**: Each File Slice is tied to a specific timestamp on the Timeline, enabling tracking of how records within a File Group evolve.

---

## Index

Each record in a Hudi table has a unique identifier called a primary key, which consists of a pair of record keys and the partition path to which the record belongs.

> *Before Hudi version 0.14.0, users needed to explicitly specify the record key. From version 0.14.0 onward, Hudi can automatically generate record keys if they are not explicitly specified.*

Using primary keys, Hudi ensures no duplicate records (primary keys) across partitions and enables fast updates and deletes on records.

For non-partitioned tables, the primary key includes only the record key, which means Hudi enforces a record uniqueness constraint over the entire table.

Primary keys in Hudi are also referred to as "hoodie keys."

Recalling that Uber faced challenges with data updates and deletes over HDFS, Hudi introduces a feature that sets it apart from Delta Lake or Iceberg—the index.

[![](https://substackcdn.com/image/fetch/$s_!6vjO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55de7846-bc38-42fb-8ad3-14dbd5641177_1198x880.png)](https://substackcdn.com/image/fetch/$s_!6vjO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55de7846-bc38-42fb-8ad3-14dbd5641177_1198x880.png)

Image created by the author.

Hudi maintains an index to enable quick record lookups. This index maps hoodie keys to file groups (`fileIds`), and this mapping remains unchanged once the first version of a record is written to a file. You can find the Hudi-supported index type [here](https://hudi.apache.org/docs/indexing#index-types-in-hudi).

---

## Outro

In this article, we learned that Uber designed Hudi to address their need for near-real-time and incremental processing over large-scale HDFS. Hudi achieves this by embedding a “mini lambda” architecture with two data layouts supporting different purposes: row-based log files enable fast writes, while hybrid table formats like Parquet enhance read efficiency.

Now, see you in my next deep-dive blog on Hudi!

---

## Reference

*[1] Vinoth Chandar, [Hudi: Uber Engineering’s Incremental Processing Framework on Apache Hadoop](https://www.uber.com/en-SG/blog/hoodie/) (2017)*

*[2] Reza Reza, [Uber’s Big Data Platform: 100+ Petabytes with Minute Latency](https://www.uber.com/en-SG/blog/uber-big-data-platform/) (2018)*

*[3] [Hudi Official Documentation](https://hudi.apache.org/docs/overview/)*

*[4] Jack Vanlightly, [Table format comparisons - How do the table formats represent the canonical set of files?](https://jack-vanlightly.com/blog/2024/8/7/table-format-comparisons-how-do-the-table-formats-represent-the-canonical-set-of-files) (2024)*

*[5] Shiyan Xu, [Apache Hudi: From Zero To One (1/10)](https://blog.datumagic.com/p/apache-hudi-from-zero-to-one-110) (2023)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-5-hours-exploring-the-story/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
