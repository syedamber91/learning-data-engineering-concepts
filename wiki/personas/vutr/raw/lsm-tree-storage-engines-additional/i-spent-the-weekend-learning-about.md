---
title: "I spent the weekend learning about one of the most iconic database storage engines."
channel: vutr
author: "Vu Trinh"
published: 2025-11-18
url: https://vutr.substack.com/p/i-spent-the-weekend-learning-about
paid: true
topics: ["Data Engineering", "Apache Kafka", "BigQuery", "Streaming", "Batch Processing", "Change Data Capture", "ETL"]
tags: [https, auto, media, substackcdn, image, fetch]
---

# I spent the weekend learning about one of the most iconic database storage engines.

*The one once common in the OLTP world, now gaining more and more adoption in OLAP systems.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-the-weekend-learning-about)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[change-data-capture|Change Data Capture]] · [[etl|ETL]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!g2iA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc146da1-6a56-4127-bc8a-03dcdf712ba2_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!g2iA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc146da1-6a56-4127-bc8a-03dcdf712ba2_2000x1428.png)

---

## Intro

If you work with OLTP databases, a high chance that you’ve heard or even worked with B-Tree, the database storage structure for optimizing query performance in databases like MySQL or PostgreSQL.

It’s excellent at speeding up reads, but the system must perform more work at write time, as it has to locate the data in the B-Tree before making any in-place changes to the entire data page in memory and writing it back to disk, even if the change volume is 1/1000 of the page.

Some workload requires higher throughput data ingestion, such as key-value stores or NoSQL databases. A storage engine, which was first introduced in the 1990s, can offer that.

