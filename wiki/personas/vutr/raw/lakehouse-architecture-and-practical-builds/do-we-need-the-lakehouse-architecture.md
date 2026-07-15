---
title: "Do we need the Lakehouse architecture?"
channel: vutr
published: 2024-04-20
url: https://vutr.substack.com/p/do-we-need-the-lakehouse-architecture
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming", "Data Quality", "ETL"]
tags: [https, lake, lakehouse, apache, warehouse, analytics]
---

# Do we need the Lakehouse architecture?

*When data lakes and data warehouses are not enough.*

> Source: [Open post](https://vutr.substack.com/p/do-we-need-the-lakehouse-architecture)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *My name is Vu Trinh, and I am a data engineer.*
>
> *I’m trying to make my life less dull by spending time learning and researching “how it works“ in data engineering.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!5vGq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71fc52a9-786c-4eb1-a115-c7de3917c1be_1397x997.png)](https://substackcdn.com/image/fetch/$s_!5vGq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71fc52a9-786c-4eb1-a115-c7de3917c1be_1397x997.png)

Image created by the author.

---

## Table of contents

* Challenges and Context
* The Motivation
* The Lakehouse Architecture

---

## Intro

I first heard about the term “Lakehouse“ in 2019 while scrolling through the [Dremio](https://docs.dremio.com/) document. With a conservative mind, I assumed this was just another marketing term. Five years later, it seems like everybody is talking about Lakehouse (after they finish discussing AI :d); all major cloud data warehouses now support reading [Hudi](https://hudi.apache.org/), [Iceberge](https://iceberg.apache.org/), or [Delta Lake](https://delta.io/) format directly in object storage, and even BigQuery has a [dedicated query engine](https://cloud.google.com/bigquery/docs/biglake-intro) for this task. The innovation doesn’t stop there; [Apache XTable](https://xtable.apache.org/) (formerly OneTable) provides abstractions and tools for translating Lakehouse table format metadata. Recently, [Confluent has announced the release of TableFlow](https://www.confluent.io/blog/introducing-tableflow/), which feeds Apache Kafka data directly into the data lake, warehouse, or analytics engine as Apache Iceberg tables. This makes me re-examine my assumption from the past: Was Lakehouse just a marketing term?

This week, we will answer that question with my note from the paper [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf).

---

## Challenges and Context

> *The impression of the data flow from data lakes to the data warehouse made me believe that the data lakes concept existed before the warehouse concept. This is not true. “[Data Lakes” was coined in 2011](https://en.wikipedia.org/wiki/Data_lake), and “Data Warehouse“ was introduced long ago.*

[![](https://substackcdn.com/image/fetch/$s_!tCAE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56dff0df-2384-4837-8490-b14054eda105_985x708.png)](https://substackcdn.com/image/fetch/$s_!tCAE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56dff0df-2384-4837-8490-b14054eda105_985x708.png)

Image created by the author

Data warehousing was first introduced to help business users get analytical insights by consolidating data from operational databases in a centralized warehouse. Analytic users use this data to support business decisions. Data would be written with schema-on-write to ensure the data model was optimized for BI consumption. This is the first-generation data analytics platform.

In the past, organizations typically coupled computing and storage to build data warehouses on-premise. This forced enterprises to pay for more hardware when the demand for analytics and data size increased. Moreover, data does not only come in tabular format anymore; it can be video, audio, or text documents. The unstructured data caused massive trouble for the warehouse system, which was designed to handle structured data.

Second-generation data analytics platforms came to the rescue. People started putting all the raw data into data lakes, low-cost storage systems with file interface that holds data in open formats, such as [Apache Parquet](https://parquet.apache.org/), [CSV](https://en.wikipedia.org/wiki/Comma-separated_values#:~:text=Comma%2Dseparated%20values%20(CSV),typically%20represents%20one%20data%20record.), or [ORC](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=31818911). This approach started with the rise of [Apache Hadoop](https://hadoop.apache.org/), which used HDFS for storage. Unlike data warehousing, data lake was a schema-on-read architecture that allowed flexibility in storing data. Still, it caused some challenges to data quality and governance. The approach would move a subset of data in the lake to the warehouse (ETL). The data-moving process ensures the analytics user can leverage the power of the data warehouse to mine valuable insights. From 2015 onwards, cloud object storage, such as [S3](https://aws.amazon.com/pm/serv-s3/?gclid=CjwKCAjw_LOwBhBFEiwAmSEQAYH-XsjU7XHQi8KBDiRz2QzRezbjog-694MESPklre7E9Kit26QLkxoCIgMQAvD_BwE&trk=55ffcfa3-95d3-4418-9a79-62a64040b867&sc_channel=ps&ef_id=CjwKCAjw_LOwBhBFEiwAmSEQAYH-XsjU7XHQi8KBDiRz2QzRezbjog-694MESPklre7E9Kit26QLkxoCIgMQAvD_BwE:G:s&s_kwcid=AL!4422!3!536452732958!e!!g!!s3!11543056249!112002966709) or [GCS](https://cloud.google.com/storage?hl=en), started replacing HDFS. They have superior durability and availability, plus extremely low cost. The rest of the architecture is mostly the same in the cloud era for the second-generation platform, with a data warehouse such as [Redshift](https://aws.amazon.com/redshift/), [Snowflake](https://www.snowflake.com/en/), or [BigQuery](https://cloud.google.com/bigquery/?utm_source=google&utm_medium=cpc&utm_campaign=japac-VN-all-en-dr-BKWS-all-all-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_658171083000-ADGP_Hybrid+%7C+BKWS+-+BRO+%7C+Txt+-Data+Analytics-BigQuery-bigquery-main-KWID_43700076364598924-aud-1596662389094:kwd-33969409261&userloc_1028581-network_g&utm_term=KW_bigquery&gad_source=1&gclid=CjwKCAjw_LOwBhBFEiwAmSEQAWmrwE69Ns67pUHNiFUBbRLaC695AZbRWKLcFAmC1of16mXDgPNBahoCB6QQAvD_BwE&gclsrc=aw.ds&hl=en). This two-tier data lake + warehouse architecture dominated the industry at the time of the paper’s writing (I guess it has dominated till now). Despite the dominance, the architecture encounters the following challenges:

[![](https://substackcdn.com/image/fetch/$s_!J9Os!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71250fa0-5eb1-4362-a880-05aae6fe15ba_683x671.png)](https://substackcdn.com/image/fetch/$s_!J9Os!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71250fa0-5eb1-4362-a880-05aae6fe15ba_683x671.png)

Image created by the author

* **Reliability:** Consolidating the data lake and warehouse is difficult and costly, requiring much engineering effort to ETL data between the two systems.
* **Data staleness:** The data in the warehouse is stale compared to the lake’s data. This is a step back from the first-generation systems, where new operational data was immediately available for analytics demands.
* **Limited support for advanced analytics:** Machine learning systems, such as TensorFlow or XGBoost, must process large datasets using complex programmatic code. Reading this data via ODBC/JDBC is not a good idea, and there is no way to access the internal warehouse data formats directly. Warehouse vendors recommend exporting data to files, which further increases the complexity of the whole system. Instead, users can run these systems on data lake data with open formats. However, this approach will trade-off for rich management features from data warehouses, such as ACID transactions or data versioning.
* **Total cost of ownership:** In addition to paying for ETL pipelines, users are billed double the storage cost for data duplication on the data lake and data warehouse.

> ***Note from me**: The point "Limited support for advanced analytics" does not reflect the reality at the moment due to the intense support of major cloud data warehouses like BigQuery, Snowflake, or Redshift for the machine learning workload. Feel free to discuss this with me in the comments if you don't think so.*

Based on these observations, Databricks discusses the following technical question: *“Is it possible to turn data lakes based on standard open data formats, such as Parquet and ORC, into high-performance systems that can provide both the performance and management features of data warehouses and fast, direct I/O from advanced analytics workloads?”*

They argue that this paradigm, referred to as a Lakehouse, can solve some of the challenges of data warehousing. Databricks believes Lakehouse will get more attention due to recent innovations that address its fundamental problems:

* **Reliable data management on data lake**s: Like data lakes, the Lakehouse must be able to store raw data and support ETL/ELT processes. Initially, data lakes just meant “a bunch of files” in various formats, making it hard to offer some key management features of data warehouses, such as transactions or rollbacks to old table versions. However, systems such as Delta Lake or Apache Iceberg provide a transactional layer for data lake and enable these management features. In this case, there are fewer ETL steps overall, and analysts can also quickly performantly query the raw data tables if needed, like the first-generation analytics platforms.
* **Support for machine learning and data science:** ML systems’ support for direct reads from data lake formats allows them efficient access to the data in the Lakehouse.
* **SQL performance:** Lakehouses must provide state-of-the-art SQL performance on top of the massive datasets in the lake. Databricks show that various techniques can be used to maintain auxiliary data for the data and optimize its layout within these existing formats to achieve performance.

  In the following sections, we will learn the motivation, technical designs, and research implications of Lakehouse platforms.

## The Motivation

Here are some reasons that make Databricks think the Lakehouse architecture could eliminate the shortcomings of the data warehouse:

* Data quality and reliability are the top challenges [reported](https://www.fivetran.com/blog/analyst-survey) by enterprise data users. Implementing efficient data pipelines is hard, and dominant data architectures that separate the lake and warehouse add extra complexity to this problem.
* More business applications require up-to-date data. Still, two-tier architectures increase data staleness by having a separate area for incoming data before loading it into the warehouse using periodic ETL/ELT jobs.
* A large amount of data is now unstructured.
* Data warehouses and lakes do not serve machine learning and data science applications well.

Some current industry trends give further evidence that customers are unsatisfied with the two-tier model:

* All the big data warehouses have added support for external tables in Parquet and ORC format.
* There is a broad investment in SQL engines run directly against data lake, such as [Spark SQL](https://spark.apache.org/docs/latest/sql-programming-guide.html) or [Presto](https://prestodb.io/).

However, these improvements can only solve some of the problems of lakes and warehouses architecture: the lakes still need essential management features such as ACID transactions and efficient data access methods to match the warehouse analytics performance.

---

## The Lakehouse Architecture

Databricks defines a Lakehouse as a data management system based on low-cost storage that enhances traditional analytical DBMS management and performance features such as ACID transactions, versioning, caching, and query optimization. Thus, Lakehouses combine the benefits of both worlds. In the following sections, we will learn about the possible Lakehouse design proposed by Databicks.

### Implementation

[![](https://substackcdn.com/image/fetch/$s_!-NTW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7db4b491-116c-42cd-a93d-5e73a5e1bc74_343x673.png)](https://substackcdn.com/image/fetch/$s_!-NTW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7db4b491-116c-42cd-a93d-5e73a5e1bc74_343x673.png)

Image created by the author.

The first idea they introduce for Lakehouse implementation is to store data in a low-cost object store (e.g., Google Cloud storage) using a standard file format such as Apache Parquet with an additional transactional metadata layer on top of it to define which objects belong to a table. The metadata layer allows them to implement management features such as ACID transactions while achieving the low-cost advantage of object storage. Some candidates for the metadata layer implementation can be named [Delta Lake](https://delta.io/), [Apache Iceberg](https://iceberg.apache.org/), or [Apache Hudi](https://hudi.apache.org/). Moreover, Lakehouses can boost advanced analytics workloads and help them better at data management by providing declarative DataFrame APIs. Many ML frameworks, such as [TensorFlow](https://www.tensorflow.org/) and [Spark MLlib](https://spark.apache.org/docs/latest/ml-guide.html), can read data lake file formats like Parquet. This means the easiest way to integrate them with a Lakehouse would be to query the metadata layer to find out which Parquet files are part of a table and pass this information to the ML library.

### Metadata Layer

Data lake storage systems such as S3 or HDFS only provide a low-level object store or filesystem interface. Over the years, the need for data management layers has emerged, starting with [Apache Hive](https://hive.apache.org/), which keeps track of which data files are part of a Hive table at a given table.

In 2016, Databricks started developing Delta Lake, which stores the information about which objects belong to which table in the object storage as a transaction log in Parquet format. Apache Iceberg, first introduced at Netflix, uses a similar design. Apache Hudi, which started at Uber, is another system in this area focused on streaming ingest into data lakes. Databricks observes that these systems provide similar or better performance to raw Parquet/ORC data lakes while improving data management, such as transactions, zero-copy, or time travel.

One thing to note here: they are easy to adopt for organizations that already have a data lake: e.g., Delta Lake can organize an existing directory of Parquet files into a Delta Lake table without moving data around by adding a transaction log over all the existing files. In addition, metadata layers can help in the implementation of data quality constraints. For example, Delta Lake constraints APIs let users apply constraints on the new data (e.g., a list of valid values for a specific column). Delta’s client libraries will reject all records that violate these constraints. Finally, metadata layers help implement governance features such as access control, e.g., it can check whether a client can access a table before granting credentials to read the table’s raw data.

### SQL performance

Although a metadata layer adds management capabilities, more is needed to achieve the warehouse’s capability. SQL performance, in which the engine runs directly on the raw data, maybe the most significant technical question with the Lakehouse approach. Databricks proposes several techniques to optimize SQL performance in the Lakehouse. These techniques are independent of the chosen data format. These optimizations are:

[![](https://substackcdn.com/image/fetch/$s_!eobr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9983abc1-eac8-4eaf-938a-b4d8ea7a7477_883x497.png)](https://substackcdn.com/image/fetch/$s_!eobr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9983abc1-eac8-4eaf-938a-b4d8ea7a7477_883x497.png)

Image created by the author.

* **Caching**: When using the metadata layer, the Lakehouse system can cache files from the cloud object store on faster devices such as SSDs and RAM.
* **Auxiliary data**: The Lakehouse can maintain other auxiliary file data to optimize queries. In Delta Lake and Delta Engine, Databricks maintains column min-max information for each data file, storing it in the same Parquet transaction log file. This enables the engine to skip unnecessary data in the scanning phase. They are also implementing a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) for the data-skipping purpose.
* **Data layout:** Lakehouse can optimize many layout decisions. The first one is record ordering, in which records are clustered together; this makes it easier for the engine to read them together. Delta Lake supports ordering records using individual dimensions or space-filling curves such as the [Z-order curve](https://en.wikipedia.org/wiki/Z-order_curve) to provide more than one dimension locality.

These optimizations work well together for the typical access patterns in analytical systems. Typical queries focus on a “hot” subset of the data in the analytics workload, which can benefit from cache optimization. The critical performance factor for “cold” data in a cloud object store is the amount scanned per query. Combining data layout optimizations and auxiliary data structures allows the Lakehouse system to minimize I/O efficiently.

### Efficient Access for Advanced Analytics

One approach is offering a declarative version of the DataFrame APIs used in Machine learning libraries, which maps data preparation computations into Spark SQL query plans and can benefit from the optimizations in Delta Lake. Thus, in implementing the Delta Lake data source, they leverage the caching, data skipping, and data layout optimizations described above to accelerate these reads from Delta Lake and accelerate ML and data science workloads.

---

## Outro

If the solution can solve the real problem, it is not just a cliché term. Lakehouse was initially introduced to relieve the pain point of two-tier architecture: maintaining two separate systems for storage (the lakes) and analytics (the warehouses). By bringing the analytics power directly to the lakes, the Lakehouse paradigm has to deal with the most challenging problem: query performance; doing analytics directly on the raw data means the engine doesn’t know much about the data beforehand, and this could cause some trouble for the optimization process. Thanks to innovation in recent years of open table formats like Hudi, Iceberge, or Delta Lake, the Lakeshouse seems to keep up with the traditional warehouse in the performance competition. It’s an exciting future to observe the rise of the Lakehouse side, to co-exist with the lake-warehouse paradigm, or to replace the two-tier architecture completely; who knows?

Thank you for reading my blog. See you next week ;)

---

## **References**

*[1] Databricks, [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.databricks.com/research/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics) (2020).*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/do-we-need-the-lakehouse-architecture/comments)

It might take you 5 minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
