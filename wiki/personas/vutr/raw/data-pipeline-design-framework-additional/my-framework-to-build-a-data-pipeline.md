---
title: "A framework I use to build a data pipeline."
channel: vutr
author: "Vu Trinh"
published: 2025-12-02
url: https://vutr.substack.com/p/my-framework-to-build-a-data-pipeline
paid: true
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Orchestration", "Streaming", "Batch Processing", "Change Data Capture", "Data Quality"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# A framework I use to build a data pipeline.

*You cannot simply say, "I'll use Spark, Kafka, and so on"; you need to ask clarifying questions to gather information for proposing a robust data pipeline.*

> Source: [Open post](https://vutr.substack.com/p/my-framework-to-build-a-data-pipeline)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]]

---

> *The 50% discount on the yearly package ends in **ONE** day. Don’t miss it.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)
>
> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*

[![](https://substackcdn.com/image/fetch/$s_!y2lg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ed7c9b2-ec5d-49f8-9483-c8d9d3042c7a_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!y2lg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ed7c9b2-ec5d-49f8-9483-c8d9d3042c7a_2000x1428.png)

---

# Intro

In last week’s article, I showed you how to destroy your data pipeline in the most miserable way possible. That was fun to write. I also said that building a robust data pipeline is not easy; there are many things to get clear before starting the process.

However, in an interview or in your daily job, when we were asked to build a data pipeline, we couldn’t say, “It’s hard”; we had to propose a pipeline that actually worked. So I wonder: is there a framework (a set of questions) we could use to gather more information, thereby making the pipeline design and development process more manageable?

In this article, I will list my go-to questions when building a data pipeline. Each question will include the information you are expected to receive.

---

# Before we move on

The ultimate goal of any data pipeline is to move data from location A to location B. During the move, some transformations are applied to make the data at location B applicable to the business.

[![](https://substackcdn.com/image/fetch/$s_!D8lN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e7c59d5-36cf-4331-bee5-7a13fad90c01_838x238.png)](https://substackcdn.com/image/fetch/$s_!D8lN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e7c59d5-36cf-4331-bee5-7a13fad90c01_838x238.png)

So, in this article, I'll categorize the questions into three sections: source, sink, and middle steps. Thinking this way helps me separate each component's concerns so I can plan better for the pipeline.

These questions are based solely on my current experience and knowledge, so they might not cover all the aspects. If you feel I’m missing something, feel free to comment.

---

# Sink

> *When building a pipeline, we should begin from the sink. More accurately, we should start from the end users.*

### Does this data pipeline serve any business purpose?

[![](https://substackcdn.com/image/fetch/$s_!BXfq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b361603-de3d-45cc-8c52-857d7d3546a5_998x472.png)](https://substackcdn.com/image/fetch/$s_!BXfq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b361603-de3d-45cc-8c52-857d7d3546a5_998x472.png)

If it doesn’t serve any purpose, our pipeline is redundant? In the real world, there is a high chance you will have a pipeline that's forgotten a week later because it doesn’t support any business process. Asking this question can help you save time by skipping a useless data pipeline.

### Does your company have a data model?

This is a critical question as the data model defines many things, from how your output will be constructed to how data quality rules will be applied.

[![](https://substackcdn.com/image/fetch/$s_!WO8F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb057aa25-84ce-4aa6-a8ad-20337bad3e68_550x332.png)](https://substackcdn.com/image/fetch/$s_!WO8F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb057aa25-84ce-4aa6-a8ad-20337bad3e68_550x332.png)

If yes, excellent, follow the data model. If the pipeline loads data to some dims/facts or calculates a metric derived from them, things are simple. However, if you have to deal with a new business flow, you need to work with a business user to model it.

If not, you have to think about data modeling first, not the entire company data model, but at least modeling entities that are related to your building pipeline, and expand it incrementally later. That ensures you still deliver the data pipeline while leaving the door open for data modeling, one of the most critical factors in a company’s data foundation.

### What is the shape of the output?

[![](https://substackcdn.com/image/fetch/$s_!ryC5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa50d9678-71ef-46e2-afe1-7a2e3b5188b4_572x368.png)](https://substackcdn.com/image/fetch/$s_!ryC5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa50d9678-71ef-46e2-afe1-7a2e3b5188b4_572x368.png)

After clarifying the modeling, it will be easier to define the expected output fields. If needed, this question should be answered with the help of business users to clarify which data fields will be included in the output.

### How will the output be served?

[![](https://substackcdn.com/image/fetch/$s_!7VPM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5ece03-cadc-4563-9787-a1c5a421f610_724x552.png)](https://substackcdn.com/image/fetch/$s_!7VPM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda5ece03-cadc-4563-9787-a1c5a421f610_724x552.png)

A table, a dashboard, a CSV file, exposing via API, exposing via web-app, or an ML training dataset. This will help you prepare better the infrastructure to deliver the output efficiently: Do I need to develop a set of APIs? Where do I store CSV files? How do I expose the tables?

### How old can the data be before it is considered stale?

> *The 50% discount on the yearly package ends in **ONE** day. I invite you to upgrade your subscription to access my high-quality, human-written data engineering articles.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!PHPH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3535b997-a392-44ac-af02-255e5d1e9981_500x440.png)](https://substackcdn.com/image/fetch/$s_!PHPH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3535b997-a392-44ac-af02-255e5d1e9981_500x440.png)

This helps you with two things:

* Determine the frequency of reaching the source? More on this when we discuss sources.
* Choose the infrastructure that could help deliver the desired freshness. If they need low latency, you need to choose the serving option that allows you to read data from memory for recent data. It could be a dedicated database, such as [Pinot](https://github.com/apache/pinot) or [Druid](https://druid.apache.org/), or a sub-option from your database; for example, [BigQuery offers BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro) for this purpose.

### What is the usage pattern of the output?

[![](https://substackcdn.com/image/fetch/$s_!ujCu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a78a2d-3d39-48a5-a66c-342abaed6671_764x408.png)](https://substackcdn.com/image/fetch/$s_!ujCu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54a78a2d-3d39-48a5-a66c-342abaed6671_764x408.png)

This helps us to apply optimization techniques to the output tables.

If users usually query data by date. Partitioning by date is a great choice.

Suppose users join the data by category, user\_id. Clustering by category, user\_id will help a lot.

Please keep in mind that although these techniques will improve query performance, write operations will be impacted, as data needs to be organized when writing; writing data naively is always faster than writing it in a predefined layout.

### What is the data retention?

Data is a product. A product with an expired date.

[![](https://substackcdn.com/image/fetch/$s_!GflP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37ae9a3c-1ee6-41a1-b4ff-fca87e7aa059_464x362.png)](https://substackcdn.com/image/fetch/$s_!GflP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37ae9a3c-1ee6-41a1-b4ff-fca87e7aa059_464x362.png)

Your business might need data from the last day or last week, but data from 2 years ago won’t contribute much. Knowing your data retention helps you set up data lifecycle management (e.g., moving it to an archived storage tier after 2 weeks or deleting it after 1 year).

### Can the sink support atomicity?

Atomicity means an operation is done all or nothing—it either completes fully or has no effect at all. This will help your data pipeline retry seamlessly if it fails. You will know for sure that when the pipeline fails, no partial data will be persisted in the sink.

[![](https://substackcdn.com/image/fetch/$s_!gIgJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa3d9ca8-5af0-429b-acfb-9f2db478f249_928x428.png)](https://substackcdn.com/image/fetch/$s_!gIgJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa3d9ca8-5af0-429b-acfb-9f2db478f249_928x428.png)

For most OLAP databases, such as BigQuery, Databricks, or Snowflake, we don’t need to worry about this, as they are ACID-compliant by design.

A case when the sink with no support for atomicity could cause corrupted data: your data scientist needs CSV files in object storage, loading data from local to object storage is atomic (support for one object only), however, downloading files to the local filesystem is not atomic, it can be interrupted halfway, leaving a partial file on disk. Corrupted data can be exposed in object storage because the upload task doesn’t know whether the data is complete.

### What kind of firewalls does the sink have?

This helps you prepare the required credentials to access the sink. It could be service accounts, API keys, database passwords…

[![](https://substackcdn.com/image/fetch/$s_!3eTe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe69cf77b-bbcd-4c1b-90e2-15d5da610f04_392x248.png)](https://substackcdn.com/image/fetch/$s_!3eTe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe69cf77b-bbcd-4c1b-90e2-15d5da610f04_392x248.png)

In addition, some sinks are deployed in a private network or a strict environment that requires approval from other teams. Getting this information to help you plan better to access the sink. (Some paperwork might take weeks.)

---

# Source

### What type of source is this?

API, Database, or someone pushes data into our side.

[![](https://substackcdn.com/image/fetch/$s_!aF6O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb14db45f-f560-4588-9840-d0164887e05b_498x310.png)](https://substackcdn.com/image/fetch/$s_!aF6O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb14db45f-f560-4588-9840-d0164887e05b_498x310.png)

This will help you prepare the infrastructure to retrieve data from the source. If it were a database, you could think of periodic file exports or CDC. If it is an API, how do we call it? If it is a stream, how do we consume it?

### How often do I need to touch the source?

[![](https://substackcdn.com/image/fetch/$s_!06Wp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd879dc4-5a63-4776-aba9-59ae7a5e5098_966x576.png)](https://substackcdn.com/image/fetch/$s_!06Wp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd879dc4-5a63-4776-aba9-59ae7a5e5098_966x576.png)

This question is strictly related to the question “How old can the data be before it is considered stale?” from the sink section. If the user needs daily or weekly data, you can use a cron job to schedule source visits. If the user needs low-latency data, your data must flow continuously from the source to capture it nearly as it happens. You even need to set up more infrastructure, such as a CDC pipeline, to make the data stream available.

### How will the source performance be impacted?

[![](https://substackcdn.com/image/fetch/$s_!ZKGd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0492230e-d8a0-426a-8ce2-f076539a7d37_636x354.png)](https://substackcdn.com/image/fetch/$s_!ZKGd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0492230e-d8a0-426a-8ce2-f076539a7d37_636x354.png)

This will help you retrieve data more reliably, both for your pipeline and for the source. For example, if it is a database, does data export affect its read/write performance? Do we need to work with the backend team to deploy the read replica? If it is an API, what is it rate-limiting?

### How long does the source retain the data?

[![](https://substackcdn.com/image/fetch/$s_!68YX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e559162-cf30-406f-85fb-7594cc2915f7_798x392.png)](https://substackcdn.com/image/fetch/$s_!68YX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e559162-cf30-406f-85fb-7594cc2915f7_798x392.png)

If you need 1 week of data but the source only keeps the last 2 days, there is no way to build a pipeline with this source. You'll need to negotiate with the pipeline's end users for the required data range, or look for another source.

This question also helps you with the backfill purpose. More on this in the “Middle Steps” section.

### Does the source have enough fields that we need? (The schema)

[![](https://substackcdn.com/image/fetch/$s_!HLau!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0e23043-b29c-4055-8639-40903f93871b_1080x380.png)](https://substackcdn.com/image/fetch/$s_!HLau!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0e23043-b29c-4055-8639-40903f93871b_1080x380.png)

From the sink section, you must already know what your output will look like. Make sure you browse and understand the source schema to see whether it provides enough material to build the outputs.

### If the schema changes, how will I know?

[![](https://substackcdn.com/image/fetch/$s_!t8VM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf2f69d3-b3f9-422e-ae2c-e20c21076008_1286x540.png)](https://substackcdn.com/image/fetch/$s_!t8VM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf2f69d3-b3f9-422e-ae2c-e20c21076008_1286x540.png)

However, knowing about the schema is a part of the story. The schema can be changed: columns can be renamed, dropped, or added. When running, your pipeline assumes the source still has the predefined schema; any schema changes will surely break it. There must be a preparation for this scenario.

How often will the schema change? If it changed, how do I get notified?

### What kind of firewalls does the source have?

[![](https://substackcdn.com/image/fetch/$s_!0vIO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d7de7b-a2a6-42a5-807a-4dbcb003419d_482x322.png)](https://substackcdn.com/image/fetch/$s_!0vIO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d7de7b-a2a6-42a5-807a-4dbcb003419d_482x322.png)

This question has the same purpose as the question in the sink section.

---

# Middle Steps

### What is the volume of the processed data?

[![](https://substackcdn.com/image/fetch/$s_!X1jX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62d77ad5-0b98-42bf-af9a-65af3927b8a0_774x482.png)](https://substackcdn.com/image/fetch/$s_!X1jX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62d77ad5-0b98-42bf-af9a-65af3927b8a0_774x482.png)

This will provide you with information to plan for processing resources. How many RAMs/CPUs do we need? Are more workers required to read the stream? Can the processing happen on a single node?

### What are the business rules?

Again, data modeling is important here. If you have a well-defined data model, you follow it and implement the business rules as the data processing logic.

If not, as I mentioned in the sink section, you need to model what you need first for the data pipeline's output. You can incrementally model other business processes later. After that, you will be clearer about what business rules to apply here.

[![](https://substackcdn.com/image/fetch/$s_!JJ1k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5bcafbe-c34f-4b10-9271-eae46f302ca7_1214x556.png)](https://substackcdn.com/image/fetch/$s_!JJ1k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5bcafbe-c34f-4b10-9271-eae46f302ca7_1214x556.png)

Another solution is to work with end users to clarify the business rules for this pipeline only. You can process faster. In return, you skip data modeling, which could leave your team with more tech debt later, as data modeling is one of the most critical factors in a company’s data foundation.

Business rules also play a crucial role in ensuring data quality. You will have a clearer view of what to check, for example, a user can’t log in twice with the same email, so the dataset can’t contain duplicate emails, or the user must fill in their name when signing up, so the name field can’t be null.

### Where can the bad data be stored?

[![](https://substackcdn.com/image/fetch/$s_!HKz_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3486892-6c63-4c44-8741-8013e2fbe108_1002x418.png)](https://substackcdn.com/image/fetch/$s_!HKz_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3486892-6c63-4c44-8741-8013e2fbe108_1002x418.png)

Bad data is not needed and must be discarded as soon as possible.

However, in some cases, we still need to have a look over the low-quality data for debugging or health-checking the source.

Bad data must be stored somewhere in an isolated manner to serve this purpose. A dedicated dataset for batch processing or a dead-letter queue for stream processing is worth consideration here.

### What if the pipeline fails?

When the pipeline fails, you can’t let it just fail. There must be a mechanism to bring back your pipeline. In most cases, it is ideal if the pipeline can re-run automatically.

[![](https://substackcdn.com/image/fetch/$s_!vRM7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7678582-fa20-4a70-b799-887b93c07ae8_1058x412.png)](https://substackcdn.com/image/fetch/$s_!vRM7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7678582-fa20-4a70-b799-887b93c07ae8_1058x412.png)

When the pipeline recovers from failure, does it run from the beginning or resume from where it failed? If your pipeline has a “checkpoint” mechanism (such as one in [Flink](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/checkpoints/) or [Spark](https://nightlies.apache.org/flink/flink-docs-master/docs/ops/state/checkpoints/)) that helps the system determine whether the piece of data has been processed, then when recovering from failure, the system can resume only the unprocessed data.

If you don’t rely on a process framework that supports checkpointing, you can achieve the same thing by persisting the intermediate data in a separate store and sharing the steps’ data through it.

For example, your pipeline has three steps. Instead of transferring data directly between tasks, we write the results of each step to object storage, and the next step picks up the data from there to continue the process. If step 3 fails, the pipeline can simply re-run from step 3, pick up the result from step 2 in object storage.

### Can the pipeline be backfilled?

Backfilling in data engineering is the process of **loading or recomputing historical data** that was missed, incorrect, or not previously processed. You typically backfill when:

[![](https://substackcdn.com/image/fetch/$s_!DZrA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ee04f45-1302-4cf0-a373-e3b6b89bdeb8_1310x380.png)](https://substackcdn.com/image/fetch/$s_!DZrA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ee04f45-1302-4cf0-a373-e3b6b89bdeb8_1310x380.png)

* Business logic changes, so your processed data must be re-applied to the new logic to reflect the changes.
* Some failures cause incomplete data.

This question is mainly related to the source, as most pipeline orchestration frameworks, such as Airflow and Dagster, allow running the pipeline in any specific date range. In addition, these platforms let you specify dependencies between steps, so backfilling tasks that require running all related steps would not be a problem. You rarely backfill only the tasks that pull data from the source; downstream tables also need to be backfilled.

The remaining problem is whether the source still keeps the data we need in the backfill range. The question above, “How long does the source retain the data?”, will provide the information you need here.

### What is the side effect of the reruns?

Idempotency means that performing the same operation multiple times produces the same result as performing it once. Idempotency makes sure your data is in a good state. For example, if the pipeline restarts a step, idempotency ensures it doesn’t cause duplicate data. For debugging, you often rerun jobs on the same data: a non-idempotent job will produce different output, making the process non-repeatable.

[![](https://substackcdn.com/image/fetch/$s_!aSSd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bcfae63-d886-4a67-a075-1577df87c5c3_834x630.png)](https://substackcdn.com/image/fetch/$s_!aSSd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bcfae63-d886-4a67-a075-1577df87c5c3_834x630.png)

For me, to ensure idempotency, we must proactively make the pipeline itself idempotent, so that **re-running any step produces the same final result,** without duplicates, corruption, or inconsistent states. For example, overwriting the table or partitions, preventing the use of non-deterministic functions such as now().

One more note about idempotency: if you want your pipeline to be fully idempotent, all its steps must be idempotent. It’s pointless to have your first two steps delete the whole partition and re-insert its data, then have your final step still only naively insert data into the final table.

### How are credentials and related configuration managed?

Based on the above sections, we must have the credentials and related configurations required to access the source and sink. Most pipeline orchestration frameworks expose an interface for managing these credentials and configurations. Just make sure you don’t hardcode them.

[![](https://substackcdn.com/image/fetch/$s_!ZChE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bc02a2f-de1b-4133-8703-c16b2bb700af_1164x556.png)](https://substackcdn.com/image/fetch/$s_!ZChE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bc02a2f-de1b-4133-8703-c16b2bb700af_1164x556.png)

Managing credentials and configurations efficiently also lets you run the pipeline across different environments (e.g., dev, prod) seamlessly, since you only need to update the input credentials and configurations for each environment.

---

# Outro

In this article, I list out all the questions I’m gonna ask to build a reliable and business-oriented data pipeline. As I mentioned earlier, this list reflects my limited experience in building data pipelines. I welcome your feedback and suggestions for expanding the list. I’m happy to learn from you guys.

Thank you for reading this far. See you in the following articles.
