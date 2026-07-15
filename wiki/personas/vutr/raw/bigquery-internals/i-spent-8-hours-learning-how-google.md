---
title: "I spent 5 hours learning how Google manages terabytes of metadata for BigQuery."
channel: vutr
author: "Vu Trinh"
published: 2024-09-17
url: https://vutr.substack.com/p/i-spent-8-hours-learning-how-google
paid: false
topics: ["Data Engineering", "Apache Iceberg", "Snowflake", "Delta Lake", "BigQuery", "Data Warehouse", "Lakehouse"]
tags: [metadata, https, auto, query, image, table]
---

# I spent 5 hours learning how Google manages terabytes of metadata for BigQuery.

*How Google manages metadata at a large scale.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-how-google)

## Topics

[[data-engineering|Data Engineering]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!D2EJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dcb77bb-4b33-4cde-bbed-d412cf4da4fe_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!D2EJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dcb77bb-4b33-4cde-bbed-d412cf4da4fe_2000x1429.png)

Image created by the author.

---

## Intro

The importance of metadata—data about data—should not be underestimated. It is vital in optimizing storage, query performance, and governance in data warehouse and lakehouse systems.

* How do we know which files belong to a table? We use metadata.
* How does the query engine know which files it can skip? The query engine uses metadata.
* How do you enforce ACID over many files in the object storage? They use metadata.

Managing metadata for small datasets is usually straightforward. However, when dealing with massive tables, the situation changes significantly. While it’s true that metadata is not typically as large as the dataset itself, this assumption holds mainly when the system records only high-level (coarse-grained) metadata. However, the more detailed the metadata, the more valuable it becomes for optimizing the query engine and storage management.

Fine-grained metadata tracks information at a much more granular level—such as metadata for each data block or each column within those blocks. This can quickly scale to millions of metadata objects, matching the scale of the underlying data. The challenge lies in efficiently managing this metadata without letting it become a bottleneck.

Google’s BigQuery, a cloud-based data warehouse, tackles these challenges head-on. Rather than treating metadata as a secondary concern, BigQuery employs innovative techniques to manage metadata at scale, treating it with the same priority as the data. This allows the system to efficiently store and query billions of metadata objects with high performance.

This week, we’ll explore Google’s distributed metadata management system, which powers BigQuery, one of the world's most robust data warehouse solutions.

