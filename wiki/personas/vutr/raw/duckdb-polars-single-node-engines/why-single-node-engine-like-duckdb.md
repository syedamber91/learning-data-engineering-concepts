---
title: "Why single-node engines like DuckDB and Polars are getting a lot of attention?"
channel: vutr
author: "Vu Trinh"
published: 2026-01-13
url: https://vutr.substack.com/p/why-single-node-engine-like-duckdb
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Streaming", "ETL"]
tags: [https, auto, media, substackcdn, image, fetch]
---

# Why single-node engines like DuckDB and Polars are getting a lot of attention?

*From cluster-based engines like MapReduce or Spark to the claim "Big Data is dead"*

> Source: [Open post](https://vutr.substack.com/p/why-single-node-engine-like-duckdb)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[etl|ETL]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=183541398)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!ytfT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a939f77-19df-44a1-9953-6fdf4c529ebc_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!ytfT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a939f77-19df-44a1-9953-6fdf4c529ebc_2000x1429.png)

---

## Intro

If you asked the internet for the go-to data processing engine in the 2000s, you would get MapReduce.

If you asked the internet for the go-to data processing engine in the 2010s-2020s, you would get Apache Spark and cloud data warehouses such as BigQuery, Snowflake, Redshift …

If you asked the internet for the go-to data processing engine at the moment, you would still get Spark, BigQuery, Snowflake, or Redshift.

But you will see recommendations for single-node solutions like Polars or DuckDB.

For the last 20 years, cluster-based engines have been the dominant player.

But now, something has changed.

In this article, I try to understand the rise of single-node solutions such as Polars or DuckDB. We will examine the evolution from the pre-Internet era, the MapReduce hype, Spark, and the dominance of cloud data warehouses to see what works. From that, we explore the motivation behind those single-node solutions.

> ***Note 1:** This article is based entirely on my research online, so it might not reflect the context at that time. Feel free to correct me.*
>
> ***Note 2:**  This article won’t dive deep into DuckDB or Polars, as I solely deliver my research on the motivation behind these systems. I might spend time researching and writing articles about DuckDB or Polars in the future.*

---

## One machine was enough

In the past, the volume of generated data was small.

[![](https://substackcdn.com/image/fetch/$s_!u4ER!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52c57c66-a12d-495f-9db7-e053e2e8c438_898x520.png)](https://substackcdn.com/image/fetch/$s_!u4ER!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52c57c66-a12d-495f-9db7-e053e2e8c438_898x520.png)

If the company needed to use data to drive business operations, the process of consolidating, cleaning, and processing data could be performed on a single machine. In addition, most of the data still resided in the OLTP systems, as data analytics was not as popular as it is today.

A single machine is enough.

---

## MapReduce

Then, the internet was invented. More and more digital data is generated. The nature of data changed from human-entered records in databases to machine-generated streams.

The data evolved in both volume and structured aspects.

[![](https://substackcdn.com/image/fetch/$s_!po8U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21f679d6-e294-4857-a921-c31301925cce_1426x436.png)](https://substackcdn.com/image/fetch/$s_!po8U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21f679d6-e294-4857-a921-c31301925cce_1426x436.png)

Google is one of the companies that understands this challenge the most.

Founded in 1998 and surviving the DotCom bubble, Google established itself as a leader in the web-based application market.

[![](https://substackcdn.com/image/fetch/$s_!gTIN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d315adc-223c-4ee4-aae4-ac62a4bdfafb_580x239.png)](https://substackcdn.com/image/fetch/$s_!gTIN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d315adc-223c-4ee4-aae4-ac62a4bdfafb_580x239.png)

Source: [Google in 2000, Google Operating System, 2007](https://googlesystem.blogspot.com/2007/12/google-in-2000.html)

Their engine at the time became the go-to choice for anyone who wanted to search for something on the internet.

For the search to work, Google had to process a lot of data, from crawled documents, web request logs, or the inverted index.

[![](https://substackcdn.com/image/fetch/$s_!Fs_U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff84505ec-3433-4352-8331-cd6bebe9d028_706x422.png)](https://substackcdn.com/image/fetch/$s_!Fs_U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff84505ec-3433-4352-8331-cd6bebe9d028_706x422.png)

Of course, with this global scale of data, Google engineers could not process it on a single machine. They needed to bring multiple computers.

There were challenges:

[![](https://substackcdn.com/image/fetch/$s_!fc5f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F555df1c8-00e3-47b7-b657-9e5a3ae5018b_1262x808.png)](https://substackcdn.com/image/fetch/$s_!fc5f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F555df1c8-00e3-47b7-b657-9e5a3ae5018b_1262x808.png)

* How to parallelize the computation?
* How to distribute the data efficiently?
* How to handle failures?

To solve this, Google designed a new abstraction that allows them to express simple computations but abstracts away the details of parallelization. This model is inspired by the `map` and `reduce` primitives in [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)) and other functional languages.

They called it MapReduce. At the high level, it has two functions, both of which are defined by the users:

[![](https://substackcdn.com/image/fetch/$s_!XNId!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8ba3862-0acc-4964-8312-71fff4e278b8_684x626.png)](https://substackcdn.com/image/fetch/$s_!XNId!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8ba3862-0acc-4964-8312-71fff4e278b8_684x626.png)

* **Map**: It takes key/value pair inputs, processes them, and outputs intermediate key/value pairs. All values of the same key are grouped and passed to the Reduce tasks.
* **Reduce**: It receives intermediate values from Map tasks. The values for the same key are merged using the logic defined in the Reduce function (e.g., Count, Sum, ...).

Map workers and Reduce workers exchange the data via disks; every output data must be persisted in hard disks. The Master coordinates the entire process.

[![](https://substackcdn.com/image/fetch/$s_!7U2z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F808a6733-819d-4d72-8148-9c4d3802bd0d_524x472.png)](https://substackcdn.com/image/fetch/$s_!7U2z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F808a6733-819d-4d72-8148-9c4d3802bd0d_524x472.png)

One of the ultimate goals of MapReduce is to process large amounts of data across multiple machines reliably, and persisting data on disk can help Google achieve that. Later, Yahoo developed and open-sourced Apache Hadoop, which included the MapReduce paradigm inspired by the Google idea.

It did not take long for Hadoop MapReduce to become famous, as it was almost the only framework at the time to promise dealing with “big data” problems.

However, that hype did not last forever.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=183541398)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

It’s hard to map every use case to the Map/Reduce paradigm, and developers must write the logic in Java; not any data practitioner can write Java.

[![](https://substackcdn.com/image/fetch/$s_!Eodb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6338bb9b-950c-49e2-a21d-a40493eb0a3d_878x534.png)](https://substackcdn.com/image/fetch/$s_!Eodb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6338bb9b-950c-49e2-a21d-a40493eb0a3d_878x534.png)

Moreover, you cannot use MapReduce for stream processing or interactive queries. Facebook invented [Hive](https://hive.apache.org/) to translate SQL queries to MapReduce jobs. However, Hive was replaced later by [Presto](https://prestodb.io/).

Persisting data in disks increases I/O traffic, overhead, and latency; not every company has the same amount of data as Google did to see the reliability benefit.

[![](https://substackcdn.com/image/fetch/$s_!Flhe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67d3feb7-57c9-4cd9-bc01-f70380923bbd_1246x548.png)](https://substackcdn.com/image/fetch/$s_!Flhe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67d3feb7-57c9-4cd9-bc01-f70380923bbd_1246x548.png)

In addition, MapReduce is not for machine learning. Many algorithms, such as K-Means clustering or Logistic Regression, are **iterative**. They need to process the same dataset multiple times to refine a result. For every iteration, MapReduce must read data from disk, process it, and write the results back to disk. This creates a massive I/O bottleneck.

Cost efficiency is also a challenge, as users must estimate, monitor, and provision “enough” resources for the cluster. This requires lots of experience and knowledge.

The throne was passed to a more efficient cluster-based processing engine.

---

## Spark

UC Berkeley’s AMPLab saw a problem that needed to be solved. Despite the potential of cluster computing, they observed that MapReduce might not be efficient.

They created Apache Spark, a functional programming-based API to simplify multistep applications with the ability to share in-memory data across computation steps efficiently.

Unlike MapReduce, Spark relies on in-memory processing. It introduced the Resilient Distributed Dataset (RDD) abstraction to keep data in memory. All higher-level abstractions introduced later, such as datasets or DataFrame, are compiled into RDDs internally.

[![](https://substackcdn.com/image/fetch/$s_!aY6V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9849eb0-76be-41ab-8ee2-83c8bf9435e4_576x544.png)](https://substackcdn.com/image/fetch/$s_!aY6V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9849eb0-76be-41ab-8ee2-83c8bf9435e4_576x544.png)

Unlike MapReduce, which achieves fault tolerance by persisting data in disks, Spark RDDs rely on lineage.

Spark keeps track of each RDD’s dependencies on other RDDs, the series of transformations that created it. Suppose any partition of an RDD is lost due to a node failure or other issues. Spark can reconstruct the lost data by reapplying the transformations to the original RDD described by the lineage. This eliminates the need to write data to disk (as in MapReduce); thus, Spark promises greater performance.

> ***Note**: Spark still spills data to disk if the data does not fit in memory.*

For those who struggle with MapReduce, the Spark introduction at that time is their biggest hope. Spark starts to gain traction. However, requiring Scala or Java to work with Spark still makes it “a specified technical tool“.

Only when Spark introduced these supports did it start to become the de facto data processing engine:

* Python support in 2013
* SQL support in 2014

> *Python and SQL have been the dominant interfaces for working with Spark, [according to Databricks statistics](https://www.youtube.com/watch?v=-vJLTEOdLvA&t=80s)*. *In 2020, 47% used Python, 41% used SQL, and 12% used Scala and other.*
>
> [![](https://substackcdn.com/image/fetch/$s_!UhzP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cf9634-37e5-46ec-94e4-5c94d29195d6_860x484.png)](https://substackcdn.com/image/fetch/$s_!UhzP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cf9634-37e5-46ec-94e4-5c94d29195d6_860x484.png)
>
> [Source](https://www.youtube.com/watch?t=80&v=-vJLTEOdLvA&feature=youtu.be)

* DataFrame abstraction in 2015

It’s not hard to explain why. If you are in data fields, you must first speak SQL, then Python. For the DataFrame abstraction, data practitioners were already familiar with it from Pandas (first released in 2008).

[![](https://substackcdn.com/image/fetch/$s_!RbmU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F276fc42e-74a6-4117-959f-6e6940732243_1006x780.png)](https://substackcdn.com/image/fetch/$s_!RbmU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F276fc42e-74a6-4117-959f-6e6940732243_1006x780.png)

Friendly interface and APIs (functional-programming styles work pretty well for data processing tasks), faster than MapReduce because data is exchanged in memory, and Spark becomes the new king.

However, there are some downsides.

First, Spark has overheads:

* Applications running time must include the time needed for the driver and the executor to be spawned

  [![](https://substackcdn.com/image/fetch/$s_!69HG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8732c897-6d4b-4c12-a73b-9c8380052e7e_896x800.png)](https://substackcdn.com/image/fetch/$s_!69HG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8732c897-6d4b-4c12-a73b-9c8380052e7e_896x800.png)
* Creating/optimizing plans and coordinating between processes also takes time.

  [![](https://substackcdn.com/image/fetch/$s_!oIcx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2fbd254-83d0-40f1-8841-9a9ee17e3954_854x644.png)](https://substackcdn.com/image/fetch/$s_!oIcx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2fbd254-83d0-40f1-8841-9a9ee17e3954_854x644.png)

These overheads can be amortized when Spark processes a large dataset, which might need hours to complete. Seconds or minutes of overhead feel like nothing. However, the user experience is affected by these overheads when processing a small dataset.

Second, Spark is a complex system. It requires a deep understanding to make it work for your needs (pretty much like the way you handle your Hadoop cluster for a MapReduce job):

[![](https://substackcdn.com/image/fetch/$s_!HaHQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd88e701b-0b7f-4cfb-a7f9-ef49fbdba1a6_458x410.png)](https://substackcdn.com/image/fetch/$s_!HaHQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd88e701b-0b7f-4cfb-a7f9-ef49fbdba1a6_458x410.png)

There are two kinds of clusters you need to manage in Spark: the physical cluster, which provides the resources for the Spark Driver-Executors cluster. The latter is where your Spark application actually runs.

* How to set up the cluster with sufficient resources?
* How to partition the data?
* How to debug when your application runs remotely on the executors?
* How to manage the dependencies, you have to make sure the client and the cluster have the same Spark version, all the jar packages must be compatible with your Spark’s Scala version, and if Python packages are required, you need to find a way to let all the executors see those packages
* How to tune tons of other configurations, from the allocation mechanism, scheduling mode, or the on-heap/off-heap memory.
* User must take care of hardware resource utilization to ensure cost efficiency
* …

In short, Spark can help process massive datasets efficiently, but at a cost: it requires deep technical knowledge.

---

## Cloud data warehouse systems

During the rise of Spark, the world also witnessed the emergence of cloud data warehouses such as BigQuery, Snowflake, Databricks (from Spark), or Redshift.

[![](https://substackcdn.com/image/fetch/$s_!GG6c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76cb5fed-972d-4f6d-8c7e-ca941e387a3e_782x314.png)](https://substackcdn.com/image/fetch/$s_!GG6c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76cb5fed-972d-4f6d-8c7e-ca941e387a3e_782x314.png)

Pay-as-you-go pricing models, cheaper storage, faster networks, and columnar storage/processing have commoditized high-performance, cost-efficient data warehouses.

I believe this emergence contributes the most to the paradigm shift from ETL to ELT. People soon realized they didn’t have to transform the data before loading it into the warehouse.

[![](https://substackcdn.com/image/fetch/$s_!9X9i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ae0e47-328b-40bc-8c04-3c2561eba38f_1220x704.png)](https://substackcdn.com/image/fetch/$s_!9X9i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ae0e47-328b-40bc-8c04-3c2561eba38f_1220x704.png)

They could dump data straight from the source (maybe some lightweight processing is needed) and let the transformation happen later, directly in the warehouse.

With just a few clicks, your shiny warehouse will be up, and most of the transformation logic can now be handled in SQL.

[![](https://substackcdn.com/image/fetch/$s_!GVrT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc45eae4-c47a-402e-9378-7e86104e3274_1378x972.png)](https://substackcdn.com/image/fetch/$s_!GVrT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc45eae4-c47a-402e-9378-7e86104e3274_1378x972.png)

Vendors abstract infrastructure management; only minimal tuning knots are exposed. Most of the time, you don’t need to manage “cluster“ as in Spark or MapReduce (as long as you don’t use Redshift). The pay-as-you-go pricing models also allow us to be more relaxed.

The barrier for users to leverage these tools for data processing is lower than for MapReduce or Spark.

Still, the barrier does not disappear:

* User must understand the pricing model (pay-as-you-go this and pay-as-you-go that) to ensure reasonable billing.
* It’s hard (impossible) to have local dev experience with these cloud data warehouses.
* In some cases, users have to understand how these solutions work behind the scenes to optimize cost and query performance

---

## What works?

After reviewing MapReduce, Spark, and cloud data warehouses, let’s examine which factors truly make a data processing solution attractive:

* **Performance:** No matter what the size of the dataset is, people don’t prefer to wait (for too long). MapReduce indeed provides the framework for distributed data processing (the map-reduce paradigm, with shuffle-based processing, is the foundation of many processing engines these days); however, exchanging data over disks is not fast. Spark was created to solve this problem.

  [![](https://substackcdn.com/image/fetch/$s_!jSAe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd1cd00c-a070-401c-af38-12799c74aee5_272x476.png)](https://substackcdn.com/image/fetch/$s_!jSAe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd1cd00c-a070-401c-af38-12799c74aee5_272x476.png)

  From Canva’s Graphics
* **Friendly interfaces:** Python, SQL language, and the DataFrame abstraction allow data practitioners to get on board faster. Spark has become the king thanks to its support for DataFrame, SQL, and Python. Cloud data warehouses even replace ETL with ELT by performing the transformation in SQL directly on top of the database. In contrast, only technical users who can write Java and understand the MapReduce paradigm can work with it.

  [![](https://substackcdn.com/image/fetch/$s_!BV6K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1da52743-74d3-44d0-9340-e24757c40ab4_824x550.png)](https://substackcdn.com/image/fetch/$s_!BV6K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1da52743-74d3-44d0-9340-e24757c40ab4_824x550.png)

  From Canva’s Graphics
* **Minimal setup and maintenance effort:** Cloud data warehouses carved out their own place during the period when Spark dominated. I believe this is because a cloud data warehouse requires less setup and maintenance effort than managing Spark clusters (even with vendor support).

  [![](https://substackcdn.com/image/fetch/$s_!xuco!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F115c2349-e7b3-436b-96a4-051ea2004c31_432x604.png)](https://substackcdn.com/image/fetch/$s_!xuco!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F115c2349-e7b3-436b-96a4-051ea2004c31_432x604.png)

  From Canva’s Graphics
* **Cost efficiency:** Processed data is great. Processed data with skyrocket billing is not. Spark and MapReduce clusters require careful resource planning to ensure cost efficiency**.** Cloud data warehouse’s pay-as-you-go model is more straightforward; however, it still requires understanding the specific solution’s pricing model to keep costs reasonable. No matter the context, cost is always a crucial factor.

  [![](https://substackcdn.com/image/fetch/$s_!Dix4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09e01f77-951a-4e59-b813-42ce55c0f8a8_362x482.png)](https://substackcdn.com/image/fetch/$s_!Dix4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09e01f77-951a-4e59-b813-42ce55c0f8a8_362x482.png)

  From Canva’s Graphics

## The rise of the single-node engines

After this look back in time, we turn to the emergence of single-node data processing systems such as Polars and DuckDB. I believe there are three bullet points behind it:

* Not every company has “big data. “
* They tick most of the factors I listed in the above section.
* Developer Experience (DevEx) is no longer optional.

### Not every company has “big data. “

MapReduce was created at Google, the company that dealt with the amount of data from nearly the entire Internet. Spark was born to solve the problem of MapReduce; thus, both are designed with “big data” in mind.

[![](https://substackcdn.com/image/fetch/$s_!HTaO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd81b2fb6-2e01-4c27-84fe-d9678707e4a5_1020x782.png)](https://substackcdn.com/image/fetch/$s_!HTaO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd81b2fb6-2e01-4c27-84fe-d9678707e4a5_1020x782.png)

Before the rise of Polars or DuckDB, people had almost two choices to process the data:

* Single-machine processing with Pandas or NumPy
* Cluster-based processing with Spark or cloud data warehouse.

The thing is, there are no feasible options for a medium-sized dataset.

Pandas or NumPy can only handle small datasets due to Python’s global interpreter limit.

Cluster-based processing seems to be overkill: understanding the pricing model, setting up the cluster, tuning, monitoring, and all other things.

[![](https://substackcdn.com/image/fetch/$s_!rt_J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d738ef4-1b29-41a2-973d-b2017709c959_1026x450.png)](https://substackcdn.com/image/fetch/$s_!rt_J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d738ef4-1b29-41a2-973d-b2017709c959_1026x450.png)

This is a market gap, as most companies out there have small-to-medium-sized datasets.

[![](https://substackcdn.com/image/fetch/$s_!cq4q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf579e19-56ac-4893-9f2f-721287589549_948x554.png)](https://substackcdn.com/image/fetch/$s_!cq4q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf579e19-56ac-4893-9f2f-721287589549_948x554.png)

Single-node engines like DuckDB and Polars come and hit the spot. Processing medium-sized datasets can now be done on a single machine. More powerful than Pandas and less overhead than Spark.

But what is the reason behind that robustness?

### They tick most of the factors

Remember the factors I listed in the “What works?“ section? The performance, the friendly interfaces, the minimal setup/maintenance effort, and the cost efficiency?

DuckDB and Polars tick all of that:

[![](https://substackcdn.com/image/fetch/$s_!NigJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbff65175-fcbf-4273-9fd6-5fe159af0918_1874x656.png)](https://substackcdn.com/image/fetch/$s_!NigJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbff65175-fcbf-4273-9fd6-5fe159af0918_1874x656.png)

* DuckDB provides SQL, and Polars offers Python Dataframe.
* Both can be installed easily on your laptop. No cluster setups.
* Dependencies are straightforward to manage (via DuckDB’s extension system and pip/uv for Polars).
* Resource provision = your laptop/server resource. This makes cost management more straightforward.

And, importantly, they are actually fast, especially on small-to-medium-sized datasets. There are several reasons behind this:

* First, there are no overheads that exist in cluster-based engines. No node cold start, no master/worker coordination overhead.

  [![](https://substackcdn.com/image/fetch/$s_!TIKS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf4fc6fb-4956-4ee1-a68d-5ef6507a25a8_572x444.png)](https://substackcdn.com/image/fetch/$s_!TIKS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf4fc6fb-4956-4ee1-a68d-5ef6507a25a8_572x444.png)
* Second, exchanging/reading data mostly happens inside the server. This is clearly faster than exchanging/reading over the network.

  [![](https://substackcdn.com/image/fetch/$s_!e3iD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544c1319-6e68-4564-9397-ec9458b21e6f_782x776.png)](https://substackcdn.com/image/fetch/$s_!e3iD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544c1319-6e68-4564-9397-ec9458b21e6f_782x776.png)
* Third, the hardware capability of a single machine has been improving significantly. The improvement prompts people to ask, “Do I really need a cluster anymore?”

  [![](https://substackcdn.com/image/fetch/$s_!kWrR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d8eedaf-2ac3-43db-907a-88cd61f3f3c7_1118x624.png)](https://substackcdn.com/image/fetch/$s_!kWrR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d8eedaf-2ac3-43db-907a-88cd61f3f3c7_1118x624.png)

  + **RAM**: A MacBook laptop can now have 128 GB of RAM, and an AWS High Memory EC2 instance can have TBs of RAM. [This RAM capability was hard to find in the past](https://www.reddit.com/r/hardware/comments/5cr2j2/how_much_ram_did_computers_have_over_time_timeline/).
  + **Disk:** The speed of the hard disk also underwent a revolution. The transition from spinning HDDs to NVMe SSDs (Non-Volatile Memory Express) fundamentally changed the “spill-to-disk” penalty. Traditional HDDs offered read speeds of ~100 MB/s. Modern [PCIe Gen5 NVMe drives provide read speeds exceeding 10,000 MB/s.](https://www.silicon-power.com/knowledge-detail/what-is-pcie5/) A 100x improvement in throughput.
  + **CPUs**: Modern CPUs have not just added more cores. Instruction sets like [AVX-512](https://en.wikipedia.org/wiki/AVX-512) allow a CPU to perform the same operation on multiple data points simultaneously (Single Instruction, Multiple Data - SIMD). Instead of adding two numbers pair by pair, a processor with AVX-512 can now add, for example, 16 pairs simultaneously. Software that exploits these instructions (Vectorized Execution) can achieve far better performance. (DuckDB and Polars both optimize the performance via Vectorized Execution + SIMD)

### DevEx is no longer optional.

For single-node engines like DuckDB and Polars, a seamless Developer Experience isn’t just a “nice-to-have”; it is the main driver of adoption.

The user base for data tools is expanding beyond specialized data practitioners with technical skills. Data analysts and data scientists want their own “local processing engine“ to play with the data.

[![](https://substackcdn.com/image/fetch/$s_!9TfD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b0d0f36-3927-4a1b-80ad-98acd4626ee9_1104x622.png)](https://substackcdn.com/image/fetch/$s_!9TfD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b0d0f36-3927-4a1b-80ad-98acd4626ee9_1104x622.png)

We are seeing Product Managers, Marketing Analysts, and even C-levels who also want to get their hands dirty.

By being embeddable (e.g., pip install duckdb or pip install polars), users can now access the powerful processing/serving engines right on their laptops.

[![](https://substackcdn.com/image/fetch/$s_!Gdiv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93021758-346b-46ed-93cd-4e5e269696c0_736x410.png)](https://substackcdn.com/image/fetch/$s_!Gdiv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93021758-346b-46ed-93cd-4e5e269696c0_736x410.png)

The more seamless the tool, the higher the "activation rate." When a user can run their first complex query in under 30 seconds, the tool becomes their favorite.

—

Beyond seamless setup and maintenance, these tools can read data from anywhere. Thanks to the **Apache Arrow** ecosystem, the physical location of data matters less than ever.

> *The [Apache Arrow](https://arrow.apache.org/) format focuses on columnar in-memory analytics workloads. The Arrow creators also aim to make it a standard in-memory data representation format for analytics workloads, thereby improving data exchange between systems. You can read my Arrow article here: [Apache Arrow For Data Engineers](https://vutr.substack.com/p/apache-arrow-for-data-engineers?utm_source=publication-search).*

Users can stand on these tools and query data in remote object storage, cloud data warehouse storage, or any supported internet repository.

[![](https://substackcdn.com/image/fetch/$s_!F0vw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c5d56e7-0911-4a20-8d75-fc93f66529fd_1290x778.png)](https://substackcdn.com/image/fetch/$s_!F0vw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c5d56e7-0911-4a20-8d75-fc93f66529fd_1290x778.png)

In addition, Arrow also offers “zero-copy” integration with the Python ecosystem (NumPy, Pandas, Scikit-learn), making working with data locally a complete experience.

[![](https://substackcdn.com/image/fetch/$s_!IcwJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F163374ef-3291-4c0b-a984-8cfcde723800_974x606.png)](https://substackcdn.com/image/fetch/$s_!IcwJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F163374ef-3291-4c0b-a984-8cfcde723800_974x606.png)

This is achieved because **Arrow** provides a standard exchange format, allowing the involved system to skip the serialization and deserialization overhead.

> ***Note:** Arrows are not exclusively implemented for DuckDB or Polar. In theory, any system that implements Arrow will achieve this benefit. The point I want to make is that the ability to query data from nearly everywhere, combined with seamless setup and maintenance, allows these single-node systems to deliver a much better end-to-end user experience.*

---

## Outro

In this article, we begin the journey from the era when a single machine could handle most data requirements, through the internet boom, which led to the creation of MapReduce as a framework for processing data across multiple machines. Then, we see Spark, the solution that aims to solve the problems of MapReduce.

During that time, the world also witnessed the rise of cloud data warehouses with powerful processing capabilities, with a friendly UI/UX and a straightforward pricing model.

From these observations, we see the factors that make a data processing solution attractive.

Finally, we try to understand the rise of the single-node processing engine, which could be summarized down to 3 bullet points:

* They have most of the factors that make a data processing solution attractive
* They close the market gap of “not every company has big data. “
* They prioritize DevEx.

—

Thank you for reading this far. See you in my next articles.

---

## Reference

*[1] Bill Chambers, Matei Zaharia, [Spark: The Definitive Guide: Big Data Processing Made Simple](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/) (2018)*

*[2] Jeffrey Dean and Sanjay Ghemawat, [MapReduce: Simplified Data Processing on Large Clusters](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) (2004)*

*[3] Travis Addair’s answer, [Why is Hadoop slower than Spark?](https://www.quora.com/Why-is-Hadoop-slower-than-Spark/answer/Travis-Addair?ch=10&oid=173920889&share=8bc70da5&srid=uIVXeO&target_type=answer)*

*[4] Barry Smart, [DuckDB: the Rise of In-Process Analytics and Data Singularity](https://endjin.com/blog/2025/04/duckdb-rise-of-in-process-analytics-understanding-data-singularity), (2025)*

*[5] Michael Stonebraker, Andrew Pavlo, [What Goes Around Comes Around... And Around...](https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf) (2024)*
