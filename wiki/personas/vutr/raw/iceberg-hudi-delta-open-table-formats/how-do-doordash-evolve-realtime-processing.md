---
title: "How does Doordash evolve realtime processing platform with Iceberg"
channel: vutr
author: "Vu Trinh"
published: 2025-05-22
url: https://vutr.substack.com/p/how-do-doordash-evolve-realtime-processing
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Delta Lake", "BigQuery", "Data Warehouse", "Orchestration", "Streaming"]
tags: [https, auto, iceberg, doordash, snowflake, good]
---

# How does Doordash evolve realtime processing platform with Iceberg

*Apache Flink + Apache Iceberg*

> Source: [Open post](https://vutr.substack.com/p/how-do-doordash-evolve-realtime-processing)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=163813438)

---

[![](https://substackcdn.com/image/fetch/$s_!EkON!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd89a8d66-ea08-4682-bab0-d8d80764b2d1_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!EkON!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd89a8d66-ea08-4682-bab0-d8d80764b2d1_2000x1429.png)

---

## Intro

In the [previous article](https://open.substack.com/pub/vutr/p/doordashs-real-time-processing-system?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false), we examined how [DoorDash](https://www.doordash.com/), one of the largest food delivery platforms in the United States, utilizes Apache Kafka, Apache Flink, and Snowflake for their real-time processing platform. They used Flink to consume Kafka messages and write them to S3, which is later loaded into Snowflake to serve data users.

Recently, DoorDash has shared how they improved this architecture with the introduction of Iceberg. Let’s dive into DoorDash’s motivation, challenges, and benefits of this decision.

All credit for the technical details goes to the DoorDash Engineering Team. This article serves as my note after consuming their [technical sharing resource](https://www.youtube.com/watch?v=_nnNHC90nMI&t=541s).

---

## Background

DoorDash developed an internal streaming platform to process real-time events from applications, enabling efficient support for business decisions.

At peak, the platform might receive a very high throughput workload with more than 30 million messages per second, which is approximately 5 GB of event data flowing into their system per second. These events originate from customers, dashers, merchants, or DoorDash's internal applications.

[![](https://substackcdn.com/image/fetch/$s_!FoxS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86f5c8a7-5d3d-4ddd-85ee-6980d7773f89_1188x402.png)](https://substackcdn.com/image/fetch/$s_!FoxS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86f5c8a7-5d3d-4ddd-85ee-6980d7773f89_1188x402.png)

The stream platform will consume these events, process them, and write them to the associated tables in the data warehouse. Some use cases require the data to be available in near real-time.

So, how did DoorDash ensure their platform is low-latency and highly scalable?

As we recall from the [previous article](https://open.substack.com/pub/vutr/p/doordashs-real-time-processing-system?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false), DoorDash buffered incoming data with Kafka and used Flink to process and write the data to the sink.

[![](https://substackcdn.com/image/fetch/$s_!OJrC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0e8d270-eace-4beb-bbe8-693adb68119e_1588x698.png)](https://substackcdn.com/image/fetch/$s_!OJrC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0e8d270-eace-4beb-bbe8-693adb68119e_1588x698.png)

[Apache Flink](https://flink.apache.org/) is a framework and distributed processing engine for stateful computations over unbounded and bounded data streams, unlike Spark, which treats bounded data as a first-class citizen and aligns stream data into micro-batches. For Flink, everything is a stream; the batch is just a special case.

> *If you want to learn more about Flink, check out [my article](https://open.substack.com/pub/vutr/p/apache-flink-overview?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false) to understand its architecture and how it can achieve fault-tolerance and provide stateful processing capability.*

[![](https://substackcdn.com/image/fetch/$s_!WfEi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ba731f8-bbfe-4efc-9d0b-27e3847cf83f_514x278.png)](https://substackcdn.com/image/fetch/$s_!WfEi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ba731f8-bbfe-4efc-9d0b-27e3847cf83f_514x278.png)

The Flink application will consume the data from Kafka and upload it to S3 in the Parquet format. Then, DoorDash used [Snowpie](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) to copy data from S3 to Snowflake. Based on the [notifications from the Amazon SQS](https://docs.snowaflake.com/en/user-guide/data-load-snowpipe-auto-s3), Snowpie will load data from S3 to Snowflake as soon as it is available using the [COPY statement](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table).

---

## Challenges

The Flink → S3 → Snowpie → Snowflake has some challenges:

* Snowflake's cost increases when more users use the data platform. When designing this solution in the first place, DoorDash only planned for hundreds of thousands of messages at peak, which is far smaller than the current peak workload (30 million messages)
* The solution wrote the data twice, the first time is Flink writing data to S3, and the second time is Snowflake writing data to Snowflake

  [![](https://substackcdn.com/image/fetch/$s_!g-oC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c73f114-0240-47cd-aaca-77bb27f8f360_366x292.png)](https://substackcdn.com/image/fetch/$s_!g-oC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c73f114-0240-47cd-aaca-77bb27f8f360_366x292.png)
* It’s vendor lock-in (Snowflake)

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=163813438)

---

## Solutions

They chose Iceberg for the new real-time data sink. DoorDash also experimented with Delta Lake, but the table format didn’t meet their expectations in terms of operational and cost aspects.

[![](https://substackcdn.com/image/fetch/$s_!DRhq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc457464c-692a-4b07-9062-c950e5e52fb5_272x264.png)](https://substackcdn.com/image/fetch/$s_!DRhq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc457464c-692a-4b07-9062-c950e5e52fb5_272x264.png)

From their perspective, Iceberg can help because:

* The open table format has more mature support for Flink. In contrast, Delta Lake is more Spark-centric.
* It offers flexible schema and partition evolution.
* Iceberg has a very active community
* It supports concurrent table writes. From what I know, this feature is not exclusive to Iceberg, as all table format supports concurrent writes with [optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control).

---

## Architecture

With the introduction of Iceberg, the DoorDash real-time processing platform remains the same, except for the S3 → Snowpie → Snowflake pipeline. Now, the Flink continues to sink data to S3 in Parquet format, but this time these files are “wrapped” with the Iceberg metadata layer.

[![](https://substackcdn.com/image/fetch/$s_!X4aH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d1c62a6-1cdb-4123-8028-1cf77f12872c_1360x600.png)](https://substackcdn.com/image/fetch/$s_!X4aH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d1c62a6-1cdb-4123-8028-1cf77f12872c_1360x600.png)

The pipeline that writes data to Snowflake is not necessary anymore, as Snowflake users can query Iceberg data directly on S3. This enables data consumers to continue using Snowflake to interact with the data without major changes or interruptions. In addition, DoorDash also spins up Trino clusters to query this data with the help of the AWS Glue catalog.

To implement the new solutions, Doordash needs to adjust the Flink jobs.

A typical Flink application comprises three parts: the source, the transformation, and the sink. For the new approach, DoorDash only needs to change the application’s sink to the new one that writes data to S3 in Iceberg format.

Flink provides support for an out-of-the-box Iceberg sink connector, so DoorDash only needs to make minor code changes to make things work.

---

## Challenges when adopting Iceberg

### Schema Evolution

Although the Iceberg specification supports schema evolution, the Flink-Iceberg connector does not support it and requires the table schema to be static. If the schema changes, they have to stop the Flink job, adjust the logic, and restart it.

However, with all the benefits that Iceberg could bring (more on this later), DoorDash considers this not a very big deal.

### Query Performance

Some users reported that their queries were very slow compared to the original solution. In these use cases, users typically query very large nested fields with hundreds of key-value pairs. This was handled well in Snowflake with the Variant Snowflake type.

DoorDash flattens these fields in Iceberg and allocates more resources for the query workload.

---

## Benefit

> So, is it worth it?

### Cost saving

With Iceberg, Doordash observed a 25-49% reduction in storage costs compared to native Snowflake storage, using only the default compression scheme (zstd).

The cost savings also come from the elimination of duplicate data writing from the original solution, which writes data first to S3 and later loads it to Snowflake's native storage.

The resources used for Snowpie are now allocated for the Iceberg operation process, such as table compaction.

### The reliability and availability

The support for concurrent writes enables DoorDash to develop multiple pipelines for a single Iceberg table. This allows them to write data from different sources or have different workloads, such as a standard data sink pipeline along with the backfill pipeline at the same time.

DoorDash also enjoys the native support of Iceberg’s time travel. Although Snowflake also supports this feature, [users must pay more to achieve higher data retention](https://docs.snowflake.com/en/user-guide/data-time-travel#data-retention-period). With Iceberg, DoorDash can achieve time travel capabilities with more control over data retention.

The Iceberg adoption aligns with their data-lake approach, which limits the dependency on any vendor, thus providing them more flexibility. For example, they can now use other engines such as Trino to query the data.

### Hidden Partitioning

Generally, partitioning a table using a transformation on a column (e.g., partition by day requires transforming the timestamp column to day and creating an extra column). Users must use this exact column to benefit from partition pruning.

For example, a table is partitioned by day, and every record must have an extra `partition_day` column derived from the `created_timestamp` column. When users query the table, they must filter on the exact `partition_day` column so the query engine can prune unwanted partitions. If the user isn’t aware of this and uses the `created_timestamp` column instead, the query engine will scan the whole table.

[![](https://substackcdn.com/image/fetch/$s_!PPNS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)](https://substackcdn.com/image/fetch/$s_!PPNS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffba22e19-185a-4371-87d6-31e56d637b42_1360x1042.png)

This is where Iceberg’s hidden partitioning shines:

[![](https://substackcdn.com/image/fetch/$s_!NAED!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)](https://substackcdn.com/image/fetch/$s_!NAED!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcffe3679-7b29-408f-9648-6ed4b4a51b18_1360x782.png)

* Instead of creating additional columns to partition based on transform values, Iceberg only records the transformation used on the column.
* Thus, Iceberg can save storage cost because it doesn’t need to store extra columns.

Another challenge with traditional partitioning is that it relies on the physical structure of the files being laid out into subdirectories; changing how the table was partitioned required rewriting the whole table.

Apache Iceberg solves this problem by storing all the historical partition schemes. If the table is first partitioned by scheme A and then later partitioned by schema B, Iceberg exposes this information to the query engine to create two separate execution plans to evaluate the filter again with each partition scheme.

Given a table initially partitioned by the `created_timestamp` field at a monthly granularity, the transformation `month(created_timestamp)` is recorded as the first partitioning scheme. Later, the user updates the table to be partitioned by `created_timestamp` at a daily granularity, with the transformation `day(created_timestamp)` recorded as the second partitioning scheme.

The data will be organized according to the partition scheme in place at the time of writing.

[![](https://substackcdn.com/image/fetch/$s_!k8Uk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d022718-2fab-4b3b-9d71-622c25f639a2_2000x1600.png)](https://substackcdn.com/image/fetch/$s_!k8Uk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d022718-2fab-4b3b-9d71-622c25f639a2_2000x1600.png)

When the application queries this table using `created_timestamp`, the query engine applies both the first and second transformations to `created_timestamp` to enable partition pruning.

[![](https://substackcdn.com/image/fetch/$s_!Q0zd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2d3932b-95cc-44e0-b54b-aca367a72cb2_1388x888.png)](https://substackcdn.com/image/fetch/$s_!Q0zd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2d3932b-95cc-44e0-b54b-aca367a72cb2_1388x888.png)

By leveraging Iceberg’s hidden partition, DoorDash helps users feel less confused when they need to know precisely what technical columns are used for partitioning.

---

## My thought

One of the advice I remember the most after reading the book [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/) is choosing common components wisely.

According to the author, data engineers should select common components that facilitate team collaboration and break down silos. They could be S3 for object storage, GitHub for version-control systems, Airflow for orchestration tools, or Spark for processing engines.

These components act like a toolkit for solving problems and prevent the need to reinvent the wheel. For the lake house specific problem, Iceberg is a strong candidate for your organization’s common component. It can work well with many systems. If you open a document from any cloud data warehouse or data processing engine, there is a very high chance that you will see Iceberg support at some level.

This provides you with more flexibility. You can make more reversible decisions. You no longer like Snowflake and want to try BigQuery, or you want to return to a self-managed, open-source solution engine like Trino. Iceberg can help you with that.

This does not mean Iceberg is the go-to choice for any data project. Every technical decision will have trade-offs, and the data practitioners should evaluate and make decisions based on the organization’s needs, not following trending tools.

Compared to using managed cloud data warehouses like BigQuery or Snowflake with their native storage offerings, adopting Iceberg requires more effort to understand how the table format works behind the scenes.

With DoorDash, I think they made a very good choice by storing data in S3 in the first place, rather than loading it directly into Snowflake. This might come from the intention of having total control over their data, but over time, this choice brings them many benefits. The most obvious one we see in this article is that it helps them onboard Iceberg more easily onto the platform.

Another observation is that we can see the advantage of “working well with many systems “ from the Iceberg, which could help DoorDash operate the Flink-Iceberg connection with just a few problems that could be easily debugged and fixed. From their sharing, DoorDash mentions more than once that they have trouble getting Flink to work with Delta Lake.

---

## Outro

In this article, we explore the motivation for the adoption of Iceberg for their real-time process platform, including its architecture, challenges, and benefits of the new approach. Finally, I have some thoughts on the trend of adopting Iceberg.

Thank you for reading this far. See you in my next article.

---

## Reference

[1] Tristan Culp, Gaurav Sharma, [Iceberg with Flink at DoorDash](https://www.youtube.com/watch?v=_nnNHC90nMI&t=541s) (2025)