In this week’s article, we will delve into the Log-Structured Merge-Tree (LSM-tree), the storage engine that supports many popular OLTP databases, such as RocksDB or Cassandra. The cool thing about this engine is that it isn’t exclusively implemented in OLTP databases; many OLAP systems, such as [Clickhouse](https://vutr.substack.com/p/i-spent-8-hours-learning-the-clickhouse?utm_source=publication-search), [BigQuery](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/), [RisingWave](https://risingwave.com/), [Apache Hudi](https://hudi.apache.org/), or [Apache Doris](https://doris.apache.org/blog/Understanding-Data-Compaction-in-3-Minutes), have implemented or inspired the idea of the LSM tree for their storage engine.

We will first explore the LSM architecture (in the simplest way), then break down its pros and cons, and finally try to answer why it is getting more and more preferred in OLAP systems (however, not all OLAP systems will implement it).

## LSM architecture

Essentially, the LSM-tree organizes data into hierarchical levels; from volatile state in memory to its final, immutable state on disk. In practice, data on disk itself is composed of multiple levels of on-disk files.

[![](https://substackcdn.com/image/fetch/$s_!lfwM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9e2db8e-5059-4ef6-87a6-5398c2f0e88b_388x450.png)](https://substackcdn.com/image/fetch/$s_!lfwM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9e2db8e-5059-4ef6-87a6-5398c2f0e88b_388x450.png)

The structure that holds data in memory is usually referred to as the Memtable, and the one on disk is called SSTables. When you write to disk, it can be considered safe; if your machine is down, it won’t affect the data written to disk (unless you burn the hard drive).

However, we can’t claim the same thing for the data that lives in memory. Your machine being down also means that whatever is stored in your memory will be lost too. That said, an LSM implementation typically includes a third component called the Write-Ahead Log, which helps with data durability.

[![](https://substackcdn.com/image/fetch/$s_!rKAy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a00917-f116-4ac7-8362-c42a24ee473c_336x270.png)](https://substackcdn.com/image/fetch/$s_!rKAy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9a00917-f116-4ac7-8362-c42a24ee473c_336x270.png)

### Memtable

A Memtable is simply a write buffer; every data modification must be ingested into this in-memory structure. Unlike what most people think (I used to be one of them), the Memtable is not an append-only log; it is a *sorted* data structure.

[![](https://substackcdn.com/image/fetch/$s_!1YnS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6d2752a-96ca-4204-901c-0af184c1b295_562x224.png)](https://substackcdn.com/image/fetch/$s_!1YnS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6d2752a-96ca-4204-901c-0af184c1b295_562x224.png)

Common data structures used for the Memtable include:

* Skip Lists
* Red-Black Trees
* AVL Trees

The shared properties of these trees are:

* Fast for writes and reads
* Self-balancing; this property contributes to the write and read performance. Read more [here on how the balance is crucial to the tree data structure](https://open.substack.com/pub/vutr/p/what-makes-oltp-databases-so-quick?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false).
* Data will be automatically sorted

Speed is reasonable, as LSM is designed to have high-throughput operations, but you might wonder what data sorting is used for.

An LSM-tree primarily supports data reading via its sorted data. A sorted O(log N) structure allows the database to find WHERE key = ‘user\_123’ by leveraging the binary search. If the data were an unsorted list, it would have to scan the entire data space (O(n)), which might be too slow.

[![](https://substackcdn.com/image/fetch/$s_!a4bi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4430f862-af7f-4398-bd7f-03483aec5f77_470x436.png)](https://substackcdn.com/image/fetch/$s_!a4bi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4430f862-af7f-4398-bd7f-03483aec5f77_470x436.png)

To ensure data is written in sorted order on disk, the most efficient approach is …to have it already sorted. You don't need to sort before or after writing to disk.

The memtable is only a temporary buffer. When it gets full, it will be flushed to SSTables on disk. As discussed, the sorting nature of the Memtable makes the disk writing process seamless; the system writes the Memtable’s contents to a new SSTable file in a single sequential pass.

[![](https://substackcdn.com/image/fetch/$s_!4xa6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01da5997-df26-44b2-91ed-577b2e18acaf_530x450.png)](https://substackcdn.com/image/fetch/$s_!4xa6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01da5997-df26-44b2-91ed-577b2e18acaf_530x450.png)

This is much quicker than random access, especially on disk, which contributes to the high-throughput design of the LSM engine.

### WAL

Data in the Memtable (RAM) could disappear when the machine fails.

[![](https://substackcdn.com/image/fetch/$s_!F_3k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46f9afc5-8a4d-45cb-9d30-fd669cd9ec24_770x548.png)](https://substackcdn.com/image/fetch/$s_!F_3k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46f9afc5-8a4d-45cb-9d30-fd669cd9ec24_770x548.png)

To prevent this, LSM-trees use a Write-Ahead Log (WAL) to provide durability. A quick note here is that WAL is not an exclusive technique in LSM; it is a common approach to ensure durability in the database, including B-Tree.

The WAL is a separate, append-only file that resides on disk. Any operations on the Memtable must be written ahead of time in the WAL.

[![](https://substackcdn.com/image/fetch/$s_!p0M4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89d79fea-db3d-46e2-8acd-01918c71e99a_548x490.png)](https://substackcdn.com/image/fetch/$s_!p0M4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89d79fea-db3d-46e2-8acd-01918c71e99a_548x490.png)

> *That’s why it got the name “Write-Ahead Log“*

Don’t overlook this simple step.

[![](https://substackcdn.com/image/fetch/$s_!_tJc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdaf3bace-a83c-4048-ba27-56bcd5ccfea5_620x398.png)](https://substackcdn.com/image/fetch/$s_!_tJc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdaf3bace-a83c-4048-ba27-56bcd5ccfea5_620x398.png)

When the system crashes, the Memtable data is gone. But that’s ok, data can be refilled by replaying the WAL. This is because the records in the WAL say that: “Hey, here are all the operations we intend to perform on the Memtable.“

### SSTables

SSTables (Sorted String Tables) are the on-disk, persistent, and immutable files used to store most of the data in an LSM-tree. An SSTable is created when a Memtable becomes full and is “flushed” to disk. It can also be produced from other SSTables via compaction processes.

> *SSTables are organized hierarchically; we will delve into this point in the “The compaction process section”. From now on, you only need to know that SSTables will be merged into larger SSTables to ensure optimal read performance and perform clean-up of stale data, such as deleted or updated records.*

[![](https://substackcdn.com/image/fetch/$s_!woD7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1142f4c3-b377-4880-9a75-a428a9a466a5_708x530.png)](https://substackcdn.com/image/fetch/$s_!woD7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1142f4c3-b377-4880-9a75-a428a9a466a5_708x530.png)

SSTables have these defining properties:

[![](https://substackcdn.com/image/fetch/$s_!NCHN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feefe89c7-ed87-4c8f-8602-875dda850ea3_338x266.png)](https://substackcdn.com/image/fetch/$s_!NCHN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feefe89c7-ed87-4c8f-8602-875dda850ea3_338x266.png)

* **Immutable:** Once an SSTable file is written to disk, it is *never* modified. Any modification is handled by writing a *new* record in a *newer* SSTable.
* **Sorted:** The key-value pairs within the file are sorted by key. This is a direct result of flushing the already-sorted Memtable. As mentioned, this property is essential for read operations.

A typical SSTable file consists of two main parts:

[![](https://substackcdn.com/image/fetch/$s_!-AlH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79269858-7ce1-477c-a334-f030d4360c3b_360x208.png)](https://substackcdn.com/image/fetch/$s_!-AlH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79269858-7ce1-477c-a334-f030d4360c3b_360x208.png)

* Data blocks, which contain the key-value pairs
* Index block, which includes a sparse index used to find the correct data block for a given key.

> *Simply said, a sparse index doesn’t provide the location of every single record as the dense index does. Instead, it keeps the location of a record after a predefined records (for example, 8000 rows). This makes the sparse index smaller and can be fitted into memory. The sparse index can only be constructed when the data is sorted.*
>
> [![](https://substackcdn.com/image/fetch/$s_!5Mnv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d8b76a3-c9f1-4290-8345-cd58c074a12a_728x344.png)](https://substackcdn.com/image/fetch/$s_!5Mnv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d8b76a3-c9f1-4290-8345-cd58c074a12a_728x344.png)
>
> *That said, it won’t help the system locate a specific record faster than the dense index, because the sparse index essentially only shows you the range of the data; when reaching the range, you still need to perform a binary search to find the data you want.*

### The writing process

> A quick note: the data must be present in the form of a key-value pair. The key is used for sorting, and the value contains the actual data.

After discovering the main components of the LSM tree, let's move on to its typical write process, which is the primary optimization target of the LSM-tree design:

* **Write to the WAL**: The operation (e.g., INSERT, UPDATE, or DELETE) is serialized and appended to the Write-Ahead Log (WAL) on disk. The system makes sure that data is already persisted on the WAL file before moving on.

  [![](https://substackcdn.com/image/fetch/$s_!e3Pw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0829f9c7-d045-4e55-9203-cfb15104a308_772x274.png)](https://substackcdn.com/image/fetch/$s_!e3Pw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0829f9c7-d045-4e55-9203-cfb15104a308_772x274.png)
* **Write to the Memtable:** Once the WAL write is confirmed, the data is ingested into the active Memtable (the one that still accepts new data). In contrast, the frozen Memtable is the one that doesn’t accept new data and is ready to be flushed to disk.

  [![](https://substackcdn.com/image/fetch/$s_!XXwA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ec80146-2b0e-4f1f-bb01-7881fff30ba9_678x324.png)](https://substackcdn.com/image/fetch/$s_!XXwA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ec80146-2b0e-4f1f-bb01-7881fff30ba9_678x324.png)
* **Return the ACK:** With the data now durable in both WAL and the Memtable, the system sends a success acknowledgement to the client. From the client’s perspective, the write is complete.
* **Flushing to disk:** However, from the LSM perspective, there is a long way to go. Writes continue to accumulate in the active Memtable until it’s full (the definition of “full“ depends on a specific system and can be configurable). When this happens, a flush operation is triggered.

  [![](https://substackcdn.com/image/fetch/$s_!UPqR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8848d85b-8f6c-4a37-8516-df809a6cf8e3_546x606.png)](https://substackcdn.com/image/fetch/$s_!UPqR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8848d85b-8f6c-4a37-8516-df809a6cf8e3_546x606.png)

  + The active Memtable is frozen, meaning it stops accepting new writes and is marked as immutable.
  + A new active Memtable is created to immediately accept new incoming writes, ensuring the continuity of the write path.
  + The system then writes the frozen Memtables to SSTables on disk. Data and index blocks are constructed at this stage.
  + The system will create a new immutable SSTable file on disk.
  + Once data is successfully persisted on disk, associated records on WAL can be dropped to prevent the WAL from growing too big.

Data updating and deleting are also treated as new writes.

When a client issues a `DELETE` operation, the system can’t go to an old SSTable and erase the data. Instead, it performs a **logical delete** by writing a “delete” flag, usually referred to as a **“tombstone”**. This tombstone is simply a key-value pair, where the value is a special flag indicating “deleted.”

[![](https://substackcdn.com/image/fetch/$s_!N47t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa6ec336-8637-4958-a81b-958fac001d15_1064x628.png)](https://substackcdn.com/image/fetch/$s_!N47t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa6ec336-8637-4958-a81b-958fac001d15_1064x628.png)

Regarding the `UPDATE` operation, the engine will write a *new* key-value pair with the same key, a new value, and a more recent timestamp. The previous data is left untouched.

However, there are cases when you need to update or delete the data that is still in the active Memtable; the update and delete will be handled by overwriting the existing keys in the Memtable:

[![](https://substackcdn.com/image/fetch/$s_!13qF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a2ecbf9-f265-4cec-82d4-24fd41af260c_788x500.png)](https://substackcdn.com/image/fetch/$s_!13qF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a2ecbf9-f265-4cec-82d4-24fd41af260c_788x500.png)

This can be done because the Memtable is designed for fast read/write and self-balancing.

### The reading process

To find a given piece of data, the system must search all potential locations in a specific order, from the most recent data to the oldest:

[![](https://substackcdn.com/image/fetch/$s_!Bril!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa67c31ad-e63a-4fe8-95b4-f2679b43a01f_760x728.png)](https://substackcdn.com/image/fetch/$s_!Bril!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa67c31ad-e63a-4fe8-95b4-f2679b43a01f_760x728.png)

* **Start with the Memtable**: The read process starts in the memory first. This search includes looking up in both frozen and active Memtables. If your required data is still here, great; you've found it, with very low latency as the operation occurs in RAM.
* **Then, check the SSTables on disks:** If the system can’t find the data in RAM, the process continues on the SSTables on disk. As SSTables are organized hierarchically, the system must perform the search on every level (potentially). The search is supported by a sparse index here, rather than scanning every record in the SSTables.

The read operation will stop immediately upon finding the data. The worst-case scenario for this process is a lookup for the data that **does not exist**. Without any optimizations, the read path will:

1. *Search all the Memtables.*
2. *Search all the SSTables*

The main solution to this problem is the **Bloom Filter**. A Bloom filter is a probabilistic data structure associated with *each* SSTable. Its functionality is simple:

* It can tell us with **100% certainty** that an item is **“definitely not in the set.”** (No false negatives).
* Or, it can tell us that an item is **“possibly in the set.”** (This might be a false positive).

By applying to the SSTables, the system can:

[![](https://substackcdn.com/image/fetch/$s_!g9aj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb26354f9-c2e2-480d-a95e-f2bcc684a638_968x764.png)](https://substackcdn.com/image/fetch/$s_!g9aj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb26354f9-c2e2-480d-a95e-f2bcc684a638_968x764.png)

* Immediately skip the entire SSTable if the bloom filter says “this key is **definitely not** in this SSTable.” This reduces the I/O cost for lookups of non-existent data.
* Check the SSTable if the bloom filter says “this key **might be** in this SSTable.”

### The compaction process

Compaction is the “Merge” in Log-Structured Merge-Tree.

It is a resource-intensive background process that maintains the engine's health and performance. The process periodically reads SSTables, merges their data (which is relatively straightforward as data is already sorted), and writes the result to *new* SSTables.

It serves the following purpose:

[![](https://substackcdn.com/image/fetch/$s_!nuIL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60120c12-ffdc-4c5a-9a22-b4ab4486b4ff_1242x646.png)](https://substackcdn.com/image/fetch/$s_!nuIL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60120c12-ffdc-4c5a-9a22-b4ab4486b4ff_1242x646.png)

* **Reclaim Disk Space:** Stale data from UPDATEs or DELETEs must be cleaned up at some point.
* **Improve Read Performance:** Flushing from Memtables can result in many small files. Compaction will merge many small files into fewer, larger ones. By doing this, the readers won’t need to open/read/close many small files, thus improving the overall performance.

There are two main strategies for this merging process. Before we move on to explore them, a point you need to know is that data flushed from the Memtable can have an overlap range. For example, at T, a Memtable with range A-E is flushed, and at T+1, a Memtable with range B-D is flushed.

> *In the scope of this article, we won’t delve much into these strategies.*

#### Size-Tiered strategy

This one is implemented in [Apache Cassandra](https://cassandra.apache.org/doc/latest/). It groups SSTables into “tiers” of similar size. When a tier accumulates the specified number of SSTables, it will merge them into a new SSTable. Then the output SSTable will be moved to a higher tier.

[![](https://substackcdn.com/image/fetch/$s_!q-8p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d4f6758-faf5-4dfc-95c7-ac1b17bcac92_1304x668.png)](https://substackcdn.com/image/fetch/$s_!q-8p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d4f6758-faf5-4dfc-95c7-ac1b17bcac92_1304x668.png)

This strategy has overlapping keys across different SSTables within the same tier because its trigger is based on the number of SSTables in a tier, not on enforcing non-overlapping key ranges.

When a read request is received, the database may need to check multiple SSTables across different tiers to find the most recent version of a specific key, as the same key can exist in several overlapping SSTables. This is usually referred to as high read amplification.

#### Leveled strategy

Data is organized into non-overlapping **Levels** except for Level 0 (L0). When one Level (e.g., L1) becomes full, one of its files is merged into the *higher* level (L2). Each level has a target size (except for the L0) larger than the previous level.

[![](https://substackcdn.com/image/fetch/$s_!dEww!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe66470cd-99d7-4cc8-a456-795051f2cdb8_1622x854.png)](https://substackcdn.com/image/fetch/$s_!dEww!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe66470cd-99d7-4cc8-a456-795051f2cdb8_1622x854.png)

* L0: Overlap is allowed here.
* L1: X size. No Overlap.
* L2: 10\* X size. No Overlap.
* L3: 100\* X size. No Overlap.
* …

The compaction process will look like this:

* The system flushes Memtables and creates new SSTables in **Level 0 (L0)**. Data here can have overlapping key ranges.

  [![](https://substackcdn.com/image/fetch/$s_!2HEp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35d2a9d9-9124-4cb2-9888-f0e190ff34e2_746x326.png)](https://substackcdn.com/image/fetch/$s_!2HEp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35d2a9d9-9124-4cb2-9888-f0e190ff34e2_746x326.png)
* When the number of files reaches a threshold, all files in L0 will be merged and a new SSTable (with no overlapping key ranges) will be created in **L1**.

  [![](https://substackcdn.com/image/fetch/$s_!3qYQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7230768-9429-4209-b908-bed7df0d0c31_650x430.png)](https://substackcdn.com/image/fetch/$s_!3qYQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7230768-9429-4209-b908-bed7df0d0c31_650x430.png)
* This might cause the **L1** to exceed the size.

  [![](https://substackcdn.com/image/fetch/$s_!xyoN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c26feb5-5c5b-42ed-8803-01f321b8fa33_670x218.png)](https://substackcdn.com/image/fetch/$s_!xyoN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c26feb5-5c5b-42ed-8803-01f321b8fa33_670x218.png)
* The system will then pick at least one SSTable in L1 and merge it with the overlapping range in L2. The merged SSTable will be placed in the L2.

  [![](https://substackcdn.com/image/fetch/$s_!kZ1i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff11c39a2-14c0-4ea1-820c-3240b79ae02e_1432x462.png)](https://substackcdn.com/image/fetch/$s_!kZ1i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff11c39a2-14c0-4ea1-820c-3240b79ae02e_1432x462.png)
* The process continues when a level exceeds the limited size; at least one file in the size-exceeded level will be merged with the overlapping range in the next level.

Compared to the Size-Tiered strategy, this one has lower read amplification because the data is not overlapping in the SSTables. Read operations need fewer “checks” to ensure it doesn’t miss the data.

In return, it has higher write amplification as the Size-Tiered strategy only rewrites when it needs to move to a higher tier. For the Leveled approach, it’s more aggressive; to move a small amount of new data into a level, it forces a large amount of old data (which has an overlapping range with the moved data) in that level to be rewritten, even if it hasn’t been modified.

## The pros

Traditional B+Tree-based storage engines perform **in-place updates**. To write a 30-byte key-value pair, the engine must:

[![](https://substackcdn.com/image/fetch/$s_!QYv1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f3e1bf3-235a-4d1e-8192-06db8601ee72_592x328.png)](https://substackcdn.com/image/fetch/$s_!QYv1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f3e1bf3-235a-4d1e-8192-06db8601ee72_592x328.png)

1. Read the 4KB or 8KB data page from disk into memory (unless it’s already cached).
2. Modify the 30 bytes within that page in memory.
3. Write the **entire** 4KB/8KB page back to disk.

This is high write amplification. A small logical write becomes a large physical read and write.

The LSM-tree design avoids this penalty. Setting the writing to WAL aside, as both B-Tree and LSM trees need to do this. The heavy I/O of flushing the Memtable is a sequential write rather than overwriting the data page as the B-Tree does. This allows the LSM-tree to achieve higher write-throughput than the B-Tree in most cases.

[![](https://substackcdn.com/image/fetch/$s_!Z0QX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb0e4816c-be01-41f0-aea2-b27978d88d9e_694x704.png)](https://substackcdn.com/image/fetch/$s_!Z0QX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb0e4816c-be01-41f0-aea2-b27978d88d9e_694x704.png)

## The cons

The most obvious downside is that the system has more work to do: the compaction process, which may impact user-facing read and write operations. This also requires the user to configure carefully, as the disk bandwidth must be used by both the compaction process and the incoming writes from clients.

[![](https://substackcdn.com/image/fetch/$s_!7Qn8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe03e1cd4-fd36-4377-bd93-b36c3b39701a_854x644.png)](https://substackcdn.com/image/fetch/$s_!7Qn8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe03e1cd4-fd36-4377-bd93-b36c3b39701a_854x644.png)

The compaction may not keep pace with the rate of new data writes, resulting in an increased number of unmerged SSTables. As a result, the disk will become full since data is not cleaned up, and read operations will be impacted as more files need to be processed.

Compared to LSM-tree, B+Trees have more predictable read latency.A query follows a single O(log n) path from the root to a leaf. This is ideal for OLTP workloads where low-latency random-access reads are crucial. The LSM-tree may be slightly slower at read. To perform a read, the LSM tree must first check the in-memory memtable.

[![](https://substackcdn.com/image/fetch/$s_!U-2D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62916271-2ac2-4c12-a28f-abd845bbdbc9_578x620.png)](https://substackcdn.com/image/fetch/$s_!U-2D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62916271-2ac2-4c12-a28f-abd845bbdbc9_578x620.png)

If the data is not there, it then has to check through various on-disk SSTables until the key is found or all files are exhausted. If the number of SSTables is large, the read process is impacted.

## Why do more OLAP systems implement it?

> ***Disclaimer**: Not all OLAP systems that support real-time analytics implement the LSM-tree.*

In the past, the LSM-tree was most commonly seen in key-value or document databases due to its high throughput. However, I have personally observed that more and more OLAP systems are implementing the concept of the LSM-tree, especially those that aim to support real-time analytics capabilities.

Historically, analytical databases have been famous for a high-latency, batch-oriented processing model. In most cases, the data from OLTP systems is periodically moved into the OLAP system. This process is managed by a batch operation known as ETL.

This traditional OLAP model is optimized for complex, read-only analytical queries that scan massive volumes of data. The underlying storage is often built on static, immutable columnar files (e.g., Parquet, ORC, or the database’s dedicated columnar format).

Users were fine with the high *data latency*: the insights generated by the OLAP system could be 12, 24, or even 48 hours delayed. For historical analysis, this was perfectly acceptable.

Things have changed.

[![](https://substackcdn.com/image/fetch/$s_!xmuE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5da8095-8dc6-4555-9d58-43bc007ec76e_640x498.png)](https://substackcdn.com/image/fetch/$s_!xmuE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5da8095-8dc6-4555-9d58-43bc007ec76e_640x498.png)

The demand is now for real-time insights, often with sub-second query latency, especially in the era where everything seems to be moving faster with the involvement of AI. Live dashboards, anomaly detection systems, real-time reporting, user recommendation or personalization,…

Waiting for days or weeks is not enough.

The first step to gaining faster insights is ingesting data more quickly. Instead of batch loads, systems must accept a high-throughput, continuous stream of unbound data. This data flows from sources such as Apache Kafka, Change Data Capture (CDC) events from OLTP databases, and high-volume application or IoT logs.

This creates a high-throughput write workload, a scenario that traditional OLAP systems sometimes overlook. Data now must be available for querying in near-real-time, often within seconds or even sub-seconds of its creation.

If you have read the article so far, you should be aware that the LSM-tree is designed for high write-throughput. Regarding low-latency data reading, the system can perform the search in memory for recent data.

[![](https://substackcdn.com/image/fetch/$s_!Bo4E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f3ddaa-9d75-4fc9-bd44-9ec6355bf677_1166x394.png)](https://substackcdn.com/image/fetch/$s_!Bo4E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f3ddaa-9d75-4fc9-bd44-9ec6355bf677_1166x394.png)

Another factor that makes LSM an attractive option is that its hierarchical data organization makes it ideal for representing data in different formats.

For fast data ingestion, data can be stored in a row-oriented format in memory and at some levels on disk. Then, it can be converted into a columnar format at deeper levels with the help of the compaction process, providing better performance for OLAP scan workloads. This property features a flexible storage engine that can be tailored to different workloads.

[![](https://substackcdn.com/image/fetch/$s_!D6C_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7fcd5c9-bb3f-4d51-b1b2-0f12d27f7307_1240x652.png)](https://substackcdn.com/image/fetch/$s_!D6C_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7fcd5c9-bb3f-4d51-b1b2-0f12d27f7307_1240x652.png)

It is worth noting that not all implementations of LSM in OLAP systems utilize different file formats for other purposes; this is based solely on my research into the potential advantages of LSM in OLAP.

Next, we will briefly explore some popular OLAP systems that implement or are inspired by LSM.

### BigQuery

In 2024, Google introduced [Vortex](https://storage.googleapis.com/gweb-research2023-media/pubtools/7810.pdf), a storage engine designed to support [real-time analytics in BigQuery](https://cloud.google.com/blog/products/data-analytics/bigquery-continuous-queries-makes-data-analysis-real-time). It is a storage system that supports streaming and batch data analytics. Instead of using infrastructure built for batch data to work with streaming, Google observes that it is better to create a storage system for streaming and then utilize it for batch processing.

> *I wrote about Vortex [here](https://vutr.substack.com/p/i-spent-4-hours-learning-the-architecture?utm_source=publication-search) and [here](https://vutr.substack.com/p/how-does-vortex-the-bigquery-storage?utm_source=publication-search).*

Vortex’s storage is organized as an LSM-tree of “Fragments”:

[![](https://substackcdn.com/image/fetch/$s_!OAtq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91738543-22cf-4662-9796-9deaf270e472_1392x876.png)](https://substackcdn.com/image/fetch/$s_!OAtq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91738543-22cf-4662-9796-9deaf270e472_1392x876.png)

1. **Ingestion Format (Hot):** Buffered data in memory is written to a **WOS (Write-Optimized-Storage)** format. It is optimized to accept high-velocity writes.
2. **Analytical Format (Cold):** A background Storage Optimization Service asynchronously converts data from the WOS format to the **ROS (Read-Optimized-Storage)** format. The ROS format is a highly compressed, columnar format.

### Hudi

Apache Hudi leverages LSM to manage the metadata.

Hudi Timeline records all actions performed on the table, providing complete views of the table while efficiently supporting the retrieval of data in the order of arrival.

Hudi’s original timeline design created a new small file for every table action. While an active timeline was kept small, older instances were moved to an archived timeline. This led to the “small file problem” on cloud storage, where long-lived tables accumulated many small archive files. This makes operations that scan the timeline (such as query planning or time travel) slow.

[![](https://substackcdn.com/image/fetch/$s_!M8L_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4571657-e06d-45f0-9ea6-93374caf6e95_1136x730.png)](https://substackcdn.com/image/fetch/$s_!M8L_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4571657-e06d-45f0-9ea6-93374caf6e95_1136x730.png)

[Hudi 1.0 introduced](https://hudi.apache.org/blog/2025/05/29/lsm-timeline/) the **LSM (Log-Structured Merge) Timeline**. Instead of a flat directory of small files, it uses a “layered tree structure” (L0, L1, L2...) just like a classic LSM-tree. Timeline metadata is now batched and sorted into larger, efficient Parquet files. The small-files problem is solved, and the metadata files are now compacted into Parquet format, which helps improve read performance.

### Clickhouse

Clickhouse’s famous MergeTree family storage engine is inspired by the idea of LSM.

> *For those who are unfamiliar, Clickhouse offers a set of storage engines for users to choose from.*

As the MergeTree engine is designed for high-rate ingestion, data in a MergeTree table is stored in horizontally divided portions called “parts,” which are later merged in the background to produce larger parts.

[![](https://substackcdn.com/image/fetch/$s_!1psE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5832e788-b9df-4dad-8695-3e6123bc0b7b_966x642.png)](https://substackcdn.com/image/fetch/$s_!1psE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5832e788-b9df-4dad-8695-3e6123bc0b7b_966x642.png)

Each part has its own directory and stores data in the primary key sort order. Data is organized in a columnar fashion; with MergeTree, Clickhouse stores each column independently.

> *I write about Clickhouse [here](https://vutr.substack.com/p/i-spent-3-hours-learning-the-overview?utm_source=publication-search) and [here](https://vutr.substack.com/p/i-spent-8-hours-learning-the-clickhouse?utm_source=publication-search).*

### Others

The list continues with other systems such as [Apache Paimon](https://paimon.apache.org/docs/master/primary-key-table/overview/), [RisingWave](https://tutorials.risingwave.com/docs/design/state/), [Apache Doris](https://doris.apache.org/docs/3.x/admin-manual/trouble-shooting/compaction), [StarRocks](https://www.starrocks.io/blog/best-practices-for-starrocks-compaction-in-shared-data-architectures), [Google Napa](https://research.google/pubs/napa-powering-scalable-data-warehousing-with-robust-query-performance-at-google/) (their internal OLAP system),…

## Outro

In this article, we first explore the LSM components and how the write/read and compaction processes look. We then come to analyze its pros and cons. Finally, we try to answer the question “Why do more OLAP systems implement it?“: It’s ideal for real-time, high-rate data ingestion and can offer flexibility in data layout at different levels of the LSM tree.

Thank you for reading this far. See you in my next articles

## Reference

*[1] Patrick O’Neil, Edward Cheng, Dieter Gawlick, Elizabeth O’Neil, [The Log-Structured Merge-Tree (LSM-Tree)](https://www.cs.umb.edu/~poneil/lsmtree.pdf)*

*[2] Martin Kleppmann, [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/), 2017*

*[3] [facebook](https://github.com/facebook)/[rocksdb](https://github.com/facebook/rocksdb)**,** [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction)*

*[4] Hemant Saxena, Lukasz Golab, Stratos Idreos, Ihab F. Ilyas, [Real-Time LSM-Trees for HTAP Workloads](https://arxiv.org/pdf/2101.06801) (2022)*

*[5] Google, [Vortex: A Stream-oriented Storage Engine For Big Data Analytics](https://storage.googleapis.com/gweb-research2023-media/pubtools/7810.pdf) (2024)*
