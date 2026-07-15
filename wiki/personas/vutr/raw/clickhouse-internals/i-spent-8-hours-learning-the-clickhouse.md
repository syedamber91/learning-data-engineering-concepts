---
title: "I spent 8 hours learning the ClickHouse MergeTree Table Engine"
channel: vutr
author: "Vu Trinh"
published: 2024-11-02
url: https://vutr.substack.com/p/i-spent-8-hours-learning-the-clickhouse
paid: false
topics: ["Data Engineering", "Snowflake", "BigQuery"]
tags: [https, auto, clickhouse, table, parts, image]
---

# I spent 8 hours learning the ClickHouse MergeTree Table Engine

*Concepts, The Write/Read Process, The Mutation and The replication*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-the-clickhouse)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!7i0g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fc8cb5e-9422-43b6-91c9-e8893c4fd0d2_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!7i0g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fc8cb5e-9422-43b6-91c9-e8893c4fd0d2_2000x1429.png)

Image created by the author.

---

## Intro

As promised in the previous article, this week I'm back with lessons and insights after (a whole weekend) researching the ClickHouse MergeTree engine.

The article is structured as follows: first, we’ll go through an overview of the MergeTree engine, then examine how data is organized on disk. We’ll continue with the write/read process, touch on the merge process, explore how mutations are handled, and finally, look at how ClickHouse replicates data across nodes.

---

## Overview

MergeTree is a family of Clickhouse storage engines that allow users to index a table’s data by its primary key, which can be a set of columns or expressions.

Based on the idea of LSM trees, data in a MergeTree table is stored in horizontal-divided portions called “parts,” which are later merged in the background with a dedicated thread. Each part has its directory and stores data in the primary key sort order. Data is organized in a columnar fashion; with MergeTree, Clickhouse stores each column independently.

> ***Note**: The “columnar” approach here differs from the columnar format in Parquet, DuckDB, Snowflake, or BigQuery, where data is first horizontally partitioned into subsets of rows, and within each subset, columns are stored closely together. In ClickHouse, the table is only vertically split; each column is stored separately.*

However, in cases of writing small parts, separating them into multiple files for each column can negatively impact read and write performance. Therefore, MergeTree provides two formats for writing columns:

* **Wide**: Data will be written in separate files, each corresponding to a column. (file name: column\_name.bin)
* **Compact**: With a small part (smaller than 10 MB by default), the columns are stored consecutively in a single file to increase the spatial locality for reads and writes. (file name: data.bin)

Back to the primary key a bit. Not every record in the table has an associated index (like in the BTree engine). Instead, an index will point to a range of data (spare index). A separate primary.idx file has the primary key value for each N-th row, where N is called index\_granularity (default N = 8192).

