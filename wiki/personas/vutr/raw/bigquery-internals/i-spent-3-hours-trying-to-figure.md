---
title: "I spent 3 hours figuring out how BigQuery inserts, deletes and updates data internally. Here's what I found."
channel: vutr
author: "Vu Trinh"
published: 2024-02-17
url: https://vutr.substack.com/p/i-spent-3-hours-trying-to-figure
paid: false
topics: ["Data Engineering", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Streaming"]
tags: [https, auto, storage, bigquery, image, files]
---

# I spent 3 hours figuring out how BigQuery inserts, deletes and updates data internally. Here's what I found.

*"Just open the file and modify the data, ... No?"*

> Source: [Open post](https://vutr.substack.com/p/i-spent-3-hours-trying-to-figure)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!7D_K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F288473f7-d1b6-4853-94d2-1c94f2a75241_1397x994.png)](https://substackcdn.com/image/fetch/$s_!7D_K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F288473f7-d1b6-4853-94d2-1c94f2a75241_1397x994.png)

Image created by the author

---

## Intro

In BigQuery, you can do these things with SQL:

* Load data using the `INSERT` statement.
* Update data using the `MERGE` statement in BigQuery.
* Delete data using the `DELETE` statement in BigQuery.

Besides SQL, you can also use other ways to interact with the data in BigQuery. All the approaches are all straightforward to the user. But have you ever wondered how BigQuery executes these operations under the hood?

If yes, then this article is for you.

*This article is my note on the section Architecture of BigQuery - Storage from [the book Google BigQuery: The Definitive Guide: Data Warehousing, Analytics, and Machine Learning at Scale - 2019](https://www.amazon.com/Google-BigQuery-Definitive-Warehousing-Analytics/dp/1492044466).*

## Background info before we get started

When you load data into BigQuery, it will be stored on [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system) - Google’s scalable storage system; after data is written to the file, it can never be modified again - another way to say that the files are immutable.

This makes it easy to parallelize the processing because we just need to send a copy of the data files to workers without worrying about the data being modified somewhere. (If the file can be modified, guarantee the data consistency between… 100 workers is a nightmare !!)

The immutability also makes some optimization more “convenient“; for example, an OLAP storage database usually maintains metadata like the min-max of the data chunks, which will be used for filtering unnecessary data files. If the system allows modified data after initial writing, it will need to re-calculate the min-max whenever the modification happens; this will slow down the whole operation of the OLAP system.

Moreover, the immutability leads to the fact that every table’s modification will result in whole new files, making features like Data Snapshot, Time Travel, and Data Cloning easier to implement. Other cloud data warehouses like Snowflake, Databricks, and Redshift also operate based on the immutability of the data storage.

Now, after getting the background information, let’s move on to understand how inserts, deletes, and updates are implemented in BigQuery.

---

## The storage set

BigQuery doesn’t treat each file as an atomic unit of data; instead, it has an abstraction called a storage set.

A storage set is created in response to a load job, streaming job, or Data Manipulation Language (DML) query.

> *A transaction will modify the table’s data by creating a new set of files (due to immutability); these files will belong to a storage set. **This means the storage sets are also immutable.***

[![](https://substackcdn.com/image/fetch/$s_!iOuz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb95bf775-3970-4926-9c54-7c91d2940d13_975x440.png)](https://substackcdn.com/image/fetch/$s_!iOuz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb95bf775-3970-4926-9c54-7c91d2940d13_975x440.png)

Image created by the author

Storage sets enable modification to BigQuery to guarantee the ACID constraint.

This means they are ***Atomic*** (all or nothing), ***Consistent*** (after they commit, they are available everywhere), ***Isolation*** (transactions can be executed independently), and ***Durable*** (the transaction won’t be lost after committing).

Storage set has a life cycle, which first is the `PENDING` state, progresses to the `COMMITTED` state after finishing the file writing process, and finally moves to `GARBAGE` whenever the storage set is no longer needed; mark the storage set ready for the garbage collector.

If a storage set has data being written to it, this storage set’s data won’t ever be visible to the users. Only when it reaches the `COMMITTED` state will the data be available.

[![](https://substackcdn.com/image/fetch/$s_!lSlB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe990b7a8-08ab-46e4-a9f6-16e6f7d40ccd_1046x288.png)](https://substackcdn.com/image/fetch/$s_!lSlB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe990b7a8-08ab-46e4-a9f6-16e6f7d40ccd_1046x288.png)

Image created by the author

Storage sets also have size information, which is how a dry run can determine how much data would be scanned without running a query.

[![](https://substackcdn.com/image/fetch/$s_!xUg5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd21c8cf8-d1fd-42b0-8598-f89dc852bfbb_282x41.png)](https://substackcdn.com/image/fetch/$s_!xUg5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd21c8cf8-d1fd-42b0-8598-f89dc852bfbb_282x41.png)

The dry run shows how much data for my random query.

---

## INSERT, UPDATE, and DELETE

> *Whole new files.*

### INSERT

When an `INSERT` operation is executed, the data will be written in a new set of files in the storage; these files will belong to a new storage set, which will be added to the metadata (this metadata has some information like the committed timestamp of the storage set, which files belong to this storage set, which storage sets belong to a table,…)

[![](https://substackcdn.com/image/fetch/$s_!lmg_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fbd8697-a8d3-4c6c-aecf-c287c8b0775d_780x441.png)](https://substackcdn.com/image/fetch/$s_!lmg_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fbd8697-a8d3-4c6c-aecf-c287c8b0775d_780x441.png)

Image created by the author

### DELETE

Removing rows from the table (from the data files physically) is more complicated than the `INSERT` operation. Because files are immutable, the system can not open the file and discard the desired rows from it. Let’s go through the `DELETE` operation with an illustration below:

[![](https://substackcdn.com/image/fetch/$s_!vuPT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f9b8dfa-9281-46c5-ae6a-e803fa3b7394_766x441.png)](https://substackcdn.com/image/fetch/$s_!vuPT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f9b8dfa-9281-46c5-ae6a-e803fa3b7394_766x441.png)

Image created by the author

1. Assume you want to delete the record where id = `ABC` and this record exists in file `Z`; file `Z` belongs to the storage set 1 along with files `X` and `Y`.
2. To execute the delete operation, the system will create a new file `Z2` with the same data as file `Z` except for the record with id = `ABC`. The file `Z2` will belong to the new storage set 2.
3. Storage set 2 must also point to files `X` and `Y` except for file `Z`.
4. Finally, storage set 1 will marked `GARBAGE.`

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

### UPDATE

`UPDATE` is implemented as the combination of `INSERT` and `DELETE` operations. Instead of updating the record directly into a file, the system will create a new file with the latest version of that record and delete the old file.

### **Storage optimization**

> *The compact process*

The storage fragmentation can happen when you write or update data over time.

Suppose you write 200 kb of data every two minutes into BigQuery. Each 200 kb will get a storage set and its own file. (I can’t find the maximum file size in BigQuery storage). After a month, you’ll have 4 TB of data, which is not much when putting it into a cloud data warehouse like BigQuery. However, this will result in a lot of files and storage sets, which will undoubtedly harm the query performance because BigQuery needs to spend time operating on many files and its associated metadata.

To overcome this challenge, the storage optimizer will re-arrange data files into a more optimal form for data reading. This process is automatically run behind the scenes. The optimizer will periodically re-write the file. The data can be written into many files based on the user's request; then, it will try to compact the data into larger files.

Let's check the following illustration for a better understanding.

[![](https://substackcdn.com/image/fetch/$s_!_V1o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb6235d4-c573-4be4-b8ab-50c9b5ca69bf_455x557.png)](https://substackcdn.com/image/fetch/$s_!_V1o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb6235d4-c573-4be4-b8ab-50c9b5ca69bf_455x557.png)

Image created by the author

---

## Partitioning

[Partitioning is BigQuery’s optimized technique that divides a large table into smaller parts called “partitions“](https://cloud.google.com/bigquery/docs/partitioned-tables). Based on the query’s filter, the system only needs to read the required files and skip all the irrelevant files.

For example, if you need data from `2024-01-01` to `2024-01-15` and your data is partitioned on the date column, only those files belonging to partitions `2024-01-01` to `2024-01-15` need to be brought up.

Internally, a partition is nothing like a table. Data from a partition will be stored separately from other partitions. This allows features like data expiration, data insertion, and data deletion to be executed effectively on partition granularity (because it’s just like a table).

At the time of writing this, [BigQuery limits the number of partitions per table to 4000](https://cloud.google.com/bigquery/docs/partitioned-tables#ingestion_time). Over-partition (which leads to the table being physically divided into multiple partitions) will affect the performance. The more partitions you have, the more metadata it produces, which causes the query optimizer to struggle when reading many metadata files.

BigQuery uses storage sets that have associated partition IDs to represent partitions in the metadata. This way, BigQuery can apply the filter at the metadata layer without opening the physical data. Let’s check another illustration here:

[![](https://substackcdn.com/image/fetch/$s_!7g5f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf9a7c36-f289-4f8c-9015-be6fba7b3172_873x406.png)](https://substackcdn.com/image/fetch/$s_!7g5f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf9a7c36-f289-4f8c-9015-be6fba7b3172_873x406.png)

Image created by the author

---

## Clustering

Besides partitioning, BigQuery also exposes another optimized technique that allows users to control how data will be stored internally.

It is clustering. Clustering is a feature that stores the data that will be semi-sorted based on a key from single or multiple columns ([max is four based on the documentation](https://cloud.google.com/bigquery/docs/clustered-tables#limitations)). Data files will get non-overlapping ranges of the key space. This allows for efficient lookups and range scans because the query engine only needs to open files with the key.

[![](https://substackcdn.com/image/fetch/$s_!u08B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e2afdea-e4ae-493a-a442-bd35bfc73130_480x464.png)](https://substackcdn.com/image/fetch/$s_!u08B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e2afdea-e4ae-493a-a442-bd35bfc73130_480x464.png)

Image created by the author

### Re-clustering

Because the data need to be maintained in some order (cluster), when new data arrives, this possibly causes data to be distributed into overlapping key ranges and affects the clustering characteristic of the data.

To solve this problem, BigQuery lets users write data as they need; the data will be written to new files as usual, and the data will be re-clustered periodically in the background.

To decide when to re-clustering, BigQuery maintains a ratio called clustering ratio, which indicates the fraction of the completely clustered data; if the ratio drops too low, it will rewrite the data in a sorted format. This will be done on the new storage set (storage set is the atomic unit of data, remember?). BigQuery automatically handles the re-clustering; users don’t need to worry about this.

One more illustration to clear the idea:

[![](https://substackcdn.com/image/fetch/$s_!WO3l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c6842b2-d55e-4d47-99dd-c1369a5056b3_670x447.png)](https://substackcdn.com/image/fetch/$s_!WO3l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c6842b2-d55e-4d47-99dd-c1369a5056b3_670x447.png)

Image created by the author

---

## **Time travel**

[BigQuery supports time travel for configurable intervals (a minimum of two days to a maximum of seven days)](https://cloud.google.com/bigquery/docs/time-travel#time_travel). This feature allows you to revisit the past state of the table at any point within that time window.

[![](https://substackcdn.com/image/fetch/$s_!gQuB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80e774e1-fcfd-416f-be1a-66e64902153f_455x337.png)](https://substackcdn.com/image/fetch/$s_!gQuB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80e774e1-fcfd-416f-be1a-66e64902153f_455x337.png)

Image created by the author

This can be useful if you accidentally delete data and want to restore it. It is also helpful in debugging scenarios when you want to check the table’s data before some transformation has already been applied. To enable time travel, BigQuery keeps track of the timestamp at which storage set transitions happen.

---

## Outro

From the article, I’ve just given you guys a glimpse into how data operations are handled physically inside BigQuery.

The key here is the immutability of the data files, which is entirely different from traditional OLTP databases, in which files can be modified after being written.

Thank you for reading this far. See you in my future blog.

---

***Reference**: [Book: Google BigQuery: The Definitive Guide: Data Warehousing, Analytics, and Machine Learning at Scale - 2019](https://www.amazon.com/Google-BigQuery-Definitive-Warehousing-Analytics/dp/1492044466), section Architecture of BigQuery - Storage.*

---

## Before you leave

I’m launching a referral program to grow the community by giving you guys valuable gifts whenever you reach a referral milestone. The condition is simple: you refer friends to subscribe to my newsletter, and you will receive a gift based on the number of friends you refer. Here are the reward milestones:

[![](https://substackcdn.com/image/fetch/$s_!lf_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)](https://substackcdn.com/image/fetch/$s_!lf_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)

Now, let’s refer friends and claim exciting rewards ;)

[Refer a friend](https://vutr.substack.com/leaderboard?&referrer_token=1xrjxy&utm_source=post)

---

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-3-hours-trying-to-figure/comments)

It might take 3 minutes to read, but it took me more than three days to prepare, so it will motivate me greatly if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
