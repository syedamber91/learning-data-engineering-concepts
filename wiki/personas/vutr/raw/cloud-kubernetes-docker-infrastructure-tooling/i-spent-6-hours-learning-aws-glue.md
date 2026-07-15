---
title: "I spent 6 hours learning AWS Glue. Here is what I found"
channel: vutr
author: "Vu Trinh"
published: 2025-01-09
url: https://vutr.substack.com/p/i-spent-6-hours-learning-aws-glue
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Delta Lake", "Data Warehouse", "Data Lake", "Lakehouse", "Orchestration", "Streaming", "ETL"]
tags: [https, auto, glue, image, substackcdn, fetch]
---

# I spent 6 hours learning AWS Glue. Here is what I found

*The cloud-native and robust data integration tool.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-6-hours-learning-aws-glue)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!0gqf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07d94d67-6d5a-4220-8635-e33cdb8efb72_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!0gqf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07d94d67-6d5a-4220-8635-e33cdb8efb72_2000x1429.png)

Image created by the author.

---

## Intro

The emergence of a centralized repo as an entry point for analytics demands has witnessed the rise of the data warehouse in the 1980s, the data lake in the 2000s, and the lakehouse in the 2020s.

Whatever paradigm you choose, you must still perform an inevitable process: gathering data from multiple sources. Moving data from a few OLTP databases is affordable, but handling data from more than 10 sources is complicated, with different data formats and retrieval mechanisms can be challenging.