[![](https://substackcdn.com/image/fetch/$s_!63nR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68c6ceca-f5f7-4f08-b36d-7b2d1be8eb33_1312x944.png)](https://substackcdn.com/image/fetch/$s_!63nR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68c6ceca-f5f7-4f08-b36d-7b2d1be8eb33_1312x944.png)

Image created by the author.

Why doesn’t the primary index in the ClickHouse map have index records for every row? The ClickHouse MergeTree engine family is designed to handle massive data volumes, with tables expected to receive millions of row inserts per second and store vast amounts of data. Data is written in parts in the table, with background rules applied to merge these parts. To avoid the overhead of updating the index for every row, each part’s primary index includes a single index entry (or "mark") per granule. Achieving high insertion rates would be challenging if the index required updates for every row written to the table.

Also, for each column, Clickhouse has a mark file that includes “marks,” which are offsets to each set of rows in the data file. Each mark is a pair:

* The offset in the file → the beginning of the compressed block
* The offset in the decompressed block → the start of the granule

ClickHouse always keeps for primary.idx in memory and data for the column.mrk files are cached.

---

## On the disks

As mentioned, every table in the MergeTree engine is divided into a set of immutable parts. A part is formed whenever a set of rows is inserted into the table. Parts include all metadata required to interpret its content.

[![](https://substackcdn.com/image/fetch/$s_!ihdA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4f18740-49b8-493d-90a5-9bc1e53be4db_584x536.png)](https://substackcdn.com/image/fetch/$s_!ihdA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4f18740-49b8-493d-90a5-9bc1e53be4db_584x536.png)

Image created by the author.

Because the insertion will result in new parts, this can affect the potential of the read operations. To deal with this, a background job merges multiple smaller parts into larger parts. The original parts are marked inactive and eventually deleted as soon as their reference count drops to zero (i.e., no query reading those parts)

A part corresponds to a directory on disk, containing one file for each column (wide format) or a single file for all columns (compact mode). Part directories have the name that follows this pattern:

[![](https://substackcdn.com/image/fetch/$s_!Ybtw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2b94419-bbc6-4699-9a48-af70bac9152d_1544x404.png)](https://substackcdn.com/image/fetch/$s_!Ybtw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2b94419-bbc6-4699-9a48-af70bac9152d_1544x404.png)

Image created by the author.

If an ALTER TABLE statement has modified the part, the directory's name will have a version. When a part is first created, it has level 0. Parts can only be merged with other parts with an adjacent block number. When parts with the same level are merged, the new part will have a level of original\_level + 1. The original parts will be deleted in the future.

[![](https://substackcdn.com/image/fetch/$s_!6zFZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc97b4325-aa62-4fab-a64b-8e0e993461b5_882x590.png)](https://substackcdn.com/image/fetch/$s_!6zFZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc97b4325-aa62-4fab-a64b-8e0e993461b5_882x590.png)

Image created by the author.

A part's column is further logically divided into groups of 8192 records, called granules. A granule is the smallest data unit processed by the scan and index lookup operators in ClickHouse.

However, reads and writes of on-disk data are executed at the block level. A block combines multiple neighboring granules within a column. New blocks are formed based on a configurable byte size per block (default 1 MB), and the number of granules per block is calculated using the column’s data type and distribution. Blocks are compressed to reduce their size and I/O costs. By default, ClickHouse employs LZ4 as a general-purpose compression algorithm, but users can also apply specialized algorithms like Gorilla or FPC.

> ***Important note**: ClickHouse uses the term "block" to refer to two concepts: first, blocks for compression and read/write operations on disk; second, blocks used for query processing (a set of rows from a table). The “block” in the paragraph above refer to block for compression.*

Blocks are decompressed on the fly when read from the disk into memory. Also mentioned above, ClickHouse stores for each column a mapping that associates every granule id with the offset of its containing compressed block in the column file and the offset of the granule in the uncompressed block (mark files)

In addition, MergeTree tables can be partitioned in range, hash, round-robin fashion or using custom expressions. If a table is configured for partitioning, Clickhouse will store the partitioning expression’s minimum and maximum values for each partition; this information will be used for data running later when the query only needs to read particular partitions.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Insert Mode

In MergeTree, data can be inserted in two modes:

[![](https://substackcdn.com/image/fetch/$s_!lIYf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9c6fe6e-23ba-4ddf-8371-57f81f50b5d0_1258x598.png)](https://substackcdn.com/image/fetch/$s_!lIYf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9c6fe6e-23ba-4ddf-8371-57f81f50b5d0_1258x598.png)

Image created by the author.

* **Synchronous mode**: Each INSERT statement creates a new part. Database clients should insert data in bulk to minimize the overhead of merges. However, this mode can suffer from significant latency because the client needs to batch data before sending, which does not satisfy the use case in which data should be processed in real-time.
* **Asynchronous mode**: ClickHouse buffers rows from multiple INSERT operations into the table and forms a new part only after the buffer size exceeds a threshold, or a timeout expires.

---

## Insert Process

> *For this section, I built the Clickhouse source code and followed the code to understand the process. If you found I wrong at some point, feel free to correct me.*

First, we need to create the table. When creating a table in ClickHouse, the user specifies the table name, schema, engine, optional primary key(s), and other parameters. This information is used to "register" the table with ClickHouse.

Now, let's insert some data into the table.

[![](https://substackcdn.com/image/fetch/$s_!ByRj!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edf031a-1621-4e81-99cf-0ad9d9957824_1218x870.png)](https://substackcdn.com/image/fetch/$s_!ByRj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edf031a-1621-4e81-99cf-0ad9d9957824_1218x870.png)

Image created by the author.

* Let’s say we insert the data using the INSERT statement; the system will first parse the SQL to understand what we are trying to input to the table.
* ClickHouse will create a sink to consume the inserted data.
* The sink will consume a chunk of data and form the in-memory data block, which will be written into a new part. The inserted block size can be controlled by the following settings: **min\_insert\_block\_size\_rows** (default: 1,048,449 rows) and **min\_insert\_block\_size\_bytes** (default: 256 MB).

> *Here, a block refers to a set of table’s rows.*

* If the table is partitioned, Clickhouse will decide which portions of the block belong to which partitions.
* Next, Clickhouse will step into the block writing process.
* It first extracts the column’s information, like name and type.
* If the table is partitioned, Clickhouse will extract the min-max of the columns included in the partition’s expression.
* Then, Clickhouse will form the part name following the pattern mentioned above. Here, the system also defines the name of the part’s temporary directory: “tmp\_insert\_” + part\_name.

  > *Clickhouse will write the part’s data in the temporary directory first.*
* The system will get information about the columns used to sort the data. These might be the primary keys or the columns in the ORDER BY field. ClickHouse starts sorting the block’s data based on the sort columns in the memory.
* Next, the disk writing process starts. The transaction begins.
* The temporary directory is created.
* ClickHouse will create the “writer“ to facilitate the writing. In this case, the *Wide* writer will be initiated to handle the data writing each file for each column’s data.
* The system writes each column into separate files within the part's temporary folder. The column data is initially written to the page cache, then compressed based on the defined compression scheme (LZ4 by default), and finally flushed to disk. The mark file and primary index file are also written at this step.
* After writing the columns’ data, the process will write other metadata files like **count.txt** (part’s number of row), **column.txt** (column description), default\_compression\_codec.txt: the default block compression algorithm (LZ4), and the **checksums.txt** is used to check the integrity of the data.
* Before renaming the temporary folder to the part’s convention name, Clickhouse will check some conditions, such as whether this transaction is used for more than one table, whether an intersected part contains overlapped data, and whether the part is empty or duplicated. If all the checks are passed, Clickhouse will rename the parts’ temporary folder.
* The transaction is committed.
* The process checks if there is more data to consume; if yes, all the steps above will be carried out for the new part.

---

## Idempotent Insert

[![](https://substackcdn.com/image/fetch/$s_!QcSS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b424508-9f23-4cd2-b439-54a09216d0d0_804x482.png)](https://substackcdn.com/image/fetch/$s_!QcSS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b424508-9f23-4cd2-b439-54a09216d0d0_804x482.png)

Image created by the author.

There are circumstances when the insertion is interrupted in the middle, such as the connection timeout; in these cases, the client might be confused about whether the data was successfully inserted. The most straightforward way to solve this is to re-send the data to the server and use some mechanism to check whether an insert is duplicated.

The ClickHouse server maintains a hash table of recently inserted parts, allowing it to skip re-inserting parts already in the hash table.

---

## Merge

In MergeTree, each insertion results in a new part, which can lead to a table accumulating many parts. Read operations may then require opening and closing multiple parts to access the data, potentially resulting in poor performance. Another performance concern is that if the merge process isn’t managed carefully, data might be written multiple times (once for the initial insertion and additional times for merging).

To maintain a sufficient number of parts, a background process merges parts to form larger parts. The process periodically wakes up to check if there are parts that should be merged. If it has nothing to do, it can go back to sleep. It uses some heuristics to select the parts to be merged, such as the part sizes, currently executed merges, or the number of parts.

---

## Read

As mentioned above, the primary key columns (if specified) will determine the sort order of the rows within every part. For every part, Clickhouse keeps a mapping from the primary key column values of each granule’s first row to the granule’s id.

Because the primary is sparse (default every 8192 rows), the primary mapping can potentially remain fully in memory. The goal of a primary key is to evaluate equality and range predicates for frequently filtered columns using binary search instead.

Let's check out a typical process of data running using the primary key:

* Give a table with column “user\_id“ as the primary key and use default index\_granularity, which is 8192.
* The table has 8,200,000 rows, resulting in 1000 granules, with the last granule having 8000 rows.

[![](https://substackcdn.com/image/fetch/$s_!L5UZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F687726d4-1bc5-454e-851e-de3fef374e0e_1064x800.png)](https://substackcdn.com/image/fetch/$s_!L5UZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F687726d4-1bc5-454e-851e-de3fef374e0e_1064x800.png)

Image created by the author.

* After writing, a primary index file maps the primary key column(s) value of the first row of every granule to an associate mark.

[![](https://substackcdn.com/image/fetch/$s_!bqvO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe11f6328-618d-421a-9780-523f79215c9b_1276x704.png)](https://substackcdn.com/image/fetch/$s_!bqvO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe11f6328-618d-421a-9780-523f79215c9b_1276x704.png)

Image created by the author.

* Besides the data and primary index file, a mark file maps records to two offsets. The first offset points to the block in the compressed column data file containing the selected granule’s compressed version. This compressed block may include several compressed granules. Once located, the compressed file block is decompressed into main memory. The second offset specifies the granule’s position within the decompressed block data.

[![](https://substackcdn.com/image/fetch/$s_!cFTS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F688b322a-c304-44f4-a893-e58cd20616e5_1046x1088.png)](https://substackcdn.com/image/fetch/$s_!cFTS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F688b322a-c304-44f4-a893-e58cd20616e5_1046x1088.png)

Image created by the author.

* Let’s assume that the user wants to query the user with the user\_id = 7543. Based on the primary index file, the query planner finds that granule 1 will contain the needed data.
* After that, the planner opens the mark file to read the mark 0’s associated offsets.
* It uses the first offset to locate and decompress the compressed block in the memory.
* Because the block might have multiple granules, the planner uses the second offset to locate the desired granule.

In addition to the primary key, users can create alternative versions of a table sorted by a different primary key (called table projections). If your query needs to filter on columns that differ from the main primary key, table projection can help. By default, projections are lazily facilitated only from parts newly inserted into the main table but not from existing parts unless the user fully materializes the projection. The optimizer decides between reading from the main table or a projection based on estimated I/O costs.

Finally, Clickhouse supports a data running option called skipping indices. The main idea is to maintain small amounts of metadata at the level of consecutive granules, which helps users avoid scanning unnecessary rows. One of the supported skipping indexes is the min-max index; it stores the minimum and maximum values of the index expression for each index block.

---

## Mutation

MergeTree is optimized for append-only use cases and expects no or rare updates and deletes. There are two approaches for updating or deleting the existing data:

* Rewriting parts to handle mutations—like `UPDATE` and `DELETE` DMLs—results in mutation tasks. It finds affected parts and rewrites them with an incremented version number. By default, mutations are carried out asynchronously to batch multiple mutations into a single operation, allowing the modified part to be rewritten together, amortizing the writing cost. Thus, mutation of a single row is expensive because an entire part needs to be rewritten.
* Lightweight deletes: Deletions only update an internal bitmap column, indicating whether a row is deleted. When executing the query, Clickhouse will look into the bitmap column to skip deleted rows from the result. Deleted rows are physically removed by regular merges at an unspecified time in the future. Depending on the column count, lightweight deletes can be much faster than mutations; In return, the query might execute slightly slower.

If your use case requires a lot of data mutation, consider a specialized merge tree engine such as the ReplacingMergeTree engine. It keeps only the most recently inserted version (mutation be insertion) of the record using the created timestamp of its associated part; older versions are deleted. The records are considered the same if they have the same primary key(s) value.

---

## Replication

Data replication is not only leveraged for high availability but also a recommended approach to increasing read throughput, as the read operations can be load-balanced across the replicas.

Each MergeTree table engine will have its associated replicate engine (MergTree → ReplicateMergeTree, ReplacingMergeTree → ReplicatedReplacingMergeTree, AggregatingMergeTree → ReplicatedAggregatingMergeTree)

Replication relies on the concept of table states, which consist of a set of table parts and metadata, such as column names and types. Nodes in the cluster can change the table state through the following operations:

* **Inserts**: Add a new part to the state.
* **Merges**: Add a new part and remove existing parts from the state.
* **Mutations and DDL statements**: Add parts, remove parts, or alter table metadata.

These operations are performed locally on a node and recorded as a sequence of state transitions in a global replication log. The log is maintained by a set of typically three ClickHouse Keepers that leverage the Raft consensus algorithm to provide.

Initially, all cluster nodes point to the same position in the replication log. As nodes execute operations, other nodes replay the replication log asynchronously. Consequently, replicated tables are only eventually consistent; nodes may temporarily read outdated table states at specific points in time, but in the end, all nodes will reach the same state.

Let’s look at an example for a better understanding:

Suppose the table is replicated across three cluster nodes.

[![](https://substackcdn.com/image/fetch/$s_!eLHe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65f3aaa7-2ef3-42d8-b1cc-a167b278d878_1408x1096.png)](https://substackcdn.com/image/fetch/$s_!eLHe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65f3aaa7-2ef3-42d8-b1cc-a167b278d878_1408x1096.png)

Image created by the author.

* Initially, the table is empty.
* Node 1 receives two `INSERT` statements and records them in the replication log.
* Node 2 replays the first log entry by fetching it from the log and then downloads the newly inserted part from Node 1.
* Meanwhile, Node 3 replays both log entries recorded by Node 1, resulting in downloading both inserted parts from Node 1.
* Node 3 merges the two downloaded parts into a new part, deletes the input parts, and records a merged entry in the replication log.
* The process goes on by all nodes replaying the replication log asynchronously.

---

## Outro

I think that’s all for this week.

Hope this can help you a bit if you’re trying to learn ClickHouse MergeTree table engine. If you like more writing on Clickhouse, please give this article a reaction or restack :)

For further discussion, feel free to comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

---

## Reference

*[1] [ClickHouse Official Github Repo](https://github.com/ClickHouse/ClickHouse)*

*[2] Ryadh Dahimene, Alexey Milovidov, [ClickHouse - Lightning Fast Analytics for Everyone](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf) (2024)*

*[3] Jack Vanlightly, [Serverless ClickHouse Cloud - ASDS Chapter 5 (part 1)](https://jack-vanlightly.com/analyses/2024/1/23/serverless-clickhouse-cloud-asds-chapter-5-part-1) (2024)*

---

## Before you leave

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
