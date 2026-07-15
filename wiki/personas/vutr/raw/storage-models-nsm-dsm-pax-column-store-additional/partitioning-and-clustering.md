---
title: "Partitioning and Clustering"
channel: vutr
author: "Vu Trinh"
published: 2025-07-01
url: https://vutr.substack.com/p/partitioning-and-clustering
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Delta Lake", "BigQuery", "Data Warehouse"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# Partitioning and Clustering

*8 minutes to understand the two most popular OLAP performance-optimized techniques.*

> Source: [Open post](https://vutr.substack.com/p/partitioning-and-clustering)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=166732941)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!W1rJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0749a4ed-95a9-48ad-baa2-bb44a6b3e1a9_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!W1rJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0749a4ed-95a9-48ad-baa2-bb44a6b3e1a9_2000x1429.png)

---

## Intro

In OLTP databases, indexes boost point look-up queries. When you use WHERE username = “bruce\_banner,” the index will tell you where to find records with the username “bruce\_banner.”

However, the typical workload in OLAP databases is different. Business users typically need to analyze and extract insights from historical data, whether from a week, a month, a year, or even longer periods.

Look-up index won’t help much in such a workload.

Scanning less data is a more viable option. Columnar storage allows the engine to read the required columns without touching others. Although this new layout helps, researchers want to skip irrelevant data at a finer-grained level.

To achieve that, I observed that there are two popular techniques: partitioning and clustering. This article will delve into them.

---

## Partitioning

Essentially, partitioning divides a dataset into smaller portions. Its ultimate goal is to reduce data scanning by skipping irrelevant portions. There are two approaches: horizontal and vertical partitioning.

[![](https://substackcdn.com/image/fetch/$s_!QcEB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12c079f3-5a4e-445d-a80d-694fbcda26b5_348x228.png)](https://substackcdn.com/image/fetch/$s_!QcEB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12c079f3-5a4e-445d-a80d-694fbcda26b5_348x228.png)

Column storage (e.g., ClickHouse) is a form of vertical partitioning where each column is stored independently, allowing for the efficient skipping of unnecessary columns. For the hybrid format (e.g., Snowflake, BigQuery, Parquet), although the data is still vertically partitioned, it is not entirely separate from one another.

[![](https://substackcdn.com/image/fetch/$s_!ZEf0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c963ea9-4024-4c9e-a728-17d68250c403_706x528.png)](https://substackcdn.com/image/fetch/$s_!ZEf0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c963ea9-4024-4c9e-a728-17d68250c403_706x528.png)

This format first horizontally partitions the data into row groups (e.g., referred to as row groups in Parquet), and within each row group, the data is vertically partitioned. This ensures that the column’s values from the same row will be stored close together in the same row groups while storing data in a columnar fashion. The system doesn’t have to scan over the disk to consolidate data from a row.

[![](https://substackcdn.com/image/fetch/$s_!bXPV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24baf6f6-d70b-4390-8e08-a2027bfdd473_472x572.png)](https://substackcdn.com/image/fetch/$s_!bXPV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24baf6f6-d70b-4390-8e08-a2027bfdd473_472x572.png)

> From now on, I will use the term "partitioning” to refer to the horizontal partitioning

That is partitioning at the file level.

BigQuery, Clickhouse Iceberg, Hudi, Hive, Delta Lake, or other OLAP systems allow users to partition data at a higher level. We can specify a column so the system can break the data using the value from this column to partition the table into smaller ones. A date column will break the table into partitions for 2025-05-01, 2025-05-02, 2025-05-03, and so on.

[![](https://substackcdn.com/image/fetch/$s_!-ExG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3179f797-1687-4c67-b977-1fb90aa0777e_672x444.png)](https://substackcdn.com/image/fetch/$s_!-ExG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3179f797-1687-4c67-b977-1fb90aa0777e_672x444.png)

Partitioning helps the system operate only on the relevant portion. If it identifies the required row groups in the Parquet files, it can ignore all other groups. If a query includes a filter predicate on the partition key (e.g., `WHERE date=2025-05-01`), the query optimizer can identify that only partition d`ate=2025-05-01`(given the table is partitioned by the day column) is relevant and can completely ignore, or "prune," all others.

[![](https://substackcdn.com/image/fetch/$s_!VlCo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a56374c-6f9c-4478-b486-3e3f254c35e5_868x418.png)](https://substackcdn.com/image/fetch/$s_!VlCo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a56374c-6f9c-4478-b486-3e3f254c35e5_868x418.png)

Although the simplicity, the act of eliminating entire partitions from consideration drastically reduces the volume of data that the query engine needs to read, write, and manage.

### How does it usually work

Most of the systems will let you specify the column to partition the table ([except for Redshift, which does not support partitioning](https://docs.aws.amazon.com/redshift/latest/dg/c_redshift-sql-implementated-differently.html)).

[![](https://substackcdn.com/image/fetch/$s_!Wj6i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8513784-6651-414e-b459-4694c7d6dba5_526x246.png)](https://substackcdn.com/image/fetch/$s_!Wj6i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8513784-6651-414e-b459-4694c7d6dba5_526x246.png)

BigQuery treats a partition as a virtual table. Data from a partition will be stored separately from the data of other partitions. This allows features like data expiration, data insertion, and data deletion to be executed effectively at the partition granularity (because it’s similar to a table). Each partition will have its associated metadata, allowing the engine to leverage it.

Clickhouse also [treats each partition](https://clickhouse.com/docs/partitions) as an independent portion, allowing Clickhouse to write, manage, and query data independently.

For Snowflake, things got different, instead of letting the user specify the partition as the unit of data management. Snowflake automatically splits the tables into micro-partitions, each of which stores between 50 MB and 500 MB of uncompressed data.

[![](https://substackcdn.com/image/fetch/$s_!bJkJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d8ea3b-8255-4af8-9913-228d87fc2bbc_546x246.png)](https://substackcdn.com/image/fetch/$s_!bJkJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71d8ea3b-8255-4af8-9913-228d87fc2bbc_546x246.png)

The micro partitions are organized similarly to the hybrid format, in which a partition contains a group of rows, and each column of data is stored together in each partition. Snowflake manages metadata for columns in the micro-partition to facilitate data management.

When explicitly managing the storage layer by yourself, we will observe a common approach to organizing data in a Hive-style manner, where data is organized into folders:

* Table: Each table has a directory.
* Partitions: Each table can have partitions. Each partition corresponds to a subdirectory.

This scheme is straightforward and has been widely adopted since its introduction. The later generation of table formats, such as Delta Lake, Iceberg, or Hudi, although users still see this partition scheme, they add more robust metadata behind the scenes to improve performance and efficiency.

Iceberg also has a feature called the hidden partition.

Users typically transform a column and use it as the partition key (e.g., partition by day requires transforming the timestamp column to a day and adding an extra column). Users must use this transformed column to benefit from partition pruning.

For example, a table is partitioned by day, and every record must have an extra `partition_day` column derived from the `created_timestamp` column. When users query the table, they must filter on the exact `partition_day` column so the query engine can prune unwanted partitions. If the user is unaware of this and uses the `created_timestamp` column instead, the query engine will scan the entire table.

[![](https://substackcdn.com/image/fetch/$s_!PPNS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)](https://substackcdn.com/image/fetch/$s_!PPNS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)

Iceberg hidden partitions took another approach:

* Instead of creating additional columns to partition based on transform values, Iceberg only records the transformation used on the column.
* Thus, Iceberg can save storage cost because it doesn’t need to store extra columns

[![](https://substackcdn.com/image/fetch/$s_!NAED!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)](https://substackcdn.com/image/fetch/$s_!NAED!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)

Additionally, Iceberg can address the challenge that traditional partitioning relies on the physical structure of the files; changing how the table is partitioned requires rewriting the entire table.

Apache Iceberg stores all the partition schemes. Given a table initially partitioned by the `created_timestamp` field at a monthly granularity, the transformation `month(created_timestamp)` is recorded as the first partitioning scheme.

[![](https://substackcdn.com/image/fetch/$s_!vYY0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84a87cbb-1214-4124-9ce6-a8fe88e97b08_686x472.png)](https://substackcdn.com/image/fetch/$s_!vYY0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84a87cbb-1214-4124-9ce6-a8fe88e97b08_686x472.png)

Later, the user updates the table to be partitioned by `created_timestamp` at a daily granularity, with the transformation `day(created_timestamp)` recorded as the second partitioning scheme. Users don’t have to rewrite the whole table; tables from the past will still be kept in month partitions, while new data will be organized in date partitions.

### Consideration

Choosing the right partition scheme for your workload is crucial.

A too coarse-grained scheme might cause the data pruning to be inefficient. Given that you mostly query at the date level, and the table is partitioned at the month level. A filter date of ”2025-05-01” might cause the engine to read the entire “2025-05” partition.

[![](https://substackcdn.com/image/fetch/$s_!d38o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8172e56-1a22-4354-b7c1-869a0319c246_1282x906.png)](https://substackcdn.com/image/fetch/$s_!d38o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8172e56-1a22-4354-b7c1-869a0319c246_1282x906.png)

In contrast, a too fine-grained scheme might result in many partitions. This increases the overhead for the system, as each partition needs to be managed by an associated metadata. Too many partitions also degrade performance; a filter date of “2025-05-05” will touch 24 hourly partitions, and a filter of “2025-05“ will touch 720 ones.

[![](https://substackcdn.com/image/fetch/$s_!tJNs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef3191e6-467d-41e4-9812-ea6818a90a13_980x558.png)](https://substackcdn.com/image/fetch/$s_!tJNs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef3191e6-467d-41e4-9812-ea6818a90a13_980x558.png)

Additionally, partitioning may cause data skew, as a single partition contains significantly more data than the others. For example, a sales day will have more activity than other days.

Thus, it is crucial to understand the pattern of how our data is used before defining the partition scheme. You need to collect and understand the requirements from your organization to make this decision.

Also, being aware of how your current system offers data partitioning. For example, Iceberg allows users to change the partition scheme without rewriting the entire table, providing sufficient flexibility to experiment with what works in your case or when your business requirements change frequently.

Or, if you’re using Snowflake, you don’t need to care about the partitioning as this cloud data warehouse will automatically handle it for you.

---

## Clustering

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=166732941)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

Like partitioning, the goal of clustering is to help the engine skip unnecessary data. However, it takes a different approach.

While partitioning provides a coarse-grained mechanism for data skipping, its effectiveness is limited by the cardinality of the partition key. To enable finer-grained query optimization, many systems use clustering.

If you partition the table, clustering organizes related data together within partitions; if not, clustering occurs at the table level.

### Sort

And the most straightforward way to make this happen is to sort your data based on one or more columns. This sorting ensures that rows with similar or identical values in the clustering columns are co-located, meaning they are more likely to be written together into the same data unit on disk. You can find the sort clustering supported by BigQuery, Snowflake, Iceberg, Clickhouse, etc.

> *[Because Clickhouse requires the primary key for each MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) table and uses this key to sort the data, we can say that the table in Clickhouse is always clustered.*

When a query engine executes a query with a filter predicate on a clustered column (e.g., `WHERE device_id = 1`), it first performs a metadata scan. For each file, it reads the min/max statistics for the `device_id` column (as it is the column used for sorting).

If the target value `1` falls outside the min-max range for a particular file (e.g., `2 <= device_id <= 3`), the engine knows that the file cannot contain any relevant rows. It can therefore skip reading the entire file, avoiding a costly I/O operation.

When users specify more than one column, the system will sort the data based on the order of the clustering columns. If we choose `device_id` and `customer_id`, the data will be sorted first by the `device_id`, then by `customer_id`.

However, this time, your queries need to align with the order of the sort clustering. If the query has the WHERE clause only on the `customer_id`, data skipping is no longer effective, as the value from the `customer_id` is distributed based on the values from the `device_id`.

Let's examine an example where the table has the following device\_id and customer\_id, each with possible values of `[0, 1, 2, 3]`. After sorting based on `device_id` and `customer_id`, we organized the data into four files:

[![](https://substackcdn.com/image/fetch/$s_!jv9S!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a180786-83ef-4113-bc6f-ec62929a0a71_812x558.png)](https://substackcdn.com/image/fetch/$s_!jv9S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a180786-83ef-4113-bc6f-ec62929a0a71_812x558.png)

* File A:

  + `device_id` = 0
  + 0 <= `customer_id` <= 3
* File B:

  + `device_id` = 1
  + 0 <= `customer_id` <= 3
* File C:

  + `device_id` = 2
  + 0 <= `customer_id` <= 3
* File D:

  + `device_id` = 3
  + 0 <= `customer_id` <= 3

If we filter `device_id = 1`, the number of files needed to scan is 1 (file A). The filter `device_id = 1 AND customer_id` also needs to scan only file A. However, if the filter only contains `customer_id = 3`, the engines need to scan all four files

That’s why there are multi-dimensional clustering techniques to help distribute the data more efficiently.

### Multiple dimensions clustering

These techniques, based on the mathematical concept of space-filling curves, aim to preserve data locality across multiple dimensions (columns). The most prominent implementations are Z-ordering.

The fundamental challenge of multidimensional clustering is that physical storage is inherently one-dimensional; data is laid out sequentially in files. As we discussed, a simple sort on device\_id will group similar `device_id` values, but it doesn’t ensure the locality of `customer_id` values within those groups. It is ineffective for queries that filter only on `customer_id`.

The **[space-filling curves](https://en.wikipedia.org/wiki/Space-filling_curve)** come to the rescue. These are continuous curves that traverse every point in a multi-dimensional space (e.g., a 2D grid defined by the values of `device_id` and `customer_id`) exactly once. It creates a mapping from an N-dimensional space to a one-dimensional line while preserving the spatial locality of the original data points. In other words, data points that are close to each other in the N-dimensional space are likely to be close to each other in the 1-D.

By calculating each data row's position on this 1D curve and then physically sorting the entire dataset based on this derived value, we can co-locate data that is "close" across multiple dimensions.

### Z-ordering

The Z-order curve, also known as Morton coding, is a popular and computationally simple space-filling curve. Its mechanism is based on the principle of bit-interleaving.

> *Imagine having two bits: 010 and 001. Bit interleaving combines these two bits. Starting from the rightmost bit, we place bits from the first set, then bits from the second set, then bits from the first set again, and so on. **010** and 001 interleaving will result in 0**0**0**1**1**0***
>
> [![](https://substackcdn.com/image/fetch/$s_!oYnK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9b9200f-cf27-44d7-bcae-76fe7e0eea45_374x168.png)](https://substackcdn.com/image/fetch/$s_!oYnK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9b9200f-cf27-44d7-bcae-76fe7e0eea45_374x168.png)

To calculate the Z-value for a data point, the system performs these steps :

1. **Binary Representation:** The values of each column being clustered are converted into their binary representations.
2. **Bit Interleaving:** A new binary number is formed by taking the first bit from the first dimension, followed by the first bit from the second dimension, and so on for all dimensions.
3. **Z-Value:** The resulting interleaved binary number is the Z-value. The dataset is then physically sorted according to these Z-values.

Returning to the example above, which includes a table with clustering columns `device_id` and `customer_id`. For each possible value, we represent it in binary and interleave the bits together to calculate the z-value:

[![](https://substackcdn.com/image/fetch/$s_!RQgU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ed4c7e5-5001-4b57-9707-68f393160aaa_770x570.png)](https://substackcdn.com/image/fetch/$s_!RQgU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ed4c7e5-5001-4b57-9707-68f393160aaa_770x570.png)

If we draw a line from 0 → 15, we will have a recursively Z-shaped curve (that’s why it’s called z-ordering)

[![](https://substackcdn.com/image/fetch/$s_!pc0A!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06c9f713-94ca-4d57-b51a-73f5e8e03fc7_702x534.png)](https://substackcdn.com/image/fetch/$s_!pc0A!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06c9f713-94ca-4d57-b51a-73f5e8e03fc7_702x534.png)

And, if we store each small Z in a file, we will have four files:

[![](https://substackcdn.com/image/fetch/$s_!YtI0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91d2d8f9-36df-4391-8e7d-06ddf4f724e5_860x650.png)](https://substackcdn.com/image/fetch/$s_!YtI0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91d2d8f9-36df-4391-8e7d-06ddf4f724e5_860x650.png)

* File A:

  + 0 <= `device_id` <= 1
  + 0 <= `customer_id` <= 1
* File B:

  + 0 <= `device_id` <= 1
  + 2 <= `customer_id` <= 3
* File C:

  + 2 <= `device_id` <= 3
  + 0 <= `customer_id` <= 1
* File D:

  + 2 <= `device_id` <= 3
  + 2 <= `customer_id` <= 3

If we filter `device_id = 1`, the number of files needed to scan is 2 (A and B). When the filter contains `customer_id = 3`, the engines need to scan 2 files (B and D).

Although the number of files to be scanned when the filter is on `device_id` is larger, the filter on `customer_id` will scan two fewer files than the sorting approach. Compared to the sorting, the z-ordering treats clustered keys more fairly.

You can find z-ordering supported by Delta Lake, Iceberg, or Hudi.

### Consideration

Like partitioning, clustering allows the engine to skip irrelevant data. However, it’s done at a more fine-grained level compared to partitioning. If your table is partitioned by date and clustered by device\_id and customer\_id, the table is first broken down into smaller daily tables, with data in each organized according to the clustered columns.

Again, to determine the clustering columns, you must carefully consider your organization's specific needs. Like any other thing in life, clustering is not free. It slows down data writing because clustering must place data in a particular order. In other words, with clustering, you sacrifice your writing for a better read.

Another consideration is that the data must be reorganized whenever new data becomes available. Records with `device_id = 1` are already stored close together in the first two files. However, at a given time in the future, new records with `device_id = 1` are ingested in the fourth and sixth files.

[![](https://substackcdn.com/image/fetch/$s_!M1aD!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c221fa-f372-42e4-b2ab-680c3864133d_1220x478.png)](https://substackcdn.com/image/fetch/$s_!M1aD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c221fa-f372-42e4-b2ab-680c3864133d_1220x478.png)

The system must rearrange the data to ensure locality.

[![](https://substackcdn.com/image/fetch/$s_!bvn4!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d4a7e29-b1e6-45ca-ab6b-0a1d54786a7c_1508x806.png)](https://substackcdn.com/image/fetch/$s_!bvn4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d4a7e29-b1e6-45ca-ab6b-0a1d54786a7c_1508x806.png)

In a cloud data warehouse like BigQuery ([free](https://cloud.google.com/bigquery/docs/clustered-tables#automatic_reclustering)) or Snowflake ([extra cost](https://docs.snowflake.com/en/user-guide/tables-auto-reclustering#automatic-clustering-costs)), this process is handled in the background automatically without affecting the table’s read-write operations.

If you want to cluster your tables, being fully aware of two things from your systems:

* Which kinds of clustering do they offer? (e.g., sorting, multi-dimensional clustering like z-ordering)
* How they maintain the desired state of the clustered tables (e.g., do I need to re-cluster the table by myself?, is it automatic?)

---

## Outro

In this article, we explored how partitioning and clustering could help OLAP engines skip unwanted files to read the data, thus improving the overall performance of our queries. Then, we explore the popular ways to implement these techniques in some well-known systems. Ultimately, we must consider several factors when applying these techniques in our real-life workload.

Thank you for reading this far.

See you in my following articles :)

P/s: For multi-dimensional clustering, besides z-ordering, there is also the [Hilbert Curve](https://en.wikipedia.org/wiki/Hilbert_curve#:~:text=The%20Hilbert%20curve%20(also%20known,by%20Giuseppe%20Peano%20in%201890.), which also tries to do the same things as z-ordering. Because I suck at Math, spending a far amount of time on the z-ordering make me exhausted :)))

Forgive me for skipping the [Hilbert](https://en.wikipedia.org/wiki/Hilbert_curve#:~:text=The%20Hilbert%20curve%20(also%20known,by%20Giuseppe%20Peano%20in%201890.) curve.

---

## Reference

*[1] Sanjeet Shukla, [Understanding Z-Order Optimization In Data lakes](https://medium.com/@sanjeets1900/understanding-z-order-optimization-in-data-lakes-a840be4de720) (2024)*

*[2] Lester Martin, [Z-Order Visualized](https://www.youtube.com/watch?v=ncqSjHeZTxU) (2023)*

*[3] Andy Pavlo, CMU Database, [#05 - Row vs. Column Storage + Compression](https://www.youtube.com/watch?v=nhlpwmOBEiE&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=7)*
