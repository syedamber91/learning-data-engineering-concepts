---
title: "How do Delta Lake, Iceberg and Hudi ensure ACID?"
channel: vutr
author: "Vu Trinh"
published: 2026-02-10
url: https://vutr.substack.com/p/how-do-delta-lake-iceberg-and-hudi
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Databricks", "Delta Lake", "Data Lake", "Lakehouse"]
tags: [https, auto, transaction, substackcdn, image, fetch]
---

# How do Delta Lake, Iceberg and Hudi ensure ACID?

*Understanding the ACID guarantees of the three famous table formats from first principles*

> Source: [Open post](https://vutr.substack.com/p/how-do-delta-lake-iceberg-and-hudi)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=186065157)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!JwRO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19a189b9-4240-498c-8116-0c1c23f45a58_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!JwRO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19a189b9-4240-498c-8116-0c1c23f45a58_2000x1429.png)

---

## Intro

If people discuss lakehouse, a very high chance that they’re talking about table formats.

Delta Lake, Iceberg, Hudi, or DuckLake are the heart of any lakehouse implementation. They are the translators that close the gap between file/object abstraction (from the storage perspective) and table abstraction (from the engine/user perspective).

Every data operation must go through the table format layer. From inserting and deleting to data compaction and cleaning. Thus, to offer data warehousing capabilities on the data lake, the lakehouse architecture relies mostly on the open table format.

Version control, security, query performance, and most importantly, the ACID guarantee. In this article, we will learn how the big three table formats, Delta Lake, Iceberg, and Hudi, ensure ACID. Instead of diving into each implementation, I researched it from the first principle. We will start by revisiting what ACID is, the challenges of ensuring ACID on object storage, take a high-level overview of these three formats, and then dive into the ‘C‘, ‘D‘, ‘I‘, and ‘A‘.

---

## What is ACID

### Overview

In the world of databases, ACID is the standard for ensuring that transactions are processed reliably. Think of it as a set of rules that prevents your data from becoming a messy, inconsistent disaster when things go wrong.

The first pillar is the Atomicity.

[![](https://substackcdn.com/image/fetch/$s_!m7sV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F304ae99f-e499-4282-84bc-637888d25917_606x308.png)](https://substackcdn.com/image/fetch/$s_!m7sV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F304ae99f-e499-4282-84bc-637888d25917_606x308.png)

This property ensures that all changes for a given transaction either succeed or fail. This allows the client to retry the transaction in case of failure.

Next is the Consistency.

[![](https://substackcdn.com/image/fetch/$s_!FbdK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0b8269e-5c42-48cb-a9ad-160568c2d35d_450x244.png)](https://substackcdn.com/image/fetch/$s_!FbdK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0b8269e-5c42-48cb-a9ad-160568c2d35d_450x244.png)

This is a special one as it also relies on the client side. The consistency is ensured when the data satisfies certain statements. For example, your application must allow users who are older than 10, and the “user\_id” must be unique. However, the statements are defined on the application side (typically based on business logic), and the database cannot be sure that all statements will be validated.

Then comes the Isolation.

[![](https://substackcdn.com/image/fetch/$s_!APL6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec402c32-55f2-4ce1-ad4c-8993959db1f6_456x306.png)](https://substackcdn.com/image/fetch/$s_!APL6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec402c32-55f2-4ce1-ad4c-8993959db1f6_456x306.png)

Isolation ensures that concurrent transactions are not interleaved. In other words, a transaction can think that it is the only one running in the database.

[![](https://substackcdn.com/image/fetch/$s_!TYyX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a8d7a-2ffa-45d1-af8a-c0e282fb6203_456x350.png)](https://substackcdn.com/image/fetch/$s_!TYyX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a8d7a-2ffa-45d1-af8a-c0e282fb6203_456x350.png)

Finally, the Durability. It ensures that, once the transaction commits successfully, its changes will never be lost under any circumstances.

### Challenges of ensuring ACID on object storage

Most lakehouses use object storage services such as S3 or Google Cloud Storage for the data persistent layer. You might wonder why we don’t use the object storage layer to provide ACID guarantees.

[![](https://substackcdn.com/image/fetch/$s_!ybRX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda6e685d-d9e2-4473-98df-d5cfcb17b4a6_1322x776.png)](https://substackcdn.com/image/fetch/$s_!ybRX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda6e685d-d9e2-4473-98df-d5cfcb17b4a6_1322x776.png)

The thing is, object storage could ensure Durability in the ACID. However, it does not support multi-object atomic transactions, which means that if your operations require writing data to 2 objects and a failure occurs, you could end up with 1 object persisted and the other never made it.

It violates the “Atomicity.”

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=186065157)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Overview of the three formats

Before diving into how Hudi, Delta Lake, and Iceberg ensure ACID, let’s first review them, focusing mostly on their data and metadata architecture. In every format, I will note a point about its transaction handle mechanism. Please keep this in mind so that when we explain ‘Atomicity‘ and the ‘Isolation‘ guarantees, it will be easier to grasp the idea.

### Iceberg

Iceberg’s architecture has three distinct layers to define a table’s state.

[![](https://substackcdn.com/image/fetch/$s_!Hf5l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a7ba58d-2b35-42d9-9c6e-e498f78ff5f4_856x938.png)](https://substackcdn.com/image/fetch/$s_!Hf5l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a7ba58d-2b35-42d9-9c6e-e498f78ff5f4_856x938.png)

* **The Data Layer** consists of the actual data files in object storage.
* **The Metadata Layer** has an immutable tree structure of metadata files. These metadata files also persist in object storage. The hierarchy allows Iceberg to track table state efficiently without relying on directory listings

  + **Table Metadata File (**`metadata.json`**):** This file serves as the root of the tree for a given table version. It is a JSON file containing a comprehensive definition of the table, including its current schema, historical snapshots, partitioning scheme, sort order, and more.
  + **Manifest List:** This is a metadata file (in Avro format) that contains a list of all the manifest files that make up a particular snapshot. This allows query planners to skip entire groups of data files without reading the manifest files themselves.
  + **Manifest File:** This is also an Avro file that lists a subset of a table’s data files. For each data file, the manifest stores detailed statistics, such as column-level metrics (minimum and maximum values, null counts, etc.). This file-level metadata is essential for query optimization, as it enables file pruning, allowing the query engine to avoid reading data files that don’t contain the required data.
* **The Catalog Layer** is the entry point for Iceberg table operations and is the single source of truth for the current state of any given table. Its primary responsibility is to map the table identifier to the location of that table’s current metadata file.

> ***Remember this:** The Iceberg transaction completes only if the catalog pointer swapping is successful. When writing data, the engine contacts the catalog to retrieve the current metadata file, writes the required metadata and data, and finally requests the catalog to atomically update the pointer from the path of the old metadata file to the path of the new metadata file.*

### Delta Lake

Delta Lake leverages the logging pattern to support atomic operations.

A Delta Lake table is a “directory” in cloud object storage that contains the table’s data objects and a log of transaction operations.

[![](https://substackcdn.com/image/fetch/$s_!2iLM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20cd24af-ec24-43c8-b446-74ee73bae9a7_960x602.png)](https://substackcdn.com/image/fetch/$s_!2iLM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20cd24af-ec24-43c8-b446-74ee73bae9a7_960x602.png)

> ***Note**: Object storage doesn’t support directories. However, users can organize data using a prefix to make it appear as **folders**. A prefix is a string of characters at the beginning of the object key. For example, two objects with the keys* `reports/2025/sales.csv` *and* `reports/2025/inventory.csv` *will appear to be in a* `2025` *folder, which is inside a* `reports` *folder.*

The data in a table is stored in Apache Parquet objects, which can be organized into directories using [Hive’s partitioning](https://delta.io/blog/pros-cons-hive-style-partionining/) (if the table is partitioned). The log stores transaction metadata, such as data files added or removed during the transaction.

[![](https://substackcdn.com/image/fetch/$s_!6g_G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff229b319-6a2f-4baa-bca7-0c6181efbaa2_974x608.png)](https://substackcdn.com/image/fetch/$s_!6g_G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff229b319-6a2f-4baa-bca7-0c6181efbaa2_974x608.png)

In the Delta Lake table directory, the transaction log is managed in a subdirectory called `_delta_log`. The log is a sequence of JSON objects with increasing, zero-padded numerical IDs (e.g., 000003). Each log record object contains a series of actions to apply to the previous version of the table to generate the next one.

> ***Remember this:** The Delta Lake transaction completes only after the engine successfully writes a new JSON log object and all data files have been written.*

### Hudi

Hudi Timeline records all actions performed on the table over time, providing instantaneous views of the table while efficiently supporting data retrieval in the order of arrival.

[![](https://substackcdn.com/image/fetch/$s_!ixeC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c41e286-6172-486f-9d40-b6679d1673ab_1166x340.png)](https://substackcdn.com/image/fetch/$s_!ixeC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c41e286-6172-486f-9d40-b6679d1673ab_1166x340.png)

Essentially, **Timeline** shared some similarity to Delta Lake’s delta\_log. It is physically stored as a set of files within the `.hoodie` directory at the root of the table path. Changes to Hudi tables are recorded as ***actions*** in the Hudi ***timeline***.

* **Instants:** Every action that occurs on a Hudi table, from data ingestion to background maintenance, is recorded on the timeline as an **instant**. Each instant is identified by a globally unique, monotonically increasing timestamp that serves as its transaction ID. This timestamp is critical to ensuring the correct order of operations.
* **Actions and State Transitions:** An instant is composed of an action type and a state. Each action progresses through a series of states, with each transition physically recorded by creating a new file on the timeline (located in the `.hoodie` directory). The standard lifecycle is:

  1. `<instant_time>.<action>.requested`: The action has been scheduled but has not yet started.
  2. `<instant_time>.<action>.inflight`: The action is currently being executed.
  3. `<instant_time>.<action>.completed`: The action has finished successfully. The creation of this file is the atomic event that finalizes the transaction.

> ***Remember this:** The Hudi transaction completes only if the engine successfully performs the final state transition on the timeline.*

---

## Brief on the ‘C‘ and the ‘D‘

For consistency, as mentioned above, it does not rely entirely on the database (the table format)

[![](https://substackcdn.com/image/fetch/$s_!h9AJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024495a2-7ac2-488a-9be4-33c66fc1557d_948x500.png)](https://substackcdn.com/image/fetch/$s_!h9AJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024495a2-7ac2-488a-9be4-33c66fc1557d_948x500.png)

Although the table format can help with some validation (e.g., not null), in most cases, the data’s validity is defined by the application. Thus, to ensure only data from users who are older than 10 years old is written, you must do that from the client side (e.g., setting the WHERE clause for the INSERT statement)\

Regarding the Durability.

When building the Lakehouse on object storage (e.g., S3 or GCS), these services will guarantee this property without requiring us to implement it explicitly. Amazon S3 and Google Cloud storage both provide 99.999999999% durability.

[![](https://substackcdn.com/image/fetch/$s_!tqAA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50c67423-015c-4092-b035-9979deb8bd30_546x248.png)](https://substackcdn.com/image/fetch/$s_!tqAA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50c67423-015c-4092-b035-9979deb8bd30_546x248.png)

For that reason, this article won’t discuss consistency and durability as much as it will discuss isolation and atomicity pillars.

Now, let’s get straight into the Isolation.

---

## Isolation

Isolation is straightforward if the two running transactions work on different data; let them run, and everything will be fine. However, things are more difficult when operating on the same data.

Over time, database researchers have identified a set of concurrency anomalies, such as a transaction seeing a piece of data with a different value later in time or reading or writing data that has not been committed.

> *For the full list of anomalies, you can [visit my previous article](https://open.substack.com/pub/vutr/p/acid-for-data-engineers?utm_campaign=post-expanded-share&utm_medium=web).*

To deal with these anomalies, isolation levels were introduced from looser to tighter:

* **Read committed**: Ensuring that you’re always reading and writing data that is committed.

  [![](https://substackcdn.com/image/fetch/$s_!_MMT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)](https://substackcdn.com/image/fetch/$s_!_MMT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)
* **Snapshot isolation**: the read committed level doesn’t prevent the scenario where a long-running read operation reads a single piece of data twice with different values at different points in time. The idea of Snapshot isolation is straightforward: each read transaction sees a consistent snapshot of the database. The transaction will only see the changes committed before it started. All changes from other ongoing uncommitted transactions and from later transactions will be ignored.

  [![](https://substackcdn.com/image/fetch/$s_!aLEc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)](https://substackcdn.com/image/fetch/$s_!aLEc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)
* **Serializability**: This level guarantees the prevention of all anomalies. (So most databases aim for this) The idea of serializability is simple: although transactions can run in parallel, their effects are equivalent to running them serially (one at a time). There are several approaches to implementing serializability, including actual serial execution (nothing much to discuss, as the idea is to run each transaction one by one explicitly), two-phase locking (pessimistic concurrency control, PCC), and snapshot isolation with serializability (optimistic concurrency control, OCC).

  [![](https://substackcdn.com/image/fetch/$s_!zsfO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbcee5b8-672b-4ed4-b585-16626b2a3724_716x462.png)](https://substackcdn.com/image/fetch/$s_!zsfO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbcee5b8-672b-4ed4-b585-16626b2a3724_716x462.png)

And OCC is our main focus today, as all three table formats implement this approach. We will take a quick overview of actual serial execution and two-phase locking before diving into snapshot isolation with serializability.

### Two-phase locking (2PL) (PCC)

The database will implement the strict locking mechanism with two kinds of locks:

* **Shared Lock:** If a transaction wants to read data, it gets a shared lock on that data. Multiple transactions can hold shared locks on the same data item simultaneously (because reading doesn’t change the data).
* **Exclusive Lock:** If a transaction wants to *write* data, it must get an exclusive lock on that data. Only *one* transaction can hold an exclusive lock on a data item at any given time; if a client holds an exclusive lock, no one else can hold any lock (exclusive or shared).

Every transaction must hold the lock until the end of the transaction. This strict locking mechanism significantly impacts performance, as write operations not only block other writes but also reads. This affects the database throughput and response time.

### Serialized snapshot isolation (SSI) (OCC)

The locking mechanism is also referred to as pessimistic concurrency control.

“If you worry things will go wrong when multiple writers are involved, just allow one to run, and the others must wait.”

[![](https://substackcdn.com/image/fetch/$s_!5t1q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d26ee0c-47a3-45f2-ad2c-405c11d1226b_1224x596.png)](https://substackcdn.com/image/fetch/$s_!5t1q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d26ee0c-47a3-45f2-ad2c-405c11d1226b_1224x596.png)

In contrast to pessimistic concurrency control, optimistic concurrency control is more relaxed.

“All of the writers, come here and do what you need; we will resolve it later.“

SSI is an optimistic concurrency control approach.

In SSI, the reads are served with consistent snapshots. For writes, it has mechanisms to detect conflicts.

[![](https://substackcdn.com/image/fetch/$s_!l6Kj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7c97505-357d-4491-b4f5-f79336a6cffa_1470x556.png)](https://substackcdn.com/image/fetch/$s_!l6Kj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7c97505-357d-4491-b4f5-f79336a6cffa_1470x556.png)

For each transaction, a consistent snapshot is provided. When the time comes to commit, the system can check if any ignored changes from other transactions were committed during the transaction.

The database will abort the committing transaction if it detects that the transaction is trying to modify data that other transactions are potentially modifying.

Compared to the 2PL, the SSI has a performance advantage because it doesn’t require locking for read or write operations. However, performance degrades as write contention increases. When detecting that the write might contain conflicting changes, the system asked the transaction to retry. Many retries can impact overall performance.

With the principle of working on an isolation snapshot for a data operation and allowing writes to proceed without locking, we will dive into how Hudi and Delta Lake implement OCC for Isolation.

### Iceberg

If two write transactions happen concurrently, here is what the process looks like in Iceberg:

[![](https://substackcdn.com/image/fetch/$s_!xrJq!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5e50e6e-bd00-44a9-acc1-c36e61b26735_1502x792.png)](https://substackcdn.com/image/fetch/$s_!xrJq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5e50e6e-bd00-44a9-acc1-c36e61b26735_1502x792.png)

1. The two transactions begin by contacting the catalog to get the current metadata file (`v1.metadata.json`)
2. They then write new data and metadata in the object storage. The readers don’t see these files at this stage.
3. Next, the first writer creates a new table metadata file (`v1.metadata.json`). This new file contains all the information from the previous metadata file and also includes an entry for the latest snapshot. Then, the first writer requests the catalog (backed by a transactional database) to atomically update the pointer from the path of the old metadata file to the path of the new metadata file. The writer tells the catalog: “If the current metadata pointer is still `v1.metadata.json`, update it to `v2.metadata.json`.” Now the pointer point to the `v2.metadata.json`
4. The second writer also tries to commit `v2.metadata.json` but fails because the catalog pointer doesn’t point to `v1.metadata.json` anymore, which implies that the current transaction has worked on a different table state than the state it retrieved from the catalog at the beginning of the transaction. This second writer must review the transaction to ensure there are no conflicts with changes from other transactions, and request that the catalog point to `v3.metadata.json` later.

### Delta Lake

If two write transactions happen concurrently, here is what the process looks like in Delta Lake:

[![](https://substackcdn.com/image/fetch/$s_!lQY9!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F730ff2b4-9dd0-411e-ab9b-186b7140ef0c_1550x776.png)](https://substackcdn.com/image/fetch/$s_!lQY9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F730ff2b4-9dd0-411e-ab9b-186b7140ef0c_1550x776.png)

* Both writers first start reading the \_delta\_log folder to get the table’s current state. (`000001.json`)
* They write new data files. Readers don’t see these files.
* The first writer attempts to commit the log object `000002.json` in the `_delta_log` directory.
* The OCC principle in Delta Lake is to avoid overwriting the delta log entry files. (e.g., two writes can not write the same log object 00002.json). The second transaction also tries to create the `000002.json`.

  + However, Delta Lake will reject it because the `000002.json` was already created by the first writer. The second transaction must be reviewed for any conflict with the new changes made by the first transaction. If yes, it must be aborted; if no, the transaction can continue to commit with the new object name (e.g., `000003.json`)

As these log files are stored in object storage (Delta Lake can’t rely on the transactional database like Iceberg), Delta Lake uses put-if-absent operations from object storage for this purpose:

* They use existing atomic put-if-absent operations from Google Cloud Storage and Azure Blob Store. The put-if-absent operation says that “only insert this object into the storage when there is no other object with the same name.“
* Initially, Amazon S3 did not support the put-if-absent operation, so Delta Lake on S3 relied on an external service to manage the table lock. The client must first acquire the table lock (via DynamoDB) to ensure that only one client can add a record with each log ID. However, [Amazon announced support for conditional writing to S3](https://aws.amazon.com/about-aws/whats-new/2024/08/amazon-s3-conditional-writes/) in August 2024. Delta Lake - S3 users no longer need DynamoDB. anymore.

## Hudi

Hudi is similar to Iceberg or Delta Take, as it also relies on atomic final-state transitions on the timeline to implement OCC. If two write transactions happen concurrently, here is what the process looks like in Delta Lake:

[![](https://substackcdn.com/image/fetch/$s_!s5fU!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e9c5e1c-7875-4a60-8f18-b2499edae96b_1540x674.png)](https://substackcdn.com/image/fetch/$s_!s5fU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e9c5e1c-7875-4a60-8f18-b2499edae96b_1540x674.png)

* The two transactions begin by requesting a new, unique, and monotonically increasing timestamp for their transactions.
* They create the `<instant_time>.<action>.requested` file on the timeline (which also lives in the object storage).
* The writers transition the state to `inflight` by creating the corresponding file and then proceed to write the data files. During this stage, the new files are not visible to the other operation.
* When all data is written successfully, the transaction performs the final, atomic step: it creates the empty `<instant_time>.<action>.completed` file on the timeline.
* However, during the final step, there is a difference compared to Iceberg or Delta Lake; the write transaction must acquire the lock (users must configure the lock provider, such as Zookeeper or DynamoDB). While it had the lock, the transaction could check the timeline for any completed commits during its execution. If yes, it checks whether the changes in the current transaction conflict with those from other commits. If there is no conflict, it creates the `<instant_time>.<action>.completed` file.

The important point is that the lock is needed only when transactions attempt to commit (to prevent the timeline from being modified), not for the entire lifetime of the transaction.

Hudi v1.0 (2024) introduced "Non-Blocking Concurrency Control (NBCC)", which allows multiple writers to concurrently write to the table without worrying about conflicts during writes. If there are conflicts, they can be resolved later in the read time (query or compaction process)

> *You can read more about NBCC [on Hudi's official blog.](https://hudi.apache.org/blog/2024/12/06/non-blocking-concurrency-control/)*

---

## Atomicity

Atomicity ensures that if your transaction makes 5 changes, all 5 changes must be persisted or discarded. It would be a nightmare if your transaction were marked as failed, but 2 changes were persisted while 3 were not. Your data becomes corrupted, and you still need to determine which changes were persisted and which were not so that you can retry properly.

Thus, atomicity makes your failures safer and easier to retry.

The common approach to implementing atomicity is to write changes to a temporary location (such as a staging file in Git). Based on the final state of the transactions, the changes are either applied (to the actual data) or dropped.

[![](https://substackcdn.com/image/fetch/$s_!3bdM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e57fbc7-35c9-4617-bf28-d351e6d93d76_1250x782.png)](https://substackcdn.com/image/fetch/$s_!3bdM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e57fbc7-35c9-4617-bf28-d351e6d93d76_1250x782.png)

The implementation of the Atomicity in Delta Lake, Iceberg, and Delta Lake is quite clear during the Isolation section above: All the data changes are persisted in object storage; however, they are not visible to any operations until the final piece of metadata is committed successfully, it is the catalog pointer in Iceberg, the log file in Delta Lake and the `<instant_time>.<action>.completed` file in Hudi.

If the transaction fails, the client can safely retry because files written by the previous failed transaction are considered orphaned and will be cleaned up.

---

## Outro

In this article, we first review what ACID is and the challenges of ensuring ACID on object storage. Then we take a quick review of the metadata-data architecture of Hudi, Iceberg, and Delta Lake.

Next, we had a brief discussion of Consistency and Durability, then spent a fair amount of time on Isolation, with the main theme being optimistic concurrency control (OCC). We then see details of OCC implementation in Hudi, Iceberg, and Delta Lake. Finally, we examine atomicity by noting that data files are visible to the user only after the transaction successfully commits the related metadata to the table format; files from failed transactions are orphaned.

Thank you for reading this far. See you in my next article.

---

*[1] Martin Kleppmann, [Designing Data-Intensive Applications, Chapter 7: Transactions](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)*

*[2] Arpit Bhayani, [Decoding Atomicity - The A in ACID](https://arpitbhayani.me/blogs/atomicity/#:~:text=Atomicity%20in%20Databases,are%20either%20applied%20or%20dropped.)*

*[3] Shiyan Xu, [Apache Hudi: From Zero To One (7/10)](https://blog.datumagic.ai/p/apache-hudi-from-zero-to-one-710)*

*[4] Tomer Shiran, Jason Hughes & Alex Merced, [Apache Iceberg: The Definitive Guide](https://www.dremio.com/wp-content/uploads/2023/02/apache-iceberg-TDG_ER1.pdf) (2024)*

*[5] Databricks, [Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf), (2020)*

*[6] Jack Vanlightly, [Understanding Delta Lake’s consistency model](https://jack-vanlightly.com/analyses/2024/4/29/understanding-delta-lakes-consistency-model) (2024)*

*[7] Timeline, [Apache Hudi official document](https://hudi.apache.org/docs/timeline/)*

*[8] How does Hudi ensure atomicity? [Design & Concepts FAQ, Apache Hudi official document](https://hudi.apache.org/docs/faq_design_and_concepts/#how-does-hudi-ensure-atomicity)*