Today, we will explore AWS Glue, the serverless data integration cloud service. The text in the upcoming sections is my note from reading the paper [The Story of AWS Glue](https://www.vldb.org/pvldb/vol16/p3557-saxena.pdf) from Amazon. If you have time, I highly recommend it.

---

## Overview

Before Glue, there was no tool in AWS to help users with data integration.

[![](https://substackcdn.com/image/fetch/$s_!hYVt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7be68bd3-c678-4fe3-9f5b-561c5b58e705_216x324.png)](https://substackcdn.com/image/fetch/$s_!hYVt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7be68bd3-c678-4fe3-9f5b-561c5b58e705_216x324.png)

Operational data from RDS or DynamoDB must be loaded into Redshift for analytics. The rise of the data lake paradigm emerged as the trend of storing semi-structured data in object storage; these data are then processed and served using Amazon EMR or Athena.

AWS customers need tools to help them discover, preprocess, and move data between services.

ETL tools at that time were designed only for structured data and didn't aim to be elastic and scalable on the cloud; their customer had to write ETL scripts and self-manage infrastructure.

[![](https://substackcdn.com/image/fetch/$s_!DYW1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82a632cd-ceed-4cc8-8c75-64e91a31eba0_350x410.png)](https://substackcdn.com/image/fetch/$s_!DYW1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82a632cd-ceed-4cc8-8c75-64e91a31eba0_350x410.png)

To address this problem, AWS built Glue, a cloud-based ETL (extract, transform, load) service designed to relieve the heavy lifting of managing and preparing data for analytics.

[![](https://substackcdn.com/image/fetch/$s_!3DRF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F002f29f6-4ef1-4a4c-848d-0cacf06e2e9f_386x266.png)](https://substackcdn.com/image/fetch/$s_!3DRF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F002f29f6-4ef1-4a4c-848d-0cacf06e2e9f_386x266.png)

It seamlessly integrates with Amazon’s ecosystem, including S3, Redshift, and Athena, making it a powerful choice for building and maintaining data lakes and pipelines.

AWS Glue was designed based on these principles:

* Provide customers the ability to solve problems when the system can not satisfy their needs. Examples include allowing customers to write code to customize ETL pipelines.
* Glue must support various analytics environments without forcing a single data model, type system, or query language. It should let customers start with their existing data structure and incrementally adopt Glue for new applications and use cases.
* It must reduce time spent managing infrastructure to enhance developer productivity.

Glue contains minor services like the ETL stacks and the Glue Catalog. Later in the article, we will briefly review and discuss these services in detail.

### ETL stack

It has some core components:

[![](https://substackcdn.com/image/fetch/$s_!fYS8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feebe29c1-3396-4906-b701-4a47e5e98c90_1388x482.png)](https://substackcdn.com/image/fetch/$s_!fYS8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feebe29c1-3396-4906-b701-4a47e5e98c90_1388x482.png)

Image created by the author.

* **Glue Studio** is a visual interface that automatically generates human-readable Apache Spark scripts.
* **AWS Glue ETL runtime** includes core Spark packages and Glue-specific libraries. Spark is chosen as the foundation due to its general-purpose nature and familiarity with developers. AWS also extends it with glue-specific libraries to enhance ETL efficiency and resilience, introducing DynamicFrame and specialized transformations to prepare and clean nested semi-structured data more efficiently
* Glue provides an **orchestration system** to stitch together multiple jobs into a pipeline.
* Glue also lets users run Spark jobs seamlessly. The user only needs to submit the Spark jobs, and this service will take care of everything else. It typically starts in a few seconds and can dynamically scale the resource during job execution.

### Glue Data Catalog

Glue also provides a scalable metadata service.

[![](https://substackcdn.com/image/fetch/$s_!ymTP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6f4d36b-9de4-4642-bf8c-8c8f59008f28_780x502.png)](https://substackcdn.com/image/fetch/$s_!ymTP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6f4d36b-9de4-4642-bf8c-8c8f59008f28_780x502.png)

Image created by the author.

It allows customers to model datasets as databases or tables, supporting data in various stores such as Amazon S3, relational databases, NoSQL stores, and streaming data services.

AWS services like Amazon Athena, Amazon EMR, and Amazon Redshift can query the tables defined in the catalog, and users can leverage an Apache Hive Metastore-compatible adapter for adopting open-source engines like Apache Spark and Presto.

Next, let’s explore the key use cases AWS Glue serves and the challenges it addresses for modern data integration.

## Use Cases and Challenge

### Use cases

AWS Glue can serve a wide array of data engineering use cases:

* **Loading Data To The Data Warehouse**: One of Glue’s earliest and most popular use cases is loading semi-structured data from Amazon S3 into Amazon Redshift. By discovering the source data schema, transforming nested or inconsistent formats, and optimizing it for analytics, Glue helps streamline the data loading workflows.

  [![](https://substackcdn.com/image/fetch/$s_!ajKD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44cbb46b-78ea-4dd5-88ec-62569bd218da_388x172.png)](https://substackcdn.com/image/fetch/$s_!ajKD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44cbb46b-78ea-4dd5-88ec-62569bd218da_388x172.png)
* **On-prem DBMBS to S3**: Glue helps build and manage the pipelines of copying data from on-prem DBMS on Amazon S3. It simplifies creating table definitions in the Glue Data Catalog, inferring schemas using crawlers, and organizing datasets into efficient, queryable formats like Parquet.

[![](https://substackcdn.com/image/fetch/$s_!EwKq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13e0281d-18da-489a-8f74-51c4399bc388_360x256.png)](https://substackcdn.com/image/fetch/$s_!EwKq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13e0281d-18da-489a-8f74-51c4399bc388_360x256.png)

* **Streaming Data Ingestion**: Glue enables ingestion and transformation of real-time data streams from sources like Amazon Kinesis or Kafka. These pipelines clean and pre-aggregate data before storing it in S3 or loading it into Redshift

  [![](https://substackcdn.com/image/fetch/$s_!g9Uk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07a0eeb0-d0c2-40b6-992e-150d28e4a406_498x372.png)](https://substackcdn.com/image/fetch/$s_!g9Uk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07a0eeb0-d0c2-40b6-992e-150d28e4a406_498x372.png)

### Challenges

In the process of helping the users with the above use cases, AWS encounter several technical challenges:

* Inconsistent or Missing Metadata: Semi-structured datasets, like JSON files, often lack schemas, or fields within the same dataset may conflict in type or structure.
* The customer also needs to integrate with many external systems. They want to process data from diverse sources, such as Amazon S3, DynamoDB, on-premise databases, and relational databases like RDS. Challenges include navigating VPC configurations, subnet management, and differing authentication protocols. The customer needs help configuring these options and reusing them for multiple ETL jobs.
* Apache Spark in Glue scales horizontally, potentially putting more pressure on relational databases or DynamoDB with hot partitions. Customers need a way to throttle ETL jobs and retry strategies to protect source systems while ensuring stable performance.
* Customers need a reliable data processing solution with predictable performance. The data workload can vary for different scenarios. The daily run might process a small amount of data due to incremental data processing, while the backfilling process requires more data.
* The customers also demand a solution to help them with the physical layout and data partition in the object-storage-based data lake. Effective partitioning helps query engines scan fewer files by running unnecessary partitions. File size also plays a crucial role in query performance. Too small files require the engine to execute more operations (fetching/opening/reading/closing), while too big files might limit the parallelism level.

Now, let’s examine the various sub-services of AWS Glue and how they address the challenges outlined above. First up is the ETL Stack.

## The ETL Stack

As mentioned above, the ETL stack comprises several components that make data transformation reliable and efficient.

### Glue Studio

[![](https://substackcdn.com/image/fetch/$s_!lsy4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b79dc13-551a-47da-b2e2-93c5e6aec273_842x324.png)](https://substackcdn.com/image/fetch/$s_!lsy4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b79dc13-551a-47da-b2e2-93c5e6aec273_842x324.png)

Image created by the author.

To help users get started with Glue, AWS built a visual interface and code generation mechanism called Glue Studio. The output is an ETL script based on the defined DAG; each node represents a data source/sink transformation. Users can customize each node or edit the generated script directly.

### Glue ETL Library with DynamicFrames

When Glue was first developed, most data query engines, including Spark, required schema before using the datasets. Spark can infer the data schema during the ingestion process. It would be easier if the data were in a self-described format such as Avro or Parquet, where it could extract the schema without reading all the data. In contrast, the process needs to perform a full data scan with JSON.

To help the customer work more effectively with semi-structured data, AWS built Glue ETL runtime, backed by a new data structure called DynamicFrame. Instead of requiring the schema beforehand, DynamicFrame embeds the schema metadata in each record and only infers the global schema when needed.

Let's dive a bit into the DynamicFrame.

Like Spark Dataframe, DynamicFrame is also stored at Spark RDD of DynamicRecords. Each record is a tree-based data structure containing column metadata and values.

[![](https://substackcdn.com/image/fetch/$s_!3ne6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0544a077-de63-4f57-baec-c59b94dd4c3b_878x398.png)](https://substackcdn.com/image/fetch/$s_!3ne6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0544a077-de63-4f57-baec-c59b94dd4c3b_878x398.png)

Image created by the author.

The Glue ETL libraries allow the creation of DynamicFrames from multiple formats, such as Avro, CSV, JSON, Parquet, or data from relational databases over JDBC.

[![](https://substackcdn.com/image/fetch/$s_!Ul7a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f9713b6-d2e0-4200-b4f5-38e831209b4a_864x530.png)](https://substackcdn.com/image/fetch/$s_!Ul7a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f9713b6-d2e0-4200-b4f5-38e831209b4a_864x530.png)

Image created by the author.

The DynamicFrame offers standard transformations such as selection or projection and lets users apply UDF in Python or Scala. It also includes transformations designed for deeply nested data.

Although DynamicFrames are flexible and valuable for ETL tasks, they lack the advanced analytics capabilities of Spark Datasets, such as joins or complex aggregations. A typical pattern in Glue involves leveraging DynamicFrames for data reading and filtering before converting them to DataFrames for further processing.

Schema inference in Glue is designed to handle diverse datasets by generating a flexible schema that accommodates any set of records, even when schema conflicts occur. The process involves inspecting every record and unifying the structures, including field names and types, encountered in the data. Glue extends schema inference beyond Spark's approach by introducing a special union type that records all possible types a field may take, such as nulls, absence of values, or conflicting types.

Let's continue with the Parquet Writer from Glue Libraries.

At first, the customers did not benefit from using DynamicFrams because the Parquet writer required the scheme beforehand.

The Glue Parquet Writer was introduced in 2019 to address the limitation. It solves this by incrementally building the first row group in memory, dynamically creating columns, and setting definition and repetition levels as new fields are encountered. Once the in-memory data exceeds a default 128 MB threshold, the first row group is flushed, setting the schema for the file.

[![](https://substackcdn.com/image/fetch/$s_!RUMh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce1c5850-8589-4d34-87b2-01ec4821bc71_1356x628.png)](https://substackcdn.com/image/fetch/$s_!RUMh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce1c5850-8589-4d34-87b2-01ec4821bc71_1356x628.png)

Image created by the author.

Any new fields discovered afterward trigger the creation of a new file with an updated schema. Systems like Spark may require configuration adjustments to effectively handle collections of files with differing schemas.

### **Serverless Execution and Auto-scaling**

Glue relieves customers from infrastructure management by offering them a serverless interface for running Glue jobs. Users only submit jobs; the serverless service handles everything else.

In Glue 1.0, the cluster-based approach was designed primarily for batch workloads, offering three job-start options:

[![](https://substackcdn.com/image/fetch/$s_!rj0z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1ab329e-4596-4e1f-9a7b-f752dc2a1991_2644x728.png)](https://substackcdn.com/image/fetch/$s_!rj0z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1ab329e-4596-4e1f-9a7b-f752dc2a1991_2644x728.png)

Image created by the author.

* Reusing pre-allocated clusters.
* Allocating clusters from a service-wide warm pool.
* Provisioning new clusters from EC2.

Jobs could only start once an entire cluster was ready, with idle clusters retired after a fixed period to control costs. Warm starts (reusing or warm-pool clusters) had latencies under one minute, but cold starts, requiring new cluster provisioning, experienced delays of 8–10 minutes. Thus, Glue 1.0 had high variability in start times.

In 2020, Glue 2.0 introduced a new resource manager and a lightweight Spark application stack to reduce job start times significantly. The new resource manager dynamically schedules jobs on clusters that begin execution as soon as the first instance is ready. Spark's scheduler was modified to use executors on workers from Glue's resource manager rather than cluster-based systems like YARN. The resource manager leverages a service-wide warm pool of pre-initialized Spark instances and ML models to predict EC2 instance demand across regions, keeping cold start times under 10 seconds.

Glue 3.0 further enhanced efficiency with auto-scaling, dynamically adjusting cluster size during jobs. Key innovations included extending Spark's shuffle tracking algorithm to safely scale down workers without losing intermediate state and dampening frequent resizing to reduce resource churn.

### Decoupling Cloud Shuffle

If you've been working with Spark, you might have to manage shuffle storage for the Spark job execution. Skew partitions or under-provision local storage can lead to running out of resources used for shuffling on an individual worker. Generally, two options to mitigate the issue are re-partitioning the dataset or putting more resources into the cluster.

[![](https://substackcdn.com/image/fetch/$s_!UOFP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe135053b-8888-48a6-8db4-e40478c5af92_892x540.png)](https://substackcdn.com/image/fetch/$s_!UOFP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe135053b-8888-48a6-8db4-e40478c5af92_892x540.png)

Image created by the author.

In 2021, AWS introduced the cloud shuffle storage plugin, which stores shuffle data in S3 to help decouple shuffle storage and compute for Spark. This plugin required extending components in Spark, such as the block manager, shuffle reader, and writers. In 2022, they added support for plugins for other cloud storage providers.

### Vectorized Readers

In 2021, Glue introduced native SIMD vectorized readers to address CPU bottlenecks in ETL workloads that transform raw formats like CSV and JSON into modern formats like Apache Parquet.

[![](https://substackcdn.com/image/fetch/$s_!iCAJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f34cdc2-240a-493e-b58d-4284b011d077_1016x612.png)](https://substackcdn.com/image/fetch/$s_!iCAJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f34cdc2-240a-493e-b58d-4284b011d077_1016x612.png)

Image created by the author.

Traditional deserialization into memory was constrained by CPU and memory bandwidths, which lagged behind S3's improved networking speeds.

The solution involved reimplementing readers in C++ and utilizing SIMD vectorized CPU instructions, which enabled micro-parallelism for faster parsing, tokenization, and indexing.

Additionally, the readers store data in an in-memory columnar format based on Apache Arrow. This helps optimize memory bandwidth utilization and reduce conversion costs when writing to columnar formats like Parquet.

### The Workflow and Incremental Processing

AWS built an orchestration layer in Glue that allows customers to orchestrate the data pipelines, which is called workflows. It lets the customers build pipelines from Glue Crawlers (more on this later), Glue Spark jobs, or Glue Python jobs.

They can define parameters to be passed between jobs, fall-back jobs in case of failure, or triggers to start the workflow based on a schedule or a combination of events. The users can monitor the entire workflow or dive into each job for troubleshooting.

Glue Job Bookmarks in the Glue ETL library enable incremental data processing by tracking and retaining the state of a job run. When enabled, bookmarks allow jobs to resume from where they left off, skipping previously processed data and supporting formats like CSV, JSON, Parquet, ORC, Avro, and JDBC sources.

For large initial loads, where millions of files in S3 prefixes can overwhelm Spark workers, Glue limits the number of files or dataset size per job run, allowing multiple executions to complete the task. This straightforward yet practical approach ensures reliable large-scale data migrations.

### Data Integration

AWS has expanded Glue's support for data formats, sources, and sinks to accommodate diverse customer needs, including legacy and unique formats.

The team has focused on optimizing high-volume sources like Amazon S3 and Redshift for performance and reliability and increasing the variety of supported data sources and formats.

For Amazon S3, Glue initially supported standard formats like CSV, JSON, Parquet, and ORC. Later, it introduced optimizations like task batching and partition pruning. It also enhanced features like handling S3 storage classes and fine-grained access control. In 2022, Glue added native support for transactional table formats such as Apache Hudi, Apache Iceberg, and Delta Lake.

Next, let’s move on to another key component of AWS Glue: the Data Catalog.

## The Glue Data Catalog

The data catalog aims to serve as the central repository for all the dataset metadata the customer needs to work on AWS. It records information such as data schema, format, or physical location.

### Overview

When data lakes in stores like Amazon S3 grow, managing metadata—such as schemas and data locations—is critical for query planning, execution, discovery, and governance across diverse query engines.

In traditional database management, needed metadata is stored in the internal catalog, which can only be used by the database's proprietary engine.

Modern data lakes require metadata to be decoupled from the query engine to support multiple engines. The Hive metastore, an open-source solution and standard in the Hadoop ecosystem, provides a familiar interface for managing metadata about databases, tables, and partitions and is widely supported by engines like Apache Hive, Trino, and Apache Spark.

However, it introduces challenges for large data lakes, as administrators must manage Hive's relational database backend, including provisioning, scaling, and patching.

AWS saw the need to provide customers with a better data catalog.

### Architecture

The Glue Catalog provides public AWS APIs for storing and retrieving metadata. It is designed as a managed replacement for the Hive Metastore. The Catalog offers CRUD APIs for databases, tables, and partitions, allowing metadata to include data types, schema, partitioning methods, and Hive Serialization/Deserialization for dataset compatibility.

[![](https://substackcdn.com/image/fetch/$s_!qlnh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8522166-936c-46b3-9d52-96e80097b6d8_1570x788.png)](https://substackcdn.com/image/fetch/$s_!qlnh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8522166-936c-46b3-9d52-96e80097b6d8_1570x788.png)

Image created by the author.

Query engines can process this metadata as JSON or through open-source adapters that convert it into formats compatible with Apache Hive or Apache Spark. While Hive conventions are followed for compatibility, the Glue Data Catalog does not strictly enforce the Hive data model, allowing flexibility for more prosperous systems and custom applications. This tradeoff means some tables may be incompatible with specific query engines, but it enables broader use cases in the diverse and fast-evolving data lake ecosystem.

Customers primarily use the Glue Data Catalog to catalog datasets in S3. Still, its flexible model supports various sources such as relational databases, NoSQL systems like MongoDB, and streaming sources like Amazon Kinesis and Apache Kafka. The catalog's connection objects let users specify the physical details for specific data stores, including VPC setup, security group configurations, and credentials or AWS Secrets Manager references. These connections are referenced by tables and passed to ETL jobs, further extending the catalog’s utility across diverse data environments.

Behind the scenes, the Glue Data Catalog is built on scalable, low-latency storage optimized for high availability and predictable performance and supports hundreds of thousands of monthly users.

Initially, standard optimizations addressed issues like skewed data and atomic table updates. However, as datasets grew, partition pruning emerged as a bottleneck. Query engines often enumerate all partitions for a table and filter them client-side, which becomes inefficient for tables with millions of partitions.

To mitigate this, AWS introduced partition indexing in 2020. Customers can create indexes on partition attributes, enabling efficient range queries. This allows query engines to push partition predicates directly to the Glue Data Catalog, retrieving only relevant partitions. The performance improvement is negligible for tables with a small number of partitions. Still, for tables with millions of partitions, the indexing significantly boosts query performance, making queries up to 8.6 times faster in some cases.

### The crawlers

The Glue Data Catalog's metadata is only valuable if it remains accurate and up-to-date.

While Glue ETL scripts and DDL statements from systems like Amazon Athena can populate the catalog, these methods are unsuitable for all use cases, such as handling large volumes of existing S3 data or datasets with unknown or dynamic schemas.

AWS Glue crawlers can help by scanning S3 data and automatically populating tables and partitions in the Data Catalog. By specifying S3 prefixes and a destination database, crawlers can detect file types, schemas, and changes, registering new partitions or evolving schemas without manual intervention.

In detail, the S3 crawling process comprises of 3 main stages:

[![](https://substackcdn.com/image/fetch/$s_!dxDg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c1adb3-49ab-4402-a29a-bcf1cdeb6a05_1020x632.png)](https://substackcdn.com/image/fetch/$s_!dxDg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c1adb3-49ab-4402-a29a-bcf1cdeb6a05_1020x632.png)

Image created by the author.

* The first crawling stage involves listing files within S3 prefixes and batching them into tasks for parallel processing during classification. This stage identifies each file's format, compression type, and schema, aggregating metadata at the prefix level for finalization. To minimize data scanning, crawlers analyze only the first megabyte of each file to infer the schema. Glue crawlers utilize classifiers specific to file formats, employing techniques like recognizing Avro's unique header or testing delimiters in text formats like CSV.
* Next, the finalizer identifies tables and partitions within a dataset by analyzing S3 prefixes and populating the Glue Data Catalog. It categorizes S3 Hive-based partition prefixes, such as/Transactions/US/2022-01-09, into tables with partitions based on country and date. Assuming partitions share similar schemas while different tables have distinct ones, it employs a schema similarity metric. This metric assigns points based on matching field names and types, calculating similarity as a ratio of intersecting fields to the minimum schema size. The finalizer computes schema similarity for sibling prefixes and infers partitions if their similarity exceeds a set threshold; otherwise, it treats them as separate tables.
* The final stage is recrawling. The crawlers let the customers incrementally crawl/recrawl only the new S3 partitions added since the last crawling. The S3 events-based crawler helps customers target and change folders.

---

## Outro

I have included above everything I discovered about AWS Glue from AWS’s paper.

It’s designed to handle real-world challenges like schema inconsistencies, scalability, and integration across diverse systems. AWS Glue empowers data engineers to focus on ETL logic and data catalog management while leaving the heavy lifting of infrastructure to AWS.

Now, it's time to say goodbye.

Feel free to correct me or give me feedback in the comments.

See you on my following pieces.

---

## **References**

*[1] AWS, [The Story of AWS Glue](https://www.vldb.org/pvldb/vol16/p3557-saxena.pdf) (2023)*

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
