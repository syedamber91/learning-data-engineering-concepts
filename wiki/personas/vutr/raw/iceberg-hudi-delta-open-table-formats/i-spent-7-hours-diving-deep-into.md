---
title: "I spent 7 hours diving deep into Apache Iceberg"
channel: vutr
author: "Vu Trinh"
published: 2024-08-31
url: https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg"]
tags: [https, auto, files, file, image, table]
---

# I spent 7 hours diving deep into Apache Iceberg

*The more details on how everything works*

> Source: [Open post](https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=148187380)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!T9hK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2646a4e1-60b7-4d71-bb93-1a730b028ae7_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!T9hK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2646a4e1-60b7-4d71-bb93-1a730b028ae7_2000x1429.png)

Image created by the author.

---

## Intro

After writing about the Apache Iceberg file format overview in this [article](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-apache-iceberg?r=2rj6sg&utm_campaign=post&utm_medium=web), I decided to spend more time understanding its internals. This article includes all the lessons I learned after hours of reading books and experimenting with this file format using PySpark, PyIceberg, and the Nessie Catalog.

We will revisit the overview of Iceberg in the following sections.

## Data Layer

[![](https://substackcdn.com/image/fetch/$s_!haSk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ad798bb-99a2-4dd7-8e5a-496efebdd61c_661x351.png)](https://substackcdn.com/image/fetch/$s_!haSk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ad798bb-99a2-4dd7-8e5a-496efebdd61c_661x351.png)

Image created by the author.

This layer contains the actual table’s data and includes data and deleted files (present if the merge-on-read mode is chosen; more on this later). The data files store the table's records, while the delete files track rows that have been removed.

Apache Iceberg supports several file formats, including Apache Parquet, Apache ORC, and Apache Avro. In practice, Apache Parquet is the most commonly used format. I will use Parquet in the rest of this article when we go into the details of the Iceberg.

## Metadata Layer

[![](https://substackcdn.com/image/fetch/$s_!fOe2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb791d7cb-6764-4677-9f0f-dc2196c76725_464x574.png)](https://substackcdn.com/image/fetch/$s_!fOe2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb791d7cb-6764-4677-9f0f-dc2196c76725_464x574.png)

Image created by the author.

Iceberg organizes metadata as the tree architecture; the highest is the metadata files, then comes to the manifest lists, and the final is the manifest files. The metadata layer is crucial for managing large datasets and enabling key features like time travel and schema evolution.

### Manifest Files

[![](https://substackcdn.com/image/fetch/$s_!DLT_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed3c9826-27a4-47dd-9717-e9933e54a2ed_1360x1526.png)](https://substackcdn.com/image/fetch/$s_!DLT_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed3c9826-27a4-47dd-9717-e9933e54a2ed_1360x1526.png)

An example of a manifest file. Created by the author with the help of carbon.now.sh

Manifest files keep track of data and delete files, as well as additional details and statistics about each file, such as the file format, the partition scheme, and the min/max, count, and null values for a data file’s columns.

In the Parquet file, some of these statistics are stored in the data files themselves (min/max of each column chunk); the reader has to open each Parquet file’s footer to find the needed statistic.

However, in Iceberge, a single manifest file stores these statistics for multiple Parquet data files, which means the reader only needs to open a single file to read the statistics for all the files tracked by this manifest file. This removes the need to open many data files and improves the read performance.

The engine records these statistics during the write operation.

### Manifest Lists

[![](https://substackcdn.com/image/fetch/$s_!ZPZQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e9e6a10-6380-4447-b40a-81d259f12c41_1360x1154.png)](https://substackcdn.com/image/fetch/$s_!ZPZQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e9e6a10-6380-4447-b40a-81d259f12c41_1360x1154.png)

An example of a manifest list. Created by the author with the help of carbon.now.sh

Each Iceberg table snapshot is associated with a manifest list. It contains an array of structs. Each array's element keeps track of a single manifest file and includes information such as:

* The manifest file’s location
* The partition this manifest file belongs to
* The upper and lower bounds of the non-null partition field values are calculated across the data files tracked by this manifest file.

### Metadata files

[![](https://substackcdn.com/image/fetch/$s_!oevU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa40cbc06-ed55-43f3-a85b-23750a9d8f39_1360x1004.png)](https://substackcdn.com/image/fetch/$s_!oevU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa40cbc06-ed55-43f3-a85b-23750a9d8f39_1360x1004.png)

An example of a metadata file. Created by the author with the help of carbon.now.sh

These files store the Iceberg table’s metadata at a specific time, including information such as

* The last sequence number tracks the order of snapshots in a table. This number is increased whenever the table changes.
* The table update timestamp.
* The table’s base location determines where to store data, manifests, and table metadata.
* The table’s schema
* The partition specification
* Which snapshot is the current one
* All snapshot information and its associated manifest lists.

## The Catalog

All the requests must be routed through the catalog, which holds the current metadata pointer for each table. The catalog stores the location of both the current and previous metadata files, ensuring that the reader always accesses the most up-to-date information.

A critical requirement for an Iceberg catalog is supporting atomic operations when updating the metadata pointer. This ensures that all readers and writers interact with the table's consistent state at a particular time.

The following sections describe the details of Iceberge's read/write operations.

## The write operation

[![](https://substackcdn.com/image/fetch/$s_!dHaC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff717704f-65ff-4a76-a830-2064e056f763_1136x812.png)](https://substackcdn.com/image/fetch/$s_!dHaC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff717704f-65ff-4a76-a830-2064e056f763_1136x812.png)

The write operation. Image created by the author.

* When writing new data to the existing Iceberge table, the writer visits the catalog to get the current metadata file location. The writer read this file to understand the table's current schema and partition scheme to prepare for the later data writing.
* After learning about these two pieces of information, the writer writes new data files following the partition scheme.
* Then, the writer creates according to manifest files in Avro format. A manifest file contains the data file location plus the file’s statistics, such as the upper and lower bounds of a column and the null value counts. The writer computes the statistics during the writing process.
* Next, the writer creates the manifest list to keep track of the manifest files. This file contains the manifest files’ location, the number of data files/rows added or deleted, the lower and upper bounds of the partition columns, etc.
* Next, it writes the new metadata file with the latest snapshots and all previous snapshots. This file includes the table base location, manifest list location, snapshot ID, sequence number, updated timestamp, etc. The writer also marks the newly created snapshot as the current snapshot.
* Finally, the writer updates the catalog's current pointer point to the newly created metadata file.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=148187380)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## The read operation

[![](https://substackcdn.com/image/fetch/$s_!CCqd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2ccb917-105d-4b4c-88c9-7dd4e7aa9a4b_1134x795.png)](https://substackcdn.com/image/fetch/$s_!CCqd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2ccb917-105d-4b4c-88c9-7dd4e7aa9a4b_1134x795.png)

The read operation. Image created by the author.

* The reader first visits the catalog to find the table's current metadata file location.
* After retrieving the metadata file, the reader collects the table’s schema to prepare for the reading process. Then, it checks the table’s partition schemes to understand how the data is organized.
* The next step is retrieving the snapshot that the reader wants to read. With a typical query, the current snapshot is selected. However, the older snapshot will be chosen for the time travel query when the user wants to read data in the previous state. Time-travel query can be executed by specifying the timestamp the application wants to read; Iceberg will look for snapshots older than that timestamp, which can be achieved thanks to the fact that the metadata file also stores the created timestamp of each snapshot. The query can also specify the snapshot ID directly.
* After choosing the snapshot, the reader will locate the manifest list associated with that snapshot.
* Then, the reader reads the manifest list to locate the manifest files’ location. It also collects the lower and upper bounds values in the partition column of each manifest file. Because a manifest file can keep track of multiple data files, these lower and upper values are calculated across those files. The reader can apply the partition filter to prune unnecessary manifest files.
* After determining the needed manifest files, the reader opens each file to read. A single manifest file contains the information for all the data files it tracks; Iceberg represents each data file as an entry that records information such as the data file’s location, the lower/upper bound partition values for each file, the file’s format, the record count, etc.
* When reading each entry, the reader can apply the partition pruning using the lower/upper bound partition values for each entry to prune the unneeded data files.
* After navigating all the manifest files, the reader has all the data files it needs to read. It then starts to read all these files using the files’ path, also collected from the manifest file.
* As you can see, the partition pruning process is carried out on two levels. This is possible because Iceberg records statistics about the partition column in both the manifest list and manifest files. The former is used to limit the needed manifest files, and the latter is used to limit the required data files.
* When reading the Parquet data file, the reader can apply other query filters to limit the needed row groups and choose only necessary columns to read to avoid scanning the whole file.
* The result is returned to the client.

The following sections describe some aspects related to the performance of the Iceberg table.

## Compaction

[![](https://substackcdn.com/image/fetch/$s_!BQPZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7df86dd5-444d-457f-af39-65950e2e105f_774x470.png)](https://substackcdn.com/image/fetch/$s_!BQPZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7df86dd5-444d-457f-af39-65950e2e105f_774x470.png)

Image created by the author

Every change in the Iceberg table results in new data files. When reading the table, after determining the necessary data files, we must open each file to read the content and close it when done. This suggests that the process becomes less efficient as the number of files we read increases.

Imagine you have an Iceberge table partitioned by the updated timestamp with day granularity. An application frequently writes to this Iceberge table daily, resulting in many data files in a single partition. You must open and close all those files when you read this partition.

What if we combine all these files into a single file so we only need to open and scan one?

In Icerberg, periodically rewriting the data in all these small files into fewer, larger files is called compaction. The writer can write as many files as they want; the compaction process will rewrite those files into larger files so they can serve the reader more efficiently. Users can control the compacting process by specifying the compaction strategy, the filter to limit which files are rewritten, the target file size, etc.

---

## Hidden Partitioning

Generally, partitioning a table using transformation on a column (e.g., partition by day requires transforming the timestamp expression to day) requires creating an extra column. Users have to use this exact column to benefit from the partition pruning.

For example, a table is partitioned by day, and every record must have an extra `partition_day` column derived from the `created_timestamp` column. When users query the table, they must filter on the exact `partition_day` column so the query engine can only know which partitions it can skip. If the user isn’t aware of this and uses the `created_timestamp` column instead, the query engine will scan the whole table.

[![](https://substackcdn.com/image/fetch/$s_!PPNS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)](https://substackcdn.com/image/fetch/$s_!PPNS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)

Original partition filter queries. Created by the author with the help of carbon.now.sh

However, the latter case is more common for data analysts or business users who want to answer an analytics question; they don’t need to know about the extra column used for technical purposes (partitioning).

This is where Iceberg’s hidden partitioning feature shines:

* Instead of creating additional columns to partition based on transform values, Iceberg only records the transformation used on the column.
* Thus, Iceberg stores less data in the storage because it doesn’t need to store extra columns.
* Because the metadata records the transformation on the original column, the user can filter on that column, and the query engine will apply the transformation to prune the data.

[![](https://substackcdn.com/image/fetch/$s_!NAED!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)](https://substackcdn.com/image/fetch/$s_!NAED!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)

Iceberg partition filter queries. Created by the author with the help of carbon.now.sh

Another challenge with traditional partitioning is that it relies on the physical structure of the files being laid out into subdirectories; changing how the table was partitioned required rewriting the whole table.

Apache Iceberg solves this problem by storing all the historical partition schemes. If the table is first partitioned by scheme A and then later partitioned by schema B, Iceberg exposes this information to the query engine to create two separate execution plans to evaluate the filter again with each partition scheme.

Given a table initially partitioned by the `created_timestamp` field at a monthly granularity, the transformation `month(created_timestamp)` is recorded as the first partitioning scheme. Later, the user updates the table to be partitioned by `created_timestamp` at a daily granularity, with the transformation `day(created_timestamp)` recorded as the second partitioning scheme.

Behind the scenes, the data is organized according to the partition scheme in place at the time of writing. For instance, the data is stored in monthly folders with month partitioning, whereas with day partitioning, it's organized into daily folders.

[![](https://substackcdn.com/image/fetch/$s_!k8Uk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d022718-2fab-4b3b-9d71-622c25f639a2_2000x1600.png)](https://substackcdn.com/image/fetch/$s_!k8Uk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d022718-2fab-4b3b-9d71-622c25f639a2_2000x1600.png)

Image created by the author.

When the application queries this table using `created_timestamp`, the query engine applies both the first and second transformations to `created_timestamp` to enable partition pruning. Refer to the figure below to better understand this process.

[![](https://substackcdn.com/image/fetch/$s_!YLYX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac2b0985-9603-449f-9cae-069948b5102c_787x486.png)](https://substackcdn.com/image/fetch/$s_!YLYX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac2b0985-9603-449f-9cae-069948b5102c_787x486.png)

Image created by the author.

---

## Sorting

While partitioning helps organize data files based on the partition columns, Iceberg gives us more fine-grained control over how data is written to data files with sorting.

Given an Iceberg table partitioned by day, the data contains data from four cities—London, Milan, Paris, and Madrid—the user wants to query data from Milan on 2024-08-08. After the query engine prunes unnecessary partitions, it reads the relevant data files. For the 2024-08-08 partition, there are five files in total. Since data from all four cities is scattered across these files, the engine must open all five files to locate the Milan data. However, if the data were sorted by city, with Milan's data consolidated into two specific files, the query engine would only need to open those three files instead of all ten.

[![](https://substackcdn.com/image/fetch/$s_!N6Kk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb306b28a-f558-4dda-bd36-cfd7c7022f3a_961x549.png)](https://substackcdn.com/image/fetch/$s_!N6Kk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb306b28a-f558-4dda-bd36-cfd7c7022f3a_961x549.png)

Image created by the author.

While reading data becomes more efficient with sorting, the process of writing data files may require additional effort due to the need to sort the data during writing. Moreover, to maintain global sorting across files, a compaction job is necessary to rewrite and sort the data across all files. This makes it crucial for users to carefully define the table’s sort order to leverage this optimization fully.

The best practice for determining the order based on [Tabular](https://tabular.io/):

* Put columns most likely to be used in filters at the start of your write order, and use the lowest cardinality columns first.
* End the order with a high cardinality column, like an ID or event timestamp.

---

## Row-level updates

When writing to storage, data files are immutable and cannot be overwritten. Any changes or updates will create new data files, which enables benefits like snapshot isolation or time travel. In Iceberg, row-level updates are handled through two modes: copy-on-write and merge-on-read.

### Copy-on-write (COW)

This mode is the default in Iceberg. If the table records are changed (updated or deleted), the data files associated with those records will be rewritten with the changes applied.

[![](https://substackcdn.com/image/fetch/$s_!pFML!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c53509-260f-4d5b-a52a-27a47ec73a93_682x275.png)](https://substackcdn.com/image/fetch/$s_!pFML!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c53509-260f-4d5b-a52a-27a47ec73a93_682x275.png)

Image created by the author.

* Pros: Fast reading; the reader only needs to read the data without merging it with deleted or updated files.
* Cons: Slow writing; rewriting all data files will slow down updates, especially if they are too regular.

### Merge-on-Read (MOR)

Instead of rewriting an entire data file, updates are made using the delete files, with changes tracked in separate files:

* **Deleting a record**: The record is listed in a delete file; when the reader reads the table, it will merge the data and the delete file to decide which record to skip.

[![](https://substackcdn.com/image/fetch/$s_!oNe3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a992c82-2141-44e2-adc2-bdf0add43f14_688x438.png)](https://substackcdn.com/image/fetch/$s_!oNe3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a992c82-2141-44e2-adc2-bdf0add43f14_688x438.png)

Image created by the author.

* **Updating a record**: The modified record is also tracked in a delete file, and then the engine creates a new data file containing the record with the updated value. When reading the table, the engine will ignore the old version of the record thanks to the deleted file and use the new version in the new data file.

[![](https://substackcdn.com/image/fetch/$s_!_Coh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf32efbd-0f14-4ec7-948d-cbeb3126b118_692x467.png)](https://substackcdn.com/image/fetch/$s_!_Coh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf32efbd-0f14-4ec7-948d-cbeb3126b118_692x467.png)

Image created by the author.

With MOR mode, there will be more files in the storage than in COW mode. To minimize the data reading cost, the user can run regular compression jobs behind the scenes to reduce the number of files.

The nature of MOR is letting the reader track which records need to be ignored in the future. There are two options to control this behavior:

* **Positional delete files**: The delete file tracks rows to ignore based on their position, allowing readers to skip specific rows. While this minimizes the reading time, it increases the writing time since the writer must read the file to identify those positions.

[![](https://substackcdn.com/image/fetch/$s_!Q0pZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F217a915e-15f3-4f22-9cd8-4cc635bd5705_382x256.png)](https://substackcdn.com/image/fetch/$s_!Q0pZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F217a915e-15f3-4f22-9cd8-4cc635bd5705_382x256.png)

An example of position delete files. Source:  ***[Apache Iceberg: The Definitive Guide](https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG_ER1.pdf)** (2024)*

* **Equality delete files**: The delete files specify the deleted values; if the row has a field that matches this value, the row will be skipped. This option doesn’t require the writer to read the data file. However, it affects the reading performance because it needs to read the data file to compare each record to the deleted value.

  [![](https://substackcdn.com/image/fetch/$s_!FNqC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34624c11-be62-4f2a-b3a4-3d6256594082_394x226.png)](https://substackcdn.com/image/fetch/$s_!FNqC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34624c11-be62-4f2a-b3a4-3d6256594082_394x226.png)

  An example of position delete files. Source: [Apache Iceberg: The Definitive Guide](https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG_ER1.pdf) (2024)

---

## Outro

Thank you for reading this far. As I haven't had the opportunity to work with Iceberg extensively in my career, my understanding of this table format may not be comprehensive, and I might have missed some details. If you notice any areas that need adjustment or improvement in this article, please feel free to leave a comment or reach out to me directly via my [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com/), or [Twitter](https://x.com/_vutrinh).

---

## **References**

*[1] Tomer Shiran, Jason Hughes & Alex Merced, **[Apache Iceberg: The Definitive Guide](https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG_ER1.pdf)** (2024)*

*[2]* *Jason Hughes, **[Apache Iceberg: An Architectural Look Under the Covers](https://www.dremio.com/resources/guides/apache-iceberg-an-architectural-look-under-the-covers/)***

*[3] Tabular, **[Setting table write order](https://tabular.io/apache-iceberg-cookbook/data-engineering-table-write-order/)***

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
