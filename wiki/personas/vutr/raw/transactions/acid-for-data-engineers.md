---
title: "ACID For Data Engineers"
channel: vutr
author: "Vu Trinh"
published: 2025-07-15
url: https://vutr.substack.com/p/acid-for-data-engineers
paid: true
topics: ["Data Engineering", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Streaming"]
tags: [https, auto, media, substackcdn, image, fetch]
---

# ACID For Data Engineers

*How well do you know about Atomicity, Consistency, Isolation and Durability?*

> Source: [Open post](https://vutr.substack.com/p/acid-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[streaming|Streaming]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> *I invite you to join the club with a **50% discount on the yearly package.** Let’s not be suck as data engineering together.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!yeQk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09f71258-0549-4767-93ae-312b14bf814e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!yeQk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09f71258-0549-4767-93ae-312b14bf814e_2000x1429.png)

---

## Intro

Like many other guys who are interested in data management systems, I heard and learned about ACID guarantees. However, I find that internet resources on this topic are quite oversimplified, and I decided to invest my time in researching it.

This article is my note on the relational database ACID constraints. I hope that the next time we read a document about an OLAP database, when it mentions that it supports ACID, we will understand what it is referring to.

> Note: This article is written for my newsletter audience, who are primarily data engineers, so that the content will focus more on the ACID properties of OLAP systems.

---

## Durability

For me, this property is the easiest one to understand. It ensures that once the transaction commits successfully, all of its changes will never be lost in any circumstances.

Most OLAP systems are multi-node, as they operate across multiple servers. Durability is ensured by successfully storing various data copies on more than one server.

[![](https://substackcdn.com/image/fetch/$s_!jeVc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F025e05bc-4d3b-47a9-ac69-d6e621b2326a_310x284.png)](https://substackcdn.com/image/fetch/$s_!jeVc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F025e05bc-4d3b-47a9-ac69-d6e621b2326a_310x284.png)

When building the data management system on object storage (e.g., S3 or GCS), these services will guarantee this property without requiring us to implement it explicitly. Amazon S3 and Google Cloud storage both provide 99.999999999% durability.

[![](https://substackcdn.com/image/fetch/$s_!tqAA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50c67423-015c-4092-b035-9979deb8bd30_546x248.png)](https://substackcdn.com/image/fetch/$s_!tqAA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50c67423-015c-4092-b035-9979deb8bd30_546x248.png)

If you're using Hudi, Iceberg, Delta Lake, or commercial solutions like Redshift, Snowflake, or Databricks—all built on object storage—you usually don’t need to worry about durability.

## Isolation

People use databases to store data. Then, the data is accessed by those who need it. They want, at the very least, the data to be accurate (it reflects what happens in real life), especially in an environment where potentially many clients use the database.

Isolation ensures that concurrent transactions are isolated. In other words, a transaction can think that it is the only one running in the database. It is straightforward if the two running transactions are working on different pieces of data; let them run, and everything will be fine. However, things are more difficult when operating on the same data.

### Anomalies

Over time, database researchers have identified a set of concurrency anomalies (potential concurrent problems). Imagine we have two concurrent transactions, T1 and T2, that operate on the same piece of data. These anomalies are:

* **Dirty Read:** T1 writes some data to the database, but it hasn’t committed the changes yet. If T2 can read these uncommitted changes, this behavior is called a dirty read.

  [![](https://substackcdn.com/image/fetch/$s_!IPb5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F079134b4-abee-4ac3-b695-00bdd06c2e22_986x540.png)](https://substackcdn.com/image/fetch/$s_!IPb5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F079134b4-abee-4ac3-b695-00bdd06c2e22_986x540.png)
* **Dirty Write:** T1 writes some data to the database, but it hasn’t committed the changes yet. If T2 can overwrite these uncommitted changes, this behavior is referred to as a dirty write.

  [![](https://substackcdn.com/image/fetch/$s_!g96v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8ae27e-458a-401e-a6a1-4bd3699610b5_954x512.png)](https://substackcdn.com/image/fetch/$s_!g96v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8ae27e-458a-401e-a6a1-4bd3699610b5_954x512.png)
* **Non-repeatable read:** During the transaction, if T1 sees a piece of data with a different value at a different point in time, this behavior is called the non-repeatable read.
* **Lost Update:** T1 reads a piece of data (a = 2), and T2 also reads the same data. T1 then modifies the object and commits (a = 3). T2 then modifies this data based on its original read (a = 2) and commits (with a new value of a = 4), accidentally overwriting T1's update.
* **Phantom read:** T1 executes a read operation with objects that satisfy a particular WHERE clause. T2 then modifies the objects that satisfy this WHERE clause and commits changes. If T1 repeats its query, it sees a different result.

  + This is different from **Non-repeatable read** and **Dirty Read** because the T1 and T2 operate on different objects.
* **Write Skew:** It can happen when T1 reads some data from the A object, makes changes based on the value it saw, and commits the changes to the B object. However, during the process of making the B’s changes, the original values of A are changed by the T2.

  + This is different from **Lost Update** and **Dirty Write** because the T1 and T2 operate on different objects.
  + The effect of changing the filter conditions during the process of making changes based on the conditions is also referred to as **phantoms**.

> ***Note**: I will provide concrete examples in the following sections for those that do not seem obvious at first glance: the **non-repeatable read**, the **lost update**, the **phantom read**, and the **write skew**.*

To deal with these anomalies, database researchers have introduced the following isolation levels, from looser to tighter:

> *For example, read committed can prevent dirty reads and dirty writes; thus, snapshot isolation can also prevent these anomalies.*

* Read committed
* Snapshot isolation
* Serializability

### Read committed

This level ensures that you’re always reading and writing data that is committed (no dirty reads and dirty writes).

[![](https://substackcdn.com/image/fetch/$s_!_MMT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)](https://substackcdn.com/image/fetch/$s_!_MMT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdf143f-a7a5-4180-a31f-6209bcded0e2_796x508.png)

For read committed, a database typically uses row-level locks. When a transaction wants to write a row, it must acquire the lock for that row. Others who wish to modify this row must wait for this transaction to finish and acquire the lock.

[![](https://substackcdn.com/image/fetch/$s_!Skvb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F827e3a50-445f-47f5-a135-0debc2c024f8_990x546.png)](https://substackcdn.com/image/fetch/$s_!Skvb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F827e3a50-445f-47f5-a135-0debc2c024f8_990x546.png)

For the read operation, although a locking mechanism can be implemented, it is inefficient, as long-running writes can affect the read operations.

[![](https://substackcdn.com/image/fetch/$s_!BpUr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2996bda0-bc8d-46ac-87e8-6ee597e768c3_770x494.png)](https://substackcdn.com/image/fetch/$s_!BpUr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2996bda0-bc8d-46ac-87e8-6ee597e768c3_770x494.png)

A more viable approach is to keep two copies of the data in the database. The old version is the one that was committed, and the new version is the one being modified by the write transaction currently holding the lock. When a transaction needs to read this data, the database provides the old value to it.

### Snapshot isolation (SI)

However, the read committed level doesn’t prevent the scenario where a long-running read operation reads a single piece of data twice with different values at different points in time, as a new value has been committed during the long-running read operation. This isn’t a dirty read, as both times the transaction read the data, it was committed (twice). The behavior is called a non-repeatable read**.**

[![](https://substackcdn.com/image/fetch/$s_!UliT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb56a3c-6429-4c3e-8d30-2fdc17fd28af_890x526.png)](https://substackcdn.com/image/fetch/$s_!UliT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb56a3c-6429-4c3e-8d30-2fdc17fd28af_890x526.png)

The SI comes to the rescue. The idea is straightforward: each read transaction reads a consistent snapshot of the database. The transaction will only see all the changes that were committed before the start of this transaction. All changes from other ongoing transactions that are uncommitted will be ignored. Changes from later transactions will also be ignored.

[![](https://substackcdn.com/image/fetch/$s_!aLEc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)](https://substackcdn.com/image/fetch/$s_!aLEc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc21b80b0-a57b-4b38-a151-8d6b8b45b374_808x480.png)

Compared to the implementation of preventing dirty reads from the read committed level, SI keeps more than two versions of a data object. Thus, some documents refer to SI as **multi-version concurrency control (MVCC)**. The cool thing about SI is that it prevents non-repeatable reads and doesn’t require read locks. However, it still requires write locks to prevent dirty writes.

Another anomaly SI can prevent is the **lost update**. Let’s consider an example where two concurrent transactions (T1 and T2) update a bank balance (currently $1,000). T1 is updated (+200), and T2 is updated (+300). Both transactions read the committed version of the balance (1,000$), T1 updates it to 1200$ and writes it back.

However, T2 still sees the 1000$ balance; it updates it to $1,300 and writes it back. The +200 is disappearing, and the client will sue the bank for stealing their money :D

[![](https://substackcdn.com/image/fetch/$s_!LoTx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3cec274-a5e6-4259-affb-94aa33d52d03_1000x466.png)](https://substackcdn.com/image/fetch/$s_!LoTx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3cec274-a5e6-4259-affb-94aa33d52d03_1000x466.png)

To prevent lost updates, the transaction that updates a piece of data can **lock** this data, preventing it from being modified by other transactions.

Some databases (which don’t support transactions) implement a **compare-and-swap** atomic operation to prevent lost updates. The idea is that the database only updates the data if it has changed since the last read from this transaction.

Let's continue with the next anomaly: the **phantom reads**. Imagine you’re building a meeting room application, and two users can’t book a room at the same time slot. The first client checks for an available room in the 1:00 - 2:00 time slot and finds that **only room A is available**. The client inserted a booking record for room A in the 1:00 - 2:00 time slot.

[![](https://substackcdn.com/image/fetch/$s_!55K7!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe097dec-0977-4e91-8df2-2ba1354c14c2_996x640.png)](https://substackcdn.com/image/fetch/$s_!55K7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe097dec-0977-4e91-8df2-2ba1354c14c2_996x640.png)

During the process of committing the new booking record for the first client, the second client commits a booking record for room A in the 1:00-2:00 time slot faster, making room A unavailable.

If the first client checks for the available rooms again, they will see an empty result. The change in the search results (room A is not available) is caused by a modification from a concurrent transaction, which is known as a phantom read.

[![](https://substackcdn.com/image/fetch/$s_!GuJY!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4bd3f9b-62ee-4967-b848-98f7472d2d63_954x682.png)](https://substackcdn.com/image/fetch/$s_!GuJY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4bd3f9b-62ee-4967-b848-98f7472d2d63_954x682.png)

The SI approach can prevent phantom reads with the help of consistent snapshots. However, it can’t stop the two clients from inserting the conflict changes here. (Both books the room A between 1:00 and 2:00)

### Serializability

The behavior of making changes (booking the room A between 1:00 and 2:00) based on conditions (the room is available), but the conditions are no longer true (a concurrent client successfully books the room A between 1:00 and 2:00)

…is called write skew.

[![](https://substackcdn.com/image/fetch/$s_!KifB!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F257f4d9a-e7d6-46af-bc9d-57fd48f0a632_1042x608.png)](https://substackcdn.com/image/fetch/$s_!KifB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F257f4d9a-e7d6-46af-bc9d-57fd48f0a632_1042x608.png)

As discussed right above, SI can’t prevent this. This anomaly can only be prevented by the strongest isolation level: serializability. This level also guarantees the prevention of all the anomalies discussed above.

[![](https://substackcdn.com/image/fetch/$s_!zsfO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbcee5b8-672b-4ed4-b585-16626b2a3724_716x462.png)](https://substackcdn.com/image/fetch/$s_!zsfO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbcee5b8-672b-4ed4-b585-16626b2a3724_716x462.png)

The idea of serializability is simple: although the transactions can run in parallel, the effect is the same as if they were run serially (one at a time). There are several approaches to implement serializability, including actual serial execution, two-phase locking, and serialized snapshot isolation.

#### Just throwing the concurrency.

The first approach is to prevent transactions from running in parallel. (If you don’t want the concurrent problems, don’t do it.) However, the database throughput (the number of transactions per second) is limited.

#### Two-phase locking (2PL)

The next approach is the two-phase locking (2PL). It also employs a locking mechanism, but it is stricter than the one used to prevent dirty writes. 2PL has two kinds of locks:

* **Shared Lock:** If a transaction wants to read data, it gets a shared lock on that data. Multiple transactions can hold shared locks on the same data item simultaneously (because reading doesn't change the data).

  [![](https://substackcdn.com/image/fetch/$s_!DJQO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6d09c78-e460-47a7-ab62-e2a8a5f2f3f1_804x482.png)](https://substackcdn.com/image/fetch/$s_!DJQO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6d09c78-e460-47a7-ab62-e2a8a5f2f3f1_804x482.png)
* **Exclusive Lock:** If a transaction wants to *write* data, it must get an exclusive lock on that data. Only *one* transaction can hold an exclusive lock on a data item at any given time: if a client has an exclusive lock, no one can have a lock (either an exclusive or a shared one).

  [![](https://substackcdn.com/image/fetch/$s_!6OyW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14a22624-8078-4a75-a318-58a4bed879c6_736x434.png)](https://substackcdn.com/image/fetch/$s_!6OyW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14a22624-8078-4a75-a318-58a4bed879c6_736x434.png)

Every transaction must hold the lock until the end of the transaction. However, this strict locking mechanism has a significant impact on performance, as the write operation not only blocks other write operations but also blocks read operations. This affects the database throughput and response time.

#### Serialized snapshot isolation (SSI)

This approach is relatively new compared to the 2PL. It still provides the serializability while performing better than the 2PL (under a condition).

The locking mechanism is also referred to as pessimistic concurrency control. “If you worry things will be messed up, just wait until the moment things are safe to go ahead”. In contrast to pessimistic concurrency control, optimistic concurrency control is more relaxed. “Don’t need to wait, things will be all right.“

[![](https://substackcdn.com/image/fetch/$s_!t5Ki!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F999fa4bc-98b4-41e9-84f7-b64a9a28b18d_748x398.png)](https://substackcdn.com/image/fetch/$s_!t5Ki!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F999fa4bc-98b4-41e9-84f7-b64a9a28b18d_748x398.png)

SSI is an optimistic concurrency control approach. SSI is still based on the SI; the readings are still served with consistent snapshots. However, SSI has mechanisms to detect conflicts between writes.

[![](https://substackcdn.com/image/fetch/$s_!GM5y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeafad0-50b4-4591-826c-0f33f58e2f53_496x260.png)](https://substackcdn.com/image/fetch/$s_!GM5y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeafad0-50b4-4591-826c-0f33f58e2f53_496x260.png)

A common approach is to detect whether the reading snapshot is stale. For a given transaction, SI provides it with a consistent snapshot and ignores changes from ongoing or new transactions. With SSI, the database can check if any ignored changes were committed during the transaction. If so, the database will abort the transaction if it’s not a read-only transaction (Write skew might happen if it were a write transaction).

[![](https://substackcdn.com/image/fetch/$s_!r7uP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d5a2360-9105-4a47-a14a-bcd0c0492643_826x428.png)](https://substackcdn.com/image/fetch/$s_!r7uP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d5a2360-9105-4a47-a14a-bcd0c0492643_826x428.png)

Compared to the 2PL, the SSI has a performance advantage as it doesn’t require locking for write or read operations. However, the performance is degraded if the rate of write contention increases. When detecting that the write might contain conflicting changes, the database asked the transaction to abort and retry. Many retry transactions can impact overall performance.

### Isolation in OLAP

For OLAP systems, you will find that most of them use SSI to support transaction isolation. From [BigQuery](https://storage.googleapis.com/gweb-research2023-media/pubtools/7810.pdf), [Snowflake](https://www.cs.cmu.edu/~15721-f24/papers/Snowflake.pdf), to [Iceberg](https://iceberg.apache.org/docs/1.6.0/reliability/), [Delta Lake](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf), or [Hudi](https://hudi.apache.org/docs/concurrency_control/). Given the benefit of non-blocking operations, it can help achieve high throughput while efficiently supporting long-running read-only transactions (typical workloads in OLAP systems) with consistent snapshots.

Given the fact that the OLAP databases' typical workload is long-running read operations, they can relax a bit on the write contention problems. However, if an OLAP database needs high-throughput write operations (streaming inserts), things might be a bit challenging.

For example, [AWS introduced their effort to deal with the write contention problem in Iceberg.](https://aws.amazon.com/blogs/big-data/manage-concurrent-write-conflicts-in-apache-iceberg-on-the-aws-glue-data-catalog/)

> *This is my observation; feel free to correct me.*

## Atomicity

This property ensures that all changes for a given transaction are complete in one of the two states: all succeed or all fail. This provides the client with simplicity in retrying the transaction in case of failure.

Just imagine that the transaction has five changes. Without atomicity, three changes are committed, and the other two changes fail. How does the client determine which changes to retry?

[A general approach for implementing atomicity in a database is to write changes in a temporary location. Based on the final state of the transactions, the changes are either applied (to the actual data) or dropped.](https://arpitbhayani.me/blogs/atomicity/#:~:text=Atomicity%20in%20Databases,are%20either%20applied%20or%20dropped.)

[![](https://substackcdn.com/image/fetch/$s_!bex2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc521d453-fc43-4bf1-ba7a-b4360dcac509_1176x468.png)](https://substackcdn.com/image/fetch/$s_!bex2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc521d453-fc43-4bf1-ba7a-b4360dcac509_1176x468.png)

[This property can also be implemented by maintaining a copy of the affected data before applying the changes.](https://arpitbhayani.me/blogs/atomicity/#:~:text=Atomicity%20in%20Databases,are%20either%20applied%20or%20dropped.)

[![](https://substackcdn.com/image/fetch/$s_!G14T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F777a46f4-4ec6-49a5-bc29-49dc608f8d6b_576x402.png)](https://substackcdn.com/image/fetch/$s_!G14T!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F777a46f4-4ec6-49a5-bc29-49dc608f8d6b_576x402.png)

For OLAP systems, the atomicity implementation is relatively straightforward, based on a crucial property of these systems: data is immutable after a successful commit, and changes are made by writing new data files.

Open table formats like Delta Lake, Iceberg, and Hudi ensure atomicity by first writing the necessary changes (new data files, metadata files) to the object storage; however, these files are invisible to readers (analogous to writing changes to a temporary location).

[![](https://substackcdn.com/image/fetch/$s_!LATk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8107f617-f7bd-4b0c-a870-c1778c9aa4fb_616x454.png)](https://substackcdn.com/image/fetch/$s_!LATk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8107f617-f7bd-4b0c-a870-c1778c9aa4fb_616x454.png)

Then, these systems rely on a lightweight atomic operation that creates the metadata object (the metadata files in Iceberg, the object logs in Delta Lake, and the completed files in Hudi) to commit the transaction successfully. During this metadata commit atomic operation, they will check for a conflict, just as the SSI approach discussed above.

## Consistency

This is a very special property. The database can completely guarantee all the properties above except for this one.

This consistency is ensured when the data satisfies certain statements. For example, your application must allow users who are older than 10 years old, and the `user\_id` must be unique.

If a transaction starts in a state where all data in the database is already valid based on the defined statements, the changes made by this transaction must also result in data that satisfies these statements.

[![](https://substackcdn.com/image/fetch/$s_!nrnS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce21150e-1c48-44db-9803-05e72c9f9afb_560x344.png)](https://substackcdn.com/image/fetch/$s_!nrnS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce21150e-1c48-44db-9803-05e72c9f9afb_560x344.png)

But here is the catch. The statements are defined from the application side (typically based on business logic), and the database cannot be sure that the data will be validated for all statements. To my humble knowledge, all OLAP systems can’t verify if a user is at least 10 years old or if the activity event occurred after 2023.

[![](https://substackcdn.com/image/fetch/$s_!h9AJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024495a2-7ac2-488a-9be4-33c66fc1557d_948x500.png)](https://substackcdn.com/image/fetch/$s_!h9AJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024495a2-7ac2-488a-9be4-33c66fc1557d_948x500.png)

Although the database can perform some validation (using primary keys, foreign key constraints, etc), most of the time, the data's validity status is defined by the application. That said, unlike other properties, consistency can’t be entirely guaranteed by the database.

Speaking of constraints, OLAP systems are more relaxed compared to OLTP systems. Because they don’t maintain a lookup index like OLTP databases, validating the uniqueness of a row is quite challenging to implement. Most cloud data warehouses, like [Snowflake](https://docs.snowflake.com/en/sql-reference/constraints-overview), [BigQuery](https://cloud.google.com/blog/products/data-analytics/join-optimizations-with-bigquery-primary-and-foreign-keys), or [Databricks](https://www.databricks.com/blog/primary-key-and-foreign-key-constraints-are-ga-and-now-enable-faster-queries), let users specify the primary key or foreign keys for a table (for better data integrity); however, the responsibility of enforcing the validation of these columns is in the hands of the users.

---

## Outro

Thank you for reading this far.

With this article, I hope to have provided you with the most comprehensive view of the ACID possible. We begin with the most straightforward property, Durability, and then spend a fair amount of time on Isolation. Next, we learn about Atomicity, and finally, we explore the strange case of Consistency.

Now, see you next time.

---

## Reference

[1] Martin Kleppmann, [Designing Data-Intensive Applications, Chapter 7: Transactions](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)

*[2] Arpit Bhayani, [Decoding Atomicity - The A in ACID](https://arpitbhayani.me/blogs/atomicity/#:~:text=Atomicity%20in%20Databases,are%20either%20applied%20or%20dropped.)*
