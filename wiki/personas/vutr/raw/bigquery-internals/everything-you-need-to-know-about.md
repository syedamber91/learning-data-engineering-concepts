---
title: "I spent 6 hours understanding the design principles of BigQuery. Here's what I found"
channel: vutr
author: "Vu Trinh"
published: 2024-01-20
url: https://vutr.substack.com/p/everything-you-need-to-know-about
paid: false
topics: ["Data Engineering", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Lakehouse", "Orchestration"]
tags: [dremel, https, storage, google, query, bigquery]
---

# I spent 6 hours understanding the design principles of BigQuery. Here's what I found

*All insights from BigQuery academic paper.*

> Source: [Open post](https://vutr.substack.com/p/everything-you-need-to-know-about)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

[![](https://substackcdn.com/image/fetch/$s_!-gKV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e0ab8ad-f137-452b-b993-05977b552014_1297x898.png)](https://substackcdn.com/image/fetch/$s_!-gKV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e0ab8ad-f137-452b-b993-05977b552014_1297x898.png)

> TL: DR
>
> Key insights from the paper **Dremel: A Decade of Interactive SQL Analysis at Web Scale**
>
> \*\* Dremel is BigQuery’s processing engine \*\*
>
> * They get back to SQL again.
> * Disaggregation of storage and shuffle layer
> * Bringing compute power close to the data.
> * Serverless architecture
> * Handling Semi-structured data in columnar storage
> * Improve performance

---

## Intro

I have already published two articles discussing interesting features of BigQuery after reading [its academic paper](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf):

1. Separated Intermediate Shuffle layer.
2. Nested and repeated fields.

However, I have come to realize that these articles are not enough to cover all the cool aspects I observed in the paper.

To explore and simplify these insights for better understanding, I have to create another article.

That's why I am writing this one.

> Even though this article focuses on the design principles of BigQuery, I will use the term 'Dremel' instead of 'BigQuery' to convey the information.
>
> This choice is made because, in the academic paper, Dremel is the main subject mentioned.
>
> Additionally, it's important to note that Dremel serves as the processing engine for BigQuery, meaning that all the features and design principles of Dremel also apply to BigQuery.

---

## They fall in love with SQL… again

> *SQL is inevitable*

Google admits that they used to believe “SQL doesn’t scale“.

With that in mind, they had moved away from SQL almost completely.

They sacrificed the ease of use (of SQL) for solving the scalability problem.

This made data analyst users have to switch to other imperative programming languages to execute the analysis jobs - which took hours in total to write, build, and debug.

Dremel came to the rescue.

Following Google, it was one of the first systems to reintroduce SQL.

For the first time, the analysis jobs could now be prepared in minutes and executed in seconds

> *The ability to interactively and declaratively analyze huge datasets, ad hoc, in dashboards, and other tools, unlocked the insights buried inside huge datasets, which was a key enabler for many successful products*

(“Interactively”, and “declaratively”, sound like SQL to me )

After falling in love with SQL again, they realized a problem: Google has many systems used for different purposes which also have different SQL dialects.

To address this complexity, they introduced the GoogleSQL project - unifying SQL implementation that could be shared across all SQL-like systems.

If you are a Google Cloud user, you will benefit from this: all the SQL systems like BigQuery, Cloud Spanner, and Cloud Dataflow, all using GoogleSQL project.

Theoretically, you can get the SQL from BigQuery and make it run at Cloud Spanner with just a little effort.

Google also notice the pattern of “Break up and get back together“ with SQL in the open-source world.

> *Users outside Google had similar scale and cost challenges with increasing data sizes. Distributed file systems and MapReduce became popular with Hadoop, and a suite of other NoSQL systems followed. These users faced the same challenges with complexity and slow iteration. A similar pivot back to SQL has happened, witnessed by the popularity of systems like HiveSQL, SparkSQL, and Presto.*

---

## Disaggregation

> Google not only separates the compute and storage but also the shuffle intermediate layer

> *Disaggregation: A division or breaking up into constituent parts, which have been aggregated or lumped together. [— Wikipedia —](https://en.wiktionary.org/wiki/disaggregation)*

The term “*Disaggregation*“makes me confused, so I will use the term “Separation“ instead.

### Storage Layer

In the beginning, Dremel operated on a few hundred shared-nothing servers. Each server kept a subset of the data on local disks.

Because at the time, it seemed it seemed the best way to squeeze out maximal performance from an analytical system was by using dedicated hardware and direct-attached disks.

In 2009, a significant shift occurred as Dremel was moved to [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) (think Kubernetes) to accommodate the increasing workload. This involved storing portions of each table on three different local disks, managed by independent servers, enabling data sharing across jobs.

This means storage and processing were coupled, which led to number of disadvantages:

* Data needs to be shifted around when resizing the cluster.
* Storage and computing can not scale independently.

Given the improvement in Google’s storage and network, they decide to revisit the shared-nothing architecture.

Google gradually shifted to shared-disk architecture which leverages the Google File System (GFS) (think S3):

> * *Their first experiment with GFS resulted in “order-of-magnitude performance degradation”.*
>
>   *→ Shared-disk architecture means the compute needs to access the storage through the network which surely increases the query latency compared to the approach where data is located directly on local disks.*
> * *They took a lot of time to fine-tune the storage format, metadata representation, query affinity, and prefetching,… to improve the query latency (Will come back with this in the final section).*
> * *Their effort finally made the Dremel on “separated storage“outperform the local-disk-based approach.*

Besides reducing query latency and complexity, this had several other advantages:

> * *GFS was a fully managed internal service, which improved the SLOs and robustness of Dremel.*
> * *The initial step of loading shared tables from GFS onto Dremel server’s local disks was eliminated.*
> * *It became easier to onboard other teams to the service since it is not necessary to resize the clusters to load their data.*

### Shuffle Intermediate Layer

[![](https://substackcdn.com/image/fetch/$s_!mmiz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d245062-08a8-452e-9952-ffb25d1354c8_1232x826.png)](https://substackcdn.com/image/fetch/$s_!mmiz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d245062-08a8-452e-9952-ffb25d1354c8_1232x826.png)

At first, Dremel did not support join operation. Then they added support for distributed joins through a shuffle primitive which is inspired by the MapReduce shuffle implementation.

Due to limitations in the coupling architecture of compute nodes and the intermediate shuffle, they decided to take a different approach.

The main idea is quite similar to that of storage: they aim to separate the shuffle layer.

I have written a detailed article about the separated shuffle layer of Dremel, which includes all the context and problems that led to Google making this decision. You can find it [here](https://vutr.substack.com/p/bigquery-processing-engine-shuffle?r=2rj6sg&utm_campaign=post&utm_medium=web).

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Did Google first introduce the “Lakehouse“?

Dremel’s initial design in 2006 was similar to traditional DBMSs: users need to load data into Dremel.

This means data can only be accessed by Dremel.

But at the time of migrating Dremel to shared-disk architecture (leveraging GFS), Google introduced a shared storage format which has two properties:

* Columnar
* Self-describing (which has metadata to describe data)

With the self-describing characteristics of the storage format in GFS, custom data transformation tools, and SQL-based analytics can utilize data in this format without the need for prior data loading.

Any file in the storage system could be part of the queryable data repository.

Having all of Dremel’s data available in shared storage with a standard format created an environment in which many tools could use and leverage this data.

Now, users don’t have to load data into the data warehouse; they just need to bring the warehouse’s computing power close to the data.

(Doesn't this sound like the concept of Lakehouse?)

---

## Serverless

> *All you need is inputting your SQL*

[![](https://substackcdn.com/image/fetch/$s_!AN1m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd712f3-403e-4d2a-b7a1-fbf3c3ad3e33_1161x874.png)](https://substackcdn.com/image/fetch/$s_!AN1m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccd712f3-403e-4d2a-b7a1-fbf3c3ad3e33_1161x874.png)

BigQuery Serverless. How magical it is.

### Ideas

At the time when Dremel was introduced, most data warehouse products out there were deployed on dedicated servers.

However, with Dremel, Google took a different approach.

Initially, Google took advantage of three core ideas to enable serverless analytics:

> * *The separation of compute, storage, and memory allows on-demand scaling and sharing of compute independently from storage.*
> * *Dremel’s query execution was built based on the assumption that the underlying compute resources may be slow or fail.*
>
>   + *→ Each sub-task in a query had to be deterministic and repeatable so in case of failure, only a small portion of the work needed to be restarted on another worker.*
>   + *→ Multiple copies of the same task have to be allocated to multiple workers to support the scenario whenever a worker fails.*
> * *Instead of relying on specific machine types and shapes, Dremel scheduling logic was designed to work with abstract units of compute and memory called slots.*
>
>   + *→ Slots continue to be the core customer-visible concept of resource management in BigQuery.*

### Dremel Serverless architecture

#### Centralized Scheduling

Dremel switched to centralized scheduling in 2012 which allowed more fine-grained resource allocation, the new scheduler uses the entire cluster state to make scheduling decisions which enables better utilization and isolation.

#### Shuffle Persistence Layer

The separated architecture allows decoupling scheduling and execution of different stages of the query.

Considering the result of shuffle as a checkpoint of the query execution state, the scheduler has the chance to dynamically schedule workers (because it is stateless now).

#### Flexible Execution DAGs

Originally, Dremel had a fixed execution tres, but it had evolved:

> * *The query coordinator is the first node receiving the query. It builds the query plan and then orchestrates the query execution with workers given to it by the scheduler.*
> * *Workers are allocated as a pool. Once the coordinator decides on the execution plan, it sends the plan (tree) to the workers.*
> * *Workers from the leaf stage read from the storage layer and write to the shuffle persistence layer, while workers from other stages read and write from/to the shuffle persistence layer. Once the entire query is finished, the final result is stored in the shuffle persistence*

#### Dynamic Query Execution

Dremel often needs to operate on previously unseen data, as discussed in the section **'Did Google first introduce the “Lakehouse“?'** above. This results in a lack of statistical information about the data.

Consequently, Dremel encounters challenges in the query planning phase since it is challenging to efficiently produce an execution plan when the nature of the data is unknown.

Google overcame this by allowing Dremel to dynamically change the query execution plan at run time, based on the statistics collected during query execution.

This approach is also backed by the separate intermediate shuffle layer and centralized query orchestration by the query coordinator.

---

## Semi-structured data in columnar storage

#### Nested and repeated field

To handle nested and repeated fields in columnar storage, Google introduced two notions:

> * *Definition level: Represents a nested field and specifies which ancestor records are absent when an optional field is not present.*
> * *Repeated level: Represents a repeated field (array-like data) and specifies, for repeated values, whether each ancestor record is appended to or starts a new value.*

If you want to understand more about this, [I also have a deep-dive article](https://open.substack.com/pub/vutr/p/lesson-learned-after-reading-bigquery?r=2rj6sg&utm_campaign=post&utm_medium=web) that was published a week ago.

Here's a fact for you: Parquet, one of the most famous columnar storage formats, also applies this encoding.

#### Capacitor file format

In 2014, Google began migrating the storage to a new columnar format: Capacitor.

(When you load data directly into BigQuery, data will be written in Capacitor format).

The Capacitor file format incorporates new features to enhance performance:

> * *Partition and predicate pruning: Various statistics are maintained about the values in each column which are used both to eliminate partitions that are guaranteed to not contain any matching rows.*
> * *Skip-indexes: At write time Capacitor combines column values into segments, which are compressed individually. The column header contains an index with offsets pointing to the beginning of each segment. When the filter is very selective, the Capacitor uses this index to skip segments that have no hits, avoiding their decompression.*
> * *Predicate reordering: Capacitor uses a number of heuristics to make filter reordering decisions, which take into account dictionary usage, unique value cardinality, NULL density, and expression complexity.*
> * *Row reordering: Capacitor uses several standard techniques to encode values, including dictionary and [run-length encodings (RLE)](https://en.wikipedia.org/wiki/Run-length_encoding). RLE in particular is very sensitive to row ordering. Usually, row order in the table does not have significance, so Capacitor is free to permute rows to improve RLE effectiveness.*
> * …

You can read more about [Capacitor here](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format).

---

## Unavoidable problem: latency

The above design choices, such as "separation" and "bringing compute power close to the data," seem not to be a standard way to build a system for interactive query latency.

Conventional wisdom at that time (and even now) suggests that colocating processing with data reduces data access latency, and dedicated machines would be faster than serverless machine resources.

Google has shared some techniques to improve performance:

> * ***Stand-by server pool**: With a distributed SQL execution engine, it is possible to bring up a system and have it ready to process queries as soon as they are submitted.*
> * ***Speculative execution**: Dremel breaks the query into thousands of small tasks, where each worker can pick up tasks as they are completed. In this way, slow machines process fewer tasks and fast machines process more tasks.*
> * ***Column-oriented schema representation**: Dremel’s storage format was designed to be self-describing. The schemas used at Google often contain thousands of fields. Parsing a complete schema might take longer than reading and processing the data columns from a partition. To address that, Dremel’s internal schema representation was itself stored in a columnar format.*
> * ***Balancing CPU and IO with lightweight compression**: The key is to pick a compression scheme that balances data size reduction with CPU decompression cost so that neither CPU nor IO becomes the bottleneck.*
> * ***Approximate results**: Many analyses do not require 100% accuracy, so providing approximation algorithms for handling top-k and count-distinct can reduce latency*
> * ***Query latency tiers**: To ensure that “small” queries remain fast and do not get blocked by users with “large” queries, Dremel used a dispatcher on the intermediate servers to schedule resources fairly.*
> * ***Reuse of file operations**: Reusing metadata obtained from the file system by fetching it in a batch at the root server and passing it through the execution tree to the leaf servers for data reads*
> * ***Guaranteed capacity**: When guaranteed capacity is underutilized, these resources are available for others to use, but when requested those resources are immediately granted to the customer.*

---

## Outro

In this article, I have delivered key insights from the paper **Dremel: A Decade of Interactive SQL Analysis at Web Scale** with my perspective.

I hope it helps you learn something after reading it.

—

I understand in advance that writing an article to convey insights from an academic paper is not an easy task.

However, I have decided to take on this challenge.

My goal is to challenge myself to present difficult and complex concepts in a way that is easy to understand.

I plan to continue with papers writing about other OLAP databases like Snowflake or Databricks

Wish me luck.

---

References: [Dremel: A Decade of Interactive SQL Analysis at Web Scale](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/everything-you-need-to-know-about/comments)

It might take you 3 minutes to read but it took me more than 3 days to prepare, so it will motivate me a lot if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
