---
title: "5 insights to help you learn any open table format faster"
channel: vutr
author: "Vu Trinh"
published: 2026-05-26
url: https://vutr.substack.com/p/5-insights-to-help-you-learn-any
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Lakehouse", "Streaming"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# 5 insights to help you learn any open table format faster

*No matter whether they are Iceberg, Delta Lake, or Hudi.*

> Source: [Open post](https://vutr.substack.com/p/5-insights-to-help-you-learn-any)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=198215810)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!UXu4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28213de4-8a6e-442c-8c37-64e00f44b490_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!UXu4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28213de4-8a6e-442c-8c37-64e00f44b490_2000x1429.png)

---

# Intro

Open table formats like Iceberg, Hudi, or Iceberg are still one of the hottest topics in data engineering. (AI is still the top 1).

The “table format” is not only a trendy or marketing term anymore.

It’s earning the trust of more and more organizations, making itself a key part of many companies’ data infrastructure. Besides the big three: Iceberg, Hudi, and Delta Lake, more players have entered the market, such as Paimon or DuckLake.

Thus, I find it helpful to have a guideline for learning these table formats faster, as I believe there are some fundamentals shared across these formats, and once you learn them, you can scale your learning super fast.

This article will do exactly that: a set of insights/observations that help you pick up any table formats in hours.

> ***Note**: This article doesn’t dive into any table format. For that purpose, please refer to my other articles.*

---

# The Metadata Layer

> *…as the Source of Truth*

When you store data as Parquet files on S3, those are just objects.

However, we, as users, usually work with data in a more friendly abstraction: a table.

[![](https://substackcdn.com/image/fetch/$s_!gNLC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82ad7f89-46fa-4330-9659-8fc6460b2229_986x372.png)](https://substackcdn.com/image/fetch/$s_!gNLC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82ad7f89-46fa-4330-9659-8fc6460b2229_986x372.png)

Thus, we must have a way to “see“ these files as a table. More precisely, every database’s query engine must have a way. From Snowflake, BigQuery, Redshift, Databricks, or even PostgreSQL. All must have a “translator“ to help them “see” the files as a table.

To do this, all the databases have a metadata layer for this purpose. Believe it or not, this is the main idea behind any table format out there, from Iceberg to Delta Lake.

[![](https://substackcdn.com/image/fetch/$s_!_QvV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6081da77-2b1c-4a33-847d-e5520962f453_1016x644.png)](https://substackcdn.com/image/fetch/$s_!_QvV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6081da77-2b1c-4a33-847d-e5520962f453_1016x644.png)

The biggest difference is that Iceberg, Delta Lake, or Hudi is a separate metadata layer.

No database dependence. That’s why they got the “open“ before the “table formats“.

—

If you’re going to pick up any table formats, remember this:

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=198215810)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

All formats need to record the metadata somehow: it’s the table name, schema, column type, snapshots, file's location, the partition scheme, the column statistics, and many more.

[![](https://substackcdn.com/image/fetch/$s_!dxOT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b0a00da-c2bb-4210-965d-27e3f95e2e5b_880x456.png)](https://substackcdn.com/image/fetch/$s_!dxOT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b0a00da-c2bb-4210-965d-27e3f95e2e5b_880x456.png)

The metadata might have a different name or different structure: Iceberg calls them manifest files and metadata files and organizes them as a tree. Delta Lake calls it the transaction log, while Hudi calls it the Timeline.

But they're solving the same problems: “How does a query engine work on these files as if it were working with a table?“

—

This insight leads to another one. The read and write operations of all the formats will look like this:

* **Write**: data files go first, then metadata files follow
* **Read:** metadata files must be read first to know which data files to read.

—

The metadata layer also plays a crucial role in schema evolution.

A new column gets added. An old one gets renamed. A data type chosen two years ago turns out to be too narrow.

These changes are common.

The table formats decouple the schema from physical data by storing the schema information in the metadata layer. And because the metadata layer is a historical record, it can track every version of the schema the table has ever had, and when each one took effect.

[![](https://substackcdn.com/image/fetch/$s_!-Uc3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e34eb8c-c089-4115-b1a4-6ef1648f7378_1294x986.png)](https://substackcdn.com/image/fetch/$s_!-Uc3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e34eb8c-c089-4115-b1a4-6ef1648f7378_1294x986.png)

This separation is what makes schema evolution safe.

When a reader queries the table, it reads the schema from metadata, not from the files themselves. It knows which schema was in effect when each file was written, and it interprets each file accordingly. Old and new files can coexist in the same table under different schemas, and the reader handles both correctly without the user having to think about it.

---

# ACID

And for the table to work correctly, we need ACID.

ACID is the standard for ensuring that transactions are processed reliably. Think of it as a set of rules that prevents your data from becoming messy when things go wrong.

Ensuring a table’s ACID is also the table format’s responsibility.

[![](https://substackcdn.com/image/fetch/$s_!UpVb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7344c6a-c3ee-4b2e-8a60-695db86aa1ce_714x466.png)](https://substackcdn.com/image/fetch/$s_!UpVb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7344c6a-c3ee-4b2e-8a60-695db86aa1ce_714x466.png)

Neither S3 nor GCS gives you that. They can only ensure a single object transaction.

—

ACID has four properties, but two of them are almost free.

Consistency and Durability don’t require much from the table format itself.

The storage layer handles durability. S3 and Google Cloud Storage both provide 99.999999999% durability out of the box.

[![](https://substackcdn.com/image/fetch/$s_!TYyX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a8d7a-2ffa-45d1-af8a-c0e282fb6203_456x350.png)](https://substackcdn.com/image/fetch/$s_!TYyX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a8d7a-2ffa-45d1-af8a-c0e282fb6203_456x350.png)

Durability

Consistency is a special one as it also relies on the client side. Consistency is ensured when the data satisfies certain conditions. For example, your application must allow users who are older than 10, and the “user\_id” must be unique.

[![](https://substackcdn.com/image/fetch/$s_!FbdK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0b8269e-5c42-48cb-a9ad-160568c2d35d_450x244.png)](https://substackcdn.com/image/fetch/$s_!FbdK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0b8269e-5c42-48cb-a9ad-160568c2d35d_450x244.png)

Consistency

However, the statements are defined on the application side (typically based on business logic), and the database cannot be sure that all statements will be validated.

Although the table format can help with some validation (e.g., not null), in most cases, the data’s validity is defined by the application.

Thus, to ensure only data from users who are older than 10 years old is written, you must do that from the client side (e.g., setting the WHERE clause for the INSERT statement)

The two left are Isolation and Atomic.

## Isolation

[![](https://substackcdn.com/image/fetch/$s_!APL6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec402c32-55f2-4ce1-ad4c-8993959db1f6_456x306.png)](https://substackcdn.com/image/fetch/$s_!APL6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec402c32-55f2-4ce1-ad4c-8993959db1f6_456x306.png)

Isolation

Isolation is easy when two transactions touch completely different data. Let them run; things will be fine. It gets complicated when they’re operating on the same data.

Database researchers have identified a set of concurrency anomalies, such as a transaction seeing a piece of data with a different value later in time or reading or writing data that has not been committed. To deal with these anomalies, isolation levels were introduced from looser to tighter:

* **Read committed**: You are always reading and writing data that is committed.

  [![](https://substackcdn.com/image/fetch/$s_!_MMT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)](https://substackcdn.com/image/fetch/$s_!_MMT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)
* **Snapshot isolation (SI)**: The read committed level doesn’t prevent the scenario where a long-running read operation reads a single piece of data twice with different values at different points in time. In SI, each read transaction sees a consistent snapshot of the database.

  [![](https://substackcdn.com/image/fetch/$s_!aLEc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)](https://substackcdn.com/image/fetch/$s_!aLEc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)

  + The transaction will only see the changes committed before it started. All changes from other ongoing uncommitted transactions and from later transactions will be ignored.
* **Serializability:** This level guarantees the prevention of all anomalies. (So most databases aim for this). It guarantees that concurrent transactions execute as if they run serially. There are several approaches to implement this level:

  [![](https://substackcdn.com/image/fetch/$s_!lsSY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40fe2240-d6eb-4f5a-a663-c44eda17e8bf_932x610.png)](https://substackcdn.com/image/fetch/$s_!lsSY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40fe2240-d6eb-4f5a-a663-c44eda17e8bf_932x610.png)

  + Actual serial execution (nothing much to discuss, as the idea is to run each transaction one by one explicitly)
  + Two-phase locking (pessimistic concurrency control, PCC),
  + Snapshot isolation with serializability (optimistic concurrency control, OCC).

PCC says, *“I’m worried we’ll conflict, so you wait until I’m done.”* A writer grabs an exclusive lock; no one else can read or write that data until the lock is released. PCC is usually implemented using Two-phase locking.

[![](https://substackcdn.com/image/fetch/$s_!5t1q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d26ee0c-47a3-45f2-ad2c-405c11d1226b_1224x596.png)](https://substackcdn.com/image/fetch/$s_!5t1q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d26ee0c-47a3-45f2-ad2c-405c11d1226b_1224x596.png)

OCC says, *“Let’s both go, we’ll sort out conflicts at commit time.”* Every writer proceeds on their own isolated snapshot. When it’s time to commit, the system checks whether a conflict happens. If yes, abort and retry. If no, go on and commit. One way to implement OCC is through Snapshot isolation with serializability.

### Two-phase locking (2PL)

The database will implement the locking mechanism with two kinds of locks:

* **Shared Lock:** If a transaction wants to read data, it gets a shared lock on that data. Multiple transactions can hold shared locks on the same data item simultaneously (because reading doesn’t change the data).
* **Exclusive Lock:** If a transaction wants to *write* data, it must get an exclusive lock on that data. Only *one* transaction can hold an exclusive lock on a data item at any given time.

Every transaction must hold the lock until the end of the transaction. This strict locking mechanism significantly impacts performance, as write operations not only block other writes but also reads. This sacrifices throughput for safety.

### Serialized snapshot isolation (SSI)

[![](https://substackcdn.com/image/fetch/$s_!ZvPR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff87d7e8f-4d8d-4e81-8e6e-6a8b419f99ab_1342x558.png)](https://substackcdn.com/image/fetch/$s_!ZvPR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff87d7e8f-4d8d-4e81-8e6e-6a8b419f99ab_1342x558.png)

In SSI, the reads are served with consistent snapshots. For writes, it has mechanisms to detect conflicts.

For each transaction, a consistent snapshot is provided. When the time comes to commit, the system can check if any ignored changes from other transactions were committed during the transaction.

The database will abort the transaction if it detects that it attempts to modify data that other transactions may be modifying.

Compared to the 2PL, the SSI has a performance advantage because it doesn’t require locking for read or write operations. However, performance degrades as write contention increases. When detecting that the write might contain conflicting changes, the system asked the transaction to retry. Many retries can impact overall performance.

—

All these table formats will implement isolation following neither approach.

As I know, Paimon uses [2PL](https://www.ververica.com/blog/apache-paimon-the-streaming-lakehouse).

Iceberg, Hudi, and Delta Lake follow the OCC (with SSI): each writer works on an isolated snapshot, writes data files freely, then attempts a single atomic commit step. Only one writer can win that step. The loser checks for conflicts and retries.

—

Speaking of the snapshot.

Every write to a table format produces new files. Old files are never modified. Thus, every table modification returns in a new snapshot, which is a complete, consistent view of the table at a specific point in time. It’s simply a pointer in the metadata layer that says: *“at this moment, the table consists of exactly these files.”*

This pointer offers us many capabilities, from time travel, rolling back to isolation.

## Atomicity

[![](https://substackcdn.com/image/fetch/$s_!m7sV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F304ae99f-e499-4282-84bc-637888d25917_606x308.png)](https://substackcdn.com/image/fetch/$s_!m7sV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F304ae99f-e499-4282-84bc-637888d25917_606x308.png)

Atomicity ensures that if your transaction makes 10 changes, all 10 changes must be persisted or discarded.

It would be a nightmare if your transaction were marked as failed, but 7 changes were persisted while 3 were not.

Your data becomes corrupted, and you need to determine which changes were persisted and which were not so that you can retry properly.

The table format implements atomicity through the final metadata commit.

All data files are written to object storage first, but no reader can see them.

[![](https://substackcdn.com/image/fetch/$s_!2A4F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F143dcabc-f3f7-4a72-a0f5-6354aeda18f7_1454x902.png)](https://substackcdn.com/image/fetch/$s_!2A4F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F143dcabc-f3f7-4a72-a0f5-6354aeda18f7_1454x902.png)

They are invisible until the final piece of metadata is committed successfully: the catalog pointer in Iceberg, the log file in Delta Lake, and the .completed file in Hudi.

If that final step succeeds, everything becomes visible at once.

If that final step fails, nothing becomes visible. The data files written so far are orphaned and will eventually be cleaned up. The client can retry safely, because there’s nothing partially persisted here.

---

# Physical data layout

Every query you run against a table format ultimately becomes a file-reading problem. The engine has to find the data you need (with the help of the metadata), open the right files, and return the result.

The question is: how many files does it have to open to get there?

Open table formats are designed for the OLAP workload

The most common optimization technique for OLAP workloads is pruning data as much as possible.

From these two, we can say that the most common optimization technique in table formats is to prune data as much as possible.

There are three levels to do that in a table format:

* **Partitioning**: Splitting the table into smaller portions, allowing the query engine to interact only with the required portion. e.g., 2026-01-01 and 2026-01-02 partitions.

  [![](https://substackcdn.com/image/fetch/$s_!VesL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F530b6e5a-c4a8-4fc3-8758-32a643b56650_1204x626.png)](https://substackcdn.com/image/fetch/$s_!VesL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F530b6e5a-c4a8-4fc3-8758-32a643b56650_1204x626.png)
* **Clustering**: Collocating data in finer-grained form by techniques such as sorting or z-ordering. e.g., sorting data by user\_id to make sure data from the same user state are close together.

  [![](https://substackcdn.com/image/fetch/$s_!HCVA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fb0159b-4ca9-4fff-935a-532ed4f891d1_1192x724.png)](https://substackcdn.com/image/fetch/$s_!HCVA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fb0159b-4ca9-4fff-935a-532ed4f891d1_1192x724.png)
* **File statistic**: A table format can store column-level statistics for each data file: the minimum value, the maximum value, the null count, and the row count. The engine uses these statistics to skip files before opening them.

# Handling Data Updates

When you write data to object storage, the files are immutable. You can’t open a Parquet file and change a value inside it the way you’d edit a row in a database. So what happens when your data changes?

Every table format has to answer this question.

And there are two main ways to answer this: Copy-on-Write (CoW) and Merge-on-Read (MoR)

## CoW

This strategy prioritizes the performance and simplicity of read operations.

[![](https://substackcdn.com/image/fetch/$s_!Susn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5513b692-307e-4f10-a3a3-75a2188d0971_814x486.png)](https://substackcdn.com/image/fetch/$s_!Susn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5513b692-307e-4f10-a3a3-75a2188d0971_814x486.png)

Any modification, UPDATE, or DELETE is executed through atomic file replacement. The system identifies all data files that contain rows affected by the operation. It then reads these files, applies the required changes in memory, and writes entirely new versions.

[![](https://substackcdn.com/image/fetch/$s_!CZSU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f99a126-26b0-418f-88ef-f84f9f348e0b_550x506.png)](https://substackcdn.com/image/fetch/$s_!CZSU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f99a126-26b0-418f-88ef-f84f9f348e0b_550x506.png)

The final step is to commit the metadata with a message like this: “For the latest version of the table, please refer to these newly created files.” The old files are still retained for a period so they can be referenced within the snapshot of the older table. Then they will be garbage-collected to free up storage.

The primary motivation for choosing a CoW strategy is to optimize the read path:

* Because all changes are fully materialized during the write process, read queries do not need to perform any reconciliation of changes.

  [![](https://substackcdn.com/image/fetch/$s_!XI4_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bfc28e7-c9af-432b-be88-5a1b97045c35_442x206.png)](https://substackcdn.com/image/fetch/$s_!XI4_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bfc28e7-c9af-432b-be88-5a1b97045c35_442x206.png)
* The physical layout of a CoW table is straightforward. At any table’s snapshot, the table is represented by a set of data files. There are no extra changes or deleted files to manage.

The trade-off is the write performance:

* Small changes (e.g., three records) could force the system to rewrite the files with thousands of records to reflect the change.

  [![](https://substackcdn.com/image/fetch/$s_!Ud63!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b3be438-0907-40a0-9903-91b98035af80_704x200.png)](https://substackcdn.com/image/fetch/$s_!Ud63!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b3be438-0907-40a0-9903-91b98035af80_704x200.png)
* The process of reading, modifying, and rewriting files is inherently slow; the write operations will have higher latency.

  [![](https://substackcdn.com/image/fetch/$s_!NusG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88616065-2e5a-4638-9fd8-19ba680af544_820x338.png)](https://substackcdn.com/image/fetch/$s_!NusG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88616065-2e5a-4638-9fd8-19ba680af544_820x338.png)
* Essentially, when rewriting the data, we keep double the storage space for that file. Although a garbage collection process eventually removes the old files, the period before this cleanup can lead to substantial storage bloat.

  [![](https://substackcdn.com/image/fetch/$s_!5QL_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15c1adf8-a0e4-4b94-b04a-31f57205dd87_340x322.png)](https://substackcdn.com/image/fetch/$s_!5QL_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15c1adf8-a0e4-4b94-b04a-31f57205dd87_340x322.png)

## MoR

This strategy prioritizes write performance and low ingestion latency. It simply says: “If you have changes, write those to separate files; the reconciliation will happen later.“

[![](https://substackcdn.com/image/fetch/$s_!pCu5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5975ea4-5a5a-4067-9f62-ca921bc92439_670x392.png)](https://substackcdn.com/image/fetch/$s_!pCu5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5975ea4-5a5a-4067-9f62-ca921bc92439_670x392.png)

It avoids the rewriting of data files during a write operation. Instead, incoming updates, inserts, and deletes are recorded in separate and smaller files. (Fewer things to write make the writing faster). Then, the writer will commit metadata to “register” these change files for the latest snapshot of the table.

[![](https://substackcdn.com/image/fetch/$s_!42Sm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5498bb0e-4241-4861-a737-fcfd46952faa_382x350.png)](https://substackcdn.com/image/fetch/$s_!42Sm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5498bb0e-4241-4861-a737-fcfd46952faa_382x350.png)

The actual “merge” of these changes with the data files is postponed until a query is executed. At that time, the query engine combines the base data files with the change files to construct the latest view of the table.

[![](https://substackcdn.com/image/fetch/$s_!fZIu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65d72aed-dc04-491a-b4b6-1a1b313cfde6_860x254.png)](https://substackcdn.com/image/fetch/$s_!fZIu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65d72aed-dc04-491a-b4b6-1a1b313cfde6_860x254.png)

To ease the burden for the reader, there is a separate process called “compaction“. It asynchronously consolidates changes from the change files into the data files, providing complete table views for readers.

The merge process no longer needs to occur at read time (although it still must happen somewhere).

As mentioned, MoR is optimized for the write path. Writing changes to small files is orders of magnitude faster than rewriting large data files. This results in lower write latency than CoW. However, it has several disadvantages.

* More work to do later: the merge process must happen in the compaction process, or when the clients read the table. If the files are already compacted, the read performance will not be affected. However, if compaction does not occur at the right time, read clients must merge the files themselves, which makes reads slower than with CoW.

---

# Compaction and File Management

Every write results in a new file write due to the immutability of the underlying data.

The table never shrinks on its own. Files will only accumulate.

And the more files a reader has to open, the slower reading becomes, because each file has overhead: locating the file, downloading it from object storage, opening it, reading it, and closing it.

[![](https://substackcdn.com/image/fetch/$s_!YpAq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7808fea9-089b-41b1-8961-107b8c0d9d5d_932x666.png)](https://substackcdn.com/image/fetch/$s_!YpAq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7808fea9-089b-41b1-8961-107b8c0d9d5d_932x666.png)

Thus, reading 100MB from a single object is faster than reading 1MB from 100 objects. Every table format will include a mechanism for compacting small files. This process is inevitable in production workload.

From the MoR section above, you know that the compaction process can help merge base and delta files. But that’s only one of its applications. In general, the compaction process helps you read a bunch of data files in the background, process them, and write them back to the target file with the target file size. It can be used to:

[![](https://substackcdn.com/image/fetch/$s_!SG8L!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c654db8-d0cd-457f-a22b-9ffb1844dfb7_1342x786.png)](https://substackcdn.com/image/fetch/$s_!SG8L!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c654db8-d0cd-457f-a22b-9ffb1844dfb7_1342x786.png)

* Pre-merge file in MoR.
* Re-optimize clustered data. For example, at first, user\_id A is in one file; over time, as new data comes in, user\_id A is scattered across 3 files. Compaction consolidates it into one file.
* Merge small files due to frequent insert data. e.g., streaming writing.

Compaction isn’t free.

A relaxed compaction strategy can lead to a significant backlog of small files, which impacts read performance. In contrast, an aggressive strategy can consume more compute resources and compete with other components.

---

# Outro

In this article, I shared my 5 observations to help you learn any table formats faster: the metadata layer, ACID, physical data layout, handling updates, compaction, and file management.

Hope my work brings value.

Thank you for reading this far. See you in my next articles.
