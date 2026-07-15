---
title: "I spent another 6 hours understanding the design principles of Snowflake. Here's what I found"
channel: vutr
author: "Vu Trinh"
published: 2024-02-10
url: https://vutr.substack.com/p/i-spent-another-6-hours-understanding
paid: false
topics: ["Data Engineering", "Apache Spark", "Snowflake", "BigQuery", "Data Warehouse"]
tags: [snowflake, https, storage, cloud, auto, table]
---

# I spent another 6 hours understanding the design principles of Snowflake. Here's what I found

*All insights from Snowflake academic paper in 2016*

> Source: [Open post](https://vutr.substack.com/p/i-spent-another-6-hours-understanding)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]]

---

> *My name is Vu Trinh, a data engineer.*
>
> *I’m trying to make my life less boring by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

---

[![](https://substackcdn.com/image/fetch/$s_!nqHI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd87e6c73-0ae0-417d-a444-1e15b0b37208_1393x994.png)](https://substackcdn.com/image/fetch/$s_!nqHI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd87e6c73-0ae0-417d-a444-1e15b0b37208_1393x994.png)

Imaged created by the author

> *Table of contents:*
>
> * *Snowflakes Disaggregation of Storage and Compute*
> * *The unlimited storage “pool “, the virtual warehouses, and the cloud services*
> * *Data skipping*
> * *Semi-structured data*
> * *Snapshot Isolation*

---

## Intro

The amount of times I worked with cloud data warehouses is distributed like this (just the estimation) :

* 5% [Redshift](https://aws.amazon.com/redshift/)
* 95% [BigQuery](https://cloud.google.com/bigquery?hl=en)

I spent my whole data engineer career with BigQuery. This makes me sometimes wonder how other cloud warehouse solutions out there work. Is it the same behind-the-scenes with BigQuery and just exposing different interfaces?

I pick up one of the most famous popular cloud data warehouse solutions to answer that question: [Snowflake](https://www.snowflake.com/en/). This article notes all the insights I self-observed after spending the weekend reading the Snowflake paper: [The Snowflake Elastic Data Warehouse](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf).

***Disclaimer:** I have never used Snowflake before, and all the insights below are derived from an academic paper in 2016; some features and characteristics of Snowflake might have been changed and improved. However, the core principle of design should still be preserved.*

---

## History

> *From [Wikipedia](https://en.wikipedia.org/wiki/Snowflake_Inc)*

Snowflake was founded in July 2012 and promises to offer cloud-based data storage and analytics service, generally termed "data-as-a-service.” The first cloud where Snowflake runs is Amazon (2014); it then supported operating on Microsoft Azure 2018 and Google Cloud in 2019.

---

## The reason behind the birth of Snowflake

At the time before the cloud, software was usually developed and maintained on local servers and shared data centers. The Cloud era changed everything. [Software as service](https://en.wikipedia.org/wiki/Software_as_a_service#:~:text=Software%20as%20a%20service%20(SaaS%20/s%C3%A6s/%5B1%5D)%20is%20a%20software%20licensing%20and%20delivery%20model%20in%20which%20software%20is%20licensed%20on%20a%20subscription%20basis%20and%20is%20centrally%20hosted.%5B2%5D%5B3%5D%20SaaS%20is%20also%20known%20as%20on%2Ddemand%20software%2C%20web%2Dbased%20software%2C%20or%20web%2Dhosted%20software.%5B4%5D) solutions hosted by Amazon, Google Cloud, or Microsoft Azure made people ask themself if they need to self-handle software on their side.

Not only the software but also the data change. Traditional DWHs are run on local, static clusters where the data's structure, volume, and rate are all relatively predictable and well-known. But in the era of big data, things are different: data grows tremendously in size and usually shows up without its definition beforehand (schema). Initially, data sources usually came from within the organization, but now, data can come from… everywhere.

Traditional DWHs need some help. Big data platforms like Spark or Hadoop have been developed to solve this problem, but it has come with a disadvantage: it requires significant engineering effort to roll out and use. So, the people behind Snowflake see the need for a solution that:

* *can replace traditional data warehouses*
* *can also leverage the power of cloud vendors: scalability.*

That’s why Snowflake was born.

One thing to note here is that the cloud can support unlimited scalability. Still, this advantage can only be leveraged when the software can scale elastically over the pool of resources in the cloud. If Snowflake was designed to run on the cloud, its internal architecture must allow efficient scalability.

> *Snowflake was not based on something other than Hadoop, PostgreSQL, or the like. The processing engine and most other parts have been developed from scratch.*

Let's move on to deep dive into Snowflake’s internal.

---

## Storage + Compute

### The shared-nothing architecture

[![](https://substackcdn.com/image/fetch/$s_!J3m-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F891e1f26-b6c2-40c5-9c89-04e59bc0480a_905x569.png)](https://substackcdn.com/image/fetch/$s_!J3m-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F891e1f26-b6c2-40c5-9c89-04e59bc0480a_905x569.png)

Imaged created by the author

At that time, shared-nothing architecture was dominant in the design of traditional data warehouses because of the performance benefit of the co-location of storage and computing. In this architecture, every node has its local disk, the data (from the table) is horizontally distributed across nodes, and each node is only responsible for that data.

Despite the performance gain, it has some disadvantages:

* *Node member changes: when a node fails or resizes, it will cause a large amount of data to be reshuffled (move data from node fail and distribute to other nodes or balance the amount of data when a new node arrives )*
* *Upgrade: Implementing online upgrades such that one node after another is upgraded without system downtime is very hard because everything is tightly coupled.*

### Disaggregation of Storage and Compute

[![](https://substackcdn.com/image/fetch/$s_!mTMm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e34bfca-db5f-4556-a09a-23be0d6f3f8f_871x584.png)](https://substackcdn.com/image/fetch/$s_!mTMm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e34bfca-db5f-4556-a09a-23be0d6f3f8f_871x584.png)

Imaged created by the author

Follow the disadvantages of shared-nothing architecture and the fact that node membership change is no longer an exception in the cloud environment. The people behind Snowflake separated computing and storage into two loosely coupled, independent services.

Storage will be provided by [Amazon S3](https://aws.amazon.com/s3/?gclid=CjwKCAiAtt2tBhBDEiwALZuhAL7_omVAOPT38tncRBGm6jIZAEhPiDeQ6et6nNHDgJ0qWZDE_sw4iRoC2ocQAvD_BwE&trk=f10cddca-7917-4465-9801-28c9cc57f288&sc_channel=ps&ef_id=CjwKCAiAtt2tBhBDEiwALZuhAL7_omVAOPT38tncRBGm6jIZAEhPiDeQ6et6nNHDgJ0qWZDE_sw4iRoC2ocQAvD_BwE:G:s&s_kwcid=AL!4422!3!589846469979!e!!g!!amazon%20s3!16178327440!136912444927) or any storage service like [Google Cloud Storage](https://cloud.google.com/storage?hl=en) or [Azure Blob Store](https://azure.microsoft.com/en-us/products/storage/blobs). Compute power will be provided by Snowflake's proprietary shared-nothing engine.

(From my understanding, compute here is just a VM machine with additional configuration from Snowflake to handle query execution effectively).

Pay attention here; the overall architecture of Snowflake is the separation of compute and storage, but in the computing aspect, it is a shared-nothing architecture with a local disk that only stores temporary data or cache data. These local disks are recommended to be SSDs. Cache helps improve the performance of the query by decreasing the latency when accessing data through downloading from object storage (through the network).

---

## The unlimited storage “pool“

> *Where the data is stored*

[![](https://substackcdn.com/image/fetch/$s_!pNZV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8df52eb0-6220-424a-a3cb-909eb5d44cc2_968x676.png)](https://substackcdn.com/image/fetch/$s_!pNZV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8df52eb0-6220-424a-a3cb-909eb5d44cc2_968x676.png)

Imaged created by the author

Regarding storage, the people behind Snowflake had to decide between object storage like S3 or developing their storage on HDFS (or other equivalents). They started experimenting with the S3 and finally concluded that despite the unpredictable performance, the S3 is a champion regarding availability and durability. Ultimately, they decided to use object storage like the S3 and try to improve the performance of local caching in the Virtual Warehouse (which I will cover in the next section).

Some characteristics of S3:

* *Unlike local disk, S3 has higher latency because you have to access the data through the network.*
* *Objects in S3 (or any object storage) can only be interacted with simple HTTP-operation PUT/GET/DELETE. Still, it supports getting a range of files.*
* *The object in S3 is immutable, which means it CAN NOT be overwritten or even append data to the end.*

With these characteristics, making it become the database storage without any enhancement is insufficient. So, how does Snowflake use S3 for data storage?

Table data is horizontally partitioned into large, immutable files, similar to blocks or pages in a traditional database. In each file, column values are grouped together and heavily compressed, equivalent to the PAX file format (Apache Parquet, for example). The file has a header, which, among other metadata, contains the offsets of each column. Because S3 supports getting ranges of files, queries only need to download the file headers and columns they need.

Not only table data but also S3 allows temp data to spill from a query or large query results when the local disk is exhausted.

> ***Note**: S3 DO NOT store metadata such as catalog objects, which s3 files belong to which table, statistic, or locks…; this will be stored in dedicated services, which we covered in the following sections.*

We have gone through the storage; now it’s the compute layer's turn.

---

## Virtual Warehouse: The muscle

> *Where the query is executed*

[![](https://substackcdn.com/image/fetch/$s_!oahc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d8e4f6d-866a-4b43-8bbd-638b9d9691ba_888x457.png)](https://substackcdn.com/image/fetch/$s_!oahc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d8e4f6d-866a-4b43-8bbd-638b9d9691ba_888x457.png)

Imaged created by the author

Snowflake introduced the concept of Virtual Warehouses (VW), which simply clusters of EC2 (or equivalent VM service from other cloud vendors). Each cluster is exposed to a single user, and each instance VM is called a worker node.

Due to self-positioning as a data-as-a-service, Snowflake hides users from complex worker configurations; the VW only comes with abstract “T-Shirt sizes” ranging from X-Small to XX-Large, abstract away service, and pricing under the cloud platform.

> This complexity hiding like this is similar to [BigQuery with the “slot” concept](https://cloud.google.com/bigquery/docs/slots).

### Elasticity and Isolation

As I said, VWs are just pure computing resources (with some additional configuration). Data stored in S3 means VWs are stateless; this allows VWs to be scaled up and down on demand without worrying about losing data.

Each query runs exactly on one VW, and workers are not shared across VWs.

> *The paper said they will consider shared workers for future work: increase utilization when isolation is not a big concern.*

In case a query fails, the query must have to rerun from the start.

> *The paper said that partial retry is not supported but will be considered for future work in cases where rerunning the whole query is insufficient (long-running query).*

Each user will have multiple VWs; each runs an individual query, which allows queries to be run concurrently in an isolated manner.

### Local Caching and File stealing

As mentioned above, Snowflake compute follows a shared-nothing architecture, but the local disk only stores cache and temporary data.

The cache is the collection of table files from S3, which is last used by the node; it holds the file header and needed columns from the query. The cache only lives during the duration of the worker node. Snowflake applies the LRU policy (discard the least-recently-used items first) for the cache. This simple scheme works surprisingly well.

Query optimizer assigns files to the worker node's cache using consistent hashing on the table name. This helps queries accessing the same table be routed to the same worker node. In cases where the set of nodes changes, data is not shuffled immediately, and Snowflake relies on the LRU replacement policy to eventually replace cache content.

When running a query, some worker nodes may execute slower than others (it handles too many files, for example). This worker is called a straggler.

If we let the straggler continue to run the overload job, it will surely increase the tail latency. So, in the case of the straggler node, Snowflake allows other finish-running nodes to come to help:

If a node finishes with its file, it requests additional files from other nodes; if the straggler nodes find too many files left, it transfers ownership of these files, and the requestor (finished node) will download these files directly from S3 to not increase the burden on the straggler node. An illustration helps you better imagine it:

[![](https://substackcdn.com/image/fetch/$s_!Bk7p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66fce1ee-cce2-474f-b78a-643305e3e1ed_714x462.png)](https://substackcdn.com/image/fetch/$s_!Bk7p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66fce1ee-cce2-474f-b78a-643305e3e1ed_714x462.png)

Imaged created by the author

### Execution engine:

Snowflake has a columnar storage and execution engine, which is generally considered superior to row-wise storage for OLAP workload:

* *More effective CPU caches*
* *More convenient for [SIMD (Single Instruction Multiple Data)](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) instruction (in the past, a CPU instruction could only execute on single data, now some CPU support single instruction can be executed on multiple data)*
* *In columnar storage, column values are stored close together, allowing for better compression performance.*

Snowflake also applies vectorized execution on its query engine; data is processed in a pipeline fashion, and each operator will receive a bath of a few thousand rows in column format. This differs hugely from traditional databases like PostgreSQL or MySQL, where each operator will pass only a single record. This approach, pioneered by [VectorWise (originally MonetDB/X100)](https://www.cidrdb.org/cidr2005/papers/P19.pdf), saves I/O and significantly improves cache efficiency.

One more thing to note here: PostgreSQL or MySQL apply the volcano-style approach for processing engine, in which the parent operators will continuously “pull“ data from the child operators. Snowflake took a different approach, allowing child operators to push data to their parent operators actively. This has some advantages, from what they said:

* *Push-based execution improves cache efficiency by removing control flow logic from tight loops.*
* *It also enables Snowflake to process DAG-shaped plans efficiently, instead of just trees, creating additional opportunities for sharing and pipelining intermediate results.*

> *The “push-based vectorized“ from DuckDB is similar to Snowflake; you can check out my DuckDB article here: [link](https://open.substack.com/pub/vutr/p/i-made-110-in-duckdb?r=2rj6sg&utm_campaign=post&utm_medium=web).*

---

## Cloud Services Layer: The brain

> *How does the whole Snowflake operate smoothly?*

[![](https://substackcdn.com/image/fetch/$s_!FXcl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd18ae71-8e79-4aad-8324-5ec31ef02068_915x460.png)](https://substackcdn.com/image/fetch/$s_!FXcl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd18ae71-8e79-4aad-8324-5ec31ef02068_915x460.png)

Imaged created by the author

Besides the storage and computing layer, Snowflake’s architecture has another component called *cloud services,* a collection of services like access control, query optimizer, transaction manager, etc.

Unlike Virtual warehouses, which are ephemeral and user-specific resources. The cloud Services layer is heavily multi-tenant. Each service in this layer is long-lived and shared across users, which improves utilization, reduces administrative overhead, and also allows better scalability than in traditional architectures where every user has an entirely private system. Every service is replicated for high availability; in the scenario where individual service nodes fail, it does not cause data loss.

### Query management and optimization

All queries by users first go through the Cloud Services layer.

Snowflake’s query optimizer follows a typical Cascades-style approach with top-down cost-based optimization. All statistics used for optimization are automatically maintained on data load and updates. Once the optimizer completes, the execution plan is distributed to the worker node.

The cloud service will continuously monitor the running queries. All information from this monitoring process is stored and exposed so the users can monitor and analyze it using GUI.

### Concurrency control

Concurrency control is handled entirely by the Cloud Services layer. Snowflake decided to implement ACID constraint using Snapshot Isolation (SI). The transaction will see the consistent SI of the database as of the time the transaction started.

SI is implemented on top of [multi-version concurrency control (MVCC)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control), which means a copy of every change on a desired object (table) is preserved for some time. Making copies of every change is an obvious choice because table data when saved in object storage, can not be modified; change can only be made by creating a whole new file that includes the change. This means any efforts to modify data in the table will produce a newer version of the table by adding and removing whole files relative to the previous version.

File additions and removals are tracked in the metadata storage (which is informed in the paper that it’s a global key-value store). This metadata information will check which set of files belongs to a specific table version.

### Data Skipping

Historically, the amount of data accessed in the database was scoped down using indexes like [B+Tree](https://en.wikipedia.org/wiki/B%2B_tree). However, the index approach is insufficient in the OLAP world. Traditional indexes can only serve well in random or point access (OLTP workload, in other words)

The OLAP workload usually needs to scan a large amount of data but is limited only to some columns; this type of workload can not benefit from the index. Moreover, maintaining the index will increase the volume of data (which is already very large).

So, to limit the amount of data scanning, Snowflake maintains the data distribution information for a specific chunk of the data (record, file, block): the min and the max of the given chunk; this mechanism is also called min-max-based pruning.

Depending on the query, these values can be used to determine which chunk is unnecessary. If your query only needs data that have values ranging from (8 to 15), the chunk where max is 7 or the chunk where min is 16 does not need to be brought up. These approaches work surprisingly well in the OLAP world; [this statistical information can also be found in Apache Parquet.](https://parquet.apache.org/docs/file-format/metadata/)

One more thing about min-max pruning is that not only Snowflake can apply it statically (must have to see the data first) but also dynamically (at run time), for example:

In [Hash Join](https://en.wikipedia.org/wiki/Hash_join), Snowflake can collect statistical information on the distribution of join keys on the build side; then, it will try to push this information to the probe side and use it to filter out the unnecessary files on the probe side.

---

## Features Highlight

All the above sections are about Snowflake's internal architecture; the rest of this blog post is for highlighting Snowflake features.

> ***Note**: These features below might seem like the norm at the moment, where almost all cloud data warehouses out there support it, but at the time Snowflake first released, these features were hugely different from other data warehouse solutions at that time.*

### Pure Software-as-a-Service Experience

SaaS means Snowflake does not need DBA for maintenance. It also releases the burden of machine-setting and maintenance from the user. From the integration perspective, Snowflake supports standard databases [JDBC](https://vi.wikipedia.org/wiki/Java_Dabase_Connectivity#:~:text=Java%20Database%20Connectivity%20(JDBC)%20l%C3%A0,CSDL%20gi%C3%A1n%20ti%E1%BA%BFp%20qua%20Java.), [ODBC](https://en.wikipedia.org/wiki/Open_Database_Connectivity), and [PYTHON PEP-0249](https://peps.python.org/pep-0249/) and works with various third-party tools.

Users can also interact directly with the UI without any significant engineering effort.

### Continuous Availability

In a time when data analytics play a significant role in business operations, availability become a must-have constraint for any data warehouse.

Snowflake’s storage is based on S3 (or any cloud object storage), so it will benefit from the availability and durability guarantee of these services (one of the most famous characteristics of cloud object storage).

Metadata stores in the cloud services layer are also replicated to ensure high availability. The remaining services are stateless nodes in multiple availability zones (AZ), with LB distributed requests between them.

According to the paper, Virtual Warehouses (VW) are NOT distributed across AZ for performance reasons, with the assumption that failure in the whole of AZ is rare. In case the VWs fail, the user needs to re-provision the VWs manually. Snowflake realized this inconvenience:

> *We accept this one scenario of partial system unavailability but hope to address it in the future.*

### When the data is schema-less and not structured anymore

#### Array, Object, Variant

Besides SQL native type (`DATE`, `VARCHAR`,…), Snowflake SQL supports additional types allowing users to handle semi-structured data: `VARIANT`, `ARRAY`, `OBJECT`.

`VARIANT` can store any native SQL type as well as `ARRAY` and `OBJECT`. The internal representation of both `ARRAY` and `OBJECT` is the same: a self-describing, binary serialization that supports fast key-value lookup, as well as efficient type tests, comparison, and hashing. `VARIANT` columns that contain `ARRAY` or `OBJECT` can thus be used as any regular columns (for join, group by, order by).

Data from JSON, Avro, or XML format can be loaded directly into a `VARIANT` column without specifying schemas; Snowflake will automatically handle parsing and type inference behind the scenes. Snowflake provides extraction operations in functional SQL notation and JavaScript-like path syntax to allow users to interact with these data types. Snowflake also lets the user construct `ARRAY` and `OBJECT` using `ARRAY_AGG` and `OBJECT_AGG`.

#### Schema-less

To achieve both the flexibility of a schema-less serialized representation and the performance of a columnar relational database, Snowflake introduces a novel automated approach to type inference and columnar storage.

When storing semi-structured data, the system automatically performs statistical analysis on the collection of documents within a single table file.

After getting this information, Snowflake performs automatic type inference and determines which (typed) paths are frequently common. The columns of that path will be removed from the documents and stored separately, using the same compressed columnar format as native relational data. For these columns, Snowflake will calculate the min-max for data chunks and then use it for pruning data (the same as the mechanism in the Data Skipping section).

Most queries are only interested in a subset of the columns from the document (need data from only a few paths from the document). In those cases, Snowflake pushes projection and cast expressions down into the scan operator so that only the necessary columns are accessed and cast directly into the target SQL type without bringing up the whole `VARIANT`.

The optimizations described above are performed separately for each table data file. However, it causes Snowflake some trouble. Suppose a query needs data from a path expression, and we would like to use pruning to restrict the set of files to be scanned. The path and corresponding column may be present in most files. But if some files where the path is not considered “common“ by the system, it will not appear in the metadata, causing the optimizer some confusion when doing the push-down filter.

The simple solution is scanning all files for which there is no suitable metadata. Snowflake improves this solution by computing [Bloom filters](https://en.wikipedia.org/wiki/Bloom_filter#:~:text=A%20Bloom%20filter%20is%20a,a%20member%20of%20a%20set.) over all paths present in the documents. These Bloom filters are stored along with the other file metadata and are used by the query optimizer during pruning. Table files that do not contain paths (which is known thanks to the Bloom Filter) required by a given query can be skipped.

#### Optimistic Conversion

Date/time values are usually represented as strings in formats like JSON. These values must be converted from strings to their actual type at some time (read or write) to preserve their semantic meaning. Moreover, the data type is usually used for filtering in OLAP workload; if these values are still in string type, it is hard for Snowflake to construct metadata (min-max range) for data skipping.

Because allowing users to not define schema at first, Snowflake performs optimistic data conversion and preserves both the result of the conversion and the original string in separate columns. Because unused columns are not loaded and accessed, keeping the original and converted data will not affect the performance but, in turn, will increase the storage volume.

### Time travel and clone

From the “Concurrency control” section, we know that Snowflake implements Snapshot Isolation (SI).

These SI have more use cases than just concurrency control. Because of the SI implementation, modified operations like insert, update, delete, or merge on a table will produce a newer version of the table by adding and removing whole files. These versions are kept for a duration (from the paper, up to 90 days, can be configured by the user).

File retention allows Snowflake to read earlier versions of the table’s data and perform time travel on the database. Users can use this feature from SQL using the convenient `AT` or `BEFORE` syntax. Using the same underlying metadata, Snowflake allows users to use the `UNDROP` keyword to restore tables. (can also apply to database and schema)

Snowflake also implements a functionality called cloning, which uses the keyword `CLONE`. Cloning a table creates a new one with the exact definition and data as the base table. Snowflake won’t copy physical underlying data when cloning; it only needs to copy the base table’s metadata to the clone table. After cloning, both tables point to the same data, but both can be modified independently without worrying about affecting each other. Cloning can also apply to schemas and databases.

### Security

Snowflake implements two-factor authentication:

* *Client-side encrypted data import and export plus secure data transfer and storage.*
* *Role-based access control (RBAC) for database objects.*

At all times, data is encrypted before being sent over the network and before being written to a local disk (for temporary and cache data) or shared storage (S3) (for persistent data).

#### Key Hierarchy

Snowflake uses strong [AES 256-bit encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard#:~:text=AES%20is%20a%20variant%20of%20Rijndael%2C%20with%20a%20fixed%20block%20size%20of%20128%20bits%2C%20and%20a%20key%20size%20of%20128%2C%20192%2C%20or%20256%20bits.) with a hierarchical key model rooted in [AWS CloudHSM](https://aws.amazon.com/cloudhsm/).

The Snowflake key hierarchy has four levels: root keys, account keys, table keys, and file keys. Each layer of (parent) keys encrypts and wraps the below (child) keys.

Hierarchical key models constrain the amount of data each key protects. Each layer reduces the scope of keys below it.

Each account key corresponds to one user account, each table key corresponds to one database table, and each file key corresponds to one table file. Each user account has a separate key, ensuring user data is isolated in the multi-tenant architecture.

Snowflake also constrains the lifetime of the key. Encryption keys go through four stages: (1) a pre-operational creation phase, (2) an operational phase where keys are used to encrypt and decrypt, (3) a post-operational phase where keys are no longer in use, and (4) a destroyed phase.

#### End-to-End Security

> ***Note***: *The paper only mentioned Amazon, but this approach also applies to other cloud vendors with equivalent service*

In addition to data encryption, Snowflake protects user data in the following ways:

* *Isolation of storage through access policies on S3.*
* *Role-based access control within user accounts for fine-grained access control to database objects.*
* *Encrypted data import and export without the cloud provider (Amazon) ever seeing data in the clear.*
* *Two-factor- and federated authentication for secure access control.*

---

## Outro

Thank you so much for reaching this point.

Few, clearly a long article.

I first intended to split this article into two parts, but I still decided to keep everything in a single article (I don’t remember exactly why; maybe I think you guys want a binge-reading experience?)

With the article, I just delivered all the insights from the Snowflake academic paper to you from my perspective.

If you want to correct or supplement information about Snowflake, please leave a comment or DM me.

---

*References: [The Snowflake Elastic Data Warehouse](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-spent-another-6-hours-understanding/comments)

It might take you 3 minutes to read, but it took me more than 3 days to prepare, so it will motivate me greatly if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
