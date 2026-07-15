---
title: "OLTP vs OLAP: Data Format and Indexing"
channel: vutr
author: "Vu Trinh"
published: 2025-09-23
url: https://vutr.substack.com/p/oltp-vs-olap-data-format-and-indexing
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Delta Lake", "BigQuery", "Streaming"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# OLTP vs OLAP: Data Format and Indexing

*In just 15 minutes, you will understand the difference in how they organize and find the data.*

> Source: [Open post](https://vutr.substack.com/p/oltp-vs-olap-data-format-and-indexing)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=173485668)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!srEQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07e9be52-6518-44cd-ab6c-f3aa6e65394b_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!srEQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07e9be52-6518-44cd-ab6c-f3aa6e65394b_2000x1428.png)

---

## Intro

A database management system (DBMS) is one of the most robust software systems that has ever been created. A simple interface that lets you input a SQL query and returns a result in 17 seconds usually gives us the perception that the database (DBMS) is a simple system.

That’s not true. I read somewhere that the database engineers are among the most talented software engineers. To build a system like PostgreSQL, MySQL, SQLite, DuckDB, Clickhouse, BigQuery, or Snowflake, the engineers have to take care of a lot of things behind the scenes.

From storing the data to parsing the query, planning and executing it, serving multiple clients as one, ensuring ACID, and many other aspects. As I know, most DBMS don’t rely on the OS for controlling physical resources like disk, RAM, or CPU, so the amount of work is even more for the engineers.

We, as data engineers, like any other end users, don’t usually have to deal with the super low-level details of a DBMS. Still, understanding the characteristics of the systems we’re working with will always be a good thing. Our primary goal is to ensure that data is stored, analyzed, and utilized efficiently within the organization.

In this article, I will delve into one of the most important aspects of a DBMS: how it stores the data. We will examine two types of DBMS, which are the two primary ones that a data engineer usually works with: the OLTP and OLAP. We will find out how they organize and find the data

## Database vs database management system (DBMS)

A database is an organized and managed collection of data that models aspects of the real world. It can be as simple as a spreadsheet or a phone contact list.

A database management system (DBMS) is software that stores and analyzes information in a database. It supports the definition, creation, querying, updating, and administration of databases based on a data model.

## Relational model

The model can take various forms—graph, key-value, document, or the most popular one, the relational model, first described by [E.F. Codd in 1969](https://en.wikipedia.org/wiki/Relational_model). This model organizes data into structured tables, also known as relations, consisting of rows and columns.

[![](https://substackcdn.com/image/fetch/$s_!OeRh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F219b3e44-b5d8-45b6-8008-0130da3768b8_428x262.png)](https://substackcdn.com/image/fetch/$s_!OeRh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F219b3e44-b5d8-45b6-8008-0130da3768b8_428x262.png)

Each table represents a specific type of entity, such as 'users' or 'orders,' with rows (tuples) representing individual records and columns (attributes) defining properties of those records, like name, age, or order date.

The data model only enforces the logical representation of the data; it does not dictate how the DBMS stores the data physically. Relational DBMSs are free to determine the data layout on disk.

## The workload of OLTP and OLAP systems

Data on disk is essentially just a series of 0s and 1s, and it is the DBMS's responsibility to organize and manage how this data is written to disk to ensure efficient write and read operations.

However, the efficiency of a data layout must be evaluated depending on the workload. Database workloads can generally be categorized into two main types:

[![](https://substackcdn.com/image/fetch/$s_!kX_X!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb85eac70-67ca-4693-bdf3-c83b1267b0ff_600x360.png)](https://substackcdn.com/image/fetch/$s_!kX_X!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb85eac70-67ca-4693-bdf3-c83b1267b0ff_600x360.png)

* The **OLTP** workload ingests new information; its data operations mostly read/write/update a small amount of data each time. Typically, the OLTP system is first built in a company to capture information from the real world. Examples include the database behind web applications and the database that records banking transactions. The workload might be more familiar to those working closely with the company’s product/service, such as the backend developers.
* The **OLAP** workload has different characteristics from the OLTP workload. Its queries require reading data from many tables (via joins). After obtaining the data, numerous aggregations may be necessary to extract insights or identify new patterns. In most cases, OLAP workloads are executed on data collected from OLTP systems. This workload might be more familiar to those in the company’s data analytics functions, such as data engineers or analysts.

## How do they organize the data?

The DBMS organizes data in a way that optimally benefits each workload. To achieve this, there are three storage models used for data organization:

* The row store.
* The column store.
* The hybrid

### OLTP

To serve its workload, most OLTP systems usually organize the data in a row-based fashion. The DBMS stores all the values of all columns for a single row together in a page.

[![](https://substackcdn.com/image/fetch/$s_!5RW2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd341f547-0b78-487a-8480-2ad54f74a277_590x380.png)](https://substackcdn.com/image/fetch/$s_!5RW2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd341f547-0b78-487a-8480-2ad54f74a277_590x380.png)

> ***Note**: The term 'page' refers to an atomic data unit; all data within a page is either read or written successfully, or none of the page's data is read or written. In a DBMS, a page can refer to hardware pages, OS pages, or database pages.*
>
> *To align with the underlying hardware, the database page is typically a constant multiple of the 4KB hardware page. (e.g., 32KB). From the rest of the article, I use “page“ to refer to the database page.*

From a data writing perspective, this is optimal when data needs to be written to the system as quickly as possible. For a single row, the writer needs to write the bytes from different columns sequentially (sequential operation is always fast).

[![](https://substackcdn.com/image/fetch/$s_!m9IB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20b5ffe4-d4ce-4858-b0d5-23a36010d864_630x238.png)](https://substackcdn.com/image/fetch/$s_!m9IB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20b5ffe4-d4ce-4858-b0d5-23a36010d864_630x238.png)

From the reading perspective, the data organization also serves well for the OLTP workload. A whole row usually needs to be read; again, the sequential operation can take place here as all of the bytes for a single row are stored together.

[![](https://substackcdn.com/image/fetch/$s_!cvYD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca27b11a-0bee-4f0c-a9e6-0abd788f0713_712x352.png)](https://substackcdn.com/image/fetch/$s_!cvYD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca27b11a-0bee-4f0c-a9e6-0abd788f0713_712x352.png)

### OLAP

With OLAP, the workloads are different. Typically, the OLAP systems are more focused on the reading side, where a large amount of historical data needs to be brought up for aggregation and joins. In most cases, a subset of columns only needs to be scanned. This characteristic causes us issues when handling the OLAP workload on the OTLP system (which uses row-format storage).

Imagine we have a table with 10 columns. All column values from a single row are stored continuously. An OLAP query that reads two columns: date and sales, then calculates the SUM of sales by date.

With the row-store, we have to load the whole row into memory; only then can the system extract data from the two columns. Let’s say the table has 1 million rows; the system overhead should be huge.

The solution is to store data from a single column continuously. There are two main approaches: the column store and the hybrid.

#### Column store

The first approach stores data from a single column separately. The problem from the example above is now solved; the system only needs to care about the pages that store data and sales data, thereby avoiding the loading of redundant data from other columns.

[![](https://substackcdn.com/image/fetch/$s_!i9EB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de8ae1d-8f17-4c33-bc70-76398b68cbc1_490x366.png)](https://substackcdn.com/image/fetch/$s_!i9EB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de8ae1d-8f17-4c33-bc70-76398b68cbc1_490x366.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=173485668)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

However, there is another thing the system must manage in this approach, which is the data offset. Because a row of data is stored in multiple places, there must be a way for the DBMS to know which row a specific column value in a page belongs to. To address this, the DSM ensures that each value in a column has the same length. This allows the DBMS to easily calculate the offset of specific values using the fixed value size.

[![](https://substackcdn.com/image/fetch/$s_!cEvy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ac7f899-4aee-42d0-93a6-145b45e410cc_774x524.png)](https://substackcdn.com/image/fetch/$s_!cEvy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ac7f899-4aee-42d0-93a6-145b45e410cc_774x524.png)

This storage model reduces wasted I/O per query, as the DBMS only reads data from the columns it needs. Additionally, it allows for better data compression, as column values often exhibit patterns. You can find this approach in Clickhouse or Redshift.

However, this model might cause some problems with writing operations. When writing to a table with 100 columns, the DBMS would need to jump around and write the data to 100 separate locations, resulting in significant overhead.

In addition, the read operations that require reading all column data give the system more work to do as the DBMS would have to consolidate data from 100 places.

[![](https://substackcdn.com/image/fetch/$s_!FdxH!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed9e52f8-4ff0-4c9f-b2dc-03c1d232fcbb_1102x414.png)](https://substackcdn.com/image/fetch/$s_!FdxH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed9e52f8-4ff0-4c9f-b2dc-03c1d232fcbb_1102x414.png)

The hybrid format comes to the rescue.

#### Hybrid

In this storage model, table data is horizontally split into row groups, with the columns' data stored next to each other within each group. The goal is to benefit from fast and efficient data scan on the column store while maintaining the locality of the row store (column values from the same row stay close together, at least in the row group).

[![](https://substackcdn.com/image/fetch/$s_!AOqG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04d7bf70-3e00-420c-bee7-fc1907a83991_510x630.png)](https://substackcdn.com/image/fetch/$s_!AOqG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04d7bf70-3e00-420c-bee7-fc1907a83991_510x630.png)

Based on my observation, this approach is more common than the column store, as seen in numerous systems, including BigQuery, Snowflake, DuckDB, Parquet, ORC, etc.

### The OLAP systems with heavy write

In recent years, I have observed more OLAP systems supporting real-time analytics capability. A bold example is BigQuery, where the engineers decided to rebuild the storage engine that treats streaming data ingestion as a first-class citizen. The high-level approach looks like this:

[![](https://substackcdn.com/image/fetch/$s_!V4P5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff781025e-969e-47a5-afb7-06a9ea257d11_850x372.png)](https://substackcdn.com/image/fetch/$s_!V4P5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff781025e-969e-47a5-afb7-06a9ea257d11_850x372.png)

* Data is ingested into row-store format.
* For consumption, data is converted to the column/hybrid format in the background.

I also see this pattern in Apache Hudi. The advantage of this approach is the separation of concerns for the two operations. However, it comes with operational complexity. Luckily, most of the systems are managing this for us. Due to information limitations, I have found that BigQuery and Hudi are the only ones implementing this approach.

That said, I believe many other systems are already using — or at least considering — this approach, especially since OLAP workloads are constantly evolving, with trends like real-time ingestion and querying

## How do they find the data?

So, we learn how they store the data. The next question is: how do they find it? Again, the strategy a database employs to locate data is a determinant of its workload.

OLTP systems, which are asked to "find this one specific thing," require a precise, map-like approach. OLAP systems, which are asked to "summarize these few attributes across everything," demand a method of efficient data elimination.

### OLTP

For OLTP, you will commonly see a B-Tree index used to locate a piece of data. For decades, it has been the main approach to optimizing performance for OLTP databases.

> ***Note:** In the scope of this article, I won’t delve too much into the B-Tree. I think we will need a dedicated article because the index itself has many aspects to discuss.*

A B-Tree is a self-balancing tree data structure that maintains sorted data, allowing for searches, insertions, and deletions in O(logn). It divides the database into fixed-size pages (e.g., [PostgreSQL is 8 KB](https://www.postgresql.org/docs/current/storage-page-layout.html#STORAGE-PAGE-LAYOUT)). One page is read or written at a time. The pages form a tree structure:

There will be three types of pages in the B-Tree:

[![](https://substackcdn.com/image/fetch/$s_!-vkG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff70e285a-7cf4-4c72-8b52-6796fd0f8e19_662x418.png)](https://substackcdn.com/image/fetch/$s_!-vkG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff70e285a-7cf4-4c72-8b52-6796fd0f8e19_662x418.png)

* **Root page**: It has no parents and acts like the entry point for the three.
* **Internal pages**: They link the root and the leaf pages
* **Leaf pages**: They are the bottom pages and don’t have child pages. All the data is stored at leaf pages.

> ***Note**: In the classic B-Tree implementation, the data can be stored in non-leaf pages. In the variant B+ Tree, only the leaf pages hold the data. This enables all data operations to focus solely on the leaf pages. B+ Tree has been widely adopted and is usually referred to as the B-Tree. This article also describes the implementation of the B+ Tree, where data is only stored in leaves.*

For non-leaf pages, they store:

* The keys, which are the index column values. A non-leaf page will have a continuous range of sorted keys (sorting to enable binary searching).

  [![](https://substackcdn.com/image/fetch/$s_!Hao9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21ecfd8-258e-43be-b4d1-0176b9cebd94_1224x374.png)](https://substackcdn.com/image/fetch/$s_!Hao9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21ecfd8-258e-43be-b4d1-0176b9cebd94_1224x374.png)
* The pointers that point to other pages.
* The keys and the pointers are related to each other: the number of pointers is equal to the number of keys + 1.
* The pointer will point to a subtree that has keys in the range of [ key\_left, key\_right). For example:

  [![](https://substackcdn.com/image/fetch/$s_!XgEn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F977c2df2-9458-4b15-9d0c-f20a566ed8ea_1018x432.png)](https://substackcdn.com/image/fetch/$s_!XgEn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F977c2df2-9458-4b15-9d0c-f20a566ed8ea_1018x432.png)

With B-Tree, the data operations boil down to finding the required data in the B-Tree. Reading and updating data are similar processes. In more detail, the process of finding data in the BTree looks like this:

[![](https://substackcdn.com/image/fetch/$s_!U02I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8895e7ca-9529-4302-a42b-110f9a02dd01_856x438.png)](https://substackcdn.com/image/fetch/$s_!U02I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8895e7ca-9529-4302-a42b-110f9a02dd01_856x438.png)

* A query with a filter on the index column, it could be a point look-up or range filter (=, <, >, between), such as fetching a customer by their ID. (This query is ubiquitous in OLTP workload)
* A search operation begins at the root page of the tree.
* The database compares the search value against the keys stored in the page to determine which child pointer to follow.
* This process is repeated, descending one level at a time, until it reaches the leaf page that has the required data.

### OLAP

As you can see from the above section, the BTree index boosts point-look-up and range scan queries. When you use WHERE username = “bruce\_banner,” the index will tell you exactly where to find records with the username “bruce\_banner.”

However, a look-up index won’t help much in OLAP. Faced with queries that scan billions of rows, the performance bottleneck is not locating a single record but minimizing the volume of data that must be read from storage and processed. The primary optimization method is to avoid reading irrelevant data as much as possible in the first place.

Columnar storage allows the engine to read the required columns without touching others. Although this new layout helps, researchers want to skip irrelevant data at a finer-grained level.

#### Lightweight Metadata

The metadata that enables this process is often referred to as a "Zone Map" or simply as block-level statistics. For each data chunk and for each column within that chunk, the system stores key metrics, most commonly the minimum and maximum values. Other statistics may include a count of null values, a count of distinct values, or more sophisticated data structures like Bloom filters for existence checks.

[![](https://substackcdn.com/image/fetch/$s_!DbY4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d56d61-de30-43b1-8c52-b516a062eefe_512x504.png)](https://substackcdn.com/image/fetch/$s_!DbY4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d56d61-de30-43b1-8c52-b516a062eefe_512x504.png)

Consider a table of sales data partitioned into monthly files, with a Zone Map for each file tracking the min/max `click_counts`. A query asking for click counts (`WHERE click\_counts BETWEEN 5 AND 7`) would cause the query optimizer to scan the metadata first. It would immediately discard all the blocks of data that don’t have `click\_counts` between 5 and 7.

Only the blocks whose click counts lie in the range of 5 and 7 would be read from disk, dramatically reducing the scope of the scan. You can find the approach to lightweight metadata for most of the OLAP systems:

* [Parquet with statistics in Row Group and Column Chunk metadata](https://vutr.substack.com/i/147908704/how-is-data-written-in-the-parquet-format). (ORC file format also does the same)
* [Iceberg with statistics recorded in the metadata files](https://vutr.substack.com/p/i-spent-7-hours-diving-deep-into). (Hudi and Delta Lake also do the same)
* [Google even built a dedicated system to manage this kind of metadata for BigQuery.](https://vutr.substack.com/p/i-spent-8-hours-learning-how-google)
* …

Next, we will discuss the two approaches that are related to how data is stored physically.

#### Partitioning

Essentially, partitioning divides a dataset into smaller portions. Its ultimate goal (like what we’re discussing) is to reduce data scanning by skipping irrelevant portions. Most of the systems allow users to partition data at a higher level.

We can specify a column that will enable the system to break the data using its value to partition the table into smaller ones. A date column will break the table into partitions for 2025-05-01, 2025-05-02, 2025-05-03, and so on.

[![](https://substackcdn.com/image/fetch/$s_!eFKa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)](https://substackcdn.com/image/fetch/$s_!eFKa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)

Partitioning helps the system operate only on the relevant portion. If a query includes a filter predicate on the partition key (e.g., `WHERE date=2025-05-03`), the query optimizer can identify that only the partition date=2025-05-03 (given the table is partitioned by the day column) is relevant and can completely ignore, or "prune," all others.

[![](https://substackcdn.com/image/fetch/$s_!s-2C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d048052-1ef7-4d17-b18d-5af7840f677f_818x426.png)](https://substackcdn.com/image/fetch/$s_!s-2C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d048052-1ef7-4d17-b18d-5af7840f677f_818x426.png)

BigQuery and most other warehouse systems treat a partition as a virtual table. Data from a partition will be stored separately from the data of different partitions. This allows features like data expiration, data insertion, and data deletion to be executed effectively at the partition granularity (because it’s similar to a table). Each partition will have its associated metadata, allowing the engine to leverage it for data pruning.

For Snowflake, things got different, instead of letting the user specify the partition as the unit of data management. Snowflake automatically splits the tables into micro-partitions, each of which stores between 50 MB and 500 MB of uncompressed data.

[![](https://substackcdn.com/image/fetch/$s_!XZnj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F138aaeda-11f3-410e-94fa-259189fd5cde_760x350.png)](https://substackcdn.com/image/fetch/$s_!XZnj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F138aaeda-11f3-410e-94fa-259189fd5cde_760x350.png)

The micro partitions are organized similarly to the hybrid format, in which a partition contains a group of rows, and each column of data is stored together in each partition. Snowflake manages metadata for columns in the micro-partition to facilitate data management.

When explicitly managing the storage layer by yourself, we will observe a common approach to organizing data in a Hive-style manner, where data is organized into folders:

[![](https://substackcdn.com/image/fetch/$s_!X0ol!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36647065-ebe4-45e0-909f-c929d3ca1996_508x342.png)](https://substackcdn.com/image/fetch/$s_!X0ol!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36647065-ebe4-45e0-909f-c929d3ca1996_508x342.png)

* Table: Each table has a directory.
* Partitions: Each table can have partitions. Each partition corresponds to a subdirectory.

This scheme is straightforward and has been widely adopted since its introduction. The later generation of table formats, such as Delta Lake, Iceberg, or Hudi, although users still see this partition scheme, they add more robust metadata behind the scenes to improve performance and efficiency.

#### Clustering

Like partitioning, the goal of clustering is to help the engine skip unnecessary data. However, it takes a different approach. While partitioning provides a coarse-grained mechanism for data skipping, its effectiveness is limited by the cardinality of the partition key.

To enable finer-grained query optimization, many systems use clustering. If you partition the table, clustering organizes related data together within partitions; if not, clustering occurs at the table level.

The most straightforward way to achieve this is to **sort** and store the data based on one or more columns. This sorting ensures that rows with similar or identical values in the clustering columns are co-located, meaning they are more likely to be written together into the same data unit on disk.

[![](https://substackcdn.com/image/fetch/$s_!Cq1S!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9898a382-b396-4a36-b579-d2c952713fd3_884x530.png)](https://substackcdn.com/image/fetch/$s_!Cq1S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9898a382-b396-4a36-b579-d2c952713fd3_884x530.png)

However, sorting does not work so well when you specify more than one column for the sorting. The system will sort the data based on the order of the clustering columns. Now, your queries need to align with the sorting order. Imagine you want to sort the data based on Column A, then Column B. The WHERE filter must follow this order: Column A first, then Column B. If you only filter based on Column B, you won’t benefit from the sorting.

Let's examine an example where the table has the following `device\_id` and `customer\_id`, each with possible values of `[100, 101, 102, 103]`. After sorting based on device\_id and customer\_id, we organized the data into four files:

[![](https://substackcdn.com/image/fetch/$s_!cZM6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b402d96-ed18-4da6-90d3-67888c95842f_928x418.png)](https://substackcdn.com/image/fetch/$s_!cZM6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b402d96-ed18-4da6-90d3-67888c95842f_928x418.png)

* File 1:

  + device\_id = 100
  + 100 <= customer\_id <= 103
* File 2:

  + device\_id = 101
  + 100 <= customer\_id <= 103
* File 3:

  + device\_id = 102
  + 100 <= customer\_id <= 103
* File 4:

  + device\_id = 103
  + 100 <= customer\_id <= 103

If we filter device\_id = 100, the number of files needed to scan is 1 (file 1). The filter device\_id = 100 AND customer\_id = 102 also needs to scan only file A. However, if the filter only contains customer\_id = 101, the engines need to scan all four files

That’s why there are multi-dimensional clustering techniques to help distribute the data more efficiently (the most prominent implementations are Z-ordering). These techniques, based on the mathematical concept of space-filling curves, aim to preserve data locality across multiple dimensions (columns).

For more details on the clustering techniques, you can read my previous article [here](https://vutr.substack.com/i/166732941/clustering).

## Outro

In this article, we first understand the difference between a database and a DBMS, then we come to the relational model and the difference between OLTP and OLAP workloads.

From those fundamentals, we continue to explore how data is organized in these two systems. The row-store is best suited for the OLTP workloads, thanks to its performance for data writing and reading a whole record at a time. However, it is not suited for OLAP workloads.

That’s where the column store and hybrid store come in. Finally, we discover the main approach for systems to find the data efficiently. For OTLP, the main approach is the BTree index. With OLAP, the primary methodology is to limit the amount of scanned data as much as possible. There are three main approaches: metadata, partitioning, and clustering.

Other aspects need to be discussed more, such as how they handle data mutation and data encoding/compression. We will have another article to discuss these aspects.

Thank you for reading this far.

## Reference

*[1] Andy Pavlo, CMU Database, [#05 - Row vs. Column Storage + Compression](https://www.youtube.com/watch?v=nhlpwmOBEiE&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=7)*

*[2] Martin Kleppmann, [Designing Data-Intensive Applications, Chapter 3. Storage and Retrieval, B-Tree section](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)*
