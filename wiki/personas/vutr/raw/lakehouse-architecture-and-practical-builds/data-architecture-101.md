---
title: "Data architecture 101"
channel: vutr
author: "Vu Trinh"
published: 2026-03-10
url: https://vutr.substack.com/p/data-architecture-101
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Modeling", "Data Warehouse", "Data Lake", "Lakehouse", "Orchestration", "Data Quality"]
tags: [https, auto, image, good, substackcdn, fetch]
---

# Data architecture 101

*What are Data Warehouse, Data Lake, Data Lakehouse, Data Fabric, and Data Mesh? Is Medallion a data architecture? How does data modeling fit into the picture?*

> Source: [Open post](https://vutr.substack.com/p/data-architecture-101)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=189467485)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!Iqc6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc498b65-a649-4cf2-9733-7fe8330da7af_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Iqc6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc498b65-a649-4cf2-9733-7fe8330da7af_2000x1429.png)

---

# Intro

In this week’s article, I note my understanding of the data architecture, what it is, and its purpose, drawing on my humble experience, observations, and learning. Then we will visit terms, such as the warehouse, the lake, the lakehouse, or the data mesh.

The article also includes my clarifications on other questions, such as “Is Medallion a data architecture?” “How does data modeling fit into the picture?”, or “How about the Modern Data Stack?“

> ***Note**: this article is purely my train of thought; if you see anything off, I welcome any feedback.*

---

# What is data architecture?

Like software architecture, there isn’t a single agreed-upon definition of data architecture. In the scope of this article, I will refer to the definition from Joe Reis and Matt Housley in the book [Fundamentals of Data Engineering](https://learning.oreilly.com/library/view/fundamentals-of-data/9781098108298/):

> *Data architecture is the design of systems to support the evolving data needs of an enterprise, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs.*

It’s the blueprint for any operations that provide insights from raw data within the organization, from data ingestion, storage, transformation, management, and serving. More importantly, as the author emphasized, the data architecture must be flexible and agile to support the rapidly growing demand from business users.

There are two main approaches to data architecture: centralized and decentralized.

---

# Centralized architecture

In a company, data hardly comes from a single source. That might be the case at first, but over time, your company will have more services/applications and integrate with more external tools, each generating its own data. Business users are always hungry for data insights; more data generated means they see more opportunities to observe, learn, and optimize the business with the data.

[![](https://substackcdn.com/image/fetch/$s_!_5mM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e441f9f-1010-45bb-8f0b-2a77a6dfc580_562x486.png)](https://substackcdn.com/image/fetch/$s_!_5mM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e441f9f-1010-45bb-8f0b-2a77a6dfc580_562x486.png)

In the centralized approach, data is consolidated in a single “place“. This “place“ is the source of truth for data ingestion, storage, processing, and serving. A centralized team mainly handles data management.

Bill Inmon called this place the data warehouse.

In the following sections, we will discuss the implementations of the data warehouse concept.

## Relational Data Warehouse

In the past, the data warehouse was mostly implemented using transactional databases, which were not designed for analytical workloads.

[![](https://substackcdn.com/image/fetch/$s_!OT-m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd60b1af0-6b4b-4849-ba96-27366a33fa39_614x622.png)](https://substackcdn.com/image/fetch/$s_!OT-m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd60b1af0-6b4b-4849-ba96-27366a33fa39_614x622.png)

In the 2000s and 2010s, OLAP databases bloomed.

The ability to process large amounts of data through scanning and aggregation, plus the pay-as-you-go pricing models of cloud solutions, has made implementing the data warehouse more performant and cost-effective.

The relational data warehouse implementation usually has a bad reputation for accepting only structured data, which is the main motivation for the data lake implementation (covered next).

However, most of the data warehouse solutions these days have richer support for semi-structured data (e.g., JSON data) or even unstructured data (e.g., [Snowflake](https://docs.snowflake.com/en/sql-reference/data-types-unstructured) and [BigQuery](https://cloud.google.com/blog/products/data-analytics/how-to-manage-and-process-unstructured-data-in-bigquery) now support storing and retrieving unstructured data such as text, image, or audio)

## Data Lake

The data lake is a concept that describes the process of storing vast amounts of data in its native format (in HDFS or later in cloud object storage). Unlike relational data warehouses, the data lake doesn’t require a schema definition in advance, so that all data can be stored in the lake without concern for its format.

[![](https://substackcdn.com/image/fetch/$s_!6aj2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F434cd1a8-6da1-4503-aabe-5046309c645f_766x532.png)](https://substackcdn.com/image/fetch/$s_!6aj2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F434cd1a8-6da1-4503-aabe-5046309c645f_766x532.png)

At first, people tried to replace the traditional data warehouse with a data lake by bringing processing directly on top of the lake.However, the approach had many serious drawbacks; the data lake soon became a data swamp due to a lack of proper data management features in the warehouse, such as data discovery, data quality and integrity guarantees, ACID constraints, and data DML support…

Thus, they combined the data lake and the data warehouse.

[![](https://substackcdn.com/image/fetch/$s_!xPUi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F718eb031-b715-4dd0-8277-626675fca7a2_1248x536.png)](https://substackcdn.com/image/fetch/$s_!xPUi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F718eb031-b715-4dd0-8277-626675fca7a2_1248x536.png)

That is why, from the mid-2000s to the 2020s, the implementation that uses the data lake for raw data ingestion and the data warehouse for a subset of transformed data is the most widely recommended approach for building a data warehouse.

## Data Lakehouse

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=189467485)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

However, keeping the data in two places poses challenges, such as the complexity of keeping both the lake and the warehouse in sync, and the total cost of ownership, as the data is stored in two systems.

So, the Lakehouse approach was introduced.

It is an architecture in which you control your data on low-cost storage (e.g., object storage) that enhances traditional analytical DBMS management and performance features, such as ACID transactions, versioning, caching, and query optimization.

[![](https://substackcdn.com/image/fetch/$s_!Izio!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0159581-25b3-40db-8cdf-900d165211dc_1184x1002.png)](https://substackcdn.com/image/fetch/$s_!Izio!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0159581-25b3-40db-8cdf-900d165211dc_1184x1002.png)

The difference from the previous effort, when people also tried to bring processing directly on top of the data lake, is that more efficient metadata layers (table formats) were introduced. Databricks created Delta Lake, Netflix created Iceberg to manage analytics data more efficiently on S3, and Uber developed Hudi to bring data upsert and incremental processing capabilities to the data lake.

The main advantage of the Lakehouse architecture is the promise of interoperability, as you can bring any query engines (in theory) to access the data stored in the lake + table format.

If you don’t know, technically, BigQuery or Snowflake is the Lakehouse implementation, as their data is stored in object storage (or a system with similar properties to object storage) with the metadata layer, and the query engine operates separately. But it is against the spirit of the lakehouse manifesto, as you don’t control your storage layer, and the use of your favorite engines depends on vendor support.

However, in recent years, those vendors have allowed organizations to use BigQuery or Snowflake as the query engine for data stored in full-control object storage, with table formats such as Iceberg or Delta Lake.

## Data Fabric

The data fabric architecture entered the field around 2016. It’s essentially the data lake + warehouse architecture with enhanced functionalities to improve data accessibility, discoverability (through metadata management and data virtualization), and security.

[![](https://substackcdn.com/image/fetch/$s_!a6PC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafbbf1fb-aabb-4a0b-b22c-99e77e54aded_1056x590.png)](https://substackcdn.com/image/fetch/$s_!a6PC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafbbf1fb-aabb-4a0b-b22c-99e77e54aded_1056x590.png)

I might get a lot of hate for saying this: although this approach could indeed improve the data lake + warehouse architecture, for me, it’s more of a marketing term used by big players to sell their solution. The data lake + warehouse architecture + other tools and layers don’t make it a good buzzword.

---

# Decentralized architecture

Instead of consolidation, data ownership in this approach is distributed across business domains. For example, the marketing team will be responsible for the marketing data.

[![](https://substackcdn.com/image/fetch/$s_!8Mrl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb17856f1-4187-4756-9dbc-916f845566f8_662x524.png)](https://substackcdn.com/image/fetch/$s_!8Mrl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb17856f1-4187-4756-9dbc-916f845566f8_662x524.png)

This approach is introduced as a counterpoint to the centralized approach, in which the productivity depends on the managed team’s capacity and business understanding of the data.

## Data Mesh

And data mesh is the pioneer in this approach.

Data Mesh was first introduced by [Zhamak Dehghani](https://x.com/zhamakd) in the blog post [How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html) (2019)

The idea was very new at that time.

(I remember very clearly the feeling of reading that article in 2020: excited and doubtful at the same time.)

Instead of a “central repository,” the data mesh decentralizes responsibility for data management. The approach is inspired by the domain-driven design (used in software architectures), data is treated as a product, and distributed ownership across business domains (e.g., marketing, sales). Each domain data product should be discoverable, secure, and interoperable.

[![](https://substackcdn.com/image/fetch/$s_!j7Rm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd05e9ee6-8a29-4679-8afc-aa86c2c15e34_864x634.png)](https://substackcdn.com/image/fetch/$s_!j7Rm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd05e9ee6-8a29-4679-8afc-aa86c2c15e34_864x634.png)

Domains can use different implementations to manage data, such as a lakehouse or a data lake + warehouse. At the end of the day, data products must be exposed in the same way a backend engineer exposes APIs.

To support resource provisioning, data pipeline onboarding, and other tasks, the data mesh implementation includes a data infrastructure team that provides these services to the other teams. This avoids duplicating effort as each domain doesn’t need to set up and maintain infrastructure.

Although the promise of no-bottleneck central teams, domain-driven data ownership, and scalability is compelling, implementing a data mesh is very challenging, especially if a company’s data maturity is low.

First, it requires a mindset change: each domain team must be responsible for the quality of the data it produces and for how other teams consume it seamlessly. If the company first adopts a centralized approach and then switches to data mesh, the transition might take a long time, as those teams are used to the request-result paradigm.

A company might need to hire more data professionals as each domain will have a small data team. Also, building a data infrastructure platform is not easy and requires even more human resources.

---

# How does data modeling fit into the picture?

> *A data model is a structured representation that organizes and standardizes data to enable and guide human and machine behavior, inform decision-making, and facilitate actions. — [Joe Reis](https://joereis.substack.com/p/my-definition-of-data-modeling-for)*

Data architecture will give you a broader, more comprehensive picture of how data is used within a company for its entire lifecycle. However, data engineers, data analysts, data scientists, or even AI models need an answer for a more detailed question: how data is actually structured. That's where data modeling comes in.

[![](https://substackcdn.com/image/fetch/$s_!P5X-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f52a0c6-1b37-4928-ad75-49a356a92651_1412x690.png)](https://substackcdn.com/image/fetch/$s_!P5X-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f52a0c6-1b37-4928-ad75-49a356a92651_1412x690.png)

Without modeling, data architecture is just a collection of pipelines and storage. You can also think of data modeling as a part/component of the data architecture.

A note is that there are no rules or restrictions on which data modeling approach to use with which data architecture. The modeling approach (e.g., Kimball, Inmon, or Vault) will be determined by your needs and context.

---

# Is Medallion a data architecture?

If you are a data engineer and have internet, you might have heard of the term Medallion. It is a term coined by Databricks to describe the organization of data into three layers in a lakehouse:

[![](https://substackcdn.com/image/fetch/$s_!yK6K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3e20e85-1291-49d6-8da6-d04a8fd8c55d_1436x354.png)](https://substackcdn.com/image/fetch/$s_!yK6K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3e20e85-1291-49d6-8da6-d04a8fd8c55d_1436x354.png)

* Bronze: raw data lives here.
* Silver: cleaned and standardized data lives here.
* Gold: business-support data lives here.

This helps control data quality, apply governance, and provide reproducibility. However, organizing data into layers is not an idea exclusive to Databricks; it has long existed under different names. One of the common versions you might have seen is: Landing, Curated, and Serving.

For me, the Medallion is more like a pattern than an architecture.

The architecture is the high-level blueprint of how data is ingested, stored, processed, and served, while a pattern is a reusable solution to a specific problem in the architecture.

In this case, Medallion is a pattern that guides you in organizing the data in your storage. Of course, this means Medallion is not data modeling either.

---

# How about Modern Data Stacks?

Another term that has been floating around in recent years is the “Modern Data Stacks”. For me, it's more like a philosophy than an architecture.

[![](https://substackcdn.com/image/fetch/$s_!MLLm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F030290f7-18cd-4ed4-ab4d-463efad00362_1210x734.png)](https://substackcdn.com/image/fetch/$s_!MLLm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F030290f7-18cd-4ed4-ab4d-463efad00362_1210x734.png)

It suggests building complete data solutions using a set of modern, cloud-native solutions such as Fivetran for ingestion, dbt for SQL transformation management, Dagster for orchestration, and cloud data warehouses such as Snowflake or Databricks.

---

# How about Lambda and Kappa?

In the Lambda approach, data is routed to two paths: The batch and the stream layer.

* The first process data in a large chunk (e.g., daily, weekly)
* The latter processes data as it arrives to provide low-latency updates.

There is an assumption about the trade-off between the two layers: the batch will be more accurate but will provide delay insights, while the stream layer provides faster insight but might sacrifice accuracy a bit.

[![](https://substackcdn.com/image/fetch/$s_!aYJt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb68748c1-57d7-43ad-9199-76f16199f7ef_1450x556.png)](https://substackcdn.com/image/fetch/$s_!aYJt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb68748c1-57d7-43ad-9199-76f16199f7ef_1450x556.png)

The results from the two layers are unified and served to users; they will observe fast insights (from the stream layer), and these might be corrected later (by the batch layer) if needed.

The biggest disadvantage of this approach is that users have to maintain two code bases and systems.

Kappa was introduced to address this problem.

Instead of treating data as hot and cold, Kappa treats everything as a stream.

[![](https://substackcdn.com/image/fetch/$s_!SiAI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F202871ec-f1d2-43aa-bbcd-7a866f0ce17e_1238x586.png)](https://substackcdn.com/image/fetch/$s_!SiAI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F202871ec-f1d2-43aa-bbcd-7a866f0ce17e_1238x586.png)

In Kappa, even historical data is “replayed” and processed as a stream. For example, re-consuming a Kafka message from an earlier offset and running the data through the same processing code again.

Now you will have a single codebase. However, the solution is not free as it requires experience in operating and maintaining stream systems such as Kafka, Flink, or Spark Micro Batching.

—

For me, Lambda and Kappa are more like patterns than architectures, as they provide solutions for data processing and serving.

---

# Outro

Most of the time in this article, I tried to clarify and categorize concepts such as data warehouse, data lake, data lakehouse, data fabric, data mesh, data modeling, Medallion, modern data stack, Lambda, and Kappa.

I hesitated to write this article at first because I also felt confused about these terms. However, I still decided to go with it, as many of you feel the same.

I hope my work clears up the mist.

If the next time you read a piece online, you can wrap your head around the terms I discussed here, please let me know.

Or, if you don’t agree with things I wrote, feel free to leave comments.

Thank you for reading this far.

See you in the next articles.

---

# Reference

*[1] James Serra, [Deciphering Data Architectures: Choosing Between a Modern Data Warehouse, Data Fabric, Data Lakehouse, and Data Mesh](https://www.amazon.com/Deciphering-Data-Architectures-Warehouse-Lakehouse/dp/1098150767) (2024)*

*[2] Joe Reis and Matt Housley, [Fundamentals of Data Engineering](https://learning.oreilly.com/library/view/fundamentals-of-data/9781098108298/) (2022)*
