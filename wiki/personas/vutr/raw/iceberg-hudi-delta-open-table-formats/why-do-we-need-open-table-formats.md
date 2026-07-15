---
title: "Why do we need open table formats like Delta Lake or Iceberg?"
channel: vutr
author: "Vu Trinh"
published: 2025-05-27
url: https://vutr.substack.com/p/why-do-we-need-open-table-formats
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming", "Data Quality", "ETL"]
tags: [https, auto, media, good, substackcdn, image]
---

# Why do we need open table formats like Delta Lake or Iceberg?

*The hope of data lake + table format = data warehouse*

> Source: [Open post](https://vutr.substack.com/p/why-do-we-need-open-table-formats)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=164015666)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!RgsF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ae4706a-66fe-4b6c-8f75-e24aa53fa3fc_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!RgsF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ae4706a-66fe-4b6c-8f75-e24aa53fa3fc_2000x1429.png)

---

## Intro

When I started self-learning for a data job 6 years ago, most resources on the Internet suggested that a data architecture should have two tiers, one to dump raw data to (the lake) and one to store clean data that’s ready for consumption (the warehouse)

Today, if you want to check the best approach to store, manage, and serve data, you still might see the two-tier architecture somewhere, but the one you start to see more and more is the lakehouse paradigm.

Following that are calls from nearly everywhere to equip yourself with the knowledge and hands-on experience of open table formats, the backbone of the lakehouse.

That makes me curious. Why?

I conducted a small research study, and this article is my note to answer the following questions: why the lakehouse is gaining popularity, and how the open table format, such as Delta Lake or Iceberg, fits into this story.

We will begin this article by learning the motivation behind the data warehouse, the data lake, and the lakehouse. Next, we examine Apache Hive and the emergence of modern table formats.

---

## The data warehouse

Imagine a scenario like this.

You are the first member of the data team. Your boss asks you to create reports for the business team based on the data collected from the company's product.

[![](https://substackcdn.com/image/fetch/$s_!cQjv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01d04ce-ec51-4c64-ab4f-078b21255fd3_438x194.png)](https://substackcdn.com/image/fetch/$s_!cQjv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01d04ce-ec51-4c64-ab4f-078b21255fd3_438x194.png)

At first, things are simple.

[![](https://substackcdn.com/image/fetch/$s_!-3ic!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c37cfa1-2ddf-4e19-a273-fd833802e9cb_368x252.png)](https://substackcdn.com/image/fetch/$s_!-3ic!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c37cfa1-2ddf-4e19-a273-fd833802e9cb_368x252.png)

There is only one database that records transactional data; you extract data directly from it, do some transformation, and voilà.

[![](https://substackcdn.com/image/fetch/$s_!JosI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6436351c-dba4-40a5-bd41-2c20a378db16_396x202.png)](https://substackcdn.com/image/fetch/$s_!JosI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6436351c-dba4-40a5-bd41-2c20a378db16_396x202.png)

Then, the company starts using a third-party service, and business users request data from this service to be included in reports. That’s still manageable.

[![](https://substackcdn.com/image/fetch/$s_!7rcA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa37f3ae3-3673-4b21-a945-086f66659c44_378x270.png)](https://substackcdn.com/image/fetch/$s_!7rcA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa37f3ae3-3673-4b21-a945-086f66659c44_378x270.png)

You pull data from the database and the third-party API, perform some joins and aggregates, and you can still provide the reports users need.

[![](https://substackcdn.com/image/fetch/$s_!XbcT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42f209e-1ad2-489f-9e49-499cbea41ddf_400x288.png)](https://substackcdn.com/image/fetch/$s_!XbcT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42f209e-1ad2-489f-9e49-499cbea41ddf_400x288.png)

But over time, your company has more services and integrates with external tools, each generating its own data. End users want all this data incorporated into their reports.

[![](https://substackcdn.com/image/fetch/$s_!f427!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8095e907-2b15-44e9-9871-882529113434_444x280.png)](https://substackcdn.com/image/fetch/$s_!f427!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8095e907-2b15-44e9-9871-882529113434_444x280.png)

At this point, you **can't** pull data from every source to compile the report like you used to. You need a more strategic approach. You need a data warehouse.

[![](https://substackcdn.com/image/fetch/$s_!HtYs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22e0ad8c-9e53-4ee9-8b71-f01d7d1854f3_724x428.png)](https://substackcdn.com/image/fetch/$s_!HtYs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22e0ad8c-9e53-4ee9-8b71-f01d7d1854f3_724x428.png)

It is a repo where we can centralize, store, and manage large amounts of data from multiple data sources to serve the company's analytics workload.

Data is extracted from many sources, transformed into a predefined structure (schema-on-read), and loaded directly into the data warehouse. The data warehouse helps businesses and organizations manage data by providing a centralized repository for data storage and retrieval.

[![](https://substackcdn.com/image/fetch/$s_!FA4b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb598e808-91b0-4a4e-9fc5-1f8a6f05f5d7_650x350.png)](https://substackcdn.com/image/fetch/$s_!FA4b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb598e808-91b0-4a4e-9fc5-1f8a6f05f5d7_650x350.png)

However, the data warehouse soon showed its limitations. Due to the rise of the Internet, the number of digital records has increased enormously. People realized they needed to collect, store, and process more data. Tabular data might not be enough; videos, documents, and images are also precious resources.

The data warehouse systems, primarily row-based relational databases at the time, did not readily adapt to the organization's needs. Data must be in a well-structured schema before loading into the warehouse. That’s caused an organizational problem: They still want a “single entry point“ for data management, but the data warehouse can’t handle unstructured data well.

---

## The data lake

Let’s store all the data elsewhere.

[![](https://substackcdn.com/image/fetch/$s_!O0XI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffae5a02-d3a2-4f42-af1c-4b8af880179d_298x232.png)](https://substackcdn.com/image/fetch/$s_!O0XI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffae5a02-d3a2-4f42-af1c-4b8af880179d_298x232.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=164015666)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

In the early 2000s, major tech companies like Yahoo and Google led the big data trend. At first, these companies continued to rely on traditional warehouses for data centralization. However, these systems struggled with data growth in both volumes and formats.

Yahoo developed Apache Hadoop to handle large datasets. It includes processing (MapReduce) and storage (HDFS) based on Google's two papers, [MapReduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) and [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf).

The data lake is a concept that describes the process of storing a vast amount of data in its native format (in HDFS or later in cloud object storage).

[![](https://substackcdn.com/image/fetch/$s_!meyG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01d0c8d8-ea8a-49a2-ad3b-6fb4fcf4d59d_622x316.png)](https://substackcdn.com/image/fetch/$s_!meyG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01d0c8d8-ea8a-49a2-ad3b-6fb4fcf4d59d_622x316.png)

Unlike traditional data warehouses, the data lake doesn’t require us to define the schema beforehand, so all data, including unstructured data, can be stored in the lake without concern about the constraint format.

With the lake, we can deal with the data source problem. However, for serving, only a data lake does not entirely replace the function of the data warehouse. In the data warehouse, data is organized neatly with the “table“ abstraction, streamlining nearly everything from access control to data consumption.

[![](https://substackcdn.com/image/fetch/$s_!_-As!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F381d4432-6da3-4c11-96e7-e41bc89eeec6_430x302.png)](https://substackcdn.com/image/fetch/$s_!_-As!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F381d4432-6da3-4c11-96e7-e41bc89eeec6_430x302.png)

People took this for granted until they attempted to replace the data warehouse entirely with the data lake. In the data lake, data is just a bunch of files. The lake lacks proper data management features, such as data discovery, data quality and integrity guarantees, ACID constraints, and data DML support, that are typically found in warehouses.

[![](https://substackcdn.com/image/fetch/$s_!MPQs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2969526-3f0a-40df-8e45-21e879735efd_744x380.png)](https://substackcdn.com/image/fetch/$s_!MPQs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2969526-3f0a-40df-8e45-21e879735efd_744x380.png)

Combining the data lake and the data warehouse is a better option. The two-tier architecture with the lake still allows us to ingest raw data in any format without concern for the predefined schema. Later, a subset of data is transformed and loaded into the warehouse system for reporting and analysis. Advanced use cases like machine learning can still access raw data in the data lakes.

Combining the data lake and the data warehouse is a better option, but some have suggested that this can be achieved without having two separate systems.

Someone from Meta.

---

## The data lakehouse

### The early effort

The mismatch of data management abstraction between the data lake and the data warehouse requires a typical data architecture at that time to have two systems to leverage the advantages of each one.

[![](https://substackcdn.com/image/fetch/$s_!33zo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8277e741-f88f-4e79-824f-2c112b8bd7f9_646x210.png)](https://substackcdn.com/image/fetch/$s_!33zo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8277e741-f88f-4e79-824f-2c112b8bd7f9_646x210.png)

In 2009, Meta released [a paper](https://www.vldb.org/pvldb/vol2/vldb09-938.pdf) introducing Apache Hive, *an open-source data warehousing solution built on top of Hadoop.*Hive has attempted to address two problems: the first is to translate SQL statements into MapReduce jobs, and the second, more closely related to our discussion, is to introduce table abstraction to the data lake. Apache Hive was a crucial component of the Hadoop data stack at the time, with the support of many systems due to its simple data model. We will dive more into Hive in the following section.

Meta tried to merge the lake and the warehouse by bringing the compute to the data. Google also thought that it was a good idea. [In a paper](https://storage.googleapis.com/gweb-research2023-media/pubtools/5750.pdf), they talked about “situ data processing, “ which refers to accessing data in its original place. Google observed several factors that lead to the transition from data warehouses to a lake-oriented architecture for analytics:

* Consuming data from many data sources
* Eliminating the ETL-based ingestion process from the data source systems to the warehouse
* The ability to use different query engines on top of the data.

Google built [Dremel](https://storage.googleapis.com/gweb-research2023-media/pubtools/5750.pdf) with this vision. It first started as an internal interactive data analysis system, and later, Google offered it publicly as part of BigQuery.

Big companies like Google or Meta invest a significant amount of time in combining the best aspects of data lakes and data warehouses. But it seems like this is still the story of the big players.

### Lakehouse came to the world

[![](https://substackcdn.com/image/fetch/$s_!mViv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4d06b22-95e2-4123-85e7-23ef146421c0_636x160.png)](https://substackcdn.com/image/fetch/$s_!mViv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4d06b22-95e2-4123-85e7-23ef146421c0_636x160.png)

It was not until 2020 that Databricks published a paper introducing the term “lakehouse,” which refers to a data management system based on low-cost storage that enhances traditional analytical DBMS management and performance features.

[![](https://substackcdn.com/image/fetch/$s_!jo5x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b57e3cc-8fb1-41e5-b64d-bd39e80505ef_1104x354.png)](https://substackcdn.com/image/fetch/$s_!jo5x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b57e3cc-8fb1-41e5-b64d-bd39e80505ef_1104x354.png)

Databricks highlighted the challenges of the two-tier architecture at that time

* Maintaining consistency between the data lake and warehouse is challenging and costly.
* The data in the warehouse is stale compared to that of the data lake
* Limited support for advanced analytics
* High total cost of ownership with ETL pipelines, double storage cost, …

They believed Lakehouse could solve these problems. A giant storage (object storage) that can store your data infinitely (except for your budget), and you can bring any query engine to the party. You will have more control over the data and have the flexibility of choosing the query engine.

However, Lakehouse has its own set of challenges.

### Lakehouse challenges

To make the data lake operate like a warehouse, we need to … bring the warehouse capability to the lake.

The most challenging problem is the one mentioned in the data lake section: The abstraction mismatch between the lake and the warehouse. Thus, the lake misses proper data management features, such as data discovery, data quality and integrity guarantees, ACID constraints, and data DML support.

[![](https://substackcdn.com/image/fetch/$s_!H7TL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9617341f-dd15-486b-a851-aa3d1be91a04_544x446.png)](https://substackcdn.com/image/fetch/$s_!H7TL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9617341f-dd15-486b-a851-aa3d1be91a04_544x446.png)

Query performance is another concern. Initially, a data warehouse is aware of the data it will process, so there is a high chance it will produce a more optimized query plan. With “bringing the query engines to the data”, the time when the engines process the data is the first time they see the data.

[![](https://substackcdn.com/image/fetch/$s_!j1Rc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89721425-bc0f-4c72-80fa-11d47f25addf_592x246.png)](https://substackcdn.com/image/fetch/$s_!j1Rc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89721425-bc0f-4c72-80fa-11d47f25addf_592x246.png)

When building Dremel to process data on the lake, Google saw [an order-of-magnitude performance degradation](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf). Databricks enhanced Spark with [the Photon engines](https://dl.acm.org/doi/10.1145/3514221.3526054) to efficiently deal with the Lakehouse workload.

—

Databricks suggested that, besides storage and compute, a lakehouse must have a metadata layer that sits between them. This layer will provide a robust table abstraction atop files in the lake, solving most of the problems we discussed. For the performance, this layer also provides more information for the query planning process. A way to make the data as “seen“ for different query engines.

[![](https://substackcdn.com/image/fetch/$s_!94jh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb9eeab3-265f-48f2-ad66-79c6bf6d603b_540x438.png)](https://substackcdn.com/image/fetch/$s_!94jh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb9eeab3-265f-48f2-ad66-79c6bf6d603b_540x438.png)

[Meta](https://www.vldb.org/pvldb/vol2/vldb09-938.pdf), [Uber](https://www.uber.com/en-VN/blog/hoodie/), and [Netflix](https://www.alluxio.io/videos/apache-iceberg-a-table-format-for-hige-analytic-datasets) also thought that was brilliant.

[In 2005, researchers from Microsoft,](https://arxiv.org/pdf/cs/0502008) the University of California, Berkeley, and Johns Hopkins University outlined a vision for scientific data management, combining databases and file systems to query petabyte-scale datasets. They also emphasized the importance of the metadata layer:

> *If the data is to be analyzed by generic tools, the tools need to “understand” the data. You cannot just present a bundle of bytes to a tool and expect the tool to intuit where the data values are and what they mean. The tool will want to know the metadata. — [Source](https://arxiv.org/pdf/cs/0502008)*

The following section will examine one of the earliest known attempts to provide this metadata layer.

---

## Apache Hive

> *We won’t discuss HiveSQL, which is designed to translate SQLs into MapReduce jobs.*

### Overview

Meta (then known as Facebook) initially [developed Apache Hive](https://www.vldb.org/pvldb/vol2/vldb09-938.pdf) to make HDFS and MapReduce a comprehensive warehouse solution.

With Hive, data is organized into folders:

* Table: Each table has an HDFS directory.
* Partitions: Each table can have partitions. Each partition corresponds to a subdirectory.

A `sales` table, which is partitioned by `date`, will have the following structure in Hive.

[![](https://substackcdn.com/image/fetch/$s_!bgeU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66118f49-9cdb-4184-ba65-fec546ad8461_402x394.png)](https://substackcdn.com/image/fetch/$s_!bgeU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66118f49-9cdb-4184-ba65-fec546ad8461_402x394.png)

* Table: root/folder\_1/**sales**
* Partitions: root/folder\_1/**sales/date=2025-01-01,** root/folder\_1/**sales/date=2025-01-02,** …

The table’s data is tracked at the directory level. Hive handles this tracking via the Hive Metastore, which is essentially a transactional database.

The most apparent advantage of Hive is its simplicity. Since it was open-sourced, it has evolved to support most processing engines. In addition, Hive is file-format agnostic.

### Problems

However, Hive soon showed its limitations.

Here are some common Hive problems when I do the research

**The first issue is the mismatch in transaction guarantees between the two systems**. Users can adjust the partition information in a transactional manner because they manage it via the Hive metastore, which is backed by a transactional relational database. However, the filesystem manages the data (Hive was built for HDFS), which does not guarantee any transaction. A file may contain corrupted data if the write process is interrupted before completion.

[![](https://substackcdn.com/image/fetch/$s_!X2r3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d930791-dfaf-4f9e-b359-5be1112c4c02_622x328.png)](https://substackcdn.com/image/fetch/$s_!X2r3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d930791-dfaf-4f9e-b359-5be1112c4c02_622x328.png)

Initially, Hive only allowed users to modify data at the partition level by copying the entire partition to a new location. Users would modify the data while replicating the partition and then update the partition’s location in the metastore to reflect the new location. This is inefficient when a small data change requires copying the entire partition.

Later, [Hive supports ACID guarantees only for ORC format in version 0.14.0](https://hive.apache.org/docs/latest/283118453/).

**The second issue is concurrent writing,** which is closely related to the first one.

[![](https://substackcdn.com/image/fetch/$s_!zRkJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f52b0cd-d6bc-42c4-83dc-e2a26bbc656c_252x332.png)](https://substackcdn.com/image/fetch/$s_!zRkJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f52b0cd-d6bc-42c4-83dc-e2a26bbc656c_252x332.png)

With Hive, users must implement locks on the Hive Metastore to enable multiple people to modify the table safely. The general idea is that a writer can only change a table if it is acquired. This affects the system's throughput.

**The third is the file listing**. Before reading files in a partition, the engine must list all the files in a directory to determine which files it will read. This can take a considerable amount of time for a large partition. This problem worsens when people try to deploy the Hive data lake using object storage.

[![](https://substackcdn.com/image/fetch/$s_!YiyA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc61af3f5-0830-47e0-adf1-14651eae593d_648x384.png)](https://substackcdn.com/image/fetch/$s_!YiyA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc61af3f5-0830-47e0-adf1-14651eae593d_648x384.png)

Netflix shared that they must wait more than 9 minutes for the engine to plan the query because the Hive table contains many files, even though they only query the needed partitions.

**The fourth issue is that Apache Hive's data organization approach may degrade the performance of read and write operations in object storage**. Although S3 or GCS allows users to store data in “subdirectories,” these object storage systems manage data differently from what we are familiar with in a filesystem. Unlike the hierarchical structure of the file system, object storage has a flat structure. The path you see in the object storage, like **bucket/country/date/…,** is the [prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) of your objects.

Cloud object storage suggests that the data read operations should have as many different prefixes as possible, so they get handled by different servers in cloud object storage.

[![](https://substackcdn.com/image/fetch/$s_!wn4M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf880059-c940-44cc-963f-341151a99fee_512x342.png)](https://substackcdn.com/image/fetch/$s_!wn4M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf880059-c940-44cc-963f-341151a99fee_512x342.png)

With Hive, data for the same partitions (prefixes on object storage) is usually retrieved together, which might cause all the requests not to be distributed evenly, thus reducing the performance.

[![](https://substackcdn.com/image/fetch/$s_!fvkO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44925396-2892-4af7-8799-486d2c618052_486x362.png)](https://substackcdn.com/image/fetch/$s_!fvkO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44925396-2892-4af7-8799-486d2c618052_486x362.png)

Initially, Hive could help with the lakehouse problem, but the industry requires a more robust metadata layer.

## The next waves of open table formats

A new-generation metadata layer must resolve Hive's challenges and bring more warehouse capability to the lake. We will examine notable attempts to achieve this.

### Hudi: Uber's Drive for Incremental Processing

[![](https://substackcdn.com/image/fetch/$s_!Hldr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F924633a1-26b0-449f-a09b-5b9c1c8a9482_1088x424.png)](https://substackcdn.com/image/fetch/$s_!Hldr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F924633a1-26b0-449f-a09b-5b9c1c8a9482_1088x424.png)

As mentioned, with Hive, data mutations only happen at the partition level. This caused serious problems for Uber, while some of their use cases require efficient incremental data processing.

For example, the Uber team found themselves bulk re-ingesting 120TB of data every 8 hours, even though less than 1% of that data (around 500GB) had changed.

Uber's internal users had different expectations for data freshness, from sub-minute to near real-time latency. At that time, Uber’s Hadoop data lake couldn’t keep up with the demand.

To address these challenges, [Vinoth Chandar](https://www.linkedin.com/in/vinothchandar/), who later founded Onehouse, started the project, initially known as the "transactional data lake," at Uber.The goal was to dramatically improve the efficiency of incremental data processing in the lake.

That’s how Hudi was created.

### Iceberg: Netflix's Solution to Hive's Limitations

[![](https://substackcdn.com/image/fetch/$s_!9Tw2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d951334-a629-4343-b1fb-6e82e6934fef_342x528.png)](https://substackcdn.com/image/fetch/$s_!9Tw2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d951334-a629-4343-b1fb-6e82e6934fef_342x528.png)

Netflix relied heavily on Apache Hive. However, as their scale and data complexity grew, Hive's critical limitations became more apparent (most of which are mentioned in Hive’s challenges section). A primary concern was **query correctness and the lack of stable atomic transactions**.

To solve the problems with Hive, Ryan Blue and Dan Weeks at Netflix initiated the Iceberg project in 2017. The main goals were:

1. **Ensure data correctness and support ACID transactions**: [Ryan Blue stated](https://atlan.com/know/iceberg/apache-iceberg-101/), "Iceberg tackled atomicity to make automation possible, even in cloud object stores".
2. **Improve performance**: This involved enabling finer-grained operations at the file level for optimal writes and, crucially, tracking the complete list of data files within a table instead of relying on directory listings for query planning.
3. **Simplify and abstract table operation and maintenance**: The aim was to make data tables easier to manage and less error-prone.

### Delta Lake: Databricks' Pursuit of Reliable Data Lakes With Spark

[![](https://substackcdn.com/image/fetch/$s_!M6sC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23354cc6-b263-4ad7-951b-827e808c523e_474x366.png)](https://substackcdn.com/image/fetch/$s_!M6sC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23354cc6-b263-4ad7-951b-827e808c523e_474x366.png)

Delta Lake was introduced by Databricks (with conceptual [origins attributed to work by Dominique Brezinski and Michael Armbrust at Apple](https://www.bigeye.com/blog/a-brief-history-of-databricks) for managing petabytes of log data) to bring a new level of reliability and performance to data lakes, particularly those powered by Apache Spark.

The primary goal was to add a transactional storage layer on top of existing data lake files (typically Parquet stored in cloud object storage), enabling ACID transactions, scalable metadata handling, and unified batch and streaming data processing.

## The problems these table formats are trying to solve

### ACID Transactions

The ACID transaction guarantee is the most critical shared capability of these table formats. Controlling transactions at the partition level in Hive is not an efficient approach. All these tables track table data at the file level.

[![](https://substackcdn.com/image/fetch/$s_!Y6kS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F476e358e-6185-4f31-ab32-696a5b188615_474x306.png)](https://substackcdn.com/image/fetch/$s_!Y6kS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F476e358e-6185-4f31-ab32-696a5b188615_474x306.png)

They implement mechanisms to ensure that operations (like writes, updates, and deletes) are atomic (either fully complete or not at all), data remains consistent even with concurrent access, concurrent operations are isolated from each other, and committed changes are durable.

This is vital for preventing data corruption from failed ETL jobs and ensuring reliable reads during concurrent modifications.

### Concurrent Write

The three formats support concurrent writes with [Optimistic Concurrency Control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) (OCC). Unlike Hive, which waits for acquiring the lock, OOC allows concurrent writes to occur at the exact times and checks if a write conflicts with any other writes. If a conflict is detected, the write will retry with modification.

### Managing Schema Evolution

These table formats enable schema modifications over time, such as adding new columns, dropping existing ones, or changing data types, without requiring the complete rewriting of the entire dataset or disrupting downstream applications. They provide mechanisms to track schema versions and apply changes gracefully.

[![](https://substackcdn.com/image/fetch/$s_!hg9t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f828925-3278-4e7f-8bc0-f18a035347a3_1802x196.png)](https://substackcdn.com/image/fetch/$s_!hg9t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f828925-3278-4e7f-8bc0-f18a035347a3_1802x196.png)

[Source.](https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison)

### Enabling Data Versioning and Time Travel

A significant advancement is the ability to maintain and query historical versions of data. Each format uses concepts like snapshots (Iceberg snapshot) or commits in a transaction log (Delta Lake, Hudi timeline) to capture the state of a table at specific points in time. This enables "time travel," allowing users to query data as it appeared in the past for debugging or roll back to a previous version in case of errors.

[![](https://substackcdn.com/image/fetch/$s_!mZ6Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb31e3f31-de9b-47d3-9604-4eba98339be3_484x290.png)](https://substackcdn.com/image/fetch/$s_!mZ6Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb31e3f31-de9b-47d3-9604-4eba98339be3_484x290.png)

In the data engineering field, more software engineering practices are being introduced to enhance the data product development process. The ability to version the data product is crucial. All these formats let us work on isolated snapshots, just like we work on Git branches.

### Facilitating Efficient Upserts, Deletes, and Merges (CRUD Operations)

These formats provide robust support for Data Manipulation Language (DML) operations such as record-level updates, deletes, and merge (or upsert) operations. Rewriting an entire table or partition is unnecessary. Hudi even has more efficient support for this by implementing the index structure to locate records more efficiently for the data operations.

### Optimizing Performance for Large-Scale Analytics

All three formats incorporate strategies to enhance query performance on large datasets. These include mechanisms for managing file sizes (e.g., compacting many small files into fewer, larger ones), optimizing data layout (e.g., through clustering, sorting, or techniques like Z-ordering), and enabling efficient data pruning (skipping irrelevant data files or partitions during query execution).

The richness of the optimization features surpasses that of Hive, which is primarily based on partition pruning to skip files.

---

## Outro

Organizations want a more cost-efficient approach, and Lakehouse can provide that, at least in theory, where they don’t need to store data in the two systems. Lakehouse also offers users more control over their data and the flexibility to use any query engine they prefer.

Another critical factor for the rise of the lakehouse is that table formats like Hudi, Iceberg, and Delta Lake are becoming more mature, both in terms of functionality and interoperability. They continually add more warehouse features to the lake and can integrate with various systems.

The lakehouse and table format will continue to get more attention.

However, this does not mean you must choose the lakehouse architecture for every scenario. The decision must be made based on the organization’s needs. Remember, every decision has a trade-off.

---

## Reference

[1] Facebook Data Infrastructure Team, [Hive - A Warehousing Solution Over a Map-Reduce](https://www.vldb.org/pvldb/vol2/vldb09-938.pdf) (2009)

[2] Google, [Dremel: A Decade of Interactive SQL Analysis at Web Scale](https://research.google/pubs/dremel-a-decade-of-interactive-sql-analysis-at-web-scale/) (2020)

[3] Databricks, [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.databricks.com/research/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics) (2020).

[4] Databricks, [Photon: A Fast Query Engine for Lakehouse Systems](https://dl.acm.org/doi/10.1145/3514221.3526054) (2022)

[5] Jason Hughes, [Apache Iceberg: An Architectural Look Under the Covers](https://www.dremio.com/resources/guides/apache-iceberg-an-architectural-look-under-the-covers/) (2021)
