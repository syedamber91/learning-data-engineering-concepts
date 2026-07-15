---
title: "Data engineering system design: 9 data processing problems"
channel: vutr
author: "Vu Trinh"
published: 2026-05-05
url: https://vutr.substack.com/p/data-engineering-system-design-9-4c5
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Orchestration", "Streaming", "Batch Processing", "Data Quality"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# Data engineering system design: 9 data processing problems

*The data volume is just a one of them.*

> Source: [Open post](https://vutr.substack.com/p/data-engineering-system-design-9-4c5)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=195410088)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!P_wH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff34ba6bb-4fac-4dac-ac57-00ee365fee7a_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!P_wH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff34ba6bb-4fac-4dac-ac57-00ee365fee7a_2000x1429.png)

---

# Intro

To complete the data-engineering system design series (after the three parts: [serving](https://vutr.substack.com/p/data-engineering-system-design-9), [sourcing](https://vutr.substack.com/publish/post/194761871?r=2rj6sg&utm_campaign=post&utm_medium=web), and [orchestration](https://vutr.substack.com/p/data-engineering-system-design-orchestration)), we will now turn to the final part: data processing.

> *It’s the last part until I feel it necessary to cover some other aspects :D*

The format will be the same.

There is a set of data processing problems that I believe are crucial. Each problem will be discussed in its own section, which includes my personal thoughts on why and how we’ll solve it. The 9 problems are:

* Batch or stream processing?
* What are the business rules?
* How do you ensure data quality at the processing layer?
* How do you ensure the processing logic is correct?
* What if the pipeline fails?
* Can the pipeline be backfilled?
* What is the side effect of reruns?
* How are credentials and configurations managed?
* How do you observe the processing?

> ***Note**: What is discussed in this article is based solely on my observations and experience; feel free to provide feedback on anything you see I may have missed.*

---

# Mental Model

Data processing is the layer that sits between the source and the sink. I want to refer to this layer as “middle steps“ as “processing” does not cover everything that happens here.

This layer takes what the source gives you and shapes it into what the sink needs.

The source doesn’t care about your output requirements.

The sink doesn’t care about what the source looks like.

The “middle steps“ absorb the gap between them and make sure the gap is filled.

Just keep in mind that, to fill that gap, many things need to be evaluated and resolved; it is not only about choosing between Flink and Spark. Business logic, data quality decisions, failure handling, schema changes, processing framework, distributed vs. single-node, and other concerns.

---

# Batch or stream processing?

This is the question that shapes every infrastructure decision that follows. The way you should think about it depends on whether you’re building a batch or streaming pipeline.

> *The choice between batch and stream processing should be defined based on [serving](https://vutr.substack.com/p/data-engineering-system-design-9) and [sourcing](https://vutr.substack.com/publish/post/194761871?r=2rj6sg&utm_campaign=post&utm_medium=web) information/requirements.*

## Batch

[![](https://substackcdn.com/image/fetch/$s_!6szE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71cdfacf-9a60-4762-ad45-2bb9f95112d9_1178x464.png)](https://substackcdn.com/image/fetch/$s_!6szE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71cdfacf-9a60-4762-ad45-2bb9f95112d9_1178x464.png)

In a batch, the natural questions are straightforward:

[![](https://substackcdn.com/image/fetch/$s_!ZlfT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51caf4b1-3599-42d9-a139-4c988f21fd51_1020x456.png)](https://substackcdn.com/image/fetch/$s_!ZlfT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51caf4b1-3599-42d9-a139-4c988f21fd51_1020x456.png)

* How much data?
* And how long does the data processing have to finish?

The two questions work together to help you identify a less straightforward problem: your system's throughput.

[![](https://substackcdn.com/image/fetch/$s_!NJLj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7f18b86-f81f-4534-8d26-e62e79ee7278_562x414.png)](https://substackcdn.com/image/fetch/$s_!NJLj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7f18b86-f81f-4534-8d26-e62e79ee7278_562x414.png)

Throughput is the sustained rate your system needs to maintain: records per second, gigabytes per hour, or terabytes per day. For me, throughput is the one that helps you estimate the resource, not the data volume. Processing 1TB of data in 20 hours is different from processing it in 30 minutes.

You need higher throughput when:

[![](https://substackcdn.com/image/fetch/$s_!4ENI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e547d38-e8f5-4d1b-ab35-c7e8cbc03519_766x212.png)](https://substackcdn.com/image/fetch/$s_!4ENI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e547d38-e8f5-4d1b-ab35-c7e8cbc03519_766x212.png)

* You increase the data, but keep the time window the same

  [![](https://substackcdn.com/image/fetch/$s_!FRl0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91685d01-4772-4cf7-a17e-1542b02d7804_820x308.png)](https://substackcdn.com/image/fetch/$s_!FRl0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91685d01-4772-4cf7-a17e-1542b02d7804_820x308.png)
* You shorten the time window and keep the input data the same

Higher throughput usually means more RAM/CPUs per worker and a large number of workers. In return, you will have higher billing.

Lower throughput happens when:

[![](https://substackcdn.com/image/fetch/$s_!70Cn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57d1015b-e73d-4e52-994a-079396a816f7_1058x242.png)](https://substackcdn.com/image/fetch/$s_!70Cn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57d1015b-e73d-4e52-994a-079396a816f7_1058x242.png)

* You decrease the data but keep the time window the same.

  [![](https://substackcdn.com/image/fetch/$s_!x3aX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f569bc5-c47d-4419-979e-63cb552f9b4e_972x272.png)](https://substackcdn.com/image/fetch/$s_!x3aX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f569bc5-c47d-4419-979e-63cb552f9b4e_972x272.png)
* You lengthen the time window and keep the input data the same.

Lower throughput usually means fewer resources are needed, which in turn can save costs.

[![](https://substackcdn.com/image/fetch/$s_!Kdp5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb130f5de-026e-4942-9523-feb7baf15b42_1024x644.png)](https://substackcdn.com/image/fetch/$s_!Kdp5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb130f5de-026e-4942-9523-feb7baf15b42_1024x644.png)

In high-throughput use cases, we can consider DuckDB or Polars with high RAM/CPU/Disk, and move to Spark or SQL-based distributed processing systems such as Snowflake, BigQuery, Databricks, or Trino if the required resources no longer fit on a single node. The tuning of all resources should also center on throughput rather than solely on data volume.

## Stream

[![](https://substackcdn.com/image/fetch/$s_!nSEq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4ebc493-9b60-400e-bfdc-71cb3ae99ee0_1232x450.png)](https://substackcdn.com/image/fetch/$s_!nSEq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4ebc493-9b60-400e-bfdc-71cb3ae99ee0_1232x450.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=195410088)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

In stream processing, you can’t have the answer for the “How much data?“ due to the nature of unbounded data in stream processing. Also, the time window is not clear here. Thus, we have two different constraints:

* **Latency**: how fast does each record need to be processed? A fraud detection system might need a decision within 100 milliseconds. A near-real-time dashboard might tolerate a 30-second delay. It’s a constraint on each record’s journey through the system.

  [![](https://substackcdn.com/image/fetch/$s_!fyVh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0d5ff8d-d07a-4d22-8259-2f6edeedddde_602x198.png)](https://substackcdn.com/image/fetch/$s_!fyVh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0d5ff8d-d07a-4d22-8259-2f6edeedddde_602x198.png)
* **Throughput**: unlike batch processing, throughput is a more explicit metric here. The challenge is that because data is now a continuous flow, a system that handles 1,000 records per second on a quiet Tuesday might need to handle 50,000 on a Friday morning due to a marketing campaign. Once the system reaches its throughput limit, incoming records start buffering elsewhere (like entering a queue and waiting to order the food)

  [![](https://substackcdn.com/image/fetch/$s_!iuah!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27862bde-fc24-40b0-a37b-908173a4636f_794x596.png)](https://substackcdn.com/image/fetch/$s_!iuah!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27862bde-fc24-40b0-a37b-908173a4636f_794x596.png)

In streaming, both latency and throughput must be designed together. Lowering latency tends to increase throughput; if the system processes a record faster, it can handle more records simultaneously.

[![](https://substackcdn.com/image/fetch/$s_!QDGM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66776916-bc93-4747-b78b-aa26adad95e9_1244x322.png)](https://substackcdn.com/image/fetch/$s_!QDGM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66776916-bc93-4747-b78b-aa26adad95e9_1244x322.png)

Adding parallelism can boost both: more workers processing records in parallel lowers the per-record wait time while increasing the overall processing rate.

However, a concern here is that a processing system rarely processes a single record at a time, since each record incurs the costs of serialization, network transfer, disk I/O, and function calls, regardless of how small the record is. These overheads impact the system throughput.

[![](https://substackcdn.com/image/fetch/$s_!AI38!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e089b27-4f57-4fb5-beb1-038f90e58fe0_924x354.png)](https://substackcdn.com/image/fetch/$s_!AI38!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e089b27-4f57-4fb5-beb1-038f90e58fe0_924x354.png)

Batching records and processing them once is the pragmatic solution. Even stream processing frameworks like Flink take this approach. Instead of processing each record individually, the system accumulates records for a short window, say 100 milliseconds, and processes them together as a small batch.

The overhead is paid once for the entire batch rather than once per record. The throughput is increased. But the tradeoff is the latency. As every record now has to wait a bit before it gets processed.

Thus, the higher the throughput and the lower the latency, the more resources will be required. The batching delay could be offset by the faster processing time of that batch.

For high-throughput use cases, and latency doesn’t need to be too low, Spark Structured Streaming might be enough.

For a low-latency use case, regardless of throughput, Flink might be your choice, given that it was designed for this purpose.

---

# What are the business rules?

Business rules are the logic that transforms raw data into meaningful output. Filters, joins, aggregations, enrichments, derivations. A user is “active” if they’ve logged in within the last 30 days or revenue excludes refunded transactions.

Data modeling is important here as it facilitates communication between the data and business teams and guides how the organization transforms, organizes, and serves data.

Here’s what I’ve observed.

A team needs a new pipeline. There’s no data model upfront. So the engineer works with the stakeholders, has his own “active user” interpretation, implements the logic in this pipeline, and builds it. The end users are happy.

2 weeks later, another team builds another pipeline for a similar use case. Same source, different engineer, slightly different interpretation of “active user.” Now, two definitions are living in two pipelines.

6 months after that, nobody knows which one is right.

Data modeling can prevent this.

[![](https://substackcdn.com/image/fetch/$s_!dKDO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd021cdd8-0171-4b1b-88a6-dd0de9341c73_1840x958.png)](https://substackcdn.com/image/fetch/$s_!dKDO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd021cdd8-0171-4b1b-88a6-dd0de9341c73_1840x958.png)

A data model defines the concepts once and for all: what an “active user” means, what a “completed order” means, and what “revenue” includes and excludes. Every pipeline that follows is implementing this “spec”.

If you have a well-defined data model, you follow it and implement the business rules as the data processing logic. You have a clear guideline.

If you don’t, you’re doing data modeling within a pipeline; my suggestion is to work with end users to model what you need first for the data pipeline’s output. You can incrementally model other business processes later. After that, you will be clearer about what business rules to apply here.

---

# How do you ensure data quality at the processing layer?

To ensure data quality, we first define what high data quality looks like. From proper data modeling and input data profiling, we can identify “binary constraints,” such as: the column should not contain nulls, the values should be unique, the count should not exceed a threshold, a column should be a float, or the data should arrive at 7:00 AM.

The rule system can easily capture these, just as with dbt test, third-party libraries such as Great Expectations, or custom SQL test logic. Useful checks to build in:

[![](https://substackcdn.com/image/fetch/$s_!9i7P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ad38092-6848-4f92-b22b-ccd5e78c6109_954x848.png)](https://substackcdn.com/image/fetch/$s_!9i7P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ad38092-6848-4f92-b22b-ccd5e78c6109_954x848.png)

* Record counts in vs out.
* Null rates on fields that should be populated
* Duplicate checks on keys that should be unique
* Value distributions on critical fields: a sudden shift in the distribution of a metric is worth investigating
* Referential integrity: if you’re joining on a key, how many records fail to join? A high non-match rate often indicates a logic error or a source problem

However, there are some bad forms of the data we don’t know upfront. The null rate threshold of 5% doesn't catch a field that slowly drifts from 0.1% to 4.9% over three months. The simple row count check can’t detect the weird trend in the data.

That’s where anomaly detection comes in.

[![](https://substackcdn.com/image/fetch/$s_!VtAK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c0e25e9-11c4-4d32-8487-b4584fa43d4e_864x656.png)](https://substackcdn.com/image/fetch/$s_!VtAK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c0e25e9-11c4-4d32-8487-b4584fa43d4e_864x656.png)

Instead of checking against fixed rules, you analyze historical patterns using time-series techniques, for example, using the moving average, to detect the trend of the drop. Some advanced detection patterns might require machine learning models, and you might need to collaborate with the data science team to implement them.

## Where can the bad data be stored?

If you catch bad data, it must be discarded as soon as possible. However, in some cases, we still need to have a look over the low-quality data for debugging or health-checking the source.

[![](https://substackcdn.com/image/fetch/$s_!-qAp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb50d5b9-1752-45b7-aa18-dfdb9e72141a_1130x524.png)](https://substackcdn.com/image/fetch/$s_!-qAp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb50d5b9-1752-45b7-aa18-dfdb9e72141a_1130x524.png)

Bad data must be stored somewhere in an isolated manner to serve this purpose. A dedicated dataset for batch processing or a dead-letter queue for stream processing is worth consideration here.

---

# How do you ensure the processing logic is correct?

Transformation logic is simply code. And the code should be tested before being deployed to production.

We should catch logic or syntax errors before they ever run in production. This is different from data quality checks, which are runtime concerns that catch bad data and flag it as it occurs. Testing is what gives you confidence that the logic and syntax are “safe” to apply to real data.

Some approaches worth considering here:

* **Unit test** critical transformation functions in isolation

  [![](https://substackcdn.com/image/fetch/$s_!vMPR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8725cf8f-af6c-49e5-ace6-1ac84b763cd4_680x418.png)](https://substackcdn.com/image/fetch/$s_!vMPR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8725cf8f-af6c-49e5-ace6-1ac84b763cd4_680x418.png)

  + Build test datasets that can “mimic“ the production dataset.
  + Test business rule logic explicitly, if “active user” means logged in within 30 days, write a test that verifies a user who logged in 31 days ago is excluded
* **Integration test**: test the full transformation pipeline end-to-end with a representative sample of real data. Unit tests can only verify individual logic. Integration tests will help you test the whole “transformation chain”.

  [![](https://substackcdn.com/image/fetch/$s_!rkJg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8de19e22-37fb-4784-8074-2189b593b901_1266x570.png)](https://substackcdn.com/image/fetch/$s_!rkJg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8de19e22-37fb-4784-8074-2189b593b901_1266x570.png)
* **Regression testing**: when you change the transformation logic, you can try running that new version against a fixed historical dataset and compare the output against the previous version. Any unexpected difference is a warning. This is especially important during backfills; you want to confirm the new logic produces ***meaningfully different results*** where it should.

  [![](https://substackcdn.com/image/fetch/$s_!Q1YD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F270e949b-0f74-4f98-932d-63896ceda1c5_1036x556.png)](https://substackcdn.com/image/fetch/$s_!Q1YD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F270e949b-0f74-4f98-932d-63896ceda1c5_1036x556.png)

---

# What if the pipeline fails?

Failures are inevitable.

When the pipeline fails, you can’t let it just fail. There must be a mechanism to bring back your pipeline. In most cases, it is ideal if the pipeline can re-run automatically. The two main questions here:

* Does it recover automatically, or does it need manual intervention? For most production pipelines, automatic retry is the norm. The orchestration layer, Airflow or Dagster, Prefect can handle the retry automatically. At the lower layer, processing frameworks or tools such as Spark, Snowflake, or BigQuery also handle retries at the infrastructure level.
* When the pipeline recovers from failure, does it run from the beginning or resume from where it failed?

  [![](https://substackcdn.com/image/fetch/$s_!Tzgg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F778c287d-6b3e-4254-a113-e19b1503ca1a_1334x654.png)](https://substackcdn.com/image/fetch/$s_!Tzgg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F778c287d-6b3e-4254-a113-e19b1503ca1a_1334x654.png)

  + If your pipeline has a “checkpoint” mechanism (such as one in [Flink](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/checkpoints/) or [Spark](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/checkpoints/)) that helps the system determine whether the piece of data has been processed, then when recovering from failure, the system can resume only the unprocessed data.
  + For a process framework without built-in checkpointing, you can achieve the same thing by persisting the intermediate data in a separate store and sharing the steps’ data through it.

    [![](https://substackcdn.com/image/fetch/$s_!Rh6J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74ccc154-7ded-4805-8909-0a570d4c5109_1238x558.png)](https://substackcdn.com/image/fetch/$s_!Rh6J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74ccc154-7ded-4805-8909-0a570d4c5109_1238x558.png)

    - For example, your pipeline has three steps. Instead of transferring data directly between tasks, we write the results of each step to object storage, and the next step retrieves them to continue the process. If step 3 fails, the pipeline can rerun from step 3 and pick up the result from step 2 in object storage.

---

# Can the processing logic be backfilled?

Backfilling in data engineering is the process of **loading or recomputing historical data** that was missed, incorrect, or not previously processed. You typically backfill when:

[![](https://substackcdn.com/image/fetch/$s_!K4t9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ba369e-8b76-42f2-a77a-dc367416c50e_896x300.png)](https://substackcdn.com/image/fetch/$s_!K4t9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ba369e-8b76-42f2-a77a-dc367416c50e_896x300.png)

* Business logic changes, so your processed data must be re-applied to the new logic to reflect the changes.
* Some failures cause incomplete data.

Most orchestration frameworks make this straightforward. You specify the date range, and tools like Airflow or Dagster handle the rest. The problems are:

* Does the source retain data long enough?
* Can the pipeline allow partial backfilling, e.g., a small range of the data or a non-contiguous range of data?

  [![](https://substackcdn.com/image/fetch/$s_!0gqk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0949becc-e8aa-4726-9fbf-5a74465eeb4c_660x644.png)](https://substackcdn.com/image/fetch/$s_!0gqk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0949becc-e8aa-4726-9fbf-5a74465eeb4c_660x644.png)

  + To do this, the processing logic must be applied in “partitions”: daily, hourly, or weekly partitions. The core idea is that each partition can be handled in isolation: fixing March 5th means rerunning only March 5th. If you treat the dataset as a whole, every rerun must happen as a whole because there is no safe way to rerun partially.
* Does the backfill run eat all the resources? A 90-day backfill means up to 90 Airflow DAG runs queued at once. Each run might need 25% of your total processing resource. If you let 4 runs happen, you will run out of resources for other use cases.

  [![](https://substackcdn.com/image/fetch/$s_!P7jY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd98e3bf6-d5e0-4bd9-bf95-832735cd869d_1242x520.png)](https://substackcdn.com/image/fetch/$s_!P7jY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd98e3bf6-d5e0-4bd9-bf95-832735cd869d_1242x520.png)

  + There are two levels to control this: first, you can set the maximum number of runs at the orchestration tool, like Airflow. Second, you can cap the resource used for backfill at the processing layer by assigning the backfill data to a dedicated resource pool.

The backfill problem list does not stop there. There is one left, and I think it needs a whole section.

---

# What is the side effect of reruns?

Backfilling is just one reason a pipeline gets rerun. Automatic retries after failure or manual debugging sessions also cause reruns.

And every rerun carries the same risk: if the pipeline isn't carefully designed, rerunning it might produce corrupt data.

—

Idempotency means that performing the same operation multiple times produces the same result as performing it once. It ensures your data is in good shape.

[![](https://substackcdn.com/image/fetch/$s_!ZoGy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7972043b-3096-4218-a4ed-8369b2aa2b68_1084x936.png)](https://substackcdn.com/image/fetch/$s_!ZoGy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7972043b-3096-4218-a4ed-8369b2aa2b68_1084x936.png)

If you re-run the processing logic, idempotency ensures it doesn’t cause duplicate data or any bad form. Having idempotency usually means having reproducibility; this is important, given that we need the bugs to happen exactly as in production when we re-run the processing logic for debugging.

For me, to ensure idempotency, we must proactively make the processing itself idempotent. Some principles are:

* **Overwrite, don’t append.** Overwrite to a table or partition completely on each run.

  [![](https://substackcdn.com/image/fetch/$s_!Nj8J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca27a005-80d9-4312-b186-ce889402ba85_712x488.png)](https://substackcdn.com/image/fetch/$s_!Nj8J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca27a005-80d9-4312-b186-ce889402ba85_712x488.png)
* **Use MERGE/upsert semantics.** Match on a unique key and replace. Duplicate runs converge on the same final state.

  [![](https://substackcdn.com/image/fetch/$s_!hN0v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e4f8068-86ca-4add-819c-0e0ea9e6f43a_598x408.png)](https://substackcdn.com/image/fetch/$s_!hN0v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e4f8068-86ca-4add-819c-0e0ea9e6f43a_598x408.png)
* **Avoid non-deterministic functions.** `NOW()`, `CURRENT_TIMESTAMP`, `RAND()` — any function that returns a different value on each run breaks idempotency.

One more important note: idempotency must be end-to-end; otherwise, it’s not effective. If your first two steps overwrite their output correctly but the final step naively appends, the whole processing layer isn’t idempotent.

---

# How are credentials and configurations managed?

Your processing layer will need credentials to communicate with external systems somehow. Reading from the source, writing to the sink, or submitting the processing job somewhere. It also needs configuration: environment-specific settings or processing parameters.

[![](https://substackcdn.com/image/fetch/$s_!2Vr_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9801027-c0cd-4061-a4c1-2bd5c40af6cf_992x584.png)](https://substackcdn.com/image/fetch/$s_!2Vr_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9801027-c0cd-4061-a4c1-2bd5c40af6cf_992x584.png)

Most orchestration frameworks expose an interface for managing these credentials and configurations. If you don’t rely on orchestration tools, all clouds have services to manage the secrets and configuration.

The point is: don’t hardcode them, store them securely (e.g., by encoding the credentials), and retrieve them when your processing layer needs them. This helps you secure your sensitive credentials and make the configurations pluggable.

Managing credentials and configurations efficiently also lets you run the pipeline across different environments (e.g., dev, prod) seamlessly, since you only need to update the input credentials and configurations for each environment.

One note: configuration that affects business logic, such as thresholds, date ranges, or processing parameters, should be versioned alongside the pipeline code. If you change the “active user” lookback window from 30 days to 60 days, that change should be traceable, reviewable, and reversible.

---

# How do you observe the processing?

When the process layer is run, it cannot run in the dark. We must observe it to ensure things are right. Before observing anything, it helps to understand the four observability primitives and what each one does.

* **Logging** tells what happened. The informativeness of the logs depends largely on how the instance outputs them.

  [![](https://substackcdn.com/image/fetch/$s_!peSH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83043963-afd5-4d16-8a6f-5902b871beec_1078x570.png)](https://substackcdn.com/image/fetch/$s_!peSH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83043963-afd5-4d16-8a6f-5902b871beec_1078x570.png)
* **Monitoring** continuously observes the system against expectations, so deviations are caught before they become incidents.

  [![](https://substackcdn.com/image/fetch/$s_!59YO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2939afc-8b43-4764-b260-c84dc53427a1_752x416.png)](https://substackcdn.com/image/fetch/$s_!59YO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2939afc-8b43-4764-b260-c84dc53427a1_752x416.png)
* **Alerting** helps deliver signals to the right one. Define who gets notified, through which channel, and with what urgency.

  [![](https://substackcdn.com/image/fetch/$s_!pvCa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63249bc7-289b-400d-8cd6-b04e1df39f38_748x394.png)](https://substackcdn.com/image/fetch/$s_!pvCa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63249bc7-289b-400d-8cd6-b04e1df39f38_748x394.png)
* **Tracing** connects cause to effect across steps. Without it, you know something went wrong, but you have a harder time finding the root cause.

  [![](https://substackcdn.com/image/fetch/$s_!9fZM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd859de8-c9df-4527-b75d-830d78b0aace_926x500.png)](https://substackcdn.com/image/fetch/$s_!9fZM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd859de8-c9df-4527-b75d-830d78b0aace_926x500.png)

Bringing observability to the processing layer, things will look like this (not comprehensive):

* **Monitoring**: record counts in vs out at each step, null rates on critical fields, duplicate rates, quarantined record counts, reconciliation against source counts. This is the runtime enforcement of what the data quality section. The validation result should be exposed and centralized, rather than split between the orchestration layer and the CI/CD pipeline.

  + You also need to monitor the underlying infrastructure: CPU and memory utilization, disk I/O, network throughput, consumer lag for streaming, task execution duration trends, or cost per run.
* **Logging**: task startup/shutdown events or error messages.
* **Alerting**: As the monitoring results are centralized, we can now set an alert on them, but with a clear distinction of severity and tie it to the downstream impact. A non-critical job fail is a Slack message. A primary key with 20% nulls in the production revenue table is a company-wide alert. The closer the affected data is to a business decision, the higher the urgency.

  [![](https://substackcdn.com/image/fetch/$s_!W4u7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F313ea070-a82d-4c20-ad77-4677b8a7a4e0_1164x594.png)](https://substackcdn.com/image/fetch/$s_!W4u7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F313ea070-a82d-4c20-ad77-4677b8a7a4e0_1164x594.png)
* **Tracing:** Where did this field come from? Which transformation touched it? Which downstream tables depend on it? This is where data lineage shines. The lineage makes it possible to answer “why is this number wrong” by following the data backward through the pipeline, and to answer “what breaks if I change this” by following it forward through the lineage.

---

# Outro

In this article, I discussed my nine concerns about designing an efficient data processing layer:

* Batch or stream processing?
* What are the business rules?
* How do you ensure data quality at the processing layer?
* How do you ensure the processing is correct?
* What if the pipeline fails?
* Can the pipeline be backfilled?
* What is the side effect of reruns?
* How are credentials and configurations managed?
* How do you observe the processing?

In each section, I discuss why it matters and approaches to deal with it.

Hope my work brings you value.

Thank you for reading this far. See you in my next article.
