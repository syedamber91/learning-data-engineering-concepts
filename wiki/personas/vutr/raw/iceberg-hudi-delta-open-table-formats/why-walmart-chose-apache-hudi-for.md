---
title: "Why Walmart Chose Apache Hudi for Their Lakehouse"
channel: vutr
author: "Vu Trinh"
published: 2025-02-20
url: https://vutr.substack.com/p/why-walmart-chose-apache-hudi-for
paid: false
topics: ["Apache Spark", "Apache Iceberg", "Delta Lake", "Data Lake", "Lakehouse", "Streaming", "Batch Processing", "Change Data Capture"]
tags: [https, hudi, auto, image, walmart, file]
---

# Why Walmart Chose Apache Hudi for Their Lakehouse

*What can we learn.*

> Source: [Open post](https://vutr.substack.com/p/why-walmart-chose-apache-hudi-for)

## Topics

[[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[change-data-capture|Change Data Capture]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=156666967)

[![](https://substackcdn.com/image/fetch/$s_!aKW9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f5d0b14-95f8-4110-beed-45144e0b61b3_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!aKW9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f5d0b14-95f8-4110-beed-45144e0b61b3_2000x1429.png)

Image created by the author.

---

## Intro

Apache Hudi often flies under the radar compared to Delta Lake and Iceberg. While both of these formats are popular in modern data lakes, Hudi has a unique design that prioritizes incremental and real-time processing. This makes it particularly valuable for organizations with constantly changing data. However, it doesn't get as much attention in discussions about modern data architectures.

Curious about its adoption, I scoured the internet for real-world implementations of Hudi. That’s when I came across Walmart’s case study.

Walmart, one of the largest retailers globally, decided to use Hudi for its lakehouse transformation. Their journey provides valuable insights into how large enterprises select, implement, and optimize data formats for real-time data processing.

In this issue, we’ll explore Walmart’s decision to use Hudi, their challenges, and the lessons we can learn from their experience. By the end, you’ll gain practical takeaways to help you make informed decisions when selecting a data format for your lakehouse.

---

## About Walmart

Before diving into the technical details, let’s get a sense of Walmart’s scale:

* 10,000+ stores worldwide
* Millions of transactions per hour
* 600K+ compute cores across Hadoop and Spark clusters

The company needed a solution to keep up with their evolving data needs.

---

## Evolving to a Near Real-Time Lakehouse

Walmart wanted to transition from a **batch-oriented data lake** to a **modern lakehouse** that supports near real-time data processing. This transformation would allow them to:

* Make faster decisions with fresher data
* Improve operational efficiency
* Enable real-time analytics

Additionally, they needed to maintain **complete control** over their infrastructure while operating across **multiple cloud providers**. They wanted an open-source format that would prevent vendor lock-in and allow them to optimize performance across their diverse tech stack.

The main issue was that Walmart’s existing batch-oriented system could not support it; without addressing these problems, the company risked falling behind in real-time analytics and operational intelligence.

* Low-latency updates for operational and analytical queries
* Efficient handling of late-arriving data
* Optimized ingestion performance across multiple workloads

We live in an era of unprecedented data generation, making real-time insights and decision-making more critical than ever. While not every organization operates at Walmart's scale, many face similar challenges when transitioning from batch processing to real-time data architectures. Companies exploring streaming and incremental processing technologies can draw valuable lessons from Walmart’s approach.

Let's dive into Walmart's detailed approach.

---

## How did Walmart choose the table format?

They spend a lot of time evaluating and benchmarking Delta Lake, Iceberg, and Hudi to select the table format that best fits their needs. This format must help them evolve batch to real-time analytics and provide complete control without vendor lock-in.

Walmart abstracts the two most popular current workloads to do the benchmark.

* The batch workload deals with partition tables (by year, month, day, or hour). It suffers from late-arriving records, causing the Spark worker to read and write many partitions in the past (e.g., one-week-late data causes Spark to update a partition from one week ago). The workload characteristics are < 0.1% Updates and > 99.9% Inserts.
* The streaming workload deals with row-level upsert to data with low latency. A multi-TB Cassandra table produces these updated data via change data capture. The workload characteristics are > 99.999% Updates and < 0.001% inserts.

They started by addressing the ingestion aspect of this workload. To prepare for the benchmarking, Walmart isolated the three separate environments. Then, they deployed ingestion jobs (Delta, Hudi, Iceberg, Legacy) in these environments, giving them time to reach a steady state.

[![](https://substackcdn.com/image/fetch/$s_!LzFq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b49db29-ec7a-44fd-84ce-7b8fb85aa0e0_591x343.png)](https://substackcdn.com/image/fetch/$s_!LzFq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b49db29-ec7a-44fd-84ce-7b8fb85aa0e0_591x343.png)

Ingestion Benchmark Scores (GB-ingested \* Time [min]) / Cores. Source: [Lakehouse at Fortune 1 Scale (2023)](https://medium.com/walmartglobaltech/lakehouse-at-fortune-1-scale-480bcb10391b)

The Hudi + Spark 3.x. was the most performant for the batch workload, more than five times faster than the legacy systems.

Delta Lake is 27% faster than Hudi for the steaming workload. However, Hudi’s compaction process was faster because its approach lacked the ZOrdering optimizations in the Delta pipeline. This Delta optimization pays off later when it significantly improves the query performance.

When it comes to query performance, Walmart leverages [TPC-H](https://medium.com/walmartglobaltech/lakehouse-at-fortune-1-scale-480bcb10391b) for benchmarking. They use Queries 1 to 7 for the batch workload and Queries 1 to 10 for the streaming workload.

[![](https://substackcdn.com/image/fetch/$s_!tG-x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F172bf639-43a7-4540-9644-680ffc24baba_555x277.png)](https://substackcdn.com/image/fetch/$s_!tG-x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F172bf639-43a7-4540-9644-680ffc24baba_555x277.png)

Query Benchmark Scores — Median Query times [min] across typical workloads. Source: [Lakehouse at Fortune 1 Scale](https://medium.com/walmartglobaltech/lakehouse-at-fortune-1-scale-480bcb10391b) (2023)

Delta Lake outperformed in most queries by about 40%, primarily due to its ZOrdering feature, which optimized query performance. However, Hudi excelled in real-time deduplication, providing faster access to the latest record. Since the benchmark, Hudi has introduced ZOrdering and improved filegroup metadata management, likely narrowing the performance gap significantly.

Regarding Iceberg, Walmart encounters challenges cleaning up to provide an optimal file size during the ingestion job. So, they skip implementing the ingestion and query benchmarking on Iceberg.

Walmart chooses Hudi in the end.

With a highly diverse tech stack spanning **600K+ cores on Hadoop and Spark** across **Google Cloud and Azure**, Hudi seamlessly integrates into the system.

So Hudi is excellent:

* It supports both batch and streaming workloads.
* It offers incremental processing capabilities, reducing the need for full table rewrites.
* It enables efficient upserts and deletes using unique keys and indexing.
* Hudi offers standout features, including Bloom filters, commit notifications, and monitoring interfaces.

But how does Hudi do all of these things? Its architecture and designs play a crucial role here.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=156666967)

---

## How Hudi Works: Architecture and Design

### Metadata Management

Metadata files are stored in <base\_path>/.hoodie/ directory. Here, a file called hoodie.properties contains Hudi table configurations, such as table name, version, partition scheme, file format, or table type.

[![](https://substackcdn.com/image/fetch/$s_!ZRrS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17d9715b-f55a-4610-983e-57f9aad15110_1460x946.png)](https://substackcdn.com/image/fetch/$s_!ZRrS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17d9715b-f55a-4610-983e-57f9aad15110_1460x946.png)

Screenshot of the hoodie.properties

Besides hoodie.properties, metadata files record transactional actions on the table, constructing the table's Timeline.

[![](https://substackcdn.com/image/fetch/$s_!Cdb-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffac3770a-e22f-43a0-8b60-712f8ebae607_622x136.png)](https://substackcdn.com/image/fetch/$s_!Cdb-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffac3770a-e22f-43a0-8b60-712f8ebae607_622x136.png)

Screenshot of the Hudi transactional metadata files.

### Hudi Timeline

Hudi Timeline records all actions performed on the table at different instants, providing instantaneous views of the table while efficiently supporting the retrieval of data in the order of arrival.

[![](https://substackcdn.com/image/fetch/$s_!tVIv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa942fe10-04b8-479e-b8c1-a12a9fed4b2d_1470x614.png)](https://substackcdn.com/image/fetch/$s_!tVIv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa942fe10-04b8-479e-b8c1-a12a9fed4b2d_1470x614.png)

Image created by the author.

A Hudi instant consists of the following components. Each transactional metadata file is associated with an instance. The file has the following pattern:

<instant timestamp>.<instant action>[.<instant state>]

A Hudi instant consists of:

* Instant timestamp: Instant time is typically a timestamp (e.g., 20241004000131320 from the screenshot), which monotonically increases in the order of the instant action’s beginning time.
* Instant action: Type of actions that can be performed on the table. COMMITS refer to an atomic write of a batch of records. CLEANS remove outdated file versions. DELTA\_COMMIT involves atomic writes to a MergeOnRead table, with data written to delta logs. COMPACTION reconciles data structures, such as converting updates from row-based logs to columnar formats, which appear as a special commit. ROLLBACK occurs when a commit fails, removing any partial files. Lastly, SAVEPOINT marks specific file groups as preserved for potential recovery, preventing their deletion by cleaners.
* State: At any given moment, instant action can be in one of three states: REQUESTED, indicating an action has been scheduled but not yet started; INFLIGHT, showing the action is currently in progress; and COMPLETED, marking the action as finished. Note: The metadata file associated with the COMPLETED state will have no state suffix. Hudi maintains two types of timelines:

Hudi manages timelines as active and archived timelines:

[![](https://substackcdn.com/image/fetch/$s_!QW_0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F619f7620-3ffa-4724-b341-670b18e13885_1838x512.png)](https://substackcdn.com/image/fetch/$s_!QW_0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F619f7620-3ffa-4724-b341-670b18e13885_1838x512.png)

Image created by the author.

* Active Timeline: It serves valid data files, ensuring that read requests don’t experience unnecessary latencies as the timeline grows. It is bounded by the instants (metadata files) it can serve.
* Archived Timeline: Hudi moves older timeline events to the archived timeline after certain thresholds. Generally, the archived timeline is not used for regular table operations but is kept for bookkeeping and debugging purposes. Any instances under the ".hoodie" directory refer to active timelines, while archived events are moved to the ".hoodie/archived" folder.

### Data Storage in Hudi

Hudi stores data as Base Files (in a columnar format like Parquet) and Log Files (in a row-based format like Avro). These files are structured into File Groups, each with multiple File Slices.

[![](https://substackcdn.com/image/fetch/$s_!pP5o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01bb900f-a7cc-4687-aaf1-e81febf2fa20_1550x694.png)](https://substackcdn.com/image/fetch/$s_!pP5o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01bb900f-a7cc-4687-aaf1-e81febf2fa20_1550x694.png)

Image created by the author.

* Base Files: Optimized for read efficiency.
* Log Files: Capture incremental changes for write optimization.

A Hudi table is divided into multiple file groups, similar to database sharding, where each group contains a subset of the table’s data. A File Group is uniquely identified by a fileId, and each group contains File Slices. Each slice has a single Base File (Parquet/ORC) and associated Log Files (Avro). A slice represents a version of the group at a specific time.

[![Image preview](https://substackcdn.com/image/fetch/$s_!umub!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e07c506-36f1-46b1-a356-b228bf942492_800x618.jpeg "Image preview")](https://substackcdn.com/image/fetch/$s_!umub!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e07c506-36f1-46b1-a356-b228bf942492_800x618.jpeg)

Image created by the author.

Hudi adopts Multiversion Concurrency Control (MVCC), where compaction action merges logs and base files to produce new file slices, and cleaning action removes unused/older file slices to reclaim space on the file system.

With this design, Hudi achieves:

* Read and write efficiency: The Base File format efficiently supports large data scans, while the row-based Log File format provides high performance for data writing.
* Data versioning: Each File Slice is tied to a specific timestamp on the Timeline, enabling tracking of how records within a File Group evolve.

### Indexing for Fast Record Lookups

Each record in a Hudi table has a unique identifier called a primary key, which consists of a pair of record keys and the partition path to which the record belongs.

[![](https://substackcdn.com/image/fetch/$s_!6vjO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55de7846-bc38-42fb-8ad3-14dbd5641177_1198x880.png)](https://substackcdn.com/image/fetch/$s_!6vjO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55de7846-bc38-42fb-8ad3-14dbd5641177_1198x880.png)

Image created by the author.

Using primary keys, Hudi ensures no duplicate records (primary keys) across partitions and enables fast updates and deletes on records. For non-partitioned tables, the primary key includes only the record key, which means Hudi enforces a record uniqueness constraint over the entire table.

Primary keys in Hudi are also referred to as "hoodie keys." Recalling that Uber faced challenges with data updates and deletions over HDFS, Hudi introduces a feature that sets it apart from Delta Lake or Iceberg—the index.

Hudi maintains an index to enable quick record lookups. This index maps hoodie keys to file groups (fileIds), and this mapping remains unchanged once the first version of a record is written to a file.

---

## Lessons Learned: What Data Engineers Can Apply

### **The Most Popular Tool Isn't Always the Best for Your Needs**

* Delta Lake and IcebergIceberg are widely used, but Hudi fits Walmart’s requirements best.
* Choose the right tool based on **workload characteristics and your company needs**, not popularity.

### **Benchmarking And Setting Benchmarking Are Crucial**

* Walmart ensured a **fair comparison** between Hudi, Delta Lake, and Iceberg.
* It is crucial to conduct performance tests fairly and in isolation. This can provide more accurate results, leading to more accurate decisions.

> *I don’t have hands-on experience with setting up benchmarking like this, so if you do, I’d love to hear from you! Feel free to share your insights and experiences in the comments—me and the readers would greatly appreciate it.*

### Open vs close

* The vendor's solutions are cool. They take care of everything. However, they will try to keep you in the loop as long as possible to maximize the lifetime value; this can limit your control over the technology and force you to depend on the vendor.
* If you want complete control, self-managed open-source deployments are a viable option. However, the trade-off for this is you have to manage everything.
* Once again, organizations must make this kind of decision based on their needs. Comparing what other companies do will not help.

---

## Outro

We explored how Walmart tackled their transition to a near real-time lakehouse by choosing Apache Hudi. Their decision was driven by the need for efficient batch and streaming processing, ensuring that they could seamlessly handle large-scale batch workloads and real-time data updates.

Another critical factor was maintaining control over their tech stack across multiple clouds. Walmart needed an open-source solution that would prevent vendor lock-in while allowing them to optimize their architecture across Google Cloud and Azure.

Finally, Walmart conducted careful benchmarking against Delta Lake and Iceberg, evaluating ingestion performance, query speed, and operational overhead. This thorough comparison helped them make an informed decision tailored to their unique needs.

Your Turn

What’s your experience with Hudi, Delta Lake, or Iceberg? Have you encountered challenges when deciding on a data lake format? Let’s discuss—reply to this email or share your thoughts in the comments!

---

## Reference

*[1] Samuel Guleff, [Lakehouse at Fortune 1 Scale](https://medium.com/walmartglobaltech/lakehouse-at-fortune-1-scale-480bcb10391b) (2023)*

*[2] [Enabling Walmart's Data Lakehouse With Apache Hudi](https://www.onehouse.ai/blog/enabling-walmarts-data-lakehouse-with-apache-hudi) (2024)*