> *I reference [a 2021 Google paper](https://www.vldb.org/pvldb/vol14/p3083-edara.pdf) for this article.*

---

## BigQuery architecture

> *Before diving to the metadata system, we first revisit the BigQuery architecture.*

[![](https://substackcdn.com/image/fetch/$s_!RsmB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4b872d4-2c4d-45c1-9f3d-85711297b933_1390x1078.png)](https://substackcdn.com/image/fetch/$s_!RsmB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4b872d4-2c4d-45c1-9f3d-85711297b933_1390x1078.png)

Image created by the author.

BigQuery is Google's serverless data warehouse, enabling PB-scale analytics for enterprises. Its architecture is based on the principle of disaggregation:

* **Colossus**: A distributed storage system that holds and stores data.
* **Dremel**: The distributed query engine.
* **Borg**: Google’s large-scale cluster management system that can manage and orchestrate reliably compute resources. ([Borg is the predecessor of Kubernetes](https://kubernetes.io/blog/2015/04/borg-predecessor-to-kubernetes/))
* **Dedicate shuffle service**: Dremel was inspired by the map-reduce paradigm to efficiently operate and manage the data shuffle between stages; Google built a separate shuffle service on top of disaggregated distributed memory. This service backs BigQuery and supports other services, such as [Google Dataflow](https://cloud.google.com/products/dataflow?hl=en).

The following section will delve into the query execution engine and the managed storage, which interact closely with the metadata system.

---

## The query execution engine

[![](https://substackcdn.com/image/fetch/$s_!cJHK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce9f93be-27bc-44a9-9b87-30238ac7fda6_972x693.png)](https://substackcdn.com/image/fetch/$s_!cJHK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce9f93be-27bc-44a9-9b87-30238ac7fda6_972x693.png)

Image created by the author.

What happens when we submit a query to BigQuery?

* The query is first routed to the Query Coordinator node, which manages query execution.
* The Coordinator parses and prepares the SQL query for the Logical Query Plan.
* The query planner then applies several transformations to the logical plan, such as pushing down computations and filters.
* Next, the Coordinator gathers information on the tables involved in the query, the requested columns from each table, and the filters applied to table scans.
* With this information, the Coordinator converts the Logical Query Plan into the Physical Query Plan.
* A query plan can be imagined as a Directed Acyclic Graph (DAG) of stages. In each stage, multiple workers run the same set of operators in parallel on a subset of data.
* After having an initial plan, the Coordinator communicates with the Scheduler to request worker resources ([slot](https://cloud.google.com/bigquery/docs/slots)). If things go well, the Scheduler returns the worker's information to the Coordinator. Processing jobs are then sent to the worker from the Coordinator.
* In the first stage, when the workers' main job is to scan data from the storage, they also query the metadata to skip unneeded files. We will revisit this process later in the article.
* In BigQuery, physical query plans are dynamic. Although it is formed initially, the plan adapts during runtime based on real-time data statistics such as the total amount of data flowing between the stages, the number of rows for each table, data distribution, and skew.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## The Managed Storage

[![](https://substackcdn.com/image/fetch/$s_!6_at!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b074d50-e8a2-473b-8d3e-0b3738292b8b_989x380.png)](https://substackcdn.com/image/fetch/$s_!6_at!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b074d50-e8a2-473b-8d3e-0b3738292b8b_989x380.png)

Image created by the author.

BigQuery stores data in Google’s distributed file system, Colossus, using a proprietary format called Capacitor. Data in BigQuery is stored in a columnar block format, with large tables often consisting of millions of blocks. BigQuery can also support tables with tens of thousands of columns. Additionally, it ensures ACID transactions with snapshot isolation, achieved through a metadata layer that tracks changes and maintains data consistency.

---

## Metadata System

Google takes a different approach than table formats like Delta Lake and Iceberg, which store metadata alongside the data. In BigQuery, Google developed a centralized metadata management system. To prevent this from becoming a bottleneck, metadata is managed and processed in a distributed manner, similar to how data is handled. This system is designed to store highly detailed metadata, scale to accommodate very large tables, and ensure that the query engine can access it efficiently.

As mentioned, a BigQuery table can contain tens of thousands of columns and millions of physical blocks. Initially, Google only recorded coarse-grained metadata due to the extensive cardinality of these objects. However, they soon realized the performance advantages of using fine-grained metadata, which captures detailed information about each block and column. To implement this, Google developed a distributed metadata management system that stores detailed column—and block-level metadata for large tables, organizing them as tables within a relational database.

To efficiently handle vast amounts of metadata, they built a query plan that seamlessly integrates metadata scans with data scans. This approach utilizes the same distributed query processing techniques used for the data. The following subsections describe this metadata system in more detail.

### Metadata structure

Metadata in BigQuery can be categorized into two types: logical and physical. The first includes details like the table schema, partitioning and clustering settings, and access controls at the column and row level. On the other hand, physical metadata refers to the internal information BigQuery uses to map a table to its actual data (e.g., a metadata layer from Delta Lake or Iceberg table format.) They include the locations of data blocks in the file system, row counts, data lineage in blocks, statistics, and properties of the column values in each block.

> *In the rest of this article, I will refer to physical metadata as “metadata.”*

Google also aims to store metadata for each column in every block. With the number of columns reaching 10,000 and the number of blocks reaching millions, the metadata size can reach tens of terabytes. Only storing these metadata might not be the problem; the real question is: How can these metadata be accessed and queried most efficiently?

[![](https://substackcdn.com/image/fetch/$s_!66m4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbadc4c38-03ec-43d6-8647-707fa5415aeb_1159x786.png)](https://substackcdn.com/image/fetch/$s_!66m4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbadc4c38-03ec-43d6-8647-707fa5415aeb_1159x786.png)

Image created by the author.

To address this challenge, Google organizes the metadata for each table into a set of metadata tables. This metadata layout is called CMETA. Data from the metadata table is organized in columnar orientation, which also leverages the Capacitor format like the data.

Google designed its metadata layout based on key observations. Thanks to the columnar structure, the amount of I/O is based on the number of columns referenced in the query rather than the entire table. Thus, they use a columnar format for metadata storage. Even though tables may have tens of terabytes of metadata, typically, only a few columns are referenced in any given query. This approach limits metadata access to just the relevant columns, improving efficiency. We will see this advantage in more detail in the following sections.

Each row in the metadata table tracks the metadata for each physical block, and each column tracks the metadata for each column in a block. The column-level metadata includes information such as the min/max column values or a dictionary of column values.

Before moving on, let’s define a dummy table that will be used for examples throughout this article:

[![](https://substackcdn.com/image/fetch/$s_!WwLf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99526d82-6e63-465a-a527-856621e484dc_1360x892.png)](https://substackcdn.com/image/fetch/$s_!WwLf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99526d82-6e63-465a-a527-856621e484dc_1360x892.png)

Image created by the author.

### Columnar Metadata

There was a predefined structure of the metadata from Google for the column primitive types:

[![](https://substackcdn.com/image/fetch/$s_!Z9PF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcecae4eb-24b8-408a-9e3a-bbf6858e9449_1360x744.png)](https://substackcdn.com/image/fetch/$s_!Z9PF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcecae4eb-24b8-408a-9e3a-bbf6858e9449_1360x744.png)

Refer to the “TYPE CMETATYPE“ in section 4.2 of the paper: [Big Metadata: When Metadata is Big Data](https://www.vldb.org/pvldb/vol14/p3083-edara.pdf) (2021)

As BigQuery supports nested (STRUCT) and repeated fields (ARRAY). There are recursive algorithms to build up the column metadata of its “child“ fields.

Using the dummy table described earlier, here is its associated CMETA table:

[![](https://substackcdn.com/image/fetch/$s_!GYyb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0b44256-92d8-4fb3-ba02-34d873a1485f_1360x930.png)](https://substackcdn.com/image/fetch/$s_!GYyb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0b44256-92d8-4fb3-ba02-34d873a1485f_1360x930.png)

Image created by the author.

### Query processing

To illustrate how BigQuery leverages CMETA for serving metadata, let's visit the example query that extracts some insight from the dummy table above:

[![](https://substackcdn.com/image/fetch/$s_!1lL1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f280f1a-ac22-41d1-a3bd-898cea8724ba_1360x296.png)](https://substackcdn.com/image/fetch/$s_!1lL1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f280f1a-ac22-41d1-a3bd-898cea8724ba_1360x296.png)

Image created by the author.

A basic approach for a processing engine handling this query would involve opening each block, reading the metadata from the header, applying filters, and then determining whether the block requires further processing.

However, performing open-read-close operations on millions of blocks is far from efficient. Instead, let’s explore how Google leverages distributed processing techniques through CMETA, significantly improving query performance by optimizing how metadata is handled and accessed.

Typically, metadata is accessed before query planning. However, loading the table metadata before query planning increases the query's runtime for tables with thousands to millions of blocks. This can cause delays ranging from milliseconds for 10GB tables to minutes for petabyte-scale tables. To address this, access to physical metadata is deferred until just before the workers begin scanning data from storage.

In the planning phase, the query planner generates the plan using only logical metadata, folding constants, and applying filters.

> *Constant folding is the process of recognizing and evaluating constant expressions at compile time rather than computing them at runtime. — [Wikipedia](https://en.wikipedia.org/wiki/Constant_folding#:~:text=Constant%20folding%20is%20the%20process,are%20known%20at%20compile%20time.) —*

The plan is then rewritten as a semi-join between the original query and CMETA (metadata) over the `_block_locator` column. This semi-join scans CMETA to identify which blocks need to be accessed based on filters from the original query. The start\_timestamp for the query reflects the snapshot timestamp, or for time-travel queries, a user-provided timestamp.

> *A [semi-join](https://www.geeksforgeeks.org/difference-between-anti-join-and-semi-join/) is a type of join that returns rows from one table where a match exists in another table, but unlike a full join, it does not return columns from the second table. The* `IN` *operator can be considered a form of **semi-join** in SQL*

[![](https://substackcdn.com/image/fetch/$s_!WSV8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9146819-ce6f-4087-bbb7-44d9cee8b27b_1360x632.png)](https://substackcdn.com/image/fetch/$s_!WSV8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9146819-ce6f-4087-bbb7-44d9cee8b27b_1360x632.png)

Image created by the author.

The subquery on CMETA is evaluated first, generating a list of necessary blocks. These are then passed to the original query, ensuring that only the identified blocks are processed, even if the table contains millions. If the column partitions the table, the number of blocks returned significantly reduces.

The advantage of columnar metadata is evident with this example, as only a few columns—such as `block_locator`, `orderTimestamp.min_value`, `orderTimestamp.max_value`,...—are read despite the metadata table potentially having up to 10,000 columns.

In the paper, Google also introduces their general framework for converting filter predicates from the `WHERE` clause of user queries into expressions that help identify which physical blocks can be skipped during query execution. For further details on this framework, you can explore [the paper](https://www.vldb.org/pvldb/vol14/p3083-edara.pdf) directly.

### Incremental Generation

When data in a BigQuery table is modified, new blocks are created at the block level, and the old blocks are marked as deleted. It is updated with every mutation to ensure the CMETA system remains the source of truth for a table’s metadata. BigQuery allows blocks to contain modified and unmodified rows, where only a subset of rows may be active at a given time.

A metadata change log records block mutations and additions, assigning timestamps for both creation and deletion. This log is stored in a highly available, durable system, ensuring ACID compliance for millions of block changes. A background process merges this log using LSM-style compaction, producing baselines and deltas of metadata changes stored as columnar Capacitor blocks. At any read timestamp, metadata is constructed by combining the baseline and incremental deltas.

After understanding how metadata helps the query engine skip unnecessary data blocks, we’ll explore additional use cases within the metadata system that enhance system performance through other processes.

## Joins

Star and snowflake schemas are common in data warehouses, where fact tables are typically much larger than dimension tables. Users extract insights by joining these tables and applying filters to the fact or dimension tables. Since dimension tables are small, scanning them usually takes little time. However, scanning large fact tables is challenging, especially if the filters are only applied to dimension tables.

[![](https://substackcdn.com/image/fetch/$s_!WXyO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff21acdbd-cbc9-4d21-a02d-afc27b65acdc_655x482.png)](https://substackcdn.com/image/fetch/$s_!WXyO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff21acdbd-cbc9-4d21-a02d-afc27b65acdc_655x482.png)

Image created by the author.

In such cases, Google uses the scan results from the dimension table to generate filter expressions for the fact table. Processing the system metadata for the fact table is delayed until these filters are computed. Once the filters are ready, they are applied to the fact table scan, allowing the system to use CMETA to skip unnecessary blocks efficiently, as if the filter had been explicitly defined for the fact table.

---

## Query Optimization

BigQuery's planner applies several optimizations based on the data's shape. The most fundamental is selecting the degree of parallelism for different query stages. More advanced optimizations are also applied, like choosing a join strategy (e.g., broadcast vs. hash join). Broadcast joins can be faster as they avoid shuffling large datasets but only work with small datasets that fit in memory.

Accurate cardinality estimates are essential for query planning but are often hard to obtain. To address this, BigQuery’s execution plan can adapt dynamically during runtime based on real-time data signals. For this dynamic scheme to work effectively, initial estimates must be not too different from the actual values. BigQuery uses per-column statistics from CMETA to generate these estimates, calculating the estimated query size by summing the bytes scanned from each table and the blocks remaining after pruning.

BigQuery's "dry-run" feature allows the users to estimate the data scanned without executing the query. This can also be achieved by querying metadata from CMETA.

[![](https://substackcdn.com/image/fetch/$s_!1o4D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4ee2843-e538-474d-a0a2-ec89c9c6f81a_592x96.png)](https://substackcdn.com/image/fetch/$s_!1o4D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4ee2843-e538-474d-a0a2-ec89c9c6f81a_592x96.png)

When you enter a query in the BigQuery console, the 'dry-run' feature estimates the data volume processed using metadata. Here's a screenshot from my random query.

---

## Outro

Storing and organizing data in a columnar format is the standard approach for managing analytics data. However, using the same columnar orientation for metadata was a novel concept when I first encountered it in Google’s paper.

This method allows them to store rich, fine-grained metadata that tracks detailed information at the lowest level without incurring the overhead typically associated with metadata management. The columnar structure enables them to leverage a distributed query engine that reads only the necessary columns, optimizing metadata access.

In my upcoming article, I will explore how Google leverages this metadata system to enhance functionality and deliver a unified, high-performance lakehouse feature called [BigLake](https://cloud.google.com/biglake?hl=en).

Now, see you in the next article ;)

---

## **References**

*[1] Pavan Edara, Mosha Pasumansky [Big Metadata: When Metadata is Big Data](https://www.vldb.org/pvldb/vol14/p3083-edara.pdf) (2021)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-8-hours-learning-how-google/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
