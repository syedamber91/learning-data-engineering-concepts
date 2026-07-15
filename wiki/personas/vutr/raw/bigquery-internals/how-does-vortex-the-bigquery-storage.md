---
title: "How does Vortex, the BigQuery storage engine work behind the scenes?"
channel: vutr
author: "Vu Trinh"
published: 2024-11-26
url: https://vutr.substack.com/p/how-does-vortex-the-bigquery-storage
paid: false
topics: ["Data Engineering", "BigQuery", "Streaming", "Batch Processing"]
tags: [https, stream, auto, vortex, image, server]
---

# How does Vortex, the BigQuery storage engine work behind the scenes?

*Vortex: The BigQuery's Stream-Oriented Storage Engine (Part 2)*

> Source: [Open post](https://vutr.substack.com/p/how-does-vortex-the-bigquery-storage)

## Topics

[[data-engineering|Data Engineering]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!hP1R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F331f0755-0b57-402d-9bb2-cb41fe185187_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!hP1R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F331f0755-0b57-402d-9bb2-cb41fe185187_2000x1429.png)

Image created by the author.

---

## Intro

This article is the second part of my writing about Vortex, BigQuery’s stream-oriented storage engine. We will explore how Vortex handles data read/write operations, manages the metadata, and the working mechanism between Vortex’s components.

---

## My last time writing about Vortex

In my previous article, I provided an overview of Vortex, as described in Google’s paper. Vortex is a storage system that supports both streaming and batch data analytics. Rather than adapting infrastructure built for batch data to handle streaming, Google created a system optimized for streaming and extended its functionality to batch processing.

The fundamental abstraction in Vortex is the Stream, which enables clients to append data. Vortex manages a Stream by dividing it into contiguous rows called Streamlets. Each Streamlet is written to two Borg clusters within a region and is further split into smaller contiguous blocks of rows called Fragments. Fragments represent ranges of rows within log files stored in Colossus.

[![](https://substackcdn.com/image/fetch/$s_!riR9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca810bb-d064-4bcd-8ed8-1386d37935a6_760x440.png)](https://substackcdn.com/image/fetch/$s_!riR9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ca810bb-d064-4bcd-8ed8-1386d37935a6_760x440.png)

Image created by the author.

I also explored the Vortex control plane, managed by the Stream Metadata Server(s) (SMS). The control plane handles metadata management, while the data plane, operated by the Stream Server, manages the Stream’s data.

The following section will discuss how clients communicate with Vortex via a dedicated library.

---

## Client Library

The client accesses, reads, and writes data to Vortex via a thick library. The library supports retrying failed requests, decrypting, and decompressing data from Fragments.

### Schema Evolution

The library gets a writable Streamlet from the SMS and returns it to the client. If the table schema changes while a client writes, the Stream Server marks the append fails and tells the client to obtain the latest schema. The client library will get the new table schema from the SMS and retries the append with the updated schema.

[![](https://substackcdn.com/image/fetch/$s_!VML_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff336a9be-5411-472e-8a45-a93eb98716db_1400x936.png)](https://substackcdn.com/image/fetch/$s_!VML_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff336a9be-5411-472e-8a45-a93eb98716db_1400x936.png)

Image created by the author.

The table schema changes are reflected in the SMS. The SMS cannot inform the client about the schema changes because the client only talks to the Stream Server when the data is appending. Instead, when there are changes, the SMS will notify the Stream Servers about the new schema version via heartbeat (more on this later). The Stream Server then tells the clients about the latest schema version when they try to append it. The client then fetches the updated schema from the SMS.

### Connection

The client library supports single-directional (unary) short-lived connections and a bi-directional long-lived connection.

* The short-lived unary connection supports a request-response mechanism and can reuse connections from the connection pool. It is suitable for infrequent append requests to a table.
* The long-lived bidirectional connection supports streaming RPCs, which let the user continually append to the table. However, it has a higher memory overhead due to its persistence and tracking of multiple operations on the same connection. This connection also supports flow control; the Stream Server can use flow control to throttle appends when a large amount of data needs to be ingested. The data stays in memory until it has been committed. If the disk (Colossus) is slow, the flow control will limit the rate of accepted data to prevent the Stream Server from running out of memory.

  [![](https://substackcdn.com/image/fetch/$s_!sKcQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2fb79e1-c77e-4767-99cb-c581dd73c9c0_566x604.png)](https://substackcdn.com/image/fetch/$s_!sKcQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2fb79e1-c77e-4767-99cb-c581dd73c9c0_566x604.png)

  Image created by the author.

### Lifetime of data in a Stream

> *Imagine the table is newly created, and there is no existing stream for it*

[![](https://substackcdn.com/image/fetch/$s_!fJs-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadaacaab-7eb7-4850-a9e7-5bb5e0188b15_1246x902.png)](https://substackcdn.com/image/fetch/$s_!fJs-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fadaacaab-7eb7-4850-a9e7-5bb5e0188b15_1246x902.png)

Image created by the author.

* The client will ask the SMS to create a new Stream.
* The SMS generates a unique ID for the Stream and the Steam’s first Streamlet.
* The SMS records the Stream information in the Spanner database to map the stream to a table.
* The SMS contacts the Stream Server to create the Streamlet.
* The SMS tells the client that it can start appending data to the Streamlet.
* The client streams data in batches of rows to the Stream Server.
* The Stream Server creates new log files as needed to store the data.

> *Reminder: Fragments are a range of rows inside a log file*

* The Storage Optimization Service asks the SMS for the candidate Fragments to convert to ROS format, commits those converted Fragments, and marks the original Fragments as deleted.
* After a configurable period, the SMS tells Stream Servers to clean up the deleted Fragments.
* When the Stream Server acknowledges it has deleted the Fragments, the SMS deletes the Fragment metadata from the Spanner database.

### Fragment File format

[![](https://substackcdn.com/image/fetch/$s_!x--n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41adce8b-a930-4828-aec7-b5c8b3a0c086_590x606.png)](https://substackcdn.com/image/fetch/$s_!x--n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41adce8b-a930-4828-aec7-b5c8b3a0c086_590x606.png)

Image created by the author.

Every Fragment has a header at the beginning of the file. The header contains the File Map, which contains information used for disaster resilience. The Stream Server buffers a write to a Fragment up to 2MB. This decision prevents many small writes to the file system and helps the Fragment achieve better compression.

Data must be compressed (Snappy) to reduce space in the WOS format before being appended to the fragment.

To preserve the data integrity, Vortex uses a CRC to protect data as it is sent from the client to the Stream Server and from the Stream Server to Colossus. The data bytes are sent with their CRC; if the corruption happens, the Colossus will discover this using the CRC and fail the write operation.

After compression, data is encrypted to protect the data content; after this step, data is ensured to be encrypted until it needs to be read back.

When the Stream Server finalizes the Fragment, it places a bloom filter, followed by a footer providing the bloom filter location—the bloom filter marks which key values exist for the partitioning and clustering columns.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

### Heartbeat from Stream Server to SMS

The Stream Server sends a heartbeat to each SMS every few seconds to inform it about changes to Streamlet metadata due to new appends, such as creating new log files or increasing the size of existing log files. The Stream Server will send a complete state snapshot of all Streamlets it owns to the SMS. If the SMS is unaware of a Streamlet existing in any table, the Stream Server deletes the Streamlet information in the Spanner.

[![](https://substackcdn.com/image/fetch/$s_!uhRQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c8ee4ee-26b6-44af-b922-532a23954eaf_600x554.png)](https://substackcdn.com/image/fetch/$s_!uhRQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c8ee4ee-26b6-44af-b922-532a23954eaf_600x554.png)

Image created by the author.

Besides the Streamlet level metadata, the Stream Server informs the SMS about its current load information (CPU, memory, and throughput). The SMS uses the stream server’s load information to balance the Streamlets between Stream Servers.

In the following sections, we will learn about the Vortex's data and metadata management functionalities.

## Storage Optimization

As mentioned, the Storage Optimization Service converts data from WOS to ROS format, which is more optimized for analytics workloads. It maintains a Log-Structured Merge (LSM) tree of Fragments, in which the deepest level is Fragments with WOS format; when moving up the tree, there are more ROS optimized version of the Fragments. As I understand it, the Storage Optimization Service not only converts Fragments from WOS to ROS but also 'merges' the converted Fragments into larger ones, which significantly enhances reading performance.

[![](https://substackcdn.com/image/fetch/$s_!w4y0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F040fa34a-2f72-4c28-b5a4-09c48cac2bc2_2804x826.png)](https://substackcdn.com/image/fetch/$s_!w4y0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F040fa34a-2f72-4c28-b5a4-09c48cac2bc2_2804x826.png)

Image created by the author.

To execute the conversion, the service determines a list of unconverted Fragments as candidates from the SMS and schedules the conversion of these Fragments on many workers.

Each Fragment has two timestamps: a creation\_timestamp and a deletion\_timestamp. The Storage Optimization Service sets the deletion\_timestamp for a Fragment whenever it is converted into a new optimized version. The new Fragment will have a creation\_timestamp.

A Fragment is available if the client reads the table at a snapshot timestamp between the interval [creation\_timestamp, deletion\_timestamp]. At each optimization step, the optimizer atomically sets the deletion\_timestamp for the previous version of the fragments and the creation\_timestamp for the new version.

The optimization service does not only handle the ROS-WOS conversion. BigQuery lets users define a table's clustering column(s); BigQuery attempts to sort storage blocks based on the values in the clustered columns. To maintain the order of the data following the clustering columns when new data is written, the optimization service will execute the data re-clustering when it observes that it’s time to do that.

---

## Metadata Management

Vortex tracks the coarse-grained metadata about Streams, Streamlets, and Fragments in the Spanner database. An example of this metadata is a Streamlet's state, indicating whether it is writable.

The source of truth for Streamlet and Fragment metadata is persisted in the Stream Server’s log. The Streamlet metadata in Spanner is mainly used for caching. It does not act as the source of truth until the Streamlet is finalized.

When the storage optimizer converts Fragments from WOS to ROS format, BigQuery’s dedicated metadata management system, Big Metadata, manages fine-grained metadata for these Fragments.

> *I also wrote an article about Big Metadata, you can find it [here](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-how-google?r=2rj6sg&utm_campaign=post&utm_medium=web). A* *touch on fine-grained metadata: it tracks information at a much more granular level—such as metadata for each data block or each column within those blocks, this information is used for accelerating query performance.*

---

## Data Verification

Vortex tracks all calls to the client library and saves information back to Vortex. It also tracks storage optimization behavior. Based on this information, Google builds the data verification pipelines to validate the correctness, executed as SQL queries in BigQuery:

[![](https://substackcdn.com/image/fetch/$s_!EZz_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd97c1d0-4b03-4da7-a5ec-3d986d76b785_888x506.png)](https://substackcdn.com/image/fetch/$s_!EZz_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd97c1d0-4b03-4da7-a5ec-3d986d76b785_888x506.png)

Image created by the author.

* For a successful Vortex API call, Google verifies that the Stream, Streamlet, and Fragment are created. In addition, the appended data must be placed at the expected location (Stream + row\_offset).
* They also verify that each record is converted from WOS to ROS precisely once. Additionally, they validate that the output records are consistent with the input records for every conversion.

In the following sections, we will discover in more detail how Vortex data is retrieved by analytics engines such as Google Dremel (BigQuery Query Engine)

## Reading the data

> *Vortex offers read-after-write consistency, which is the gurantee to view changes (read data) right after making those changes (write data).*

BigQuery query engine (Dremel) reads data directly from the Colossus via the client library.

[![](https://substackcdn.com/image/fetch/$s_!B_00!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7adfd1a7-207d-4abe-897b-f29177e36a71_512x506.png)](https://substackcdn.com/image/fetch/$s_!B_00!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7adfd1a7-207d-4abe-897b-f29177e36a71_512x506.png)

Image created by the author.

If the Stream Server is available, it can serve the in-memory metadata for the client to determine the Fragments and offsets it needs to read. For a log file, clients read the File Map to get the finalized size of the Fragment; they won’t read past this size to ensure they don’t read failed or partial writes at the end of a Fragment.

Next, see how Vortex handles the partition pruning for a query.

> *BigQuery let user define partition column for a table; it will devide the table horizontally based on the partition column value. The common pattern is partitioning the table by a date column. The query engine can use the query’s filter (on partition column) to determine which partition is required, thus, improve the overall query performance.*

In Vortex, a partition refers to each of the Fragments and Streamlets returned by the SMS. It eliminates partition by tracking column properties (e.g., min/max values) and bloom filters for table partitioning/clustering columns. The Stream Server maintains these properties for each Streamlet as data is written.

Once a Fragment is finalized, the Stream Server sends its properties to the SMS for caching (on Spanner) via the heartbeat. The Stream Server maintains the properties of the latest written Streamlet.

Upon receiving the query, BigQuery uses the query’s filters to build the derivative expressions on the column properties. It then evaluates the expression on the column properties for each Fragment and Streamlet returned by the SMS to check if it is needed for the query.

> *For the process of builing the derivative expressions on the column properties, I also explored it on [my article](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-how-google?r=2rj6sg&utm_campaign=post&utm_medium=web) on Big Metadata.*

---

## Data Mutation

BigQuery supports table data updates via the SQL DML statements such as UPDATE, DELETE, and MERGE.

To implement the deletion, Vortex allows a range of rows in a Fragment or Streamlet to be marked as deleted by a mask. A DELETE statement first determines the candidate deleted rows and persists a deletion mask to the Streamlet or Fragment at commit time.

[![](https://substackcdn.com/image/fetch/$s_!MhZp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c7800bc-2e2d-4f32-b655-39bed2c07680_594x550.png)](https://substackcdn.com/image/fetch/$s_!MhZp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c7800bc-2e2d-4f32-b655-39bed2c07680_594x550.png)

This is for illustration purposes only based on my understanding and may not reflect the exact Vortex implementation of deletion. Image created by the author.

Vortex sometimes marks unaffected rows as deleted to limit the deletion mask size. Google calls these reinserted rows; copies of reinserted rows are committed to the table atomically, along with the commit of the deletion mask.

Vortex implements UPDATE statements by combining old rows deletion and the updated rows insertion.

This delete approach above assumes that SMS is aware of the Fragments affected by the DML. However, there are cases when SMS is not aware of some of the latest Streamlet Fragments because the Vortex design lets the Stream Server asynchronously report its status to the SMS via heartbeat; there is a high chance that between the two heartbeats, the client writes the data to a Streamlet. Google calls these unreported portions of the Streamlet the tail.

When the DML needs to delete the records in the Streamlet tail, the SMS will mark the whole Streamlet tail as deleted. When the Stream Server informs the SMS about the Streamlet’s tail in the next heartbeat, the SMS maps the deleted record range recorded in the Streamlet to actual deletion masks.

There is another potential issue with the DML process here. Remember that the Storage Optimization Service will mark old Fragments as deleted and commit new Fragments during the WOS-ROS conversion or other optimization processes such as re-clustering. Marking a fragment as deleted can conflict with running DML operations that have already marked the fragment’s set of rows as deleted.

Google has a straightforward solution: the storage optimization service will not commit whenever a DML statement is running. However, long-running DML statements may block the optimized process for a while, preventing data in WOS from being converted into the ROS format and thus causing poor read performance on the table. To solve this, Vortex supports a 1:1 Fragment conversion from WOS to ROS format.

---

## Outro

Thank you for reading this far.

In this article, we explored how clients interact with Vortex through a thick library and how it converts Fragments from a write-optimized format to a read-optimized format. We then delved into Vortex’s data and metadata management functionalities. Finally, we discussed how query engines like Dremel (BigQuery Query Engine) retrieve data from Vortex.

Now, it’s time to say goodbye!

---

## **References**

*[1] Google,* [Vortex: A Stream-oriented Storage Engine For Big Data Analytics](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/)

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/how-does-vortex-the-bigquery-storage/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
