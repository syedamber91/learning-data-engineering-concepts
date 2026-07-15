---
title: "8 minutes to understand Presto"
channel: vutr
author: "Vu Trinh"
published: 2025-01-30
url: https://vutr.substack.com/p/8-minutes-to-understand-presto
paid: false
topics: ["Data Engineering", "Apache Spark", "Snowflake", "Databricks", "BigQuery", "Lakehouse", "Batch Processing", "ETL"]
tags: [https, auto, presto, image, media, substackcdn]
---

# 8 minutes to understand Presto

*Uber, Netflix, Airbnb, and LinkedIn uses this query engine.*

> Source: [Open post](https://vutr.substack.com/p/8-minutes-to-understand-presto)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[batch-processing|Batch Processing]] · [[etl|ETL]]

---

> *I'm offering **an** **exclusive** **sponsorship slot** **in each issue** to keep this newsletter free for readers. If you want to feature your product in my newsletter, explore my media kit:*
>
> [View Media Kit & Sponsor Now](https://vutr.substack.com/p/media-kit)

> *I’m making my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned. Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!gyaQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbebcf596-7b61-431c-b45e-c40de96bc0cd_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!gyaQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbebcf596-7b61-431c-b45e-c40de96bc0cd_2000x1429.png)

Image created by the author.

---

## Intro

Apache Spark is the king of data processing.

It was developed in 2012 in response to limitations in the [MapReduce](https://en.wikipedia.org/wiki/MapReduce).

People first adopted Spark for ETL processes. However, in 2015, the Spark team introduced SQL capability, making it an attractive option for a relational query engine.

In 2020, Databricks introduced the lakehouse paradigm. [They equipped Spark with the Photon engine](https://open.substack.com/pub/vutr/p/why-did-databricks-build-the-photon?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false) to make it more efficient as the query engine over the datalake.

A robust query engine operating on vast amounts of unseen data can provide many advantages.

Not only Databricks realizes this.

BigQuery is the query engine (Dremel) that operates on giant storage systems (Coloussus).

Snowflake is a set of workers that operates on S3.

Aside from cloud data warehouses, a big tech company joined the party.

Facebook developed an interactive SQL query engine with the same vision in 2012.

They called it Presto. With the promises of “[SQL on everything](https://trino.io/Presto_SQL_on_Everything.pdf). “

---

## Overview

Facebook developed Presto to address the growing need to extract insights from large amounts of data. The goal was to use SQL to make data analytics accessible to more people in the organization.

In late 2018, Facebook's data professionals used Presto for most SQL analytic workloads, including interactive/BI queries and long-running batch ETL jobs.

Presto is a distributed SQL query engine that processes hundreds of petabytes of data and quadrillions of rows daily at Facebook.

[![](https://substackcdn.com/image/fetch/$s_!Puiv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99a88a84-7109-496e-a54e-72242076a098_1090x322.png)](https://substackcdn.com/image/fetch/$s_!Puiv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99a88a84-7109-496e-a54e-72242076a098_1090x322.png)

Image created by the author.

Here are its characteristics:

* It can run hundreds of resource-intensive queries at the same time.
* It can scale to thousands of workers.
* It can query multiple data sources, even in the same query.
* It can support many use cases with different constraints and performance characteristics.
* It promises to operate at high performance.

Some use cases at Facebook are:

* **Interactive Analytics:** Engineers and data scientists use Presto to examine small amounts of data, test hypotheses, and build visualizations or dashboards**.**
* **Batch ETL:** Presto supports users migrating from legacy batch processing systems for ETL queries. These queries are more resource-intensive than interactive ones.
* **A/B Testing:** Presto supports Facebook's A/B testing infrastructure**.**It helps join multiple large datasets to produce experiment details or population information.
* **Developer/Advertiser Analytics:** Presto supports custom reporting tools, such as [Facebook Analytics](https://www.facebook.com/business/help/966883707418907), for external developers and advertisers**.**

---

## Presto or Trino

Before learning about Presto’s architecture, I will explore its history.

As mentioned, Facebook started developing Presto in 2012 and later opened it in 2013.

In 2014, Netflix shared that they used Presto on 10 petabytes of S3 data.

In 2016, Amazon announced the famous service [Athena](https://en.wikipedia.org/wiki/Amazon_Athena). They built Athena based on Presto.

In 2017, Starburst Data was found to support Presto commercially.

In 2018, original Presto developers left Facebook due to a policy change that gave Facebook committers more privilege to commit changes over the open source community.

In 2019, Presto development forked PrestoDB, maintained by Facebook, and PrestoSQL, which the Presto Software Foundation maintains.

In the same year, Facebook donated PrestoDB to the Linux Foundation.

In December 2020, PrestoSQL was rebranded as Trino because Facebook had obtained a trademark for "Presto."

---

## Architecture

[![](https://substackcdn.com/image/fetch/$s_!3w6A!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b1d4259-ce97-4b8a-8957-065537b120bc_1302x1002.png)](https://substackcdn.com/image/fetch/$s_!3w6A!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b1d4259-ce97-4b8a-8957-065537b120bc_1302x1002.png)

Image created by the author.

A Presto cluster has a coordinator node and a set of worker nodes:

* The coordinator parses, plans, and orchestrates queries.
* The workers execute the query.

Here is a typical flow:

[![](https://substackcdn.com/image/fetch/$s_!aoi7!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31e9fd29-66f7-46de-b5eb-ddbea5844658_1580x1004.png)](https://substackcdn.com/image/fetch/$s_!aoi7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31e9fd29-66f7-46de-b5eb-ddbea5844658_1580x1004.png)

Image created by the author.

* The client sends an HTTP request with the SQL statement to the coordinator.
* The coordinator parses and analyzes the SQL.
* It then creates and optimizes the execution plan.
* The coordinator sends the plan to the workers.
* Workers start executing the tasks, operating on splits, which are chunks of data in an external storage system.
* Workers' inputs are remote splits or intermediate results from upstream workers. Workers store intermediate data in memory as much as possible.

Facebook designed Presto with the extensibility in mine; they introduced the plugin interface for Presto. The interface lets users make many customizations:

* Custom data types
* Custom function
* Custom access control implementations.
* Custom queuing policies
* Custom connectors enable Presto to communicate with external data stores through the Connector API, which has four parts: the Metadata API, Data Location API, Data Source API, and Data Sink API.

---

## Key Design Decision

### SQL Dialect

Presto adheres to the ANSI SQL to achieve broad compatibility. Facebook also selected extensions from ANSI SQL for Presto, such as lambda expressions and higher-order functions, to improve usability with complex data types like maps and arrays.

### Client Interface

[![](https://substackcdn.com/image/fetch/$s_!Vl3A!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74f41092-e0b5-452f-8a31-15248b319c38_474x320.png)](https://substackcdn.com/image/fetch/$s_!Vl3A!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74f41092-e0b5-452f-8a31-15248b319c38_474x320.png)

Image created by the author.

Presto provides multiple client interfaces:

* A RESTful HTTP interface for clients.
* A command-line interface.
* A JDBC client, enabling compatibility with BI tools like Tableau.

### Query Planning And Optimization

The logical planner generates an intermediate representation (IR) of the query plan based on the syntax tree. The IR is a plan nodes tree. Each node is a physical or logical operation; it receives input from its children.

[![](https://substackcdn.com/image/fetch/$s_!DfM_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbbac06-461c-405a-9ae5-d1b21a74e3db_516x314.png)](https://substackcdn.com/image/fetch/$s_!DfM_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbbac06-461c-405a-9ae5-d1b21a74e3db_516x314.png)

Image created by the author.

The query optimizer creates the physical plan from the logical plan. This process uses a set of transformation rules, such as predicate and limit pushdown, column pruning, and decorrelation.

### Data Layouts

Presto leverages the physical layout of data provided by the connector's Data Layout API to optimize queries. Some layout information includes data location, its partitioning schema, the data index, and how they sort or group the data.

[![](https://substackcdn.com/image/fetch/$s_!qlbG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a8e619d-c25e-4d35-99a7-4154750ba594_646x262.png)](https://substackcdn.com/image/fetch/$s_!qlbG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a8e619d-c25e-4d35-99a7-4154750ba594_646x262.png)

Image created by the author.

For a table, the connector can return more than layout information; the optimizer can select the most efficient layout for the query. (e.g., leverage partitioning but ignoring the sorting)

### Predicate Pushdown

Presto can push down predicates to the data source through connectors to improve filtering efficiency. The optimizer will talk with the connector to decide when to execute this technique.

### Inter-node parallelism

[![](https://substackcdn.com/image/fetch/$s_!HBuo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc59d26a3-ef00-4e83-af56-c2aacacd4ef0_392x346.png)](https://substackcdn.com/image/fetch/$s_!HBuo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc59d26a3-ef00-4e83-af56-c2aacacd4ef0_392x346.png)

Image created by the author.

The optimizer also decides which plan stages can run parallel across workers. A stage can have many tasks, executing the same logic on a subset of input data. A shuffle happens when exchanging data between stages. Data shuffling increases latency and uses a lot of CPU and memory. Thus, the optimizer must consider the number of shuffles in a plan.

### Intra-node parallelism

[![](https://substackcdn.com/image/fetch/$s_!7Aj9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc25897c4-6915-431d-938c-57aca43ae351_404x250.png)](https://substackcdn.com/image/fetch/$s_!7Aj9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc25897c4-6915-431d-938c-57aca43ae351_404x250.png)

Image created by the author.

The optimizer can identify and parallelize sections in a plan stage across threads on a single worker. This is much more efficient than inter-node parallelism; threads can share memory data, such as hash tables or dictionaries, with less overhead.

### Scheduling

To execute a query, the engine makes two scheduling decisions:

* **Stage Scheduling**: Presto supports two policies: all-at-once and phased. The first schedules all stages concurrently, which benefits latency-sensitive use cases such as Interactive Analytics. The phased policy executes stages in a topological order. For example, a hash-join will not schedule tasks from the probe phase until it’s finished with the build phase. The phased policy improves memory efficiency for the batch use case.

  [![](https://substackcdn.com/image/fetch/$s_!iYqJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F065e51ba-6cca-4475-b5c2-415e5b8a2af7_642x294.png)](https://substackcdn.com/image/fetch/$s_!iYqJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F065e51ba-6cca-4475-b5c2-415e5b8a2af7_642x294.png)

  Image created by the author.

> *In a hash join, the build phase creates a lookup table (by hashing) from one dataset. The probe phase uses this table to find matching rows from the lookup table.*

* **Task Scheduling**: The task scheduler categorized stages into leaf and intermediate. The leaf stages read data from the connector, and the intermediate stages process results from other stages. **Leaf stages** read data from connectors; placement considers network and connector constraints. **Intermediate Stages** process intermediate results; they can be placed on any worker node.

  [![](https://substackcdn.com/image/fetch/$s_!IAY9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92eae417-2b1e-4249-99ee-14b0c0704f79_544x360.png)](https://substackcdn.com/image/fetch/$s_!IAY9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92eae417-2b1e-4249-99ee-14b0c0704f79_544x360.png)

  Image created by the author.

In a leaf stage, the node receives one or more splits (chunks of data) from the external systems. The coordinator must assign one or more splits to a leaf stage task for it to become eligible to run. Intermediate-stage tasks are always eligible to run and finish when all upstream tasks are completed.

The coordinator assigns splits after Presto sets up tasks for the worker nodes. Presto asks connectors to enumerate small batches of splits and assigns them to tasks lazily. This has some benefits:

* Queries that don't need to process all data, like those with filters or LIMIT clauses, can be canceled early**.**
* It separates the time it takes to get the first result from the total time it takes to enumerate all splits. This is useful when connectors like Hive might take significant time to list all partitions and files.
* Lazy enumeration prevents storing all split metadata in memory; a Hive connector can handle millions of splits.
* The worker has a queue of assigned splits. The coordinator assigns splits to tasks with the shortest queue, keeping the queue size small and helping manage variations in processing times across different splits and worker performance.

### Query Execution

A thread executes in a loop over a split. The data unit the driver loop operates on is a page, a columnar encoding of a sequence of rows.

[![](https://substackcdn.com/image/fetch/$s_!WuPn!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6ab8f96-d25d-41d2-a934-63b9d44010c1_1528x658.png)](https://substackcdn.com/image/fetch/$s_!WuPn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6ab8f96-d25d-41d2-a934-63b9d44010c1_1528x658.png)

Image created by the author.

Presto uses in-memory buffered shuffles over HTTP for efficient data exchange between worker nodes. Workers store produced data in the memory so other workers can consume it by issuing HTTP polling. The engine tunes parallelism to maintain target utilization rates for output and input buffers. Full output buffers cause split execution to stall and take up all memory, while underutilized input buffers add unnecessary processing overhead.

For the result writing process, Presto employs an adaptive approach to increase writer concurrency dynamically.

### Resource management

Presto is ideal for multitenant deployments because of its fine-grained resource management system; a cluster can handle hundreds of queries at the same time.

Facebook designed Presto's CPU scheduling mechanism to maximize overall cluster throughput; they prioritize the total CPU time spent processing data.

Presto uses a cooperative multitasking model and schedules concurrent tasks on every worker node to achieve multi-tenancy. A given split can only run on a threat for a maximum execution time slice, called quanta. After that time, the thread will stop processing this split, whether it is finished or not. This approach ensures that no single split takes all the resources and allows for efficient sharing among multiple queries.

[![](https://substackcdn.com/image/fetch/$s_!XvzE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbea56aff-4e23-4f8e-b6d4-3fae287dd2aa_528x328.png)](https://substackcdn.com/image/fetch/$s_!XvzE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbea56aff-4e23-4f8e-b6d4-3fae287dd2aa_528x328.png)

Image created the author.

> *[Cooperative multitasking](https://www.devx.com/terms/cooperative-multitasking/) is a multitasking method used by operating systems where each running process must periodically signal that it has completed its task or that it no longer needs CPU resources to allow other processes to execute. This approach relies on the voluntary cooperation of each process to take control of system resources to other processes.*

Presto provides a mechanism for operators to give up control to address the challenges of long-running computations within a cooperative multi-tasking environment. If an operator exceeds its quanta, the scheduler “charges" the task with the thread time used, temporarily reducing its future execution frequency.This adaptability ensures efficient resource sharing even with diverse query shapes.

Instead of predicting resource needs in advance, Presto classifies tasks based on their accumulated CPU time. As a task uses more CPU, it moves to higher queue levels, each receiving a configurable fraction of the available CPU time. This strategy ensures that less demanding queries receive resources, as they accumulate less CPU time and remain in lower queue levels. This reflects the expectation that users prioritize fast responses for interactive queries while being less sensitive about the return time of intensive jobs.

After the CPU, we will see how Presto manages memory resources.

Presto categorizes memory allocations as user or system memory. User memory refers to memory usage that users can estimate based on their understanding of the query and data. System memory represents usage from implementation choices, such as shuffle buffers.

Presto has limits on user and total memory (user + system). It will kill a query requiring a memory resource larger than the cluster’s memory or a per-node limit. These separate limits provide flexibility in managing diverse workloads.

When a worker node's memory is exhausted, Presto halts task processing on that node. Presto employs several strategies to address memory pressure and prevent cluster instability:

* **Spilling**: Presto can revoke memory from eligible tasks when a node runs out of memory by writing their in-memory state to disk. Presto prioritizes the process based on task execution time, starting with the longest-running tasks. Of course, spilling to disk will increase the overall query response time. At Facebook, they don’t enable spilling by default because users appreciate the predictable latency of in-memory execution.

  [![](https://substackcdn.com/image/fetch/$s_!vfQN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ef71d04-cf8d-4f85-a133-81b5f430fd8e_400x298.png)](https://substackcdn.com/image/fetch/$s_!vfQN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ef71d04-cf8d-4f85-a133-81b5f430fd8e_400x298.png)

  Image created by the author.
* **Reserved Pool:**Another mechanism is the reserved memory pool. Presto divides the node’s memory pool into general and reserved pools. Presto promotes the query to consume memory resources in the reserved pool. The system counts this query's memory usage against the reserved pool, preventing it from competing with other queries for the general pool.

  [![](https://substackcdn.com/image/fetch/$s_!J-ns!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b3bee58-2c52-4a7d-8721-5a3509a073a0_392x304.png)](https://substackcdn.com/image/fetch/$s_!J-ns!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b3bee58-2c52-4a7d-8721-5a3509a073a0_392x304.png)

  Image created by the author.

### Fault Tolerance

Here are the effects if failures happen:

* **Coordinator:** If the coordinator fails, the cluster becomes unavailable.
* **Worker Node:** If a worker node crashes, all queries running on that node will fail

To mitigate the impact of these failures, Presto relies on external mechanisms:

[![](https://substackcdn.com/image/fetch/$s_!1FXB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ad35fc9-f2f8-4b74-b58c-a452afa8cb2c_942x374.png)](https://substackcdn.com/image/fetch/$s_!1FXB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ad35fc9-f2f8-4b74-b58c-a452afa8cb2c_942x374.png)

Image created by the author.

* **Standby Coordinators:** Facebook employs a backup coordinator, ready to take over if the primary one fails.
* **Multiple Active Clusters:** Facebook runs multiple active Presto clusters. If one cluster fails, queries can run on another available cluster.
* **External Monitoring:** External systems monitor Presto clusters, identify failing nodes, and remove them from the cluster

While these mechanisms reduce downtime, they can't eliminate it. Implementing traditional fault tolerance methods like checkpointing or replication is challenging and resource-intensive. At the time of paper writing, Facebook was working to improve fault tolerance for long-running queries.

---

## Optimization

> *Facebook implement some techniques to optmize the Presto query processing.*

### JVM and Code Generation

Because Facebook developed Presto in Java, they leverage the strengths of the Java Virtual Machine (JVM) while minimizing the impact of its limitations**.** Presto utilizes the JVM's Just-In-Time (JIT) compiler to optimize performance-critical code.

Presto avoids allocating large objects to prevent performance issues and uses flat memory arrays for critical data structures, reducing garbage collection overhead.

### File Format Features

Presto utilizes features of columnar file formats to optimize data processing:

* **Data Skipping**: Custom readers for formats like ORC and Parquet use statistics in file headers and footers (e.g., min-max ranges, Bloom filters) to efficiently skip irrelevant data sections.

  [![](https://substackcdn.com/image/fetch/$s_!9MHK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9cd5b2b0-8474-41b2-9043-04847867e5eb_622x426.png)](https://substackcdn.com/image/fetch/$s_!9MHK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9cd5b2b0-8474-41b2-9043-04847867e5eb_622x426.png)

  Image created by the author.
* **Direct Block Conversion**: The readers can directly convert compressed data into Presto's native block format, enabling efficient processing without decompression overhead.

  [![](https://substackcdn.com/image/fetch/$s_!_uE-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F291eeeef-a905-44b2-add0-a7c0291005e1_474x332.png)](https://substackcdn.com/image/fetch/$s_!_uE-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F291eeeef-a905-44b2-add0-a7c0291005e1_474x332.png)

  Image created by the author.

### Working with Compressed Data

Presto processes data in its compressed form whenever possible:

* **Dictionary and Run-Length-Encoded (RLE) Block Processing**: Presto performs operations right on compressed data, taking advantage of their structure for efficient processing. It processes dictionaries in fast, unconditional loops, and their structure is exploited during hash table building for joins and aggregations.

* **Compressed Intermediate Results**: Presto produces compressed intermediate results, minimizing data movement and storage. For instance, the join processor generates dictionary or RLE blocks for output data, leveraging the existing compressed structures.

### Lazy Data Loading

Presto supports lazy materialization, loading, and processing data only when required: Presto only decompresses and decodes data in compressed blocks (dictionary or RLE) when accessing the block’s cells. This minimizes the data fetched and processed, leading to significant performance gains.

---

## Outro

Above are all my notes after reading the paper [Presto: SQL on Everything](https://research.facebook.com/publications/presto-sql-on-everything/) from Facebook.

We explored why Facebook created Presto, its history, architecture, key decisions made during its development, and the optimization techniques it implemented for the query engine.

Thank you for reading this far.

See you on my following pieces.

---

## **References**

*[1] Facebook, [Presto: SQL on Everything](https://research.facebook.com/publications/presto-sql-on-everything/) (2019)*

*[2] Wikipedia, [Presto (SQL query engine)](https://en.wikipedia.org/wiki/Presto_(SQL_query_engine))*
