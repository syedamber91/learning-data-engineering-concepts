---
title: "A glimpse of Apache Pinot, the real-time OLAP system from LinkedIn"
channel: vutr
published: 2024-03-30
url: https://vutr.substack.com/p/a-glimpse-of-apache-pinot-the-real
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Snowflake", "Streaming"]
tags: [pinot, https, query, time, segments, auto]
---

# A glimpse of Apache Pinot, the real-time OLAP system from LinkedIn

*Insights from paper the Pinot: Realtime OLAP for 530 Million Users - 2018*

> Source: [Open post](https://vutr.substack.com/p/a-glimpse-of-apache-pinot-the-real)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[streaming|Streaming]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!cgZF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ea2eaa4-2af6-4f79-9d04-07753dacc209_1396x994.png)](https://substackcdn.com/image/fetch/$s_!cgZF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ea2eaa4-2af6-4f79-9d04-07753dacc209_1396x994.png)

---

## Table of contents

* *Background*
* *Pinot’s architecture*
* *Pinot’s essential features to get performance at scale*

---

## Intro

I read an interesting article, [Stream Processing vs. Real-time OLAP vs. Streaming Database](https://hubertdulay.substack.com/p/stream-processing-vs-real-time-olap), not long ago while looking for resources about real-time processing; this article introduced me to a term I had never heard before: real-time OLAP, the system that serves real-time analytics. This led me to the research journey of Apache Pinot, LinkedIn’s real-time OLAP system. After spending a few hours [reading the paper Pinot: Realtime OLAP for 530 Million Users](https://cwiki.apache.org/confluence/download/attachments/103092375/Pinot.pdf), this blog is my note[.](https://cwiki.apache.org/confluence/download/attachments/103092375/Pinot.pdf)

---

## Background

OLTP systems are born to handle transaction data: they enable the real-time execution of large transactions with many concurrent queries and require fast response times. On the other hand, OLAP requires running complex queries on large numbers of records. OLAP systems have high throughput but do not offer low query latencies or high queries per second (QPS) like the OLTP systems.

What if a use case requires analytical insight, lightning-fast response time, and high QPS? Another way to ask is: What if we need OLAP to execute in more real-time? A “Who viewed my profile“ feature from LinkedIn is a bold example of this. [It serves a large user base and demands low latency response time at very large QPS.](https://www.youtube.com/watch?v=GvVYG6chYoI&t=412s) LinkedIn [introduced Pinot first in 2013](https://en.wikipedia.org/wiki/Apache_Pinot), a system used in production that can operate efficiently with tens of thousands of analytical QPS; it also offers near-real-time data ingestion from streaming data sources, while traditional OLAP typically relies on bulk data loads.

LinkedIn highlights critical requirements for near-realtime OLAP services like Pinot as follows:

* **Fast, interactive-level performance**: Users can not tolerate extended periods for query results. Although approaches such as MapReduce and Spark have high throughput, [“their high latency and lack of online processing limit fluent interaction.”](https://dl.acm.org/doi/pdf/10.1145/2133416.2146416)
* **Scalability:** Providing near-linear scaling to handle the operational requirements of large-scale deployments, allowing the system to adapt to high numbers of concurrent queries.
* **Cost-effectiveness:** As data volumes and query rates continue to increase, there must be an upper bound on cost.
* **Low data ingestion latency:** Users can query recently added data points in near real-time without waiting for batch jobs. Many available analytics systems cannot handle single-row operations and rely on bulk loads for data ingestion.
* **Flexibility**: The system should not limit users with predefined dimensions in pre-aggregated results when drilling down.
* **Fault tolerance:** System failures should not significantly impact end users.
* **Uninterrupted operation:** The system should operate continuously, without downtime for upgrades or schema changes.
* **Cloud-friendly architecture:** The services should be easily deployed on available cloud services.

The following sections will describe Pinot’s architecture.

## Overall

Pinot is a distributed OLAP data store that delivers low-latency analytics and offers fresh data in seconds. It is optimized for analytical workload on immutable append-only data. LinkedIn has been running Pinot in production for many years across hundreds of servers and processing thousands of queries per second to serve analytics customer-facing applications that require very low latency.

Pinot follows the [lambda architecture](https://en.wikipedia.org/wiki/Lambda_architecture). It supports near-real-time data ingestion by consuming online data directly from [Kafka](https://kafka.apache.org/) and offline data from the [Hadoop](https://hadoop.apache.org/) system. Offline data will serve as a global view, while online data will provide a more real-time view.

---

## Data and query model

Pinot logically organizes data into tables. Each table has a fixed schema and multiple columns, each of which can be a dimension or a metric. Pinot introduces a special timestamp dimension column called a time column. The time column is used when merging offline and online data (which I will deliver later).

[![](https://substackcdn.com/image/fetch/$s_!jI1z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e6d93d7-9f2d-4fde-af4d-4c1ae9d50700_959x727.png)](https://substackcdn.com/image/fetch/$s_!jI1z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e6d93d7-9f2d-4fde-af4d-4c1ae9d50700_959x727.png)

Image created by the author.

Tables are partitioned into segments, subsets of a table’s records. A typical Pinot segment has a few dozen million records, and a table can have tens of thousands of segments.

> ***Note**: I’ve researched a little from Pinot’s document; it says, [“Pinot lets tables grow to an unlimited number of segments.”](https://docs.pinot.apache.org/basics/components/table/segment) I’m not sure why there is a difference between the paper and the doc; please comment if you know this.*

Pinot stores segments redundantly to guarantee data availability. Segments are immutable, which means the data update results in new segments. Pinot stores segments in a columnar manner, ranging from a few hundred megabytes to a few gigabytes. Pinot employs various encoding schemes to minimize the data size, including [dictionary encoding](https://en.wikipedia.org/wiki/Dictionary_coder) and [bit packing of values](https://towardsdatascience.com/smart-way-of-storing-data-d22dd5077340).

To interact with Pinot’s data, users must use [PQL](https://pinot.apache.org/docs/user-guide/pql/), a subset of SQL. It is modeled around SQL but does not support joins, nested queries, DDL, and record-level operations.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Components

[![](https://substackcdn.com/image/fetch/$s_!5R_7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c4072b-49d2-4d11-a005-df87242909a7_986x1170.png)](https://substackcdn.com/image/fetch/$s_!5R_7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96c4072b-49d2-4d11-a005-df87242909a7_986x1170.png)

Image created by the author.

Pinot’s architecture has four main components: ***controllers, brokers, servers, and minions***. It also leverages two external services: [Apache Zookeeper](https://zookeeper.apache.org/) for state management and a persistent object store. Pinot uses [Apache Helix](https://helix.apache.org/), a framework that manages partitions, replicas, and resources in a distributed system for cluster management.

### Servers

Servers are in charge of hosting segments and query execution. Pinot stores a segment as a directory in the [UNIX filesystem](https://en.wikipedia.org/wiki/Unix_filesystem), which consists of a metadata file and an index file:

* **The segment metadata** provides information about the segment’s columns: type, cardinality, encoding scheme, column statistics, and the indexes available for that column.
* **The index file** stores indexes for all the columns. The files are append-only.

Pinot stores multiple replicas of a segment for high availability. This also improves query throughput, as all the replicas participate in the query processing. Pinot’s servers have a pluggable architecture that supports loading columnar indexes from different storage formats. This allows servers to read data from distributed filesystems like [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) or object storage like [Amazon S3.](https://aws.amazon.com/s3/)

> ***Note**: Pinot stores segments in object storage and loads them into servers for data processing; it does not initially store them in the server.*

### **Controllers**

This component maintains the mapping of segments to servers using a configurable strategy. Controllers also trigger changes to the mapping based on requests or changes in server availability (servers down, adding servers, etc.). Controllers support administrative tasks such as listing, adding, or deleting tables and segments. The component also allows users to define the table’s retention interval used for the garbage collector. LinkedIn deploys three controller instances in each data center for fault tolerance with a single master.

### **Brokers**

Brokers route the user's HTTP query requests to the servers that host necessary segments. They also collect sub-part query responses, merge them into the final result, and send it back to the client (Pinot takes a [scatter-gather-merge](https://www.youtube.com/watch?v=SnnGargfSOA) approach). For better performance, the user can place a load balancer before a group of broker instances.

### Minions

Minions are responsible for maintenance tasks. The controllers’ job scheduler assigns tasks to the minions. An example of a minions task is data purging. LinkedIn must purge specific data to comply with legal requirements. Because data is immutable, minions must download segments, remove the unwanted records, rewrite and reindex the segments, and finally upload them back into the system.

### Zookeeper

Zookeeper acts as a centralized metadata store and as the communication mechanism between nodes in the cluster. It stores all information about the cluster, such as states, segment assignments, and metadata.

---

## Common Operations

> *We will see how Pinot handles segment load, routing table update, query processing, server-side query execution, data update, and real-time segment completion.*

### Segment Load

[![](https://substackcdn.com/image/fetch/$s_!sxtJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F611f7cf3-6cff-4ceb-8b29-4a6db2f9dbcc_847x475.png)](https://substackcdn.com/image/fetch/$s_!sxtJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F611f7cf3-6cff-4ceb-8b29-4a6db2f9dbcc_847x475.png)

Image created by the author.

Apache Helix uses state machines to manage the cluster state; each resource has its current and desired state. When the state changes, Helix sends change information to respective nodes. The nodes will execute based on this information to achieve the desired state.

In the beginning, segments have `OFFLINE` state. To make segments `ONLINE`, Helix asks server nodes to fetch the relevant segments from object persistent storage based on mapping information; the servers then unpack and load the segments, finally making it ready for query execution. Once the process is complete, Helix marks the segment as `ONLINE`.

In the case of real-time ingestion from Kafka, the segments will transit from `OFFLINE` to `CONSUMING` state. We will explore real-time ingestion further in the *“Real-time segment completion“* section.

### Routing table update

Helix updates the cluster state when servers load or unload segments. The brokers listen to the cluster state changes and update its routing table and mapping between servers and segments.

### Query processing

Here is the Pinot’s query journey:

[![](https://substackcdn.com/image/fetch/$s_!8EgP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36b3426b-0b85-43f0-b470-984a6ef87e4d_579x891.png)](https://substackcdn.com/image/fetch/$s_!8EgP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36b3426b-0b85-43f0-b470-984a6ef87e4d_579x891.png)

Image created by the author.

* The broker receives the query, then parses and optimizes it.
* Pinot picks a routing table for a particular table.
* Pinot communicated with all servers in the routing table to process the query on a subset of the table’s segments.
* Servers generate logical and physical query plans using index information and column metadata.
* Pinot then schedules the execution plan.
* When all query plan executions are completed, the results are gathered, merged, and returned to the broker. The broker returns the final result to the client.

> **Note**: *Processing jobs from servers that are errors or timeouts, Pinot will mark the final result as partial. Users have the choice to view the incomplete results or resubmit the query.*

Moreover, Pinot allows dynamically merging data from offline and real-time systems. When a query that needs to read data from both systems arrives, Pinot rewrites the query into two queries: one query for the offline part, which queries data before the time boundary, and a second one for the real-time part, which queries data at or after the time boundary. When both queries are complete, Pinot merges these results. Let's check an example from the paper for a better understanding:

> *A hypothetical table with two segments per day might have overlapping data for August 1st and 2nd. When such a query arrives in Pinot, it is transparently rewritten into two queries: one query for the offline part, which queries data before the time boundary, and a second one for the real-time part, which queries data at or after the time boundary.*

[![](https://substackcdn.com/image/fetch/$s_!bh9K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc037908-4f6a-46de-ad09-d5ee3a7c1fc3_1392x506.png)](https://substackcdn.com/image/fetch/$s_!bh9K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc037908-4f6a-46de-ad09-d5ee3a7c1fc3_1392x506.png)

Hybrid Query Rewriting. Pinot: Realtime OLAP for 530 Million Users (2018). [Source](https://cwiki.apache.org/confluence/download/attachments/103092375/Pinot.pdf)

### Server-side query execution

As mentioned in the *“Query processing“* section, the servers generate the physical and logical plans. Because segments have different index schemes and physical layouts, servers create the query plan for each segment based on its characteristics. They also generate special plans for queries that don’t need to touch the actual segments. These queries can use the segment’s metadata, such as the maximum of the column’s value.

### Data upload

When data must be uploaded, the controller loads the segments using [HTTP POST](https://en.wikipedia.org/wiki/POST_(HTTP)). Then, it unpacks the segments to ensure data integrity and checks if the segment’s size is larger than the table’s quota. After that, the controller writes segment metadata in Zookeeper and then updates the cluster state by marking the segment `ONLINE` with the desired number of replicas.

### Real-time segment completion

Pinot implements real-time Kafka consumption independently on segment replicas. Each replica starts consuming from the same beginning offset and has the same end criteria. When the consumption meets the criteria, the system flushes the segment to disk and commits it to the controller. Pinot supports flushing segments with two configurable options:

* Flushing after the number of records
* Flushing after an amount of time.

Ideally, independent consumers read from the same Kafka offset and partition with the same number of records will consume the same data. However, the divergence can happen after a while because each consumer uses their local clock. Pinot deals with this problem by developing a segment completion protocol to ensure that independent replicas have a consensus on the contents of the final segment. When the server completes segment consuming, it gives its current Kafka offset to the controller and polls for the instructions. The controller then returns an instruction to the server. Here are all possible instructions:

> * `HOLD` *Instructs the server to do nothing and poll at a later time*
> * `DISCARD` *Instructs the server to discard its local data and fetch an authoritative copy from the controller; this happens if another replica has already successfully committed a different version of the segment.*
> * `CATCHUP` *Instructs the server to consume up to a given Kafka offset, then start polling again*
> * `KEEP` *Instructs the server to flush the current segment to disk and load it; this happens if the offset the server is at is the same as the one in the committed copy*
> * `COMMIT`*: Instructs the server to flush the current segment to disk and attempt to commit it; if the commit fails, resume polling; otherwise, load the segment*
> * `NOTLEADER` *Instructs the server to look up the current cluster leader as this controller is not currently the cluster leader, then start polling again*

Pinot manages the controller’s replies using a state machine that waits until enough replicas have been contacted or a defined amount of time has passed since the first poll to determine if a replica is a committer. The state machine tries to get all replicas to catch up with all replicas and picks one of the replicas with the largest offset to be the committer. This minimizes network transfers between controller and servers while ensuring all replicas have the same data when the segments are flushed.

---

## Cloud-Friendly Architecture

LinkedIn designs Pinot to run on cloud infrastructure in the first place. There are two factors required for Pinot that cloud providers can satisfy:

* Compute local ephemeral storage
* Object storage system

Pinot has a share-nothing architecture with stateless instances. It stores all persistent data in the object storage system and metadata in Zookeeper services. Pinot only uses local storage for caching, and the data can be refilled by fetching data from the object storage or Kafka (similar to [Amazon Redshift](https://aws.amazon.com/redshift/) and [Snowflake](https://www.snowflake.com/en/)). Thanks to that, Pinot can add or remove server nodes anytime without concern about data loss or performance degradation.

This architecture allows LinkedIn to run Pinot on container execution services and requires only code changes to communicate with the cloud object storage system. It also makes it easy to deploy and scale using container managers such as [Kubernetes](https://kubernetes.io/docs/concepts/overview/).

The following sections describe Pinot’s essential features to get performance at scale.

## Query Execution

> *The physical operators*

People from LinkedIn designed Pinot to accommodate new operators and query shapes. At first, Pinot did not support queries that only needed to operate on metadata, such as `SELECT COUNT(*)`; LinkedIn added support for such queries by making changes to the planner and adding a new metadata-based physical operator without touching the underlying architecture. LinkedIn also specializes in Pinot’s physical operators; different data encoding schemes have different physical operators. This allows new index types and data structures to be added for query optimization.

---

## Iceberg Queries

[An iceberg query performs an aggregate function over a column (or a set of attributes) and then discards aggregate values below a specified threshold.](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=a0203b4a547a6d172a053d39d1d618ee47ce3e31) For example, the user might be interested in knowing which top countries contribute the most page views but not all countries. This is especially critical in data that have a [long tail distribution](https://en.wikipedia.org/wiki/Long_tail).

[Iceberg cubing](https://dl.acm.org/doi/10.1145/304181.304214) expands on [traditional OLAP cubes](https://en.wikipedia.org/wiki/OLAP_cube) to answer iceberg queries. Research on iceberg cubing has brought several advances, such as star cubing, which makes it more efficient to compute than other approaches in most cases. In star cubing, a pruned hierarchical structure called a star-tree is constructed and can be used to answer queries efficiently.

> *Star-trees consist of nodes of pre-aggregated records; each level of the tree contains nodes that satisfy the iceberg condition for a given dimension and a star **node** that represents all data for this particular level. Navigating the tree allows answering queries with multiple predicates.*

[LinkedIn implements the star-tree index](https://www.linkedin.com/blog/engineering/open-source/star-tree-index-powering-fast-aggregations-on-pinot) for Pinot to enhance analytical queries for internal data analytics tools. If a user runs a query that can be optimized using the star-tree index, Pinot returns pre-aggregated results from the index; if not, query execution runs on the original data. This LinkedIn blog provides detailed information about the [star-tree index](https://www.linkedin.com/blog/engineering/open-source/star-tree-index-powering-fast-aggregations-on-pinot).

[![](https://substackcdn.com/image/fetch/$s_!8QEc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7d2b557-7bf6-4d76-a7b5-0e7c63bacbba_1302x798.png)](https://substackcdn.com/image/fetch/$s_!8QEc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7d2b557-7bf6-4d76-a7b5-0e7c63bacbba_1302x798.png)

An example of the star-tree index is the two-dimensional split order Country and Browser. Each node contains the aggregated data for that dimension. A query will traverse through the tree to retrieve the desired answer. Pinot: Realtime OLAP for 530 Million Users (2018). [Source](https://cwiki.apache.org/confluence/download/attachments/103092375/Pinot.pdf)

Besides the star-tree index, Pinot supports other index strategies like:

* [Range index](https://docs.pinot.apache.org/basics/indexing/range-index) allows better performance for queries that need filtering over a range.
* [Bitmap inverted index](https://docs.pinot.apache.org/basics/indexing/inverted-index): Pinot maintains a map from a value to a bitmap of rows, which makes value lookup take constant time.

You can check the complete support indexing list from Pinot [here](https://docs.pinot.apache.org/basics/indexing).

---

## Query Routing and Partitioning

Pinot pre-generates a routing table for an unpartitioned table; this routing table is a list of servers and their subset of segment mapping. Pinot supports various query routing options:

* **The default balanced strategy** divides all the table’s segments equally across all servers. This strategy works well for small and medium clusters but is not fit for larger clusters. With a larger cluster, there is a high chance that a cluster’s server has issues, slowing the query processing when a server holds necessary segments down
* **Dedicated strategy for large clusters** that limits the number of hosts communicated in the cluster for any given query; this minimizes the impact of any failed host and reduces tail latency. LinkedIn implements a random [greedy](https://en.wikipedia.org/wiki/Greedy_algorithm) strategy that produces an approximately minimal number of assignments and ensures balancing workloads between servers. Pinot generates various routing tables *“by taking a random subset of servers and adding additional servers until the number of segments is covered.”* Then, Pinot selects the final routing table based on a specific metric.

---

## Multi-tenancy

Pinot supports multiple tenants co-located on the same hardware. Pinot prevents tenant resource contention by using the token bucket to distribute query resources. Each query takes some tokens from its tenant’s bucket proportional to the query execution time. When no token is left in the bucket, Pinot puts queries on hold until a token is available again. Pinot slowly refills tokens to allow for short spikes in workload and prevent a misbehaving tenant from taking all resources for others.

---

## Use Case Types

LinkedIn observed that users of Pinot are divided into two categories:

* Use cases require high throughput, low-complexity queries for simple analytics. This type of use case requires data located in memory to serve high QPS workloads. Users also run a small number of query patterns in these use cases.
* Use cases require running with complex queries or larger data volumes; however, they don’t need high query rates. This type of use case requires data co-located on hardware with [NVMe](https://en.wikipedia.org/wiki/NVM_Express) storage. LinkedIn locates the hardware for these workloads with other tenants to ensure efficient resource utilization.

---

## Operational Concerns

LinkedIn operates Pinot as a service model; the Pinot team runs the system and provides ongoing support. As the demand for Pinot increases, the dedicated staff that operates Pinot will grow over time. LinkedIn has to design Pinot as a self-service model as much as possible.

LinkedIn allows Pinot to add new columns to the existing schema without downtime. When a new column is added, Pinot auto-fills it with default values from all existing segments and makes the column available after a few minutes. Pinot also parses the query logs and execution statistics to automatically add inverted indexes to columns if the system finds that doing so would improve performance.

Moreover, LinkedIn stores table configurations in source control and synchronizes with Pinot using REST API. This allows users to audit, search, validate, and review code for all configuration changes.

---

## Outro

Through the article, I’ve delivered some highlights I found interesting after reading Pinot’s academic paper. I still spend time understanding more about the start-tree index and might update this article in the future.

I hope my work brings some value. Now, see you next week.

---

## **References**

*[Pinot: Realtime OLAP for 530 Million Users - 2018](https://cwiki.apache.org/confluence/download/attachments/103092375/Pinot.pdf)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/a-glimpse-of-apache-pinot-the-real/comments)

It might take you 5 minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
