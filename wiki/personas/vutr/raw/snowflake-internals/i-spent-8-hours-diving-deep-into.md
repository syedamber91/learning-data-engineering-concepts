---
title: "I spent 8 hours diving deep into Snowflake (again)."
channel: vutr
author: "Vu Trinh"
published: 2024-09-28
url: https://vutr.substack.com/p/i-spent-8-hours-diving-deep-into
paid: false
topics: ["Data Engineering", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse"]
tags: [https, auto, snowflake, image, storage, node]
---

# I spent 8 hours diving deep into Snowflake (again).

*Virtual Warehouse, Intermediate Storage, Cache and Remote Storage*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-diving-deep-into)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!or5p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c623efa-ab6f-48ac-adf7-d8c178d0d45a_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!or5p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c623efa-ab6f-48ac-adf7-d8c178d0d45a_2000x1429.png)

Image created by the author.

---

## Intro

Looking back on things we've learned with a fresh perspective gained through new experiences over time is a great way to solidify knowledge, at least for me. At the beginning of 2024, I had the opportunity to research and write about Snowflake—one of the most powerful cloud data warehouse solutions. This week, I decided to revisit Snowflake’s internals to see if I missed anything and to extract any new insights from my previous work.

The article is structured as follows: first, we will explore Snowflake's background, then move on to its overall architecture, followed by a detailed look at each component—computing, storage, and cloud services.

---

## Background

