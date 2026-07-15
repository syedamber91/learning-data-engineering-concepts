---
title: "OLTP vs OLAP: Making changes to the data"
channel: vutr
author: "Vu Trinh"
published: 2025-09-30
url: https://vutr.substack.com/p/oltp-vs-olap-making-changes-to-the
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Governance"]
tags: [https, auto, fetch, substackcdn, image, good]
---

# OLTP vs OLAP: Making changes to the data

*In just 15 minutes, you will understand the difference in how they handle writing, updating and deleting the data*

> Source: [Open post](https://vutr.substack.com/p/oltp-vs-olap-making-changes-to-the)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-governance|Data Governance]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=173554718)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!1kwp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2f54049-4c06-4a0e-9568-1eedca4ee653_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!1kwp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2f54049-4c06-4a0e-9568-1eedca4ee653_2000x1428.png)

---

## Intro

Business users need to observe what is actually happening. When does the user buy a book? When a driver finishes the trip. Why don't users use this feature, and how does a competitor win that market?

We, as data engineers, collect, store, and prepare data to help them achieve that purpose. However, the data is not static; it is added, updated, and deleted to align with real-life events. Handling data changes is crucial.

In this article, we will see how OLTP and OLAP relational databases handle data mutation.

> *Since the physical data mutation is implemented differently depending on the database, this article presents only the idea of common approaches. For a detailed implementation of the database, refer to its official documentation.*

## OLTP

OLTP systems primarily handle ingesting new information; their data operations typically read/write/update a small amount of data each time. They power everything from ATM transactions and e-commerce orders to inventory management.

[![](https://substackcdn.com/image/fetch/$s_!eGIG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5bfa440-4a1b-4a77-9b6a-3429dfee4db1_560x332.png)](https://substackcdn.com/image/fetch/$s_!eGIG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5bfa440-4a1b-4a77-9b6a-3429dfee4db1_560x332.png)

Their primary objectives (not comprehensive) are:

* **High Concurrency:** To support thousands of users and processes simultaneously reading and writing data without interfering with each other.
* **High Throughput for Writes:** To quickly process a large volume of minor, frequent updates, inserts, and deletes.

So, the way they manage the data changes is optimized for a small number of rows. From the [previous article](https://open.substack.com/pub/vutr/p/oltp-vs-olap-data-format-and-indexing?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false), we know that most OLTP systems manage data in a row-store format. In more detail, an OLTP relational system, like PostgreSQL, stores row data side by side in pages

## Page

A **database page** is a unit of storage created and managed by the database software itself. This is different from the disk page, which is a unit of storage managed by the disk hardware.

[![](https://substackcdn.com/image/fetch/$s_!YeS3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F657fa26f-d2d3-4c23-9c8e-5bf61efc2c93_442x292.png)](https://substackcdn.com/image/fetch/$s_!YeS3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F657fa26f-d2d3-4c23-9c8e-5bf61efc2c93_442x292.png)

A database page is the fundamental unit of I/O for a DBMS. When the database needs to read data, it doesn’t fetch a single row from the disk; it reads the **entire page** containing that row into memory. Likewise, when it writes data, it writes the whole modified page back to disk.

[![](https://substackcdn.com/image/fetch/$s_!0gio!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9347a20-e2b4-4dc6-b978-0d47be1db512_698x364.png)](https://substackcdn.com/image/fetch/$s_!0gio!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9347a20-e2b4-4dc6-b978-0d47be1db512_698x364.png)

The page’s size varies depending on the database. It is typically a multiple of the disk block size, e.g., **8 KB** in PostgreSQL. A page contains metadata, actual data, or indexes, and usually it doesn’t include a mix of data types (e.g., a page for data only or a page of indexes only). Each page will have a unique identifier from the database. There is mapping (depending on the database implementation) to help the database find the physical location of a page.

Typically, pages are organized in heap files, which store a set of pages in random order. The database also has a mechanism to determine the number of pages in a file and which one still has available space to store more data (it is a special page called a directory page, but we won’t discuss it in more detail here).

Keep in mind that the smallest unit of read and write is a page. Next, we will examine how data is organized on a page and explore how data mutation works.

## Tuple-oriented

The common sense “storing the row data right next to each other “ usually makes us think rows (tuples) are simply appended from the beginning to the end. In fact, there is a more robust scheme to store data. Most SQL OLTP databases use the **slotted page (**here are the details from [PostgreSQL](https://www.postgresql.org/docs/current/storage-page-layout.html)**).** It’s a fixed-size page with four main areas: the header, the slot array, the free space, and the data area:

* Tuples will be first added at the end of the page and stacked toward the beginning of the page. Tuples can vary in size. Each will have a unique identifier and a header. Metadata, such as the map for null values or information used for transaction and concurrency control, is stored in the header. The space where tuples reside is typically referred to as the **data area**.

  [![](https://substackcdn.com/image/fetch/$s_!3wWp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08206dd5-54fa-4352-80b5-6bb951dd5f80_436x354.png)](https://substackcdn.com/image/fetch/$s_!3wWp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08206dd5-54fa-4352-80b5-6bb951dd5f80_436x354.png)
* At the beginning of the page, there is a **header**. It contains metadata about the page, which allows the DBMS to quickly understand the page’s contents without scanning the data. Key metadata includes the number of slots currently in use in the slot array, pointers to the end and start of free space, ...

  [![](https://substackcdn.com/image/fetch/$s_!_aRd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ec9056-876d-45da-aaf9-807640c7c2c5_414x344.png)](https://substackcdn.com/image/fetch/$s_!_aRd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ec9056-876d-45da-aaf9-807640c7c2c5_414x344.png)
* Then comes the **slot array**. Each contains the pointer to the beginning of an associated row in that page. In contrast to the data, a slot array will be added as an item and grow toward the end of the page.

  [![](https://substackcdn.com/image/fetch/$s_!gae6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90bc6600-1bb0-48b6-bcaa-addb9e6265b0_424x350.png)](https://substackcdn.com/image/fetch/$s_!gae6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90bc6600-1bb0-48b6-bcaa-addb9e6265b0_424x350.png)
* The space between the data and the slot array is free space for new data. As new tuples are inserted, a new slot is added to the slot array, and the tuple data is added to the data area, causing the free space to shrink from both sides. A page is considered full when the slot array and the data area meet.

  [![](https://substackcdn.com/image/fetch/$s_!ipOK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6ed0680-7e95-46f1-87ab-310e2bf9c869_408x358.png)](https://substackcdn.com/image/fetch/$s_!ipOK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6ed0680-7e95-46f1-87ab-310e2bf9c869_408x358.png)

What is the motivation behind this design? We don’t just append the data from the beginning to the end. Its main advantage is the ability to separate the logical (slot) and physical addresses of the tuples.

* A row (tuple)’s unique address of a record (commonly referred to as Record Identifier (**RID**)) is not its physical byte offset. Instead, it is a composite key ⟨Page ID, Slot Index⟩. (Database can use indexes such as B+Tree to help find the RID faster.)

  [![](https://substackcdn.com/image/fetch/$s_!PEQp!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d9fa71-cebe-4572-8138-2f475608740d_974x342.png)](https://substackcdn.com/image/fetch/$s_!PEQp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88d9fa71-cebe-4572-8138-2f475608740d_974x342.png)
* The PageID directs the DBMS to the correct page on disk, and the SlotIndex (or slot number) provides an index into the Slot Array on that page. The slot provides the final pointer to the record’s *current* physical location within the data area.
* This allows the DBMS to move record data freely within the page

  [![](https://substackcdn.com/image/fetch/$s_!myYi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdb522f2-8f4a-4b0e-8666-665c3617316e_830x584.png)](https://substackcdn.com/image/fetch/$s_!myYi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdb522f2-8f4a-4b0e-8666-665c3617316e_830x584.png)
* For example, when compacting the data to reclaim free space, the data needs to be moved; the only update required is to the pointers (that pointed to the physical location of the data) stored in the slots themselves.
* External structures (e.g., indexes) can retain these stable RIDs without concern that they will become invalid when the physical data is reorganized.

  > ***Note**: the data reorganization is inevitable, as data rows can be deleted at any time, and free space needs to be reclaimed to prevent fragmentation.*
* If a DBMS uses the physical location of the tuple for the RID, it must frequently update the RID whenever the data is moved, which is clearly inefficient.

After knowing how the data is stored in a slotted page, let’s find out how the data mutation is implemented.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=173554718)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

> ***Note**: To ensure [isolation with MVCC](https://vutr.substack.com/i/167820093/snapshot-isolation-si), data mutations, such as updates, are still attempted to maintain the previous state of the data in most OLTP SQL databases. For example, [PostgreSQL](https://cloud.google.com/blog/products/databases/deep-dive-into-postgresql-vacuum-garbage-collector)’s UPDATE query retains the existing row version and creates a new version with the updated data. With the DELETE operation, the affected row will be marked as “deleted, “ but it will not be physically removed. The inactive record will be garbage collected later (e.g., PostgreSQL’s [VACUUM process](https://cloud.google.com/blog/products/databases/deep-dive-into-postgresql-vacuum-garbage-collector))*
>
> *The idea of MVCC is straightforward: each read transaction reads a consistent snapshot of the database. The transaction will only see all the changes that were committed before the start of this transaction. All changes from other ongoing transactions that are uncommitted will be ignored.*

### Slotted-page: insertion

[![](https://substackcdn.com/image/fetch/$s_!KGcQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a7d9f7-ca85-4970-b7ff-89b3bde36495_806x406.png)](https://substackcdn.com/image/fetch/$s_!KGcQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a7d9f7-ca85-4970-b7ff-89b3bde36495_806x406.png)

1. **Check for available space:** The system first checks the page header to determine the amount of available free space. The required space must accommodate both the new data record and a new entry in the slot array.
2. **Allocate a new slot:** If there is enough space, a new entry is added to the end of the slot array. This new slot will store the offset (the starting position) and the length of the data record.
3. **Write the Data:** The new data record is written into the free space. To maintain contiguity of the free space, the data is typically added at the end of the data area, growing backward from the end of the page. There is metadata to tell the system that this record is “active“.
4. **Update the Slot:** The position of the newly written data are recorded in the newly allocated slot in the slot array.
5. **Update the Page Header:** Finally, the metadata in the page header is updated.

### Slotted-page: deletion

[![](https://substackcdn.com/image/fetch/$s_!kEyt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfab7a7e-c773-4629-bb2e-46fe316beba7_614x360.png)](https://substackcdn.com/image/fetch/$s_!kEyt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfab7a7e-c773-4629-bb2e-46fe316beba7_614x360.png)

1. **Locate the Record:** The system uses the Record Identifier (**RID**) to find the page and the corresponding slot in the slot array. This slot points to the *current active version* of the record.
2. **Mark Version as Deleted:** The system does **not** remove the data. Instead, it finds the data record on the page and updates its header with the metadata to notify the system that it is an “inactive“ row.

### Slotted-page: updating

[![](https://substackcdn.com/image/fetch/$s_!qcP3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e301257-b35b-44cd-a384-8899ec3ad8df_728x496.png)](https://substackcdn.com/image/fetch/$s_!qcP3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e301257-b35b-44cd-a384-8899ec3ad8df_728x496.png)

An UPDATE is treated as a DELETE of the old version and an INSERT of the new one.

* **Locate the Old Version:** The system finds the current live version of the record using the RID.
* **Mark Old Version as Inactive:** The metadata of the old version is updated to mark it “inactive.” (Like the deletion)
* **Insert the New Version:** A completely new version of the record, containing the updated data, is inserted onto the page following the standard insertion process. It has the metadata to mark it as “active”. If the new version cannot fit on the page, it will be written on a different page.
* **Update the Slot:** The original slot in the slot array is now updated to point to the offset of the newly inserted version.

## Log-structured storage

Besides the slotted page scheme above, there is a common approach to organizing data on a page called log-structured storage. However, it is less commonly seen in relational databases such as PostgreSQL or MySQL. It’s widely implemented in key-value (e.g., RocksDB) or NoSQL databases (e.g., Cassandra)

That said, it is still worth our time to examine it, as more OLAP systems (e.g., [BigQuery](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/), [Apache Hudi](https://hudi.apache.org/blog/2025/05/29/lsm-timeline/), [Apache Paimon](https://paimon.apache.org/docs/1.2/primary-key-table/overview/), or [RisingWave](https://tutorials.risingwave.com/docs/design/state/)) or modern OLTP systems (e.g., [Neon](https://neon.com/blog/get-page-at-lsn)) have implemented this approach due to high-throughput write performance.

> ***Note:** Within the scope of this article, we will only examine the high-level aspects of this approach; its details will be discussed in another article.*

The approach was first introduced as [a log-structured merge tree (LSM Tree) in 1996](https://dsf.berkeley.edu/cs286/papers/lsm-acta1996.pdf). It is based on a philosophy: all changes—be they insertions, updates, or deletions—are handled by appending new records to a sequential log.

[![](https://substackcdn.com/image/fetch/$s_!pks1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdd70205-2dab-40e5-bfb8-e098eb9b18ff_464x390.png)](https://substackcdn.com/image/fetch/$s_!pks1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdd70205-2dab-40e5-bfb8-e098eb9b18ff_464x390.png)

In a slotted page discussed above, every data operation must involve locating the page that contains the data. The log-structured storage doesn’t need to do that. **To add a new row,** we write at the end of the log. **To update a row**, we don’t find the old entry and write a new version. We write at the end of the log. For deletion, we also write at the end of the log to mark a row as deleted (tombstone).

The key is “the end of the log“

Every operation involves appending an entry at the end of the log (file). No more finding (like on a slotted page); just sequential write to the file, so the writes are fast.

Take a closer look at its implementation; it has components in both memory (RAM) and on disk.

* **Memtable** (In-Memory): This is a sorted data structure living entirely in fast RAM (e.g., a balanced binary tree or skip list). All new writes (inserts, updates, and deletes) should go here first. Every record will have a key, which is used for sorting and data modification (via the compact process, which is discussed right above)

  [![](https://substackcdn.com/image/fetch/$s_!PPAs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1a64b69-49f2-4220-a317-529587121e52_514x252.png)](https://substackcdn.com/image/fetch/$s_!PPAs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1a64b69-49f2-4220-a317-529587121e52_514x252.png)
* Because it’s in memory, writing to it is super fast.
* SSTable (Sorted String Table) (On-Disk):

  + When the Memtable grows to a specific size, it gets written to disk.

    [![](https://substackcdn.com/image/fetch/$s_!Nuyt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e29d552-ad9f-47f4-bf8a-196d7f7ad197_278x358.png)](https://substackcdn.com/image/fetch/$s_!Nuyt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e29d552-ad9f-47f4-bf8a-196d7f7ad197_278x358.png)
  + The data from the Memtable is written out as a new, **immutable (read-only)**, sorted file called an SSTable.
  + These SSTables are then later compacted on disk to produce larger SSTables. This improves the read performance.

    [![](https://substackcdn.com/image/fetch/$s_!KKf8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e155b58-d41c-40ea-82f8-893fb5809342_548x360.png)](https://substackcdn.com/image/fetch/$s_!KKf8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e155b58-d41c-40ea-82f8-893fb5809342_548x360.png)
  + Because the data is already sorted in memory, compacting these SSTables can be achieved using the [sort-merge algorithm](https://en.wikipedia.org/wiki/Merge_sort).
  + After the compaction, only the latest value is preserved. This is how data mutation implementation is in this approach. Tombstone values and old values of the updated key will be discarded

    [![](https://substackcdn.com/image/fetch/$s_!iBD7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a523cf-6623-43f9-8d40-5cfac0289214_860x368.png)](https://substackcdn.com/image/fetch/$s_!iBD7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a523cf-6623-43f9-8d40-5cfac0289214_860x368.png)

The trade-offs for high-throughput writes are that the system has more work to do later. The compact process must happen to ensure the read performance. Read operations could be slower compared to the slotted page approach (with an index like B+Tree), as the client might need to perform the read in multiple places (the Memtable in memory and the SSTables on disk)

As I mentioned, a future article will discuss this approach in more detail.

## OLAP

The storage layer of the OLAP systems is typically built on immutable storage systems, such as public object storage services (e.g., Amazon S3 or Google Cloud Storage), HDFS, or internal solutions like [Google Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system).

That said, modern cloud data warehouses, such as Google BigQuery, Snowflake, and Databricks, as well as open-source table formats like Iceberg, Hudi, and Delta Lake, are built around a fundamental principle that sets them apart from traditional transactional databases:

When data is written, it is immutable.

Unlike OTLP systems that handle frequent, minor updates, OLAP thrives on a stable foundation of historical records. Data immutability ensures that the data being analyzed is a consistent and unchangeable record of past events. It also provides the following advantages:

* **Simplified Concurrency:** With immutable data, a query can operate on a consistent snapshot of the data (simplify the MVCC implementation) at a particular point in time, without being affected by concurrent write operations that are creating new versions of the data. Many clients can read the query with concern about race conditions.
* **Time travel and Data Governance:** Immutable data powered the “time travel” ability. Since old versions of the data are preserved, users can:

  + **Audit and Reproduce:** Easily audit data changes and reproduce the “bug“with the exact data that was used at a previous time.
  + **Recover from Errors:** Quickly recover from accidental data modifications or deletions by simply querying the data from a time before the error occurred and restoring it.

So, data is organized in immutable files. How did we modify it? There are two main approaches, all of which, of course, rely on writing new data for modification: the copy-on-write and merge-on-read.

### Copy on write

The Copy-on-Write (CoW) strategy prioritizes the performance and simplicity of read operations.

[![](https://substackcdn.com/image/fetch/$s_!Susn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5513b692-307e-4f10-a3a3-75a2188d0971_814x486.png)](https://substackcdn.com/image/fetch/$s_!Susn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5513b692-307e-4f10-a3a3-75a2188d0971_814x486.png)

Any modification, UPDATE, or DELETE is executed through atomic file replacement. The system identifies all data files that contain rows affected by the operation. It then reads these files, applies the required changes in memory, and writes out entirely new versions of those files.

[![](https://substackcdn.com/image/fetch/$s_!CZSU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f99a126-26b0-418f-88ef-f84f9f348e0b_550x506.png)](https://substackcdn.com/image/fetch/$s_!CZSU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f99a126-26b0-418f-88ef-f84f9f348e0b_550x506.png)

The final step is to commit the metadata to say something like this: “For the latest version of the table, please refer to these newly created files.” The old files are still retained for a period so they can be referenced within the snapshot of the older table. Then, they will be garbage collected to free up storage.

The primary motivation for choosing a CoW strategy is to optimize the read path:

* Because all changes are fully materialized during the write process, read queries do not need to perform any reconciliation of changes (clients need to open and read only the data files).

  [![](https://substackcdn.com/image/fetch/$s_!XI4_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bfc28e7-c9af-432b-be88-5a1b97045c35_442x206.png)](https://substackcdn.com/image/fetch/$s_!XI4_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bfc28e7-c9af-432b-be88-5a1b97045c35_442x206.png)
* The physical layout of a CoW table is straightforward. At any table’s snapshot, the table is represented by a set of data files. There are no extra changes or deleted files to manage.

In return, it has the high cost of writing:

* Small changes (e.g., three records) could force the system to rewrite the files with thousands of records to reflect the change.

  [![](https://substackcdn.com/image/fetch/$s_!Ud63!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b3be438-0907-40a0-9903-91b98035af80_704x200.png)](https://substackcdn.com/image/fetch/$s_!Ud63!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b3be438-0907-40a0-9903-91b98035af80_704x200.png)
* The process of reading, modifying, and rewriting files is inherently slow; the write operations will have higher latency.

  [![](https://substackcdn.com/image/fetch/$s_!NusG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88616065-2e5a-4638-9fd8-19ba680af544_820x338.png)](https://substackcdn.com/image/fetch/$s_!NusG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88616065-2e5a-4638-9fd8-19ba680af544_820x338.png)
* Essentially, when rewriting the data, we keep double the storage space for that file. Although a garbage collection process eventually removes the old files, the period before this cleanup can lead to substantial storage bloat.

  [![](https://substackcdn.com/image/fetch/$s_!5QL_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15c1adf8-a0e4-4b94-b04a-31f57205dd87_340x322.png)](https://substackcdn.com/image/fetch/$s_!5QL_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15c1adf8-a0e4-4b94-b04a-31f57205dd87_340x322.png)

That said, this strategy is ideal for read-heavy or infrequently changing workloads.

### Merge on read

The merge-on-read (MoR) strategy prioritizes write performance and low ingestion latency. It simply says: “If you have changes, write those to separate files; the reconciliation will happen later.“

[![](https://substackcdn.com/image/fetch/$s_!pCu5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5975ea4-5a5a-4067-9f62-ca921bc92439_670x392.png)](https://substackcdn.com/image/fetch/$s_!pCu5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5975ea4-5a5a-4067-9f62-ca921bc92439_670x392.png)

It avoids the rewriting of data files during a write operation. Instead, incoming changes—updates, inserts, and deletes—are recorded in separate and smaller files. (Fewer things to write make the writing faster). Then, the writer will commit metadata to “register“ these change files for the latest table’s snapshot.

[![](https://substackcdn.com/image/fetch/$s_!42Sm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5498bb0e-4241-4861-a737-fcfd46952faa_382x350.png)](https://substackcdn.com/image/fetch/$s_!42Sm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5498bb0e-4241-4861-a737-fcfd46952faa_382x350.png)

The actual “merge” of these changes with the data files is postponed until a query is executed. At that time, the query engine is responsible for combining the base data files with the relevant change files to construct the latest view of the table.

[![](https://substackcdn.com/image/fetch/$s_!fZIu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65d72aed-dc04-491a-b4b6-1a1b313cfde6_860x254.png)](https://substackcdn.com/image/fetch/$s_!fZIu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65d72aed-dc04-491a-b4b6-1a1b313cfde6_860x254.png)

To ease the burden for the reader, there is a separate process called “compaction“. It asynchronously consolidates changes from the change files into the data files, providing complete views of the table for readers. The merge process no longer needs to occur at read time (although it still must happen somewhere).

[![](https://substackcdn.com/image/fetch/$s_!CuO_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68bfa3d8-f7a8-487c-aed1-bf08c309005d_888x530.png)](https://substackcdn.com/image/fetch/$s_!CuO_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68bfa3d8-f7a8-487c-aed1-bf08c309005d_888x530.png)

As mentioned, MoR is optimized for the write path. Writing changes to small files is orders of magnitude faster than rewriting large data files. This leads to lower write latency compared to CoW. However, it has several disadvantages.

* More work to do later: the merge process must happen in the compaction process, or when the clients read the table. If the files are already compacted, the read performance will not be affected. However, if the compaction did not occur at the right time, the read clients must merge the files on their own, which makes the read slower compared to CoW.
* Users must manage another component, the compaction process. It must be scheduled, monitored, and tuned correctly. A poorly configured compaction strategy can result in a significant backlog of change files, negatively impacting read performance. In contrast, an overly aggressive strategy can consume more compute resources and interfere with the main data ingestion pipelines.

## Outro

In this article, we first explore the standard approach for organizing row data in an OLTP system, the slotted page. The process of modifying the data in this slotted page involves locating the page, making the adjustment (inserting the new version or marking the current row as “inactive“), and then updating the slot page. Next, we have a high-level overview of log-structured storage. Unlike the slotted page, data modification always involves appending a new log record; a merge process will be used to update the data later, keeping only the latest version.

Then, we come to OLAP systems, which are based on the principle of data immutability. There are two approaches to make changes to the data. The CoW is optimized for read, but sacrifices the write performance when it needs to rewrite the whole file. The MoR, on the other hand, optimizes for write operations, but the “merge“ processes must happen later to ensure the read performance.

Thank you for reading this far. See you in my next article.

## Reference

*[1] Ken Wagatsuma, [Slotted Pages: The Backbone of PostgreSQL’s Data Storage](https://kenwagatsuma.com/blog/postgresql-slotted-pages), 2025*

*[2] Martin Kleppmann, [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/), 2017*

*[3] Andy Pavlo, [Database Storage: Files & Pages (CMU Intro to Database Systems)](https://www.youtube.com/watch?v=dSxV5Sob5V8&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq), 2024*

*[4] Andy Pavlo, [Database Storage: Log-Structured Merge Trees & Tuples (CMU Intro to Database Systems)](https://www.youtube.com/watch?v=IHtVWGhG0Xg&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=6), 2024*
