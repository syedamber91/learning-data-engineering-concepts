---
title: "I spent another 8 hours understanding the design of Amazon Redshift. Here's what I found."
channel: vutr
author: "Vu Trinh"
published: 2024-03-16
url: https://vutr.substack.com/p/i-spent-another-8-hours-understanding
paid: false
topics: ["Data Engineering", "Snowflake", "BigQuery", "Data Warehouse", "ETL"]
tags: [redshift, https, amazon, auto, query, image]
---

# I spent another 8 hours understanding the design of Amazon Redshift. Here's what I found.

*All insights from Redshift academic paper: Amazon Redshift Re-invented - 2022.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-another-8-hours-understanding)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[etl|ETL]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!9grN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F809f83a1-a889-470c-a7a9-8a68dd3003a7_1401x999.png)](https://substackcdn.com/image/fetch/$s_!9grN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F809f83a1-a889-470c-a7a9-8a68dd3003a7_1401x999.png)

Image created by the author.

---

> *Table of contents:*

* *History and background*
* *High-level architecture*
* *The life of the query*
* *Code Generation*
* *Compilation Service*
* *Storage*
* *Compute*
* *Integration*

---

## Intro

As I got older, I realized I was wrong about many things. One of them is about [Amazon Redshift](https://aws.amazon.com/redshift/). The first time I used [Google BigQuery](https://cloud.google.com/bigquery?hl=en) after nearly a year stuck with Redshift, I told myself BigQuery was more advanced than 5x times Redshift (primarily due to BigQuery's serverless experience). That impression lasted for three years. Thinking back, I laugh at myself and question why I was so naive.

To deliver outstanding products like BigQuery, Redshift, or [Snowflake](https://www.snowflake.com/en/), each database will have its approach to dealing with hardware constraints and solving system design problems. Instead of comparing which [database is faster](https://www.youtube.com/watch?v=_3fpVb40IYk), I like to look into their internal implementation and learn valuable things. This article is my effort to dive deep into Amazon Redshift - the OLAP system I used to overlook.

I will use most of the material from the academic paper [Amazon Redshift Re-invented](https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf) (2022); additional reference documents will be included at the end of the article.

## History

> *From [Wikipedia](https://en.wikipedia.org/wiki/Amazon_Redshift)*

Amazon Redshift is a column-oriented massively parallel processing data warehouse designed for the cloud. The system is built on top of technology from the [massive parallel processing (MPP)](https://en.wikipedia.org/wiki/Massively_parallel) data warehouse company [ParAccel](https://en.wikipedia.org/wiki/ParAccel) (later acquired by [Actian](https://en.wikipedia.org/wiki/Actian)). It is based on an older version of [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) [8.0.2](https://en.wikipedia.org/wiki/PostgreSQL#Release_history), and Redshift has made changes to that version. An initial [preview beta](https://en.wikipedia.org/wiki/Software_release_life_cycle#Stages_of_development) was released in November 2012, and a full release was made available on February 15, 2013.

---

## High-level architecture

[![](https://substackcdn.com/image/fetch/$s_!ZsTn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f3f4ca2-638a-4357-88af-7f860b69fa0e_890x874.png)](https://substackcdn.com/image/fetch/$s_!ZsTn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f3f4ca2-638a-4357-88af-7f860b69fa0e_890x874.png)

Image created by the author.

A Redshift cluster consists of multiple compute instances to handle the query execution. Each cluster has a single coordinator node (a.k.a leader) and multiple worker nodes.

Data is stored on Redshift Managed Storage (RMS), which leverages the [Amazon S3](https://aws.amazon.com//s3/?gclid=Cj0KCQiA5-uuBhDzARIsAAa21T9qbwjJF7YtpIyDEk0j9Qnw6G3cLceBjSBU9r2oMtnZOTaIGxYJgpMaAmtpEALw_wcB&trk=f10cddca-7917-4465-9801-28c9cc57f288&sc_channel=ps&ef_id=Cj0KCQiA5-uuBhDzARIsAAa21T9qbwjJF7YtpIyDEk0j9Qnw6G3cLceBjSBU9r2oMtnZOTaIGxYJgpMaAmtpEALw_wcB:G:s&s_kwcid=AL!4422!3!589846469979!e!!g!!amazon%20s3!16178327440!136912444927) behind the scenes. When Redshift processes the query, data is cached in compute nodes on local SSD in a compressed column-oriented format. (With my limited knowledge, this is similar to [the Snowflake storage hierarchy](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf)).

The table’s data is partitioned into multiple buckets distributed to all worker nodes. Redshift can apply the partition scheme based on the data’s characteristics, or the user can explicitly declare the desired partition scheme, such as round-robin or hash.

Besides the compute and the storage, Redshift has other components like :

* [AQUA](https://aws.amazon.com/blogs/aws/new-aqua-advanced-query-accelerator-for-amazon-redshift/) is the layer that leverages [FPGAs](https://vi.wikipedia.org/wiki/FPGA) to accelerate the query performance.
* [Compilation-As-A-Service](https://aws.amazon.com/blogs/big-data/fast-and-predictable-performance-with-serverless-compilation-using-amazon-redshift/) is a caching service for the generated code (from the query).
* [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html) allows users to query data directly in S3 from Redshift.

---

## The life of the query

> *What happened when you submitted your SQL?*

[![](https://substackcdn.com/image/fetch/$s_!LEPu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa944f055-4925-442d-9124-b416e1ffb385_877x569.png)](https://substackcdn.com/image/fetch/$s_!LEPu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa944f055-4925-442d-9124-b416e1ffb385_877x569.png)

Image created by the author.

Before moving on to see architecture components in detail, let's take a glimpse at Redshift’s query journey:

* The query says “Hi“ to the leader node first; it will be parsed, rewritten, and optimized here.
* Redshift uses the cluster’s topology to select the optimal plan. The planning process also uses the data distribution information of data under the neath to prevent expensive data movement.
* After the planning phase, Redshift moves to the execution phase. The plan will be divided into individual execution units. Each unit will consume intermediate output from previous units. Redshift generates and compiles optimized C++ code for each unit and ships the code to the compute nodes over the network.
* The columnar data is scanned from locally attached SSDs or hydrated from Redshift Managed Storage.

> As I understand it, the term “hydrate“ indicates the process of filling the SSD with data from Redshift Managed Storage. Correct me if I’m wrong.

Redshift execution’s engine applies many optimization techniques to improve the performance:

* Using zone-maps - a small hash table that stores the min-max value for each data block. (Snowflake and BigQuery also do this.)
* The scan operation leverages [Vectorization](https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf) and [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) processing.
* Lightweight compression format.
* [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)
* [Prefetching](https://en.wikipedia.org/wiki/Cache_prefetching)
* Redshift’s AZ64 compression.

We also see these techniques again when I go into detail about Redshift components.

---

## Code Generation

In the OLAP world, there are two main ways to enhance query performance: [Vectorization](https://www.youtube.com/watch?v=yU1S8gwjGEw&list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&index=7) and [Code Specialization](https://www.youtube.com/watch?v=UPQ53hM6AWE&t=687s).

> ***Note**: These approaches are not mutually exclusive.*

The main idea of Vectorization is that instead of processing one record, the engine will process a batch (vector) of values.

> ***Note**: It has nothing to do with the vector database here.*

For the latter approach, the engine generates the code for each query to reduce the CPU instructions. In a system that doesn’t apply code specialization, each operator has to go through a condition block (switch) to check for the data type and then choose the appropriate function for the input data type. The code generation approach avoids this because all operators for a specific query are generated during execution.

[![](https://substackcdn.com/image/fetch/$s_!6n4b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef967d28-f342-4049-ad9a-0625ee65e4ce_643x356.png)](https://substackcdn.com/image/fetch/$s_!6n4b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef967d28-f342-4049-ad9a-0625ee65e4ce_643x356.png)

Image created by the author.

Redshift has applied the code generation approach. The system generates C++ code specific to the query plan and the executed schema. The generated code is then compiled, and the binary is delivered to the compute nodes for execution. Each compiled file is called a segment, which is a part of the physical query plan.

> ***Note**: We don’t debate [which approach is better](https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf) (vectorization or code specialization). Each will have its strengths and trade-offs.*

Despite applying the code generation for the rest of the execution steps, Redshift, Redshift adds a SIMD-vectorized data scan layer to the generated code. The vectorized scans function is precompiled (instead of being generated on the fly) and covers all the data types (with the Switch statements). This helps Redshift achieve better data scan performance and reduces the amount of [inline code](https://www.geeksforgeeks.org/inline-functions-cpp/) that must be compiled for each query.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Compilation Service

As we know from the above section, Redshift will use the compiled optimized objects for the query execution; these objects will be cached in the local cluster cache, so whenever the same or similar queries are executed, the compiled objects are reused, which results in faster runtime because Redshift doesn’t need to compile the query. This strategy only boosts the performance if the necessary compiled objects are in the local cache; if not, Redshift must generate the code, which incurs latency.

[![](https://substackcdn.com/image/fetch/$s_!XGno!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ad189b3-a0a3-4fe3-8607-39ef2145ea74_574x363.png)](https://substackcdn.com/image/fetch/$s_!XGno!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ad189b3-a0a3-4fe3-8607-39ef2145ea74_574x363.png)

Image created by the author.

[In 2020, Redshift introduced compilation services](https://aws.amazon.com/about-aws/whats-new/2020/06/amazon-redshift-now-delivers-better-cold-query-performance/) (correct me if I’m wrong about the milestone). The service uses separate resources instead of cluster resources. The compilation service caches the compiled objects in the external cache so that Redshift can serve the cache objects for multiple clusters.

Besides that, the compilation service leverages the parallelism of the external compilation service to compile the code faster if the desired objects are present in neither the local cache nor the external cache.

People behind Redshift observe that:

> *With the release of the compilation service, cache hits across the Amazon Redshift fleet have increased from 99.60% to 99.95%. In particular, 87% of the time, an object file was not present in a cluster’s local code cache, but Redshift found it in the external code cache.*

---

## CPU-Friendly Encoding

Redshift stores compressed data on disk. Besides generic compression algorithms such as [LZO](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Oberhumer) and [ZSTD](https://github.com/facebook/zstd), Redshift also supports optimized type-specific algorithms such as the [AZ64 algorithm](https://aws.amazon.com/about-aws/whats-new/2019/10/amazon-redshift-introduces-az64-a-new-compression-encoding-for-optimized-storage-and-high-query-performance/), which covers numeric and date/time data types. [Amazon introduced AZ64 in 2019; the compression is designed to achieve a high compression ratio and improved performance.](https://aws.amazon.com/about-aws/whats-new/2019/10/amazon-redshift-introduces-az64-a-new-compression-encoding-for-optimized-storage-and-high-query-performance/) AZ64 achieves a compression comparable to ZSTD but has a faster decompression rate.

A cool thing that needs to be mentioned here is that [the user can explicitly define the compression scheme on column granularity](https://docs.aws.amazon.com/redshift/latest/dg/c_Compression_encodings.html) besides the [AUTO option](https://docs.aws.amazon.com/redshift/latest/dg/c_Compression_encodings.html#:~:text=ENCODE%20AUTO%20is%20the%20default%20for%20tables.) (which lets Redshift automatically define the compression for your data). Moreover, after defining it, the user can change the compression scheme using the `ALTER TABLE` clause. I think this is an exciting feature; the user is the most understanding about the data, so allowing flexible compression options will help us have better control of how data is being stored; in return, the more power, the more responsibility; if we’re not careful, bad (compression) choice can hurt us with the performance and cost. As far as I know, Google does not allow this in BigQuery. I’m unsure whether Snowflake supports this; please comment if you know the answer.

---

## Adaptive Execution

Redshift’s query engine makes runtime decisions to improve performance by adjusting the generated code or runtime properties on the fly based on execution statistics. Using Bloom Filter during the execution is a bold example of Redshift’s dynamic optimizations.

> *This seems similar to BigQuery’s Dynamic Query Execution, which allows the system to change the number of workers or shuffle partitions at runtime.*

---

## AQUA for Amazon Redshift

[![](https://substackcdn.com/image/fetch/$s_!uEnL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8a72051-27c8-4645-b3eb-c928ce2fcd7a_662x389.png)](https://substackcdn.com/image/fetch/$s_!uEnL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8a72051-27c8-4645-b3eb-c928ce2fcd7a_662x389.png)

Image created by the author.

Advanced Query Accelerator (AQUA) is a multi-tenant service [introduced by Redshift in 2021](https://aws.amazon.com/about-aws/whats-new/2021/04/aws-announces-general-availability-of-aqua-for-amazon-redshift/). It serves as a caching layer for Redshift Managed Storage and an accelerator for complex scans and aggregations[.](https://aws.amazon.com/about-aws/whats-new/2021/09/aqua-amazon-redshift-ra3-xlplus-nodes/)

AQUA caches hot data (being accessed multiple times) for clusters on local SSDs, avoiding the latency of pulling data from a regional service like Amazon S3 and reducing the need to fill cache data in the cache storage in Redshift compute nodes. Redshift detects applicable scan and aggregation operations (from the input query) and pushes them to AQUA, which processes them with the cached data.

People from Amazon designed custom servers that leverage [AWS’s Nitro ASICs](https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-components-of-the-nitro-system.html) to accelerate compression and encryption while using [FPGAs](https://vi.wikipedia.org/wiki/FPGA) to boost the execution of filtering and aggregation operations.

---

## Query Rewriting Framework

Redshift also introduced a novel Query Rewriting Framework (QRF) with two goals:

* Rewriting rules for optimizing the execution order between unions, joins, and aggregations.
* Creating scripts for incremental materialized view query and maintenance. (which will be covered shortly)

---

## Storage

This section will explore Redshift's storage layer, from Redshift Managed Storage to concurrency control.

### Redshift Managed Storage (RMS)

> ***Note**: RMS is only available **in the RA3 cluster type and the serverless Redshift service**. RMS allows customers to scale computing and storage independently, thanks to data being offloaded from the compute node. Before the time of RMS, data was stored directly at the compute node.*

When choosing the RA3 cluster type or Redshift serverless, the data is stored in the RMS. This storage layer, based on Amazon S3, achieves a durability of [99.999999999% and 99.99% availability](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DataDurability.html) over a given year across multiple zones. RMS lets customers scale and pay for computing and storage independently because data is stored off the compute nodes. As RMS is based on S3, it also uses optimizations, such as data block temperature and blockage, to deliver high performance.

RMS is built on the [AWS Nitro System](https://aws.amazon.com/ec2/nitro/), which features high-bandwidth networking. RMS uses high-performance SSD-based local storage as a tier-1 cache. Redshift leverages techniques like automatic fine-grained data eviction and intelligent data prefetching to get the best from local SSD while achieving unlimited scalability of S3.

[![](https://substackcdn.com/image/fetch/$s_!w0Ma!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb638339-bf4e-408f-8f86-f8549950ce97_474x464.png)](https://substackcdn.com/image/fetch/$s_!w0Ma!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb638339-bf4e-408f-8f86-f8549950ce97_474x464.png)

Image created by the author.

RMS improves data access from S3 by using a prefetching mechanism that puts data blocks into memory and caches them to local SSDs. RMS tunes cache replacement to keep the relevant blocks locally available by tracking accesses to every block. Another layer of cache above the local SSDs is called the in-memory disk cache size; this layer can be dynamically changed to balance queries' performance and memory needs.

Data from a table is partitioned into data slices and stored as a logical chain of blocks. Each block ([1MB in size](https://d1.awsstatic.com/events/reinvent/2019/Deep_dive_and_best_practices_for_Amazon_Redshift_ANT418.pdf)) has a header that contains information like identity, table ownership, or slice information. Block is indexed using in-memory construct - *superblock*. According to the paper, a superblock is an indexing structure with characteristics similar to many filesystems. The query gets the necessary data blocks using zone maps to scan the superblock. In addition, the superblock also contains query tracking information for data blocks processed by running queries.

RMS synchronously commits transactions to Amazon S3, enabling multiple clusters to access consistent data. Data is written to S3 across different available zones by batching the write request. The concurrent clusters are brought up on demand for concurrent writes and reads rely on snapshot isolation.

When data is deleted from the main cluster, Redshift ensures it is no longer needed for any query and marks this data ready for the garbage collector in the object storage. As data is backed up in Amazon S3, it will not be lost if the SSDs fail.

Amazon S3 also stores the data snapshots. These snapshots act as restore checkpoints. Redshift supports restoring a whole cluster’s data as well as individual tables. Amazon S3 also serves as the source of truth for data sharing and machine learning.

### Separating Metadata from Data

Separating metadata from the data makes implementing processes like Elastic Resize and Cross Instance Restore easier. Both require moving metadata from one cluster configuration to another.

Elastic Resize allows customers to resize their clusters by adding nodes to improve performance or removing nodes to save costs. Cross-Instance Restore will enable users to restore snapshots taken from a cluster of one instance type to a cluster of different instance types or different numbers of nodes.

Here are the details of how these processes are implemented:

> * *Ensures that a copy of data is stored in Amazon S3.*
> * *Before any reconfiguration, Redshift takes the cluster’s data into account. It generates a plan of reconfiguring with minimal data movement, which also results in a balanced cluster.*
> * *Redshift records count and checksums on the data before reconfiguration and validate correctness after completion.*
> * *In case of restoration, Redshift records counts of the number of tables, blocks, rows, bytes used, and data distribution, along with a snapshot. It validates the counts and checksums after restoring before accepting new queries.*

Following the paper:

> *Elastic Resize and Cross-Instance Restore are heavily used features; customers use them for reconfiguration over 15,000 times a month. The failure rates are less than 0.0001%.*

### Beyond Local Capacity

Redshift leverages Amazon S3 for unlimited scalability and uses the local memory and SSD as caches. (like Snowflake).

The cluster maintains its working data set locally based on the information on the number of accesses of data blocks in each data block. The tiered cache is in charge of keeping track of this information. The cache has two-level:

[![](https://substackcdn.com/image/fetch/$s_!TVPR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d8c7f89-87c5-4d6f-8ba7-3f55dfde3f8e_610x493.png)](https://substackcdn.com/image/fetch/$s_!TVPR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d8c7f89-87c5-4d6f-8ba7-3f55dfde3f8e_610x493.png)

Image created by the author.

* **Low level**: This level stores cold data blocks. Every time the query accesses a data block, the system increases the block’s reference count.
* **High level**: the cold blocks become hot (after being accessed multiple times), and the policy promotes data blocks to a high level.

During eviction, the reference count of each block is decremented. When the reference count reaches zero, the block will be moved down to the low level or entirely evicted from the cache.

(Sounds like [Python object’s reference count](https://docs.python.org/3/c-api/refcounting.html), huh?)

RMS also uses the tiered-storage cache to refill the data on local SSDs after a cluster reconfiguration (e.g., Elastic Resize ). In a scenario like this, the compute nodes fill local disks with the data blocks most likely to be accessed by the customer queries.

Finally, Redshift has another cache layer called dynamic [disk-cache](https://en.wikipedia.org/wiki/Disk_buffer) to maintain the hottest blocks in the memory (being accessed many times). It also stores temporary blocks from a specific query. This cache automatically scales up when memory is available and scales down as the system runs out of memory.

### Incremental Commits

To save costs, RMS only captures the data changes compared to the last commit; these changes are later updated in the commit log. Redshift’s log-based commit protocol separates the in-memory structure from the persisted structure (disk); each superblock is a log of changes. From the paper:

> *The log-based commit improves commit performance by 40% by converting a series of random I/Os into a few sequential log appends.*

This log-structured metadata reduces the cost of features like concurrency scaling and data sharing, which access consistent data by applying the (global) log to their local superblock.

### Concurrency Control

Redshift implements [Multi-version Concurrency Control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control), which prevents the read process from being blocked by other read requests. The write request may only be blocked by other concurrent write requests.

Each transaction sees a consistent snapshot of the database established by all committed transactions before the time the transaction starts. From the paper, Amazon used a new design based on [Serial Safety Net (SSN) as a certifier on top of Snapshot Isolation](https://arxiv.org/pdf/1605.04292.pdf), which allows for ensuring strict serializability in a memory-efficient way because it only uses the summary information from prior committed transactions.

---

## Compute

Following Amazon, Redshift processes billions of queries every week. Users can choose the following options to scale the compute power on demand:

### Cluster Size Scaling

> *Elastic Resize*

[![](https://substackcdn.com/image/fetch/$s_!U_UO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c0b9840-5232-458c-97f4-cdf5f2eb2892_779x868.png)](https://substackcdn.com/image/fetch/$s_!U_UO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c0b9840-5232-458c-97f4-cdf5f2eb2892_779x868.png)

Image created by the author, [reference source](https://d1.awsstatic.com/events/reinvent/2019/Deep_dive_and_best_practices_for_Amazon_Redshift_ANT418.pdf).

This configuration allows customers to add or remove compute nodes from the cluster based on their needs. Instead of shuffling the data beneath, Elastic Resize re-distributes the data partition assignment (just metadata) to ensure data partitions are organized and balanced between nodes. After resizing, the compute note's local cache (SSD )is filled with the data from S3 according to the assignment information. (Redshift priorities hot data)

However, this can cause potential problems: after resizing, the number of data responsible for each node differs from the time before resizing, which can cause inconsistent query performance. Redshift deals with this by decoupling the compute parallelism (Number of workers, processes, threads) from the data partitions:

[![](https://substackcdn.com/image/fetch/$s_!j7e6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6af594e-19d8-4b12-bbc7-37a96e43988e_490x595.png)](https://substackcdn.com/image/fetch/$s_!j7e6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6af594e-19d8-4b12-bbc7-37a96e43988e_490x595.png)

Image created by the author.

* When computing parallelism < the number of data partitions: individual compute process will work on multiple data partitions.

* When computing parallelism > the number of data partitions, multiple compute processes share work from an individual data partition.

Redshift achieves this thanks to work units being sharable.

> ***Note**: When I researched more on Redshift’s document, I discovered a new concept from Redshift: [Node Slices](https://docs.aws.amazon.com/redshift/latest/dg/c_high_level_system_architecture.html#:~:text=requiring%20any%20action.-,Node%20slices,-A%20compute%20node). Each slice has a portion of the node's memory and disk space. Node slice can be considered a virtual compute node, acting as an abstraction for data-parallel processing. The data will be distributed to node slices using the distribution key. I can’t find the concept in the paper, or the paper might use the term “**compute parallelism**“ to refer to the slice (if you know this, please comment below). Another thing to note: this differs from the Data Slice concept above in the RMS section.*

### Concurrency Scaling

This configuration helps the user deal with one of the OLAP system's classic challenges: concurrency. It will dynamically scale out whenever users need more concurrency capability from Redshift.

[![](https://substackcdn.com/image/fetch/$s_!Kx8N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F742dbb86-68cc-44dc-b253-4633b900398f_762x481.png)](https://substackcdn.com/image/fetch/$s_!Kx8N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F742dbb86-68cc-44dc-b253-4633b900398f_762x481.png)

Image created by the author.

With Concurrency Scaling, users maintain a single cluster act endpoint for query submission. When Redshift detects that resources are fully utilized and new queries keep coming, Redshift automatically adds additional Concurrency Scaling compute clusters. It routes the queries waiting to be processed to these clusters. Furthermore, the added cluster fills the local disk with data from S3.

### Compute Isolation

Redshift allows customers to share data across different Redshift compute clusters and AWS accounts. Compute clusters can access a single data source, eliminating the need to develop ETL pipelines or incur the cost of copying data.

Users can share data at many levels, from the schemas and tables to the user-defined functions (UDF). To share data with others, the data’s owner (producer) first creates the data share and grants access to the consumers. Redshift using IAM policies and metadata to implement authentication and authorization.

Consumer queries shared objects using metadata requests. The request can be served only when the consumers are authorized to access the shared data. Each request goes through a directory service and proxy layer. The proxy authenticates and authorizes requests and routes metadata requests to the appropriate producer. After receiving the metadata on the consumer side, it reads the desired data from the RMS and processes the query. The cache process when querying shared data is unchanged: the shared data is cached on the cluster, and in subsequent queries, it will read data locally.

---

## Automated tuning and operations

From the first days, Redshift simplified many aspects compared to the traditional data warehouse system (building local servers and data centers). Still, some maintenance and tuning tasks require an experienced database administrator: the users must explicitly schedule the vacuum process or decide on the distributed or [sort key](https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html) to gain a performance boost.

At the moment, Redshift runs common tasks like vacuuming, analyzing, or refreshing materialized views behind the scenes without any performance impact on customer workloads. Redshift observes and analyzes user workloads and identifies opportunities for performance enhancement, for example, pointing out the optimal distribution and sorting key for the workload and applying it automatically.

Furthermore, Redshift employs an advanced forecasting mechanism to make additional nodes available as soon as possible through the warm pool, [quite similar to Snowflake's pre-warm worker pool](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf)) for node failures or concurrency scaling; this leads to query latency and downtime reduction. Finally, Amazon Redshift offers a serverless option (like Google BigQuery) that is easy to run and scale without user intervention.

### Automatic Table Optimizations

Optimizing properties like distribution and sort keys allows users to optimize the workload’s performance. The distribution key is a table property that indicates how that table’s data is distributed all over the cluster, helping the system allocate parallelism resources efficiently. The sort key organizes data based on one or more columns to leverage the zone map indexing. A zone map is an indexing structure that stores the min-max of a data unit, which is very useful for skipping unnecessary data; sorting the data can make use of a zone map efficiently. (Does this sound like [BigQuery clustering](https://www.google.com/search?q=bigquery+clustering&oq=bigquery+clustering&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg70gEIMjg4MmowajSoAgCwAgA&sourceid=chrome&ie=UTF-8)?)

[![](https://substackcdn.com/image/fetch/$s_!gkLz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1afc9075-8b75-4afa-9247-8451c2730310_591x282.png)](https://substackcdn.com/image/fetch/$s_!gkLz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1afc9075-8b75-4afa-9247-8451c2730310_591x282.png)

Image created by the author.

In the past, these keys are explicitly defined by the user. Now, Redshift auto the process through [Automatic Table Optimization (ATO)](https://docs.aws.amazon.com/redshift/latest/dg/t_Creating_tables.html). ATO analyzes the workload to recommend optimal distribution and sort keys. To generate the recommendation, it periodically collects query execution metadata like the optimized query plans, cardinalities, and predicate selectivities.

The recommended keys with goals:

* **Distribution key**: minimizing the cost of data movement, the system needs to make the recommendation by examining all tables in a specific workload.
* **Sort key**: reducing the amount of data that needs to be read from the disk.

After having the recommendations, Redshift offers customers two options:

* Manual applying through the console.
* Automatic background workers apply the recommendations. This worker will apply the configuration incrementally and run the job only when the cluster is not too busy.

### Automatic Workload Management

> *Redshift applies machine learning (ML) to predict resource requirements to improve response time and throughput.*

[Redshift’s Automatic Workload Manager (AutoWLM)](https://docs.aws.amazon.com/redshift/latest/dg/automatic-wlm.html) is responsible for admission control, scheduling, and resource allocation. After receiving the query, AutoWLM converts the execution plan and optimized statistics into a vector format. Then, Redshift inputs the vector into the ML model to predict the compilation and execution time. Redshift uses the model’s result to place the query in the queue: based on the predicted execution time, Redshift will schedule short queries before long ones. The query processes to the execution phase only when the estimated memory need (also predicted by the model) can be satisfied by the available memory pool. Moreover, AutoWLM can throttle the concurrency rate to avoid query latency when it detects resource utilization is too high.

AutoWLM employs a [weighted round-robin](https://en.wikipedia.org/wiki/Weighted_round_robin) mechanism for scheduling higher-priority queries more often than low-priority ones. Moreover, higher-priority queries that need to meet some SLAs will be favored with a more significant share of hardware resources. Redshift divides CPU and I/O in [exponentially decreasing](https://www.quora.com/What-does-decreasing-exponentially-mean) portions when queries with different priorities are running at the same time. This boots higher-priority queries exponentially as compared to lower-priority ones.

If a higher priority query comes after a lower running priority, AutoWLM will redeem resources from the lower priority query to make room for the higher priority one. To prevent resource exhaustion in lower-priority queries, the probability of the resource being taken back by the system will reduce each preemption. As a result, when the resources are exhausted, Redshift queues lower-priority queries to give higher-priority resources.

### Query Predictor Framework

As said in the above section, AutoWLM uses a machine-learning model to predict metrics like memory consumption or execution time. The Redshift’s Query Predictor Framework is responsible for maintaining these models. The framework runs in the Redshift cluster, collects data, trains with the [XGBoost](https://en.wikipedia.org/wiki/XGBoost) model, and outputs the result when needed. Running a framework on the cluster helps quickly adapt to changing workloads. The code compilation service mentioned above also uses the query predictor framework for optimization.

### Materialized Views

[![](https://substackcdn.com/image/fetch/$s_!Aft3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638ef15d-5fe4-49a0-834c-7252e5008ae1_378x386.png)](https://substackcdn.com/image/fetch/$s_!Aft3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638ef15d-5fe4-49a0-834c-7252e5008ae1_378x386.png)

Image created by the author.

Both [SQL View](https://en.wikipedia.org/wiki/View_(SQL)) and [Materialize View (MV)](https://en.wikipedia.org/wiki/Materialized_view) provide a way to represent the result of a query as if it were a table. Unlike View, which does not store data in the disk, MV persists data physically, speeding the execution time when users query the data from the MV. Redshift automates MV management in the following ways:

* Incrementally maintaining filter, select, group by, and join in reflecting changes on base tables.
* Automate the maintenance time: Redshift detects which MV needs to be refreshed. This is done using two factors: the utility of a materialized view in the query workload and the materialized view refreshing cost.
* Auto-rewriting the query over the MV to achieve optimal performance. The incremental maintenance and the query rewriting use the framework mentioned in the “Query Rewriting Framework“ section.

### Smart warm pool

> *Does “smart“ always refer to a system backed by machine learning or some AI models?*

In the cloud era, hardware failure is no exception anymore. To prevent performance downgrade due to machine failure, Redshift uses a smart warm pool architecture (compute machines are warm-up before being served). This architecture allows efficiency in many processes: failed node replacement, cluster resumption, automatic concurrency scaling…

[![](https://substackcdn.com/image/fetch/$s_!vkJB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73d15ee3-13ed-43fd-bc91-a91ca8f051b4_943x480.png)](https://substackcdn.com/image/fetch/$s_!vkJB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73d15ee3-13ed-43fd-bc91-a91ca8f051b4_943x480.png)

Image created by the author.

Warm pools are a group of EC2 compute instances with pre-installed software and networking configurations. A distinct warm pool is located in each AWS availability zone for each region. Keeping the operations low latency requires a high hit rate when a node is acquired from the warm pool. Redshift uses a machine learning model to forecast the number of needed EC2 instances for a given warm pool at any time. The system adjusts warm pools dynamically in each region and availability zone to save infrastructure costs.

---

## Integrations

As AWS's native service, Redshift benefits significantly from the Amazon Cloud Service Ecosystem. Here are some of Redshift’s integration options

* [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html) allows users to query data directly in S3. This feature provides massive scale-out processing, performing scans and aggregations of data in Parquet, Text, ORC, and AVRO formats.
* Redshift ML with [Amazon Sagemaker](https://aws.amazon.com/pm/sagemaker/?gclid=CjwKCAiArfauBhApEiwAeoB7qMVDVvq19yqIYeW4yEmRoCdAcRYz0vRbqnuc2INyUlWGvLDhboSEuxoCyt4QAvD_BwE&trk=b92e5bb5-847d-49ae-bd86-21239cc9ac5e&sc_channel=ps&ef_id=CjwKCAiArfauBhApEiwAeoB7qMVDVvq19yqIYeW4yEmRoCdAcRYz0vRbqnuc2INyUlWGvLDhboSEuxoCyt4QAvD_BwE:G:s&s_kwcid=AL!4422!3!532425958059!e!!g!!amazon%20sagemaker!11543056255!112002968389) makes it easy to train machine learning models and perform prediction using SQL. Behind the scenes, Redshift ML leverages Amazon SageMaker, an AWS fully managed machine learning service. After a model has been trained, Redshift exposes it with SQL function, and the user can use directly using SQL
* [Redshift Federated Query](https://docs.aws.amazon.com/redshift/latest/dg/federated-overview.html) lets Redshift connect directly to the customer’s OLTP database (Postgres, MySQL,…) to fetch data. This convenience removes the need for the ETL pipeline to extract data from the OLTP source.
* [Super Schemaless Processing](https://docs.aws.amazon.com/redshift/latest/dg/r_SUPER_type.html)**:** SUPER semistructured type can contain schemaless, nested data. A value of SUPER type can consist of Redshift string and number scalars, arrays, and structs. Using SUPER type, users don’t need to define schema beforehand. After the semistructured data are stored in SUPER data value, users can query it without imposing a schema. Redshift’s dynamic typing can detect nested data without the schema.
* [Redshift with Lambda](https://docs.aws.amazon.com/redshift/latest/dg/udf-creating-a-lambda-sql-udf.html)**:** Redshift supports user-defined functions (UDFs) backed by AWS Lambda code. The Lambda UDF can be written in Java, Go, PowerShell, Node.js, C#, Python, and Ruby.

---

## Outro

Few, quite a long article, right? This article is my longest one.

Despite the “8 hours” mentioned in the title, I spent nearly a week finishing this blog. The Redshift paper delivers many new things, making me struggle a little. Moreover, this is the first time I have researched an OLAP system that chooses the code specialization approach to optimize the query engine (all the systems I studied before use vectorization: BigQuery, Snowflake, DuckDB).

Besides the code specialization, Redshift's features worth mentioning are compilation services, Redshift management storage, and the application of machine learning for database operation. Furthermore, The Redshift warm pool architecture is similar to Snowflake’s pre-warm pool; both solutions try to minimize the latency of compute scaling, but with Redshift, the solution leverages machine learning models to operate.

At the moment, I see Redshift is the only system that explicitly says it uses machine learning for behind-the-scenes operations; neither Snowflake nor BigQuery mentioned this. (Please correct me if I miss something)

It’s time to say goodbye now. See you next week!

---

## **References**

***Paper**: [Amazon Redshift Re-invented - 2022](https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf)*

***Document**: [Amazon Redshift Official Document](https://docs.aws.amazon.com/redshift/)*

***PowerPoint Presentation**: [Deep dive and best practices for Amazon Redshift](https://d1.awsstatic.com/events/reinvent/2019/Deep_dive_and_best_practices_for_Amazon_Redshift_ANT418.pdf)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-another-8-hours-understanding/comments)

It might take you 5 minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
