---
title: "Everything you need to know about CDC"
channel: vutr
author: "Vu Trinh"
published: 2025-10-28
url: https://vutr.substack.com/p/everything-you-need-to-know-about-741
paid: true
topics: ["Data Engineering", "Apache Kafka", "Apache Flink", "Snowflake", "Data Warehouse", "Batch Processing", "Change Data Capture", "ETL"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# Everything you need to know about CDC

*What it is, why we need it, its typical real-life implementations, and more.*

> Source: [Open post](https://vutr.substack.com/p/everything-you-need-to-know-about-741)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[data-warehouse|Data Warehouse]] · [[batch-processing|Batch Processing]] · [[change-data-capture|Change Data Capture]] · [[etl|ETL]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!FzLM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F159e3246-6b18-484d-9d61-6296c966b6ad_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!FzLM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F159e3246-6b18-484d-9d61-6296c966b6ad_2000x1428.png)

---

## Intro

Your company has a PostgreSQL database.

Every day, you have to extract the data from the database, load and process the data in your Snowflake database.

You ask the software engineer to get into the database so you can dump the snapshot.

It works fine for a while.

The company’s app growth. More data to come. The snapshot dump process gets slower. The database has high resource utilization. Business users require lower latency.

Dumping everything does not work. You tried to extract the data incrementally and realized that some big tables don’t have the `updated\_timestamp`.

—

In such a case, Change Data Capture (CDC) can help you. This article will delve into this mechanism. By the end of this article, you will understand what CDC is, its common types and use cases, real-life implementations, and the extent to which OLAP systems support this mechanism.

## Overview

Essentially, CDC refers to the process of tracking and shipping the changes made to data in a source database—specifically INSERT, UPDATE, and DELETE operations—and then delivering those changes to a downstream process or system.

[![](https://substackcdn.com/image/fetch/$s_!jq3n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf592b68-2f2b-4bcd-9ace-213ce7b6a09c_596x194.png)](https://substackcdn.com/image/fetch/$s_!jq3n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf592b68-2f2b-4bcd-9ace-213ce7b6a09c_596x194.png)

It is an approach to track and action on the “deltas” or incremental modifications, rather than scanning and exporting the full dataset.

The output of a CDC process is a delta dataset. It could be a batch of changes over a period or a continuous stream of changes.

[![](https://substackcdn.com/image/fetch/$s_!jSk0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d5df055-af6b-4f00-b2db-8ae708115dbf_682x390.png)](https://substackcdn.com/image/fetch/$s_!jSk0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d5df055-af6b-4f00-b2db-8ae708115dbf_682x390.png)

For the latter, the stream provides a granular and chronological record of every modification that has occurred within the source system: Each feed’s event not only contains the data that changed but also metadata, such as the type of operation performed (INSERT, UPDATE, and DELETE).

## Type of CDC

There are three typical types of CDC. They are distinguished by the way of tracking changes and the form of the output (batch or stream)

### Query-Based

Query-based CDC, also known as polling-based CDC, is the simplest method to implement but is also the most limited in its capabilities.

[![](https://substackcdn.com/image/fetch/$s_!rubo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46d989c6-ee2b-405a-871b-f65f837b546a_668x258.png)](https://substackcdn.com/image/fetch/$s_!rubo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46d989c6-ee2b-405a-871b-f65f837b546a_668x258.png)

This method involves periodically executing SQL queries to check for changed records since the last run. The most common technique relies on a dedicated column in the source table, such as an `updated\_timestamp`.

The CDC process maintains a “checkpoint” (the timestamp of the last run) and queries for all rows where the timestamp is greater than this checkpoint. The checkpoint is then updated so the next run can continue to query change records.

#### Advantages

* **Simplicity**: This is often the easiest method to implement. It uses standard SQL queries and typically does not require any special database features.

#### Disadvantages

* **Can’t track deletes**: Once a row is physically deleted from the source table, it no longer exists to be selected by a subsequent query.

  [![](https://substackcdn.com/image/fetch/$s_!Ga1r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe28b2034-7331-4bc0-b9dc-3710ea354e61_596x244.png)](https://substackcdn.com/image/fetch/$s_!Ga1r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe28b2034-7331-4bc0-b9dc-3710ea354e61_596x244.png)

  Therefore, DELETE operations are skipped, which might lead to data inconsistencies between the source and target. (e.g., row A is deleted in the source, but it still exists in the target because the process doesn’t know it was deleted.)
* **Put pressure on the source**: Frequent scanning of large tables makes the source database do more work, making the resource utilization high.

  [![](https://substackcdn.com/image/fetch/$s_!ksFY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c91d9d8-bee3-4227-8b1a-614617b4e60d_552x296.png)](https://substackcdn.com/image/fetch/$s_!ksFY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c91d9d8-bee3-4227-8b1a-614617b4e60d_552x296.png)

  To avoid impacting the source database that serves production traffic, the polling queries can be routed to a read-only replica.
* **Latency**: The freshness of the data depends on the polling interval. If the system polls every five minutes, the data in the target system can be up to five minutes stale.
* **Required additional column:** This approach is only available if the table has a column to help identify changed records.

  [![](https://substackcdn.com/image/fetch/$s_!jaNg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabaeb6b1-4371-4e25-9ec8-d0b245c6e97d_520x254.png)](https://substackcdn.com/image/fetch/$s_!jaNg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabaeb6b1-4371-4e25-9ec8-d0b245c6e97d_520x254.png)

  If your colleagues forget to add it, you'll need to find alternative solutions.

### Trigger-Based

This approach utilizes database triggers, which are stored procedures that are executed in the background to follow the specific data modification events on a table. For CDC, `INSERT`, `UPDATE`, and `DELETE` triggers are created on the source tables.

[![](https://substackcdn.com/image/fetch/$s_!kOXR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa09da912-81fd-4cab-9f23-5cfa05e1ad69_798x292.png)](https://substackcdn.com/image/fetch/$s_!kOXR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa09da912-81fd-4cab-9f23-5cfa05e1ad69_798x292.png)

When a change occurs, the associated trigger fires and writes a record of that change—including the operation type and the affected data—into a separate table within the same database. The CDC process periodically reads new entries from the shadow table to capture changes.

#### Advantages

* Can track **any data changes**, including DELETE
* **Immediacy**: Triggers capture changes immediately as they happen.

  + However, how fast the changes are propagated to downstream systems also depends on the running interval of the CDC process (to read the table that contains changes from the trigger’s writes)
* **Availability**: The concept of triggers is a standard feature and is widely supported across the common relational databases.

#### Disadvantages

* **Performance**: This is the typical drawback of this approach. Every transaction on a tracked table incurs additional write overhead.

  [![](https://substackcdn.com/image/fetch/$s_!SFUN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f752ca1-bd4e-4efb-8c37-adbc83b11c26_660x292.png)](https://substackcdn.com/image/fetch/$s_!SFUN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f752ca1-bd4e-4efb-8c37-adbc83b11c26_660x292.png)

  + The database must perform at least two writes: one for the original table and a second for the write from the trigger.
  + In case you need your database to be high-throughput, this overhead can significantly degrade performance.
* **Maintainability**: Managing a large number of triggers can become complex. Plus, you still need a separate process to read the tracked table.

### Log-Based

This method operates by reading changes directly from the database’s transaction “log”. It is implemented differently depending on the DBMS. However, the high-level idea is quite the same.

[![](https://substackcdn.com/image/fetch/$s_!dYIV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab3417be-2b04-4a71-bb1b-8d460f937bb2_590x364.png)](https://substackcdn.com/image/fetch/$s_!dYIV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab3417be-2b04-4a71-bb1b-8d460f937bb2_590x364.png)

The “log“ serves as an ordered, durable, and complete record of every committed transaction. A CDC tool with a log-based reader taps into this stream of log records, parses them, and propagates them to downstream systems.

#### Advantages

* **Minimal Performance Impact**: This is the most significant advantage of this approach. Because the process reads from log files rather than executing queries against the tables, log-based CDCD allows for continuous changes capture with minimal performance overhead.
* **Completeness**: The “log” is the ultimate source of truth for all data modifications. Log-based CDC can therefore capture all types of changes.
* **Low Latency**: By reading changes as they are committed to the log, this method provides near real-time changes shipping to consumed systems.

#### Disadvantages:

* **Complexity**: Log-based CDC often requires specific database configurations, such as enabling logical replication in PostgreSQL. It may also require elevated system permissions to grant the CDC process access to the transaction log files, which can be a challenge in strictly controlled environments.

  [![](https://substackcdn.com/image/fetch/$s_!wWzm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16dfd49-286e-45c3-915c-987b1fd479dd_1092x318.png)](https://substackcdn.com/image/fetch/$s_!wWzm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16dfd49-286e-45c3-915c-987b1fd479dd_1092x318.png)

  + Because consuming change logs in this approach boils down to consuming a real-time stream, you will need infrastructure to do that, from the message queue, the producer/consumer, to whether your destination accepts the stream.
  + The CDC vendor can help you abstract some level of complexity; still, you have to manage lots of things.
* **Proprietary Log Formats**: Each DBMS implements its own format for the “logs”. This creates a dependency on the CDC tool’s connector to interpret the specific log format of the source database.

## Dive into the Log-Based approach.

Given its characteristics of minimal performance impact on the source and the low latency, log-based CDC is widely adopted as the most efficient, scalable, and reliable approach for use cases that require continuous change synchronization.

### The WAL

As we discussed, the technology behind log-based CDC is the database transaction log. It’s worth mentioning that this log was not designed for data integration but to support core DBMS operations.

[![](https://substackcdn.com/image/fetch/$s_!hJKu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0309613b-0830-4ffb-96a2-a88c905c0775_422x368.png)](https://substackcdn.com/image/fetch/$s_!hJKu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0309613b-0830-4ffb-96a2-a88c905c0775_422x368.png)

This log—known as the redo log in Oracle, the Write-Ahead Log (WAL) in PostgreSQL, or the binary log (binlog) in MySQL—is a fundamental component of modern transactional databases. They share a principle called **write-ahead logging** (WAL); all data changes must be recorded in the log on stable storage (disk) *before* they are applied to the database’s data files.

By following this rule, if the database system crashes after a transaction has committed but before its changes were written from the in-memory buffers to the data files, the system can use the WAL to **find** committed transactions that *are* in the log but *might not* have made it to the main data file and **reapply** these changes. This is important for the DBMS to ensure **durability**.

Because the log is the definitive record of all committed changes, it is the ideal source for the CDC process.

### A typical Log-Based CDC Pipeline

In real life, the log-based CDC pipeline will vary depending on your tech stack. However, at the conceptual level, the pipeline will look like this:

[![](https://substackcdn.com/image/fetch/$s_!ai9S!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc6c3d59-c689-4fdc-b292-0ff19940b95a_924x242.png)](https://substackcdn.com/image/fetch/$s_!ai9S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc6c3d59-c689-4fdc-b292-0ff19940b95a_924x242.png)

* **Change in Source Database**: The process begins when a user or application commits a transaction (`INSERT`, `UPDATE`, or `DELETE`) to a source transactional database (e.g., PostgreSQL, MySQL).
* **Transaction Log Write**: As part of its standard operation to ensure durability, the database writes a record of this transaction to its native transaction log before the changes are finalized in the data files.
* **The log reader**: An instance will read this log with a specific configuration for the source database. It continuously monitors for new log records. You will rarely build this on your own; instead, you will rely on the available CDC connector for this purpose. (e.g., [Debezium Connector For PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html))
* **The log publisher:** An instance will publish the new log record to the message queue. Again, you rarely build this instance from scratch. The CDC connector will also handle this task.
* **Message broker**: The log records are then stored in the message broker (e.g., Apache Kafka). This step is to ensure reliable log delivery. Additionally, it helps decouple log producers and log consumers, allowing the two instances to operate at their desired pace. (e.g., the source can generate hundreds of changes per minute, but the source doesn’t need to keep up with that rate, as it only needs to query all the data changes in the last 1 hour)
* **Downstream Consumers**: Downstream systems and applications subscribe to the relevant broker topics. These consumers read the change events from the message broker and process them according to their specific needs

## Use cases

> *There are many potential use cases of CDC, so that I won’t deliver every single one. Instead, I tried to group these use cases into larger categories.*

### Incremental and real-time data synchronization

In a traditional ETL/ELT pipeline, data extraction is the very first step.

[![](https://substackcdn.com/image/fetch/$s_!2MZ5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F922fa85f-1824-4203-baf4-f532ec8f0074_412x174.png)](https://substackcdn.com/image/fetch/$s_!2MZ5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F922fa85f-1824-4203-baf4-f532ec8f0074_412x174.png)

The worker executes the query like `SELECT \* FROM customers`, which pulls the entire state of a table. If it contains millions of rows, all the million rows are read, transferred over the network, and landed into your data warehouse, even if only … 100 records have changed since the last run.

[![](https://substackcdn.com/image/fetch/$s_!rmB-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c174c15-88ce-4449-bdc8-0556fb061829_410x180.png)](https://substackcdn.com/image/fetch/$s_!rmB-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c174c15-88ce-4449-bdc8-0556fb061829_410x180.png)

Pressure on your source database, along with inefficiency in data processing and loading.

If your colleagues specify the `updated\_timestamp` column for the table. Great, you can use it (**Query-Based CDC**) to limit only updated data over a period of time (e.g., “give me all the data updated in the last 1 day“)

[![](https://substackcdn.com/image/fetch/$s_!xxag!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e8c6944-ad7f-4068-a6ba-366711a524e4_404x176.png)](https://substackcdn.com/image/fetch/$s_!xxag!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e8c6944-ad7f-4068-a6ba-366711a524e4_404x176.png)

What if the table doesn’t have that column?

[![](https://substackcdn.com/image/fetch/$s_!UeAo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13bfd805-1e9b-4b69-9d0b-d93fb25c17c8_422x206.png)](https://substackcdn.com/image/fetch/$s_!UeAo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13bfd805-1e9b-4b69-9d0b-d93fb25c17c8_422x206.png)

**Log-based CDC** can help. With the ability to propagate data changes via the database log, users no longer need to perform full table exports or rely on artificial columns. The changes are continuously shifted to your warehouse, allowing you to choose how to process the delta changes as you see fit.

Log-based CDC also opens up a new processing capability.

The latency of batch processing has long constrained traditional business intelligence. The approach eliminates this limitation by feeding BI tools and dashboards with the most up-to-date data possible, allowing companies to observe what happens with their business in (near) real-time.

[![](https://substackcdn.com/image/fetch/$s_!c_bv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F982bb001-4467-4da8-b150-d4141e8684fd_562x164.png)](https://substackcdn.com/image/fetch/$s_!c_bv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F982bb001-4467-4da8-b150-d4141e8684fd_562x164.png)

This capability extends beyond dashboards to offer the new class of time-sensitive, data-driven applications. For instance, in financial services, the approach can be utilized to capture and analyze transactional data changes in real-time, facilitating fraud detection and risk management.

Besides the analytics use case, CDC in general can serve as a synchronization engine to replicate changes from the source (e.g., the OLTP database ) and propagate them to any number of target systems—such as caches, search indexes, or other microservices.

### Data Exchange Between Services

In distributed systems, the outbox pattern is a design approach where a service reliably saves both its state change and the corresponding event to its own database within a single atomic transaction *before* publishing that event to a message broker.

This pattern solves the “dual-write” problem, which can lead to data inconsistencies in distributed systems. Imagine a user signs up. Your `UserService` needs to do two things:

[![](https://substackcdn.com/image/fetch/$s_!ZXZq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8378f2dd-43ee-46d6-9626-04758f1b3f50_600x270.png)](https://substackcdn.com/image/fetch/$s_!ZXZq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8378f2dd-43ee-46d6-9626-04758f1b3f50_600x270.png)

1. **Save the user** to the database.
2. **Publish a** UserCreated **event** to a message broker (like Kafka or RabbitMQ) so other services can react (e.g., an `EmailService` can send a welcome email).

If you perform these operations sequentially, what happens if the database write succeeds but your service crashes just before publishing the event? The user exists in your database, but no other service knows about it. The welcome email is never sent.

[![](https://substackcdn.com/image/fetch/$s_!d-Kj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F720386d8-55fe-4345-b0a4-e1c96e81d4b7_476x224.png)](https://substackcdn.com/image/fetch/$s_!d-Kj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F720386d8-55fe-4345-b0a4-e1c96e81d4b7_476x224.png)

The Outbox Pattern uses the service’s own database as a reliable, temporary holding area for messages, ensuring the state change and the event are never separated.

Here’s how it works:

[![](https://substackcdn.com/image/fetch/$s_!HbHG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e9b0842-12db-425d-984d-53d993a8999f_748x274.png)](https://substackcdn.com/image/fetch/$s_!HbHG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e9b0842-12db-425d-984d-53d993a8999f_748x274.png)

1. **A Single Atomic Transaction:** When the user signs up, the service performs two actions *within the same database transaction*:

   * It inserts the new user’s data.
   * It inserts a record representing the event (e.g., { event\_type: “UserCreated”, payload: “...” }) into a special “outbox” table
2. **Commit:** The transaction is committed. Because it’s **atomic**, either **both** writes succeed, or **both** fail. It’s impossible to have a new user without a corresponding event waiting in the “outbox”.
3. **The Message Relay:** A separate, independent process (the “relay”) monitors the “outbox” table to

   * Read unprocessed events.
   * Publish them to the message broker.

CDC (both Trigger and Log-based) could act as the **message relay**. It continuously monitors for any new entries in the “outbox” table (e.g., with the type of “INSERT“). When a new event is committed to this table, CDC captures this change and publishes a message to a broker like Kafka or RabbitMQ.

### Audit Log

One of the most significant advantages of CDC is capturing the entire history of changes (except for the Query-Based approach), which would be very helpful in case you need an audit log for your database.

[![](https://substackcdn.com/image/fetch/$s_!-Ywd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F490b094c-abb4-43a0-8952-306005c61ad3_576x360.png)](https://substackcdn.com/image/fetch/$s_!-Ywd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F490b094c-abb4-43a0-8952-306005c61ad3_576x360.png)

Many industries are governed by strict regulations that legally require organizations to maintain detailed audit trails of access to sensitive data. Failure to comply can result in legal action. For example:

* **Healthcare (HIPAA)**: The Health Insurance Portability and Accountability Act requires that any access or modification to patient electronic health records (ePHI) must be logged to ensure patient privacy.
* **Finance (SOX, PCI DSS)**: The Sarbanes-Oxley Act (SOX) requires public companies to have controls over financial reporting data, which includes auditing database changes. The Payment Card Industry Data Security Standard (PCI DSS) requires detailed logs of all access to cardholder data.

Beyond compliance, audit logs can assist in debugging application issues and understanding system behavior. They provide a historical record that can help reconstruct events to find the root cause of a problem. For example, if a product’s price is suddenly `$0.00`, the log can show the exact `UPDATE` statement that caused it.

## Consideration

### Performance overhead

Like anything in the world, the CDC is not free. From the simplest (query-based) to the most robust (log-based) approach, each will have its own performance consideration:

* **Log-Based CDC:** This is generally the lowest-impact method, but it still requires reading the database’s transaction logs (e.g., binlog, WAL, redo logs). Additionally, the database may need to provide more detailed information in the log to better meet the consumers' needs.
* **Trigger-Based CDC:** Triggers fire for *every* `INSERT`, `UPDATE`, and `DELETE` on the tracked tables. This adds write overhead directly into the application’s transactions.
* **Query-Based CDC:** Periodically polling tables can create a significant read load, especially on large tables.

When implementing the CDC pipeline, we must collaborate with the teams responsible for the source databases to plan and test the pipeline before deploying it to production. Some infrastructure changes may be needed for the source databases, like setting up a new read-replica for the CDC process.

### Operational Complexity and Monitoring

CDC is a process that requires robust monitoring, particularly when adopting the log-based approach, which involves multiple components:

* **Lag Monitoring:** Replication lag indicates how far behind the CDC process is from the live database. High lag causes your data to be stale and suggests that there is a bottleneck (s) in the CDC pipeline.
* **Alerting:** You need to know when the pipeline fails, when lag exceeds a threshold, or when unexpected changes enter the pipeline (e.g., schema change)
* **Failure Recovery:** You'd better have a guideline for what to do when it fails. How to restart the process? How can we bridge the gap?

### Schema Changes

The schema can change. Developers can add, drop, or change data types in columns. When a developer runs an ALTER TABLE statement to modify the schema, the schema changes are propagated to the consumers, who might not be aware of this change beforehand, causing these applications to fail.

For this concern, I think the best way to handle it is to communicate with the source database’s team actively so that any changes in the schema will be notified. The notification can be used as a signal for an event-driven architecture, enabling the target system to adjust its schema accordingly based on changes from the source database. As I know, databases allow for tracking of schema changes via triggers following the DDL statement, which can also serve as a schema change notification.

Last year, Flink introduced [Flink CDC 3.0](https://www.alibabacloud.com/blog/flink-cdc-3-0%EF%BD%9C-a-next-generation-real-time-data-integration-framework_601223), which has the capability to handle schema evolution.

### Security

The CDC tool needs permissions to read the database’s internal transaction logs. The credentials for the CDC tool must adhere to the **principle of least privilege**. We need to work with teams responsible for the source databases to figure out which permissions the CDC needs for the process, and follow the vendor's suggestion to provide the credentials for the connector securely.

## Outro

In this article, we first understand the high-level idea of the CDC mechanism and move on to explore three major types of CDC processes: query-based, trigger-based, and log-based. Then, we delve into the most robust approach among the three: the log-based CDC, from understanding its idea, which database principle (WAL) backs the process, to its typical implementation in production.

Next, we explore some use cases of CDC, and finally discover some concerns when operating a CDC pipeline in production.

Thank you for reading this far. See you in my next article.

## Reference

*[1] [Debezium connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)*

*[2] Gunnar Morling, [CDC Use Cases: 7 Ways to Put CDC to Work](https://www.decodable.co/blog/cdc-use-cases), 2023*

*[3] Hans-Peter Grahsl, [Schema Evolution in Change Data Capture Pipelines](https://www.decodable.co/blog/schema-evolution-in-change-data-capture-pipelines), 2024*

*[4] Wikipedia, [Change data capture](https://en.wikipedia.org/wiki/Change_data_capture)*
