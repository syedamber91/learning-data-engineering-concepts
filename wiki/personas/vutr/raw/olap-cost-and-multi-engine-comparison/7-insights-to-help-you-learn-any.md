---
title: "7 insights to help you learn any OLAP systems"
channel: vutr
author: "Vu Trinh"
published: 2025-12-30
url: https://vutr.substack.com/p/7-insights-to-help-you-learn-any
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Lake", "Lakehouse"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# 7 insights to help you learn any OLAP systems

*Before learning BigQuery, Databricks, Snowflake, Redshift, DuckDB, Clickhouse,.. you must read this.*

> Source: [Open post](https://vutr.substack.com/p/7-insights-to-help-you-learn-any)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=182411333)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!OG_3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e052d2f-4832-4f78-a8d1-11de14e0f61e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!OG_3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e052d2f-4832-4f78-a8d1-11de14e0f61e_2000x1429.png)

---

# Intro

Last week, one of my readers asked how I’m able to understand so many OLAP systems. That question motivated me to write this article.

—

I love OLAP systems, from cloud data warehouses to open lakehouse architectures.

Besides working with BigQuery at my job, I’ve spent a lot of time learning about other systems. The more I explore, the more I realize that they share some fundamental concepts, and if we understand those, we can learn almost any OLAP system more easily.

At a time when everything is moving faster (for example, your company might decide to migrate to Databricks because it offers a better deal, or you might join a new company that uses AWS for everything), I believe the ability to learn and understand any OLAP system quickly provides an unfair advantage.

This article shares my 7 insights to help you do exactly that.

---

# Shared-nothing and shared-disk architecture

In the past, when the network was not as fast as today and hard disks were expensive, a common approach to building any database was to stitch compute and storage together. A database could be deployed across multiple servers, each with its own disk and a subset of data.

[![](https://substackcdn.com/image/fetch/$s_!mKlw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9389311-a93a-448b-af59-0de3ffc2cdf3_1052x880.png)](https://substackcdn.com/image/fetch/$s_!mKlw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9389311-a93a-448b-af59-0de3ffc2cdf3_1052x880.png)

This approach is known as the shared-nothing architecture.

The advantage is performance, as data is read and written from local disks.

However, it has several downsides.

First, changing the node membership requires moving data between nodes to achieve the “balance state.” This might make the database unstable during this process.

[![](https://substackcdn.com/image/fetch/$s_!hRv_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ec36c9-e089-4e85-936d-ccfdc5ba0b4a_718x712.png)](https://substackcdn.com/image/fetch/$s_!hRv_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ec36c9-e089-4e85-936d-ccfdc5ba0b4a_718x712.png)

Second, both compute and storage can’t be scaled independently, as the only way to increase one is to add more servers, which results in inefficient resource usage.

—

Storage has been cheaper, and networks have been faster over time.

Database researchers thought it was time to separate storage and compute.

[![](https://substackcdn.com/image/fetch/$s_!6kEU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3963c02b-05c4-48b0-a5dc-fee258c74d5d_1220x812.png)](https://substackcdn.com/image/fetch/$s_!6kEU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3963c02b-05c4-48b0-a5dc-fee258c74d5d_1220x812.png)

Data is stored in a giant store and shared between stateless workers. Storage and compute can now be scaled independently. The architecture usually leverages an object store service (or a similar solution) for the storage layer, thanks to its unbeatable scalability, availability, and durability.

[![](https://substackcdn.com/image/fetch/$s_!IU2D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8b8ed10-63a5-4cb0-8878-fd7cde2047cc_1264x710.png)](https://substackcdn.com/image/fetch/$s_!IU2D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8b8ed10-63a5-4cb0-8878-fd7cde2047cc_1264x710.png)

The downside of this approach is that performance might degrade compared to the shared-nothing architecture, as workers must read data over the network; an optimized mechanism, such as a cache layer, must be implemented.

—

When you learn any OLAP systems, they’re designed in one of the two approaches discussed above

* Shared-nothing: Clickhouse, DuckDB, StarRock, Apache Pinot, Apache Druid, Apache Doris, Redshift (except RA3 option)
* Shared-disk: BigQuery, Snowflake, Databricks, Redshift (only RA3 option)

> ***Note 1**: Trino and Spark are special cases as they only serve as the compute engine; your data must be stored somewhere. To some extent, the architecture that has Spark or Trino could also be considered as shared-disk.*
>
> ***Note 2**: Modern systems are blurring the line. For example, **Snowflake** uses a shared-disk model but caches data locally on the worker server, acting like a shared-nothing system during execution. Conversely, **ClickHouse** supports using object storage as the primary store.*

Understanding the storage-compute architecture of an OLAP system will help you manage resources and optimize performance better.

---

# How is metadata managed?

A table is a collection of immutable files. This helps the vendor implement concurrency and version control more seamlessly because once data is written, it cannot be modified; any changes result in writing new files.

There must be metadata to identify which files comprise a table.

Beyond that fundamental role, this metadata must also enable OLAP systems to handle transactions (e.g., checking for conflicts, discarding the entire operation if it fails), version control, query optimization, governance, etc.

—

When you learning any OLAP system, there are two main approaches to managing this metadata:

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=182411333)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

## Metadata Stored in Object Storage

Here, the metadata is just another set of files (JSON or Avro) sitting right next to your data in S3 or GCS. Every time you write data, the system creates new associated metadata files. This file lists exactly which data files make up the current version of the table. Open table formats such as Apache Iceberg, Delta Lake, and Apache Hudi implement this approach.

[![](https://substackcdn.com/image/fetch/$s_!yds9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59fece6f-b92b-4f5e-a098-440a29114f6b_988x462.png)](https://substackcdn.com/image/fetch/$s_!yds9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59fece6f-b92b-4f5e-a098-440a29114f6b_988x462.png)

* **The Pro:** Because the metadata lives in storage, you can use any query engine that implements the protocol to consume it. You can query an Iceberg table from Spark, then query it from Snowflake later, because all the information is shared via the metadata files in object storage.
* **The Con:** As a table grows to millions of files, the metadata files themselves get huge. This indeed affects the query engine's read performance. In addition, because metadata lives in object storage, reading a single piece of metadata can take longer because it must be transferred over the network.

## Metadata in a Transactional Database

Traditional cloud warehouses prefer to keep their metadata in a specialized, high-speed database (often a Key-Value store or a distributed RDBMS). When you query a table, the engine doesn’t look at files in object storage to find the schema.

[![](https://substackcdn.com/image/fetch/$s_!39U0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00a641e3-84eb-4396-96c1-07de8e2ce532_1470x980.png)](https://substackcdn.com/image/fetch/$s_!39U0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00a641e3-84eb-4396-96c1-07de8e2ce532_1470x980.png)

It asks a dedicated “Metadata Service” (backed by something like FoundationDB for Snowflake or Google Spanner for BigQuery) for the latest metadata. DuckLake, the open table format built by MotherDuck, the company behind DuckDB, also takes this approach.

* **The Pro:** You don’t need to care much about the explosion of metadata, as it was stored as files in object storage. The database also provides more sophisticated transactional capabilities than object storage. In addition, reading a record from a database is undoubtedly faster and more straightforward than requesting, opening, and parsing metadata from files in object storage.
* **The Con:** Because the metadata is locked inside a proprietary database, it’s harder for external tools to “understand” the data. If the metadata database can’t be scaled based on the data workload, it will become the bottleneck, as every operation must go through it. (DuckLake promises to solve this problem, but I have not looked into its details yet.)

---

# How is data stored?

OLAP systems focus on reading large volumes of historical data and performing aggregations and joins. In most cases, a subset of columns only needs to be scanned. This characteristic causes issues when handling OLAP workloads on the OTLP system (which uses row-format storage).

Imagine we have a table with 10 columns.

A query that reads two columns: date and sales, then calculates the SUM of sales by date. With the row-store format, where all column data for a single row is stored next to each other, we must load the entire row into memory before the system can extract data from the two columns.

This is inefficient.

The solution is to store data from a single column continuously. There are two main approaches: the column store and the hybrid.

## Column store

The first approach stores data from a single column separately. The system only loads the required columns’ data and does not need to handle other columns.

This approach requires the system to manage the data offset. Because a row of data is stored in multiple places, there must be a way for the DBMS to know which row a specific column value belongs to.

To address this, the DSM ensures that each value in a column has the same length. This allows the DBMS to easily calculate offsets for specific values based on the fixed value size.

[![](https://substackcdn.com/image/fetch/$s_!i9EB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de8ae1d-8f17-4c33-bc70-76398b68cbc1_490x366.png)](https://substackcdn.com/image/fetch/$s_!i9EB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de8ae1d-8f17-4c33-bc70-76398b68cbc1_490x366.png)

This storage model reduces wasted I/O per query by allowing the DBMS to read only the columns it needs. Additionally, it allows for better data compression, as column values often exhibit patterns. You can find this approach in Clickhouse or Redshift.

However, this model may cause issues with writing operations. When writing to a table with 100 columns, the DBMS would need to jump around and write the data to 100 separate locations, resulting in significant overhead.

In addition, read operations that require reading all column data place more work on the system, as the DBMS would have to consolidate data from 100 places.

The hybrid format comes to the rescue.

## Hybrid

In this storage model, table data is horizontally split into row groups, with the columns’ data stored next to each other within each group. The goal is to benefit from fast, efficient data scans on the column store while maintaining the locality of the row store (column values from the same row stay close together, at least within the row group).

[![](https://substackcdn.com/image/fetch/$s_!AOqG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04d7bf70-3e00-420c-bee7-fc1907a83991_510x630.png)](https://substackcdn.com/image/fetch/$s_!AOqG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04d7bf70-3e00-420c-bee7-fc1907a83991_510x630.png)

Based on my observations, this approach is more common than the column store, as seen in numerous systems, including BigQuery, Snowflake, DuckDB, Parquet, and ORC.

---

# What are the optimization techniques?

For any OLAP systems, the primary optimization method is to avoid reading irrelevant data as much as possible in the first place.

## Lightweight Metadata

The metadata that enables this skipping is often called a “Zone Map” or simply block-level statistics. For each data chunk on disk and for each column within that chunk, the system stores statistics, most commonly the minimum and maximum values. Other statistics may include counts of null values, distinct values, or more sophisticated data structures such as Bloom filters to check if a record exists in that data unit.

[![](https://substackcdn.com/image/fetch/$s_!DbY4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d56d61-de30-43b1-8c52-b516a062eefe_512x504.png)](https://substackcdn.com/image/fetch/$s_!DbY4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d56d61-de30-43b1-8c52-b516a062eefe_512x504.png)

Consider a table of sales data partitioned into monthly files, with a Zone Map for each file tracking the min/max `click_counts`. A query asking for click counts (`WHERE click_counts < 25`) would cause the query optimizer to scan the metadata first. It would immediately discard all the blocks of data that don’t have `click_counts` between `< 25`.

Only blocks whose click counts are `< 25` would be read from disk, dramatically reducing the scope of the scan.

## Partitioning

(Horizontal) Partitioning divides a dataset into smaller subsets. Its ultimate goal is to reduce data scanning by skipping irrelevant portions. Most of the systems allow users to partition data at a higher level.

We can specify a column that enables the system to partition the table based on its values. A date column will partition the table into 2025-05-01, 2025-05-02, 2025-05-03, and so on.

[![](https://substackcdn.com/image/fetch/$s_!eFKa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)](https://substackcdn.com/image/fetch/$s_!eFKa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)

Partitioning helps the system operate only on the relevant portion. If a query includes a filter predicate on the partition key (e.g., `WHERE date=2025-05-03`), the query optimizer can identify that only the partition date=2025-05-03 (given the table is partitioned by the day column) is relevant and can completely ignore, or “prune,” all others.

[![](https://substackcdn.com/image/fetch/$s_!s-2C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d048052-1ef7-4d17-b18d-5af7840f677f_818x426.png)](https://substackcdn.com/image/fetch/$s_!s-2C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d048052-1ef7-4d17-b18d-5af7840f677f_818x426.png)

## Clustering

Like partitioning, clustering helps the engine skip unnecessary data. However, it takes a different approach. While partitioning provides a coarse-grained mechanism for data skipping, its effectiveness is limited by the partition key’s cardinality.

[![](https://substackcdn.com/image/fetch/$s_!Cq1S!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9898a382-b396-4a36-b579-d2c952713fd3_884x530.png)](https://substackcdn.com/image/fetch/$s_!Cq1S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9898a382-b396-4a36-b579-d2c952713fd3_884x530.png)

To enable finer-grained query optimization, many systems use clustering. If you partition the table, clustering organizes related data within partitions; otherwise, it occurs at the table level.

The most straightforward way to achieve this is to **sort** and store the data based on one or more columns. This sorting ensures that rows with similar or identical values in the clustering columns are co-located, making them more likely to be written together into the same data unit on disk. Beyond sorting, there are advanced mechanisms like z-ordering to help with clustering across multiple columns.

## Point Look-up indexes

As mentioned, the primary optimization method in an OLAP system is to avoid reading irrelevant data. That said, a point look-up index, such as a B-Tree, in an OLTP system does not contribute much here.

However, it still exists in some OLAP systems with niche workloads.

For example, Apache Hudi maintains [a point lookup index](https://hudi.apache.org/docs/indexes/) to help locate records faster during the upsert process (as it was designed to offer the upsert capabilities for the data lake)

---

# How is the query executed?

When you are trying to understand how any OLAP system executes the query behind the scenes, most of the time, you will encounter one of the two approaches.

> ***Note**: In the scope of this article, I will only introduce you to the two approaches and won’t dive into comparing them.*

## Vectorized Execution

In OLTP databases, the system processes a single row at a time, then moves to the next. This is fine because OLTP databases don’t need to handle large numbers of rows like OLAP databases.

In the world of **OLAP**, that approach is too slow.

Instead of moving one row at a time, some OLAP engines move a **Vector,** a batch of multiple values.

[![](https://substackcdn.com/image/fetch/$s_!6pHd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d49cb5b-4079-40c3-af2f-c5811a6bf943_950x524.png)](https://substackcdn.com/image/fetch/$s_!6pHd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d49cb5b-4079-40c3-af2f-c5811a6bf943_950x524.png)

By processing in batches, OLAP systems amortize the overhead. The engine performs the computation only once per batch, not once per row.

Modern CPUs have special registers that can perform the same operation on 8 or 16 values simultaneously. Vectorization is designed to leverage this “shortcut “.

Lots of OLAP use this approach: ClickHouse, Snowflake, DuckDB, BigQuery, Databricks’ Photon engine,…

## Code Compilation

Code Compilation (often called Just-In-Time or JIT) takes a different approach. Instead of using pre-written code to handle your query, the database writes a new program specifically for your SQL query and compiles it into machine code on the fly.

By doing so, the engine reduces the number of CPU instructions required to execute a query.

[![](https://substackcdn.com/image/fetch/$s_!R6XX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F373e4e0d-097d-4769-aa77-09926336da54_1042x504.png)](https://substackcdn.com/image/fetch/$s_!R6XX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F373e4e0d-097d-4769-aa77-09926336da54_1042x504.png)

In a system that doesn’t apply this approach, each operator has to go through a condition block (switch) to check for the data type and then choose the appropriate function for the input data type. The code compilation approach avoids this because all operators for a given query are generated at execution time.

OLAP systems that leverage these approaches are Redshift and Spark.

---

# How are the joins executed?

In any database, a very high chance that the join operations will be handled in the three following approaches:

## Nested Loop Join (NLJ)

The Nested Loop Join is the most straightforward join strategy, working by iterating over every record in the left table with a primary loop and scanning the right table for matches with a secondary loop.

[![](https://substackcdn.com/image/fetch/$s_!MiYR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b2c5d37-2cfe-4415-b774-e170523f21ca_954x312.png)](https://substackcdn.com/image/fetch/$s_!MiYR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b2c5d37-2cfe-4415-b774-e170523f21ca_954x312.png)

It performs best when the left table is small or when the right table has an index on the join column, allowing the system to perform quick lookups rather than looping through the table end-to-end.

## Sort Merge Join (SMJ)

The Sort Merge Join operates in two distinct phases. First, sort both tables by their join columns and then “merge” them by walking through the sorted data with pointers.

[![](https://substackcdn.com/image/fetch/$s_!Rqhb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbccdbc4b-5bad-49ed-aea4-b39491bde00b_1122x354.png)](https://substackcdn.com/image/fetch/$s_!Rqhb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbccdbc4b-5bad-49ed-aea4-b39491bde00b_1122x354.png)

During the merge phase, the system advances pointers to identify matches and stops once either table is exhausted. While the initial sorting can be resource-intensive, this strategy is a strong candidate if the tables are already sorted or if the final query requires the output to be ordered by the join key.

## Hash Join

The Hash Join is designed for “equi-joins” and uses a hash table to match records, avoiding sorting or nested loops.

In the “Build Phase,” the database hashes the join columns of the smaller table to create an in-memory hash table.

In the “Probe Phase,” it hashes the larger table’s rows to find matching rows from the build table.

[![](https://substackcdn.com/image/fetch/$s_!zohg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F314940bb-5ab5-41d4-9763-bd744d8b8e59_672x318.png)](https://substackcdn.com/image/fetch/$s_!zohg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F314940bb-5ab5-41d4-9763-bd744d8b8e59_672x318.png)

This method is very fast when the build table fits in memory.

Still, if the data is too large, the system must use **Grace Hash Join**, which partitions both tables into smaller buckets on disk and processes them in pairs to prevent memory overflow.

[![](https://substackcdn.com/image/fetch/$s_!1QSZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74386447-d8d9-451b-97ba-134184e94160_862x336.png)](https://substackcdn.com/image/fetch/$s_!1QSZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74386447-d8d9-451b-97ba-134184e94160_862x336.png)

## Join in OLAP systems

In OLAP systems, the **Nested Loop Join** is generally considered unsuitable.

While popular in OLTP environments like PostgreSQL, it relies on small table sizes or pre-built indexes to avoid slow sequential scans. Since OLAP workloads typically involve massive datasets on both sides and lack the point-lookup indexes, the strategy is inefficient.

Consequently, OLAP engines primarily focus on **Hash Joins** and **Sort-Merge Joins**, which are better suited for large-scale data processing.

To handle the scale of analytical workloads, OLAP systems execute these joins in **parallel across multiple machines**.

[![](https://substackcdn.com/image/fetch/$s_!YRTt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a27427c-03c0-41af-98c9-6de4e6e0449d_1372x834.png)](https://substackcdn.com/image/fetch/$s_!YRTt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a27427c-03c0-41af-98c9-6de4e6e0449d_1372x834.png)

The process begins by dividing the data into smaller chunks: the system applies a hash function to the join columns of both tables, distributing them across different workers into buckets. Each worker then performs a local join.

A significant challenge here is **data skew**; if a specific join key is overly dominant, it can overwhelm a single worker, forcing the system to re-partition or re-hash the data to balance the load.

The **Hash Join** is the most widely adopted in modern OLAP engines.

Systems like Snowflake and BigQuery rely heavily or exclusively on hash joins, while Spark supports both hash and sort-merge options. The preference for hash joins often stems from their efficiency in memory-heavy environments and their ability to avoid the expensive sorting overhead required by Sort-Merge joins, provided there is enough memory to hold the hash tables.

A common optimization used by these engines for the Hash Join is the **Broadcast Hash Join.**

If a table is small enough to fit in memory, the system skips the expensive network shuffle of both tables. Instead, it broadcasts the entire small table to every worker node. Each worker then builds a local hash table and joins it against its specific slice of the larger table.

This significantly reduces network traffic.

Modern engines, such as BigQuery and Snowflake, automatically detect these broadcast opportunities at runtime.

---

# Does the system support real-time analytics?

In some modern OLAP systems, the questions are evolving from “How much data can you process?” to “How fresh is that data?”; users want real-time analytics capability.

There are two main mechanisms an OLAP database can use to achieve this (and they’re not mutually exclusive).

## The In-Memory Buffer

[![](https://substackcdn.com/image/fetch/$s_!DRt4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d9d1404-4595-48a4-bf14-fe6ca8ab0b06_900x646.png)](https://substackcdn.com/image/fetch/$s_!DRt4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d9d1404-4595-48a4-bf14-fe6ca8ab0b06_900x646.png)

Real-time systems like Apache Pinot, Apache Druid, or StarRocks don’t wait for data to hit the disk before making it searchable.

As data streams in from message systems like Kafka or Pulsar, the OLAP systems put it into a volatile, in-memory structure. When you run a query, the engine actually queries two places at once: the “Cold” historical data on disk and the “Hot” real-time data in RAM.

## The Hierarchical Storage Model

This approach is based on an observation that ingestion and analytics have different needs:

[![](https://substackcdn.com/image/fetch/$s_!D6C_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7fcd5c9-bb3f-4d51-b1b2-0f12d27f7307_1240x652.png)](https://substackcdn.com/image/fetch/$s_!D6C_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7fcd5c9-bb3f-4d51-b1b2-0f12d27f7307_1240x652.png)

* **Ingestion (Writes)** loves **Row Format**: It’s fast to append one row at a time.
* **Analytics (Reads)** prefers **Columnar Format**: It’s fast to scan and aggregate.

BigQuery first ingests data into a memory buffer and later flushes it to disk in row format. This ensures the system can handle millions of small data inserts per second without the penalty of rewriting huge columnar files. In addition, the query can perform in memory for recent data (just like the in-memory buffer approach)

The row-format data is merged into blocks and “flipped” into column format to support read operations better.

# Outro

In this article, I share my insights to help you learn OLAP systems faster, covering its compute-storage architecture, metadata management, data storage format, query and join execution, optimization techniques, and how an OLAP system supports real-time analytics.

Thank you for reading this far. See you in my next articles.