Snowflake was founded in July 2012 by [Benoit Dageville](https://www.linkedin.com/in/benoit-dageville-3011845/) and [Thierry Cruanes](https://www.linkedin.com/in/thierry-cruanes-3927363/), two ex-Oracle engineers, and Vectorwise co-founder [Marcin Zukowski](https://www.linkedin.com/in/marcinzukowski/). The platform launched on Amazon Web Services (AWS) in 2014 and expanded to support Microsoft Azure in 2018 and Google Cloud in 2019.

In the past, shared data centers were the norm, but the rise of cloud computing changed everything. Services like Amazon Web Services, Google Cloud, and Microsoft Azure have made many organizations rethink the management of software in-house.

It wasn’t just software that evolved—data management did, too. Traditional data warehouses (DWHs) operated on static local clusters, where data volume and structure were predictable. However, the big data era introduced enormous, unstructured data flows from diverse sources.

Traditional DWHs struggled to keep pace, leading to the birth of big data platforms like Spark and Hadoop. However, they required significant engineering effort to implement. Snowflake's creators saw the need for a solution that:

* Replaced traditional data warehouses.
* Leveraged the scalability of cloud platforms.

---

## Overview Architecture

[![](https://substackcdn.com/image/fetch/$s_!Y3x8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d83e7e1-4d42-4597-9026-b1cdcfb32e50_1024x996.png)](https://substackcdn.com/image/fetch/$s_!Y3x8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d83e7e1-4d42-4597-9026-b1cdcfb32e50_1024x996.png)

Image created by the author.

At the time, the shared-nothing architecture was the dominant choice for traditional data warehouse design, mainly due to the performance advantage of co-locating storage and computing. Table data is horizontally distributed across the nodes’ local disks in this setup.

However, this architecture comes with a few drawbacks:

* **Node changes:** When a node fails or is resized, a large amount of data must be reshuffled. This means redistributing data from the failed node to other nodes or rebalancing data when adding a new node.
* **Upgrading:** Performing online upgrades—where each node is updated one at a time without system downtime—is difficult due to the tight coupling of components.

Given these limitations and the growing need for flexibility in cloud environments, the Snowflake team decided to build a new OLAP database in C++. Their solution separates computing and storage into two loosely coupled, independent services.

For storage, Snowflake relies on services like [Amazon S3](https://aws.amazon.com/s3/), [Google Cloud Storage](https://cloud.google.com/storage?hl=en), or [Azure Blob Store](https://azure.microsoft.com/en-us/products/storage/blobs). Compute power comes from Snowflake’s proprietary shared-nothing engine, which uses cloud virtual machines and aggressively uses local disks for data caching. Caching significantly enhances query performance by reducing data access latency from object storage.

Unlike Photon from Databricks or Dremel from Google, Snowflake avoids shuffle-based execution. Instead, workers can exchange data directly with one another.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## **The computing**

[![](https://substackcdn.com/image/fetch/$s_!sK9v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e45d247-c314-4fbb-9a22-3e11cc6c8d80_932x926.png)](https://substackcdn.com/image/fetch/$s_!sK9v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e45d247-c314-4fbb-9a22-3e11cc6c8d80_932x926.png)

Image created by the author.

Snowflake introduced the concept of Virtual Warehouses (VW), essentially clusters of cloud virtual machine instances. Each instance in a cluster is referred to as a worker node.

As a data-as-a-service provider, Snowflake hides users from complex worker configurations. They offer Virtual Warehouses in abstract “T-shirt sizes,” ranging from X-Small to XX-Large, simplifying service management and pricing on cloud platforms.

> *This abstraction is quite similar to [BigQuery’s “slot”](https://cloud.google.com/bigquery/docs/slots) concept.*

### Isolation

Virtual Warehouses (VWs) are essentially virtual machines. Since data is stored in S3, VWs are stateless, allowing them to scale up or down on demand without affecting the data. Each query runs on exactly one VW, and worker nodes are not shared across VWs, ensuring performance isolation. When a new query arrives, each worker node in a VW spawns a new worker process, which lives only for the duration of its associated query.

[![](https://substackcdn.com/image/fetch/$s_!FYRu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e45479f-3d76-484e-8549-2e25c87ea047_1360x738.png)](https://substackcdn.com/image/fetch/$s_!FYRu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e45479f-3d76-484e-8549-2e25c87ea047_1360x738.png)

Image created by the author.

> *You can think of it like a Spark Application: when submitted to the cluster manager, the physical workers spawn executor processes to handle the the Spark job.*

Snowflake does not support partial retries—if a query fails, it must be rerun from the beginning.

Each user can run multiple VWs, each capable of handling various concurrent queries. Since data is stored remotely in object storage, all VWs have access to the same shared tables without needing to copy the data physically.

### **Execution engine**

Snowflake uses a columnar storage and execution engine. Columnar storage uses [CPU caches](https://en.wikipedia.org/wiki/CPU_cache) and [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instructions better while providing more opportunities for lightweight compression.

In addition, Snowflake employs vectorized execution, processing data in batches of thousands of rows in column format. This differs from traditional databases like PostgreSQL or MySQL, which process data one row at a time.

Unlike systems such as MapReduce, Snowflake's vectorized approach avoids materializing intermediate results. Instead, data is processed pipelined, handling batch rows at a time. This method, pioneered by [VectorWise (MonetDB/X100)](https://www.cidrdb.org/cidr2005/papers/P19.pdf), significantly reduces I/O and boosts cache efficiency.

[![](https://substackcdn.com/image/fetch/$s_!Ze7_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8213b478-aa41-4ad4-95da-b5a3d7fbdf4f_1330x746.png)](https://substackcdn.com/image/fetch/$s_!Ze7_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8213b478-aa41-4ad4-95da-b5a3d7fbdf4f_1330x746.png)

Image created by the author.

Additionally, Snowflake's push-based execution allows relational operators to push results downstream rather than waiting for operators to pull data.

This push-based system enhances cache efficiency by eliminating control flow from tight loops. It enables Snowflake to handle DAG-shaped plans efficiently and creates more opportunities for sharing and pipelining intermediate results.

> *DuckDB also uses a push-based vectorized model.*

### Cache

Each worker node in a VW maintains a local cache of table data on its disk, composed of previously accessed table files (S3 objects). Instead of caching entire files, the cache stores file headers and specific columns, as queries only download the necessary columns.

This cache persists for the lifetime of the worker node and is shared among all queries running on that node. The cache operates under a simple least-recently-used (LRU) replacement policy.

Snowflake uses consistent hashing to improve cache hit rates and minimize redundant caching across multiple worker nodes within a VW. This process assigns table files to worker nodes based on file names, ensuring that queries accessing the same data will likely hit the same node.

> *Consistent hashing is a technique that distributes data across multiple servers to minimize reorganization when servers are added or removed. Servers and data (like keys) are placed on a virtual circle based on their hash values, and each key is assigned to the first server it encounters, moving clockwise. When a server joins or leaves, only a tiny portion of the keys need to be reassigned.*

Snowflake will schedule the task that operates on a persistent data file to the node on which its file consistently hashes. This is called the locality-aware scheduling mechanism.

[![](https://substackcdn.com/image/fetch/$s_!V420!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a6a2e19-8b60-4813-9820-14c76158e8b0_1596x876.png)](https://substackcdn.com/image/fetch/$s_!V420!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a6a2e19-8b60-4813-9820-14c76158e8b0_1596x876.png)

Image created by the author.

Snowflake takes a "lazy" approach to consistent hashing when the number of worker nodes changes due to resizing or node failures, avoiding immediate data reshuffling. It achieved this by exploiting the fact that a copy of cached data is stored at a remote persistent data store. Let’s look at an example here for a better understanding:

[![](https://substackcdn.com/image/fetch/$s_!0a4Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10797f1f-1356-4d2a-ae67-2381af774b80_1202x1088.png)](https://substackcdn.com/image/fetch/$s_!0a4Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10797f1f-1356-4d2a-ae67-2381af774b80_1202x1088.png)

Image created by the author.

* At t1, the cluster has four nodes: files 1–4 are stored on nodes 1–4 while file 5 is placed on node 1 (node 1 has two files, 1 and 5, while other nodes have one file for each node) and five tasks: Task 1–4 are placed on node 1–4, and task 5 is placed on node 1 (because node 1 also has file 5)
* At time *t1* > *t*0, a node 5 is added to the cluster. Then, instead of immediately reshuffling the files (resulting in File 5 being moved from node 1 to node 5), Snowflake will wait until Task 5 is executed again. When task 5 is scheduled, Snowflake will schedule it on node 5 because consistent hashing will now place file 5 on that node. At this time, file 5 will be read by node 5 directly from the remote persistent store and cached locally. File 5 on node 1 will no longer be accessed and will eventually be evicted from the cache.

### Intermediate Result

Intermediate data generated by query operators only needs to persist during the query’s life and must be accessed with low latency and high throughput. Snowflake stores intermediate data alongside the cache data in worker nodes. It prioritizes the space for the immediate data over cache data.

[![](https://substackcdn.com/image/fetch/$s_!X21-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3c97af4-11fd-4b48-8601-16e264595787_1278x1114.png)](https://substackcdn.com/image/fetch/$s_!X21-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3c97af4-11fd-4b48-8601-16e264595787_1278x1114.png)

Image created by the author.

To meet these requirements, Snowflake built an ephemeral storage system to handle intermediate data. This system is co-located with compute nodes in Virtual Warehouses (VWs). Two key design decisions were made for Snowflake's ephemeral storage system:

[![](https://substackcdn.com/image/fetch/$s_!6a7V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9fcdf278-3d48-4f27-9816-0b91f04705fa_1040x984.png)](https://substackcdn.com/image/fetch/$s_!6a7V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9fcdf278-3d48-4f27-9816-0b91f04705fa_1040x984.png)

Image created by the author.

* **Memory and SSD Usage:** Intermediate data is first written to local memory. When memory is full, it spills over to local SSDs. While in-memory storage offers better performance, storing hundreds of GBs or TBs of intermediate data entirely in memory is not feasible.
* **Spilling to Remote Storage:** If local SSDs are at full capacity, data spills to remote storage. This prevents overloading other compute nodes and simplifies tracking intermediate data locations, ensuring the system remains thin and efficient.

### File Stealing

Snowflake uses a technique called file stealing to address performance imbalances, or "skew," which occur when certain worker nodes, known as stragglers, process data more slowly than others.

[![](https://substackcdn.com/image/fetch/$s_!8qcj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff897318a-d576-4467-995b-c60fbeec695d_1154x1146.png)](https://substackcdn.com/image/fetch/$s_!8qcj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff897318a-d576-4467-995b-c60fbeec695d_1154x1146.png)

Image created by the author.

When a worker finishes scanning its assigned files, it can request additional files from other worker nodes. If a peer has many files left, it will transfer ownership of one file to the requesting node, which downloads the file directly from S3. This approach ensures that file stealing doesn't burden slower nodes and keeps the system running efficiently.

---

## Storage

[![](https://substackcdn.com/image/fetch/$s_!_R3Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c70fec4-870e-4ad2-9035-e5f889e4cfb9_1712x822.png)](https://substackcdn.com/image/fetch/$s_!_R3Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c70fec4-870e-4ad2-9035-e5f889e4cfb9_1712x822.png)

Image created by the author.

When it came to storage, the team behind Snowflake had to choose between using object storage like S3 or building their solution on HDFS (or similar systems). They experimented with S3 and, despite its unpredictable performance, concluded that S3 excelled in availability and durability. Ultimately, they opted for object storage like S3, focusing on improving the performance of local caching in the Virtual Warehouse and optimizing it with their proprietary storage format.

Table data is horizontally partitioned into large, immutable files, similar to blocks or pages in a traditional database.

[![](https://substackcdn.com/image/fetch/$s_!D2rk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F424a73fa-0bfe-483a-80f4-d362807c4897_804x1032.png)](https://substackcdn.com/image/fetch/$s_!D2rk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F424a73fa-0bfe-483a-80f4-d362807c4897_804x1032.png)

Snowflake’s proprietary file format is similar to the PAX file format. Image created by the author.

Column values are grouped together and heavily compressed in each file, equivalent to the PAX file format (also known as the hybrid file format, which is also implemented in Parquet).

> *It's important to note that when Snowflake was built in 2012, formats like Parquet and ORC, which were introduced in 2013, did not yet exist.*

The file contains a header, which includes metadata such as the offsets for each column. Since S3 supports retrieving specific file ranges, queries only need to download the file headers and the required columns.

Traditionally, databases used indexes like B+Tree to reduce the data search space, but this approach falls short in OLAP workloads. While indexes work well for random or point access (OLTP), OLAP workloads typically require scanning large volumes of data but only a subset of columns.

To address this, Snowflake uses min-max-based pruning, storing the minimum and maximum values for each chunk of data. Based on these values, queries can skip unnecessary chunks. For example, if a query needs data with values between 8 and 15, chunks with a max of 7 or a min of 16 are excluded from scanning.

> *Min-max-based pruning is widely used in OLAP-related file/table formats, including Parquet files, Capacitor (BigQuery's proprietary format), Iceberg, Delta Lake, DuckDB’s proprietary format, and many others.*

---

## Cloud service

Besides the storage and computing layer, Snowflake’s architecture has another component called *cloud services,* a collection of services like access control, query optimizer, transaction manager, etc. Internally, Snowflake uses [FoundationDB](https://en.wikipedia.org/wiki/FoundationDB) to manage the data catalog.

> *[FoundationDB](https://en.wikipedia.org/wiki/FoundationDB) is a free and open-source multi-model distributed NoSQL database.*

The cloud Services layer is heavily multi-tenant. Each service in this layer is long-lived and shared across users, which improves utilization, reduces administrative overhead, and also allows better scalability than in traditional architectures where every user has an entirely private system. Every service is replicated for high availability; in the scenario where individual service nodes fail, it does not cause data loss.

### Query management and optimization

All user queries pass through the Cloud Services layer, where the initial stages of the query lifecycle are managed—such as parsing, object resolution, access control, and plan optimization.

Snowflake’s query optimizer uses a Cascades-style approach with top-down, cost-based optimization. The statistics required for optimization are automatically maintained during data loads and updates. Snowflake collects statistics at multiple levels:

* Table: number of rows, size in bytes
* Column level: min/max, null and distinct count

Snowflake also supports runtime adaptivity. Runtime adaptivity optimization refers to the system's ability to make real-time adjustments during query execution based on current conditions.

Unlike traditional static optimization, which relies heavily on pre-execution plans, runtime adaptivity allows the system to modify decisions dynamically as data is processed, such as changing join strategies or adjusting resource allocation based on intermediate results or workload imbalances.

> *This approach improves performance, particularly in unpredictable data volumes or query patterns. Google BigQuery, Databricks, and other systems also employ this approach.*

During execution, Cloud Services continuously monitors the query's state, gathering performance data and detecting node failures. All query information and statistics are stored for audit and performance analysis, and users can easily monitor past and ongoing queries.

### Concurrency control

Snowflake decided to implement the ACID constraint using Snapshot Isolation (SI). As of its start, the transaction will see the database's consistent SI.

SI is implemented on top of [multi-version concurrency control (MVCC)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control), which means a copy of every change on a desired table is preserved for some time. Making copies of every change is an obvious choice because table data is immutable in object storage; changes can only be made by creating a whole new file that includes the change.

This means modifying data in the table will produce a newer version by adding or removing files relative to the previous version. File additions and removals are tracked in the metadata storage (FoundationDB), which helps Snowflake check which set of files belongs to a specific table version.

---

## Outro

Thank you for reading this far. In this article, we explored Snowflake's internals, covering its Virtual Warehouse abstraction, execution engine, query planning, how the cache is distributed among workers, and its ephemeral and remote storage design.

Now, see you in the next article.

---

## Reference

*[1] Andy Pavlo, [S2024 #19 - Snowflake Data Warehouse Internals (CMU Advanced Database Systems)](https://www.youtube.com/watch?v=NhWp1bTG0Cw&t=1875s) (2024)*

*[2] Snowflake Computing, [The Snowflake Elastic Data Warehouse](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf) (2016)*

*[3] Snowflake Computing, [Building An Elastic Query Engine on Disaggregated Storage](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf) (2020)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-8-hours-diving-deep-into/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
