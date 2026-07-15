---
title: "Data engineering system design: 9 data serving problems"
channel: vutr
author: "Vu Trinh"
published: 2026-04-21
url: https://vutr.substack.com/p/data-engineering-system-design-9
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Lakehouse", "Streaming", "Data Quality"]
tags: [https, auto, good, fetch, image, substackcdn]
---

# Data engineering system design: 9 data serving problems

*Data serving is not only about performance.*

> Source: [Open post](https://vutr.substack.com/p/data-engineering-system-design-9)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=194032566)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!CKeZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F096e05f5-2984-4e88-b1a3-d111346d885a_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!CKeZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F096e05f5-2984-4e88-b1a3-d111346d885a_2000x1429.png)

---

# Intro

I’d spend most of my time on ingestion and transformation. Pick the right data pipeline configs. Argue about scaling the data processing. And then, when it came time to talk about how the data would actually reach the people who needed it, I’d wave a hand and say, “W*e’ll expose it through the warehouse.”*

The serving layer was the part I treated as obvious, although it’s the most vital component that determines the pipeline's overall success. Business users care about insights, dashboards, or reports; they don’t care about the robust pipeline that could scale to 10x the data.

This is a sharing of what I’ve come to believe about serving data, the questions I keep returning to, and the patterns I’ve watched work and fail. Some of it I learned the hard way. I learned some of it by observing better engineers.

This article focuses on the technical aspect of the serving layer. Problems covered are:

* How will data be stored and served?
* How old can the data be before it is considered stale?
* What is the “raw” level of data?
* What is the usage pattern of the data?
* How many consumers will read this data concurrently?
* How do you handle serving stale or incorrect data?
* Can the serving layer guarantee safe writes?
* Who can access the data, and at what level?
* How about the AI models?

In each section, I will explain what information we could have when we answer the question, and from that, we can design a better serving layer.

> ***Note 1**: What is discussed in this article is based solely on my observations and experience; feel free to provide feedback on anything you see I may have missed.*

Before we step into the problems, let’s agree on the “mental model“ throughout this article.

---

---

# The mental model

If you're starting your data engineering journey, there's a very high chance you will encounter the “one wide table to serve everything” situation.

I was tasked with building a dashboard and letting users run ad hoc SQL queries. I decided to build one that's beautifully modeled and pre-joined, and let everyone query it. Dashboards queried it. The data science team queried it. An internal app pulled from it. A downstream pipeline ingested from it.

It felt clean at first. Then it wasn’t.

[![](https://substackcdn.com/image/fetch/$s_!AX-I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5274da8a-0af6-4351-a07c-0ccc476b0a39_758x632.png)](https://substackcdn.com/image/fetch/$s_!AX-I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5274da8a-0af6-4351-a07c-0ccc476b0a39_758x632.png)

I want pre-aggregated data for the dashboard because scanning the full table for every filter was slow. The data scientists wanted data at a lower grain. The app needed sub-second lookups by user\_id, which were slowed by the columnar layout and the large data scan without indexing. The refresh frequency varies across use cases: data scientists are fine with daily updates, while the dashboard requires hourly refreshes.

My lesson is that you will never have a single-serving approach that satisfies every use case. Some need raw files, some need tables. Some view on the dashboard, some consume via API. You must identify how your data will be used.

In other words, requirements gathering and understanding are very important; they guide you in every decision you make.

---

# How will data be stored and served?

This is the first question I ask.

A table, a dashboard, a CSV file, exposing via API, exposing via web-app, or an ML training dataset.

[![](https://substackcdn.com/image/fetch/$s_!CSWl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa34fa254-927c-432a-a870-3b4b67c8e4ff_872x718.png)](https://substackcdn.com/image/fetch/$s_!CSWl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa34fa254-927c-432a-a870-3b4b67c8e4ff_872x718.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=194032566)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

This will help you prepare better the infrastructure to deliver the output efficiently: Do I need to develop a set of APIs? Where do I store CSV files? Do I serve the table in columnar or row formats?

Some example use cases and what you need to prepare:

* **A table in a warehouse**: analysts and BI tools will query it directly. Columnar format + partitioned or/and clustered if needed
* **A dashboard**: usually backed by warehouse tables or pre-aggregated tables. The real engineering is in the pre-aggregation and caching.
* **File**: downstream consumes the data via script, spreadsheet, or handoff to another system. The question is: where do you store it, which format to use, who’s allowed to fetch it, and how do you version it? Cloud object storage could be the answer most of the time
* **API**: application consumers, such as an internal data tool. You're now running a service. That means uptime SLAs, authentication, rate limiting, versioning, and API designing (a whole new world)

---

# How old can the data be before it is considered stale?

This question provides two things:

[![](https://substackcdn.com/image/fetch/$s_!HdI6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7950c910-473d-460b-9646-2484c226e953_944x642.png)](https://substackcdn.com/image/fetch/$s_!HdI6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7950c910-473d-460b-9646-2484c226e953_944x642.png)

* Determine the frequency of reaching the source? More on this when we discuss sources in the future article.
* Choose the infrastructure that could help deliver the desired freshness.

  + If they need low latency, choose the serving option that lets you read from memory for recent data. It could be a dedicated database, such as [Pinot](https://github.com/apache/pinot) or [Druid](https://druid.apache.org/), or a sub-option from your database; for example, [BigQuery offers BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro) for this purpose.
  + A materialized view could be an option for many real-time use cases; it refreshes the data based on the source change every X interval.

    [![](https://substackcdn.com/image/fetch/$s_!DXJ7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a1b0604-5929-41d1-b5e8-dd2a4715e373_1030x356.png)](https://substackcdn.com/image/fetch/$s_!DXJ7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a1b0604-5929-41d1-b5e8-dd2a4715e373_1030x356.png)
  + For use cases that are fine with once a day or once a week, you rarely need to do anything else besides exposing your data via a data warehouse solution.

---

# What is the “raw” level of data?

This question sounds simple.

It isn’t.

“Raw” means different things to different users.

To a data scientist, raw means event-level, every click, every transaction, every state change, with nothing filtered or rolled up.

To a BI analyst, it often means fact-table level, denormalized events with dimensions joined in, ready to slice.

To an application backend, raw might mean the latest state of an entity, one row per user, reflecting the current value.

This question helps you prepare for the output data grain, the lowest level of detail, or specifically what an individual row represents (e.g., "one row per event” or “one row per country").

[![](https://substackcdn.com/image/fetch/$s_!ZS86!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F798c86e5-697e-4001-ab9a-24a1063c198e_1346x722.png)](https://substackcdn.com/image/fetch/$s_!ZS86!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F798c86e5-697e-4001-ab9a-24a1063c198e_1346x722.png)

The principle is that the lower the grain, the more flexible you have. This is because lower grain could be aggregated to higher grain later (e.g., (date, event) → date);

[![](https://substackcdn.com/image/fetch/$s_!ivjc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57aeab3f-9181-4e27-850b-3cf5108644b9_774x762.png)](https://substackcdn.com/image/fetch/$s_!ivjc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57aeab3f-9181-4e27-850b-3cf5108644b9_774x762.png)

However, a higher grain table could not be down back to the lower grain (e.g., (date) can not → (data, event))

[![](https://substackcdn.com/image/fetch/$s_!Porj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F516892e9-5288-429a-ba55-c108babf859c_1116x610.png)](https://substackcdn.com/image/fetch/$s_!Porj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F516892e9-5288-429a-ba55-c108babf859c_1116x610.png)

In return, the higher-grain table could be more performant and more convenient for the users. If the user only needs data at the date level and the table is already prepared for that range, they don’t need to execute the GROUP BY.

Dashboard users usually prefer higher-grain tables, while ad hoc and exploratory use cases require lower-grain tables.

---

# What is the usage pattern of the data?

This question decides your physical layout.

You might know about partitioning and clustering. You might know their benefits: partitioning helps you break your table into smaller ones, while clustering helps you colocate similar data. This helps boost query performance if they can leverage the partitioning and clustering specs. (e.g., filtering on the “date“ partition or join on the clustered column “user\_id“)

[![](https://substackcdn.com/image/fetch/$s_!rTyP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c7acda2-2150-4ea7-a8f0-dae7f93f7e6b_1320x580.png)](https://substackcdn.com/image/fetch/$s_!rTyP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c7acda2-2150-4ea7-a8f0-dae7f93f7e6b_1320x580.png)

However, it came with the cost of the write process: as data needs to be organized when writing, writing data naively is always faster than writing it in a predefined layout.

[![](https://substackcdn.com/image/fetch/$s_!uprI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F006db85b-94db-444b-9a78-66d353ce5438_1046x358.png)](https://substackcdn.com/image/fetch/$s_!uprI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F006db85b-94db-444b-9a78-66d353ce5438_1046x358.png)

Thus, you must ensure that the optimization techniques you apply can actually help your users (for at least 80% of the queries they execute on this table). If they don't, it wastes resources (on the write side) but gets nothing in return.

Some example questions are:

* Do consumers filter by date, region, or another dimension? Which one is hit in 80% of queries?
* Do they frequently join on a specific key, user\_id, product\_id?
* …

Another hidden factor that impacts your physical layout is how often new data arrives. As OLAP systems operate with an immutable data file, new data will result in a new file. The more frequent the insert, the more (small) files are created. The read operations now require opening more files to execute the query.

In addition, clustered data might not be in an optimal layout as more data comes in; for example, when sorting data by user\_id, data with id A is organized close together across two files. However, when new data with id A arrives, it is now spread non-contiguously across 4 files.

—

[![](https://substackcdn.com/image/fetch/$s_!6mwq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe3a464d-519c-47a6-8ce1-a0ec3b1e74b5_744x416.png)](https://substackcdn.com/image/fetch/$s_!6mwq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe3a464d-519c-47a6-8ce1-a0ec3b1e74b5_744x416.png)

This requires a compaction process that consolidates data files into a single larger file to improve read performance and ensure the data follows the desired layout (e.g., sorting). You don’t need to worry about this process when using cloud data warehouses such as BigQuery or Snowflake, as they automatically run compaction in the background. However, if you self-manage, for example, a lakehouse solution with a table format like Iceberg, you must manage the compact process yourself.

---

# How many consumers will read this data concurrently?

Usually, OLAP use cases don’t deal with concurrency as much as OLTP use cases. We rarely handle 10,000 concurrent queries, as our data warehouse is mostly used internally, unlike an OLTP database that could back a worldwide-scale application. However, we still need to keep the concurrency problem in mind, as it is not only about how many people are reading at the same time but also about resource consumption:

[![](https://substackcdn.com/image/fetch/$s_!nF3p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbefccd83-4fd4-470a-a5d2-f81ed5d62a2d_1024x994.png)](https://substackcdn.com/image/fetch/$s_!nF3p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbefccd83-4fd4-470a-a5d2-f81ed5d62a2d_1024x994.png)

More queries mean more resource contention. Let’s say you have A resource, 1 query run could have all A. But 1000 queries run concurrently will share A (in the worst case, under FIFO scheduling, where the “giant” query takes all the resources and leaves all others waiting), slowing down every query. In addition, most systems have a limit on the number of concurrent queries/requests; exceeding the limit causes your query to be abandoned.

Here, we assume data access is at the internal scale; there are (rare) cases when you need to design a user-facing analytics application (e.g., a profile view on LinkedIn), and your infrastructure must adapt to a larger scale of consumption.

Thus, asking about the concurrency requirements in analytics use cases might feel unnecessary at first, but it’s the one you should ask and prepare:

* Most cloud warehouses could handle the concurrency requirement if it’s not extremely high. Keep in mind your cloud data warehouse concurrency quotas.
* You can think of reducing the workload of a single query to make it finish faster, which could then give up their “slot” for other queries:

  [![](https://substackcdn.com/image/fetch/$s_!nGWl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d04d07b-fef4-435a-bcf8-7d3719d60447_556x648.png)](https://substackcdn.com/image/fetch/$s_!nGWl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d04d07b-fef4-435a-bcf8-7d3719d60447_556x648.png)

  + Pre-aggregate the data.
  + Caching the result using the cloud data warehouse’s caching mechanism, materialized view, or caching on the client side.
* Considering isolating resources into “pools“ to avoid a heavy query could “eat“ all the resources from the “light query. “

  [![](https://substackcdn.com/image/fetch/$s_!O7QN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F014e21c8-af15-4d0b-85d8-b6d14b030798_1234x376.png)](https://substackcdn.com/image/fetch/$s_!O7QN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F014e21c8-af15-4d0b-85d8-b6d14b030798_1234x376.png)
* In some cases, you might need to consider specialized solutions such as Apache Pinot or Clickhouse.

---

# How do you handle serving stale or incorrect data?

Bad things will happen. The question isn’t whether your serving layer will ever serve bad data. The question is whether it’s honest about it, or whether your users find out before you do.

Some related questions that can be asked are:

* Can consumers tolerate stale data during a failure, or is stale data worse than no data?
* If upstream corrects a number from a week ago, does serving need to reflect it?
* How will consumers know whether what they’re looking at is fresh or stale? Good or corrupted?

Some action could bring more trust to the user:

* **Explicitly confirming at the serving layer**: Alert on what consumers actually experience.

  [![](https://substackcdn.com/image/fetch/$s_!RMb2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaf48aa1-c51e-4c75-a919-018a9f17bfb4_874x484.png)](https://substackcdn.com/image/fetch/$s_!RMb2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaf48aa1-c51e-4c75-a919-018a9f17bfb4_874x484.png)

  + You might implement the “data contracts” here: it formalizes what producers guarantee (schema, freshness, completeness). In other words, it is a sign that says “this data is good to go”.
  + The goal is to catch the “weird things“ before users use and give users peace of mind when using the data.
  + For a scenario that you can’t catch the issue before the user notices, the best move is to communicate about the issue explicitly, notify that the data isn’t good to go, and then spend time fixing it. The root cause must be communicated broadly, and further action is needed to prevent it from happening again (e.g., add data quality check rules)
* **Backfilling:** When issues happen, we need to fix them and might need to backfill. Because backfill can happen on a wide range of data. The data before and after backfilling might look very different. End users might be in shock if the dashboard from 2 hours ago looked very different compared to the current version.

  [![](https://substackcdn.com/image/fetch/$s_!ddS6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90010cbd-4311-42c3-9bfb-c5ad88569aec_786x582.png)](https://substackcdn.com/image/fetch/$s_!ddS6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90010cbd-4311-42c3-9bfb-c5ad88569aec_786x582.png)

  + You can try writing the backfill result to a separate table, then run some checks to ensure it’s correct. Then send a notification to the user about the backfill process, and rename the backfill table to the main table.

---

# Can the serving layer guarantee safe writes?

The serving layer is not only about exposing data but also about accepting data from write operations (such as data transformation tasks). Thus, the serving layer must be questioned to clarify its ability to ensure:

* Atomicity
* Idempotency
* Schema Evolution

## Atomicity

Atomicity means an operation is done all-or-nothing; it either completes fully or has no effect. This will help your serving layer retry seamlessly if it fails. You will know for sure that when the writing task fails, no partial data will be persisted in the serving layer.

[![](https://substackcdn.com/image/fetch/$s_!gIgJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa3d9ca8-5af0-429b-acfb-9f2db478f249_928x428.png)](https://substackcdn.com/image/fetch/$s_!gIgJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa3d9ca8-5af0-429b-acfb-9f2db478f249_928x428.png)

For most OLAP databases, such as BigQuery, Databricks, or Snowflake, we don’t need to worry about this, as they are ACID-compliant by design.

A case where the serving layer with no support for atomicity could cause data corruption: your data scientist needs CSV files in object storage; loading data from local to object storage is atomic if you’re operating on one object. But it isn’t when you work with two or more objects. There are 3 CSV objects, but the process uploads only 1 successfully.

Because object storage does not support multi-object atomicity, it results in a partial result (1 CSV file in object storage), and the data scientist might now read incomplete data.

## Idempotency

Idempotency is about what the serving layer does when it receives the same logical write more than once.

[![](https://substackcdn.com/image/fetch/$s_!hmX5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd660c6d6-a7dd-416d-8c06-50ab77fb7e96_818x332.png)](https://substackcdn.com/image/fetch/$s_!hmX5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd660c6d6-a7dd-416d-8c06-50ab77fb7e96_818x332.png)

A pipeline publishes today’s partition. However, you realize there is a bug. You fixed and kicked off a run. Now the serving layer is seeing the same logical write arrive twice, and the question is whether the table ends up in the right shape or with duplicates.

This is a property of how the serving layer absorbs the write. Things need to be clarified:

* If the same logical write arrives at the serving layer twice, what happens to the data?
* Can the table detect that a given batch, partition, or event has already been written, and reject or absorb the duplicate cleanly?
* Does the serving layer support overwrite-by-key semantics, or only append?
* If a consumer reads the table before and after the duplicate write, will they see the same result both times?

Then, we can think of

[![](https://substackcdn.com/image/fetch/$s_!XCBE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2192a8ed-e699-4171-b8e3-eb9a27c7a426_1326x896.png)](https://substackcdn.com/image/fetch/$s_!XCBE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2192a8ed-e699-4171-b8e3-eb9a27c7a426_1326x896.png)

* **MERGE/upsert semantics**: the serving layer can absorb the same logical write repeatedly and converge on the same final state. The second write doesn’t add rows; it matches on key and replaces.
* **Overwrite-by-partition**: the serving layer treats a partition as the unit of truth. Writing today’s partition twice replaces it twice, leaving the table in the same shape.
* **Deduplication on write**: the serving layer itself filters duplicates based on a key before persisting the data.
* **Append-only with dedup on read**: the table accepts everything, and consumers deduplicate at read time using a mechanism such as the “latest version” view. It can work if your serving layer only supports appending, but it adds complexity for consumers and makes our table less trustworthy.

## Schema evolution

Your business users might need more fields or remove some; a field type might be changed to promote an INT to a BIGINT to avoid overflow. The question is whether your serving layer can absorb those changes safely or break and take consumers down with it.

You might want to clarify:

* Can columns be added to the serving table without rewriting historical data?
* Can columns be renamed without breaking existing queries?
* Can types be promoted (INT → BIGINT, FLOAT → DOUBLE) safely?
* How do consumers find out when the schema has changed?
* Is there a way to roll back a schema change if it turns out to be wrong?

Then you can think of:

[![](https://substackcdn.com/image/fetch/$s_!FdD_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe71e5e96-0d27-46df-814d-c4b2f95724c5_1530x682.png)](https://substackcdn.com/image/fetch/$s_!FdD_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe71e5e96-0d27-46df-814d-c4b2f95724c5_1530x682.png)

* **Table formats with native schema evolution:** Delta, Iceberg, Hudi, or native cloud data warehouse support adding, renaming, and type-promoting columns as metadata operations. No data rewrite. The table format tracks which version of the schema each file was written under and reconciles at read time.
* **Additive-only evolution**: You might consider only allowing adding new nullable columns; never rename, never drop, never change types. Old queries continue to work because the columns they reference still exist. It’s restrictive, but it’s safe, especially if many downstream systems consume the table.
* **Versioned tables/snapshots**: instead of evolving the schema in place, publish a new version (`user`, `user_v2`, `user_v3`) and migrate consumers over time. Heavier operationally, but useful when the change is so large that in-place evolution is risky.
* **Schema registry** (such as Confluent, AWS Glue): for streaming serving layers, especially. Producers register their schema; consumers fetch it. Backward- and forward-compatibility rules are enforced at publish time, so any incompatible change is rejected before it reaches production.
* **Verify schema changes at build time**: before a schema change is merged, run tests against a simulated new-schema version. We can catch breaking changes at the CI pipeline, not in the production dashboard.

---

# Who can access the data, and at what level?

Here is the pattern you might see:

A team ships fast in the early days, giving everyone broad access so everything can move fast. The team promises to “tighten it up later.” Time passes; there are hundreds of tables, a handful of sensitive datasets, and any user could have access to all of them.

The first time the security team requests an audit, the team spends a full month reinforcing access controls and praying they don’t have any issues, such as data leaking or someone accidentally deleting a table they’re not supposed to have access to.

What to ask in the design phase:

* Does the serving infrastructure need to be in a private network or publicly reachable?
* Which teams or services are allowed to connect? How are permissions granted, and how are they revoked?
* Do different users need to see different rows or columns, or only different tables?

Then, we can implement the access control on different levels:

[![](https://substackcdn.com/image/fetch/$s_!_IZi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9915df58-de5b-48b4-be3c-3dad702e193c_1072x702.png)](https://substackcdn.com/image/fetch/$s_!_IZi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9915df58-de5b-48b4-be3c-3dad702e193c_1072x702.png)

* **Infrastructure**: You might need a private VPC, private endpoints, or IP allowlists. (You might need to work with the infrastructure team here)
* **Service**: service accounts, API keys, IAM roles, credential rotation. Who is the caller: the data warehouse, the dashboard, or this API endpoint? Are they authorized?
* **Table**: then move one to control access by granting and revoking at the dataset or table level. It is the most common access control level, and it is handled natively by most warehouses.
* **Row-level:** Data warehouses such as Snowflake, BigQuery, Databricks support row-level security policies. You can also use a view (and grant access control on the view) to filter out which subset of rows a user can read.
* **Column-level**: In the same table, different users see different fields. Some data warehouses support this level of access control.

---

# How about the AI models?

In today's world, discussing anything without bringing AI into it is a crime.

Joking aside, the demand for feeding data to AI models such as GPT, Gemini, Opus, or a self-hosted model is real. Plus, the incentive of “AIs can do anything, so they can also answer my analytics question” is everywhere.

Speaking about the serving layer, the AI models can now be in two roles:

[![](https://substackcdn.com/image/fetch/$s_!TWMq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ac3c9b9-a444-45cc-b2f3-4a3009f6fb94_860x278.png)](https://substackcdn.com/image/fetch/$s_!TWMq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ac3c9b9-a444-45cc-b2f3-4a3009f6fb94_860x278.png)

* The customer: we serve data to AI models.
* AI models are the serving layers: a chat interface and the CEO can ask about the revenue trend for the last three months (?)

For the first case, where we treat AI models as customers, most of what we’ve discussed so far in this article applies. However, we must apply with a new mindset:

* Besides the data, the pipeline now centers on the model. Versioning model, testing model, and deploying it. (with the help of AI engineers, if you’re lucky)
* Data might be more unstructured than ever; it doesn’t stop at a nested field in a table, it could be a PDF, an image, or even a video.
* It’s no longer only point lookup and history scan; it’s now an approximate nearest neighbors index to help AI models find the relevant vectors faster. Besides the OLAP database, we might need to spend time on a vector database.

For the case where AI models are the serving layers themself, things get more complicated. GPT or Gemini could indeed give you the answer to what you asked, as long as you make sure they have the context to understand and the tools to execute. And, this opens a new world.

Just imagine you’re building a chat interface that lets business users input questions. The AI model analyzes the input, gathers information, generates SQL, executes the SQL, and creates a report or chart. To ensure a reliable answer, we must:

* Ensure there is enough context: we can provide the guidelines via the system prompts, provide them with the MCPs to read the document somewhere, or equip them with a semantic layer, [which acts as the information repository as well as the guardrail.](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-the-semantic?utm_campaign=post-expanded-share&utm_medium=web)
* Ensure there are enough tools: we provide them with the permissions to execute the queries, create the dashboard, or run some code.
* Coordinate agents: some complex jobs might require a set of agents working together, and the agent can encounter different kinds of challenges: memory overflow, lack of permission, or stay idle without any clear reasons.
* Tailor and keep it consistent: Because LLM is simply a giant probabilistic text generator, your daily report might have different insights when you ask for it twice. Providing feedback, adjusting the guideline, or doing something called harness engineering (honestly, I’m not sure if I understand the term properly).

Making an AI model a serving layer is not an exclusive challenge in the data field; it’s a challenge in nearly every field. We need to resolve these challenges with the same mindset when we serve data directly to users: insights must be retrievable in a timely, accurate, and safe manner.

---

# Outro

In this article, I discussed my nine concerns about designing a robust data serving layer:

* How will data be stored and served?
* How old can the data be before it is considered stale?
* What is the “raw” level of data?
* What is the usage pattern of the data?
* How many consumers will read this data concurrently?
* How do you handle serving stale or incorrect data?
* Can the serving layer guarantee safe writes?
* Who can access the data, and at what level?
* How about the AI models?

In each section, I discuss why it matters and patterns/solutions to resolve it. Hope my work brings you value.

Thank you for reading this far. See you in my next article.
