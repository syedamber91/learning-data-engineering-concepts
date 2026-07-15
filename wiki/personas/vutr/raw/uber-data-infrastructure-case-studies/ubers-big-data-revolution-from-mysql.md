---
title: "Uber’s Big Data Revolution: From MySQL to Hadoop and Beyond"
channel: vutr
author: "Vu Trinh"
published: 2024-09-14
url: https://vutr.substack.com/p/ubers-big-data-revolution-from-mysql
paid: false
topics: ["Apache Kafka", "Apache Spark", "Data Warehouse", "Data Lake", "Batch Processing", "Data Quality", "ETL"]
tags: [uber, https, auto, hadoop, image, fetch]
---

# Uber’s Big Data Revolution: From MySQL to Hadoop and Beyond

*Volume: 100+ PB Data, Latency: Minutes*

> Source: [Open post](https://vutr.substack.com/p/ubers-big-data-revolution-from-mysql)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[batch-processing|Batch Processing]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=148723247)

[![](https://substackcdn.com/image/fetch/$s_!GPhu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f1d45a3-9d00-48b4-a955-11579de6d7fa_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!GPhu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f1d45a3-9d00-48b4-a955-11579de6d7fa_2000x1429.png)

Image created by the author.

---

## Intro

This week, we journeyed through the evolution of Uber’s Big Data infrastructure, exploring the challenges, solutions, and innovations defining each phase of this transformation.

> ***Note**: This article primarily focuses on batch processing at Uber. For insights into their real-time processing, you can check my previous article [here](https://open.substack.com/pub/vutr/p/i-spent-7-hours-understanding-ubers?r=2rj6sg&utm_campaign=post&utm_medium=web). Additionally, this article references Uber’s original piece from 2018, so some details and figures may have changed since then.*

---

## Growing Pains of Data

> *Generation 1*

Data management was straightforward in Uber's early days. Before 2014, the company’s data was small enough to fit within a few MySQL and PostgreSQL databases.

Uber’s data was fragmented at this stage, spanning across different databases. Users who wanted a holistic view had to consolidate data manually.

[![](https://substackcdn.com/image/fetch/$s_!9n5e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdadd33c2-a901-42bf-b3e0-96ba8b24dccd_772x476.png)](https://substackcdn.com/image/fetch/$s_!9n5e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdadd33c2-a901-42bf-b3e0-96ba8b24dccd_772x476.png)

Image created by the author.

Although this setup worked for a time, Uber’s global expansion requires a more robust data solution. The number of riders, drivers, and trips exploded across many cities. Suddenly, Uber needed to handle not just terabytes but potentially petabytes of data, and they needed to do so in a reliable and scalable way.

### The First Data Warehouse

[![](https://substackcdn.com/image/fetch/$s_!aice!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bebeec0-ba52-4853-bac4-aa6a487522f8_976x685.png)](https://substackcdn.com/image/fetch/$s_!aice!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bebeec0-ba52-4853-bac4-aa6a487522f8_976x685.png)

Image created by the author.

Uber made a significant leap by building their first data warehouse. This new system centralized all of Uber’s data into a single place. Thanks to its speed, scalability, and column-oriented design, they chose Vertica for the data warehouse solution.

With Vertica, Uber’s engineers standardized SQL as the primary interface for data access, making it easy for thousands of users across the company to run queries and extract valuable insights.

After a few months, Uber’s data warehouse grew to tens of terabytes, and hundreds of users were querying the system daily.

However, it didn’t come without challenges. They observed the data unreliability through the ETL job that ingested data to the Vertica. In particular, the lack of a formal schema agreement between the upstream data producing and downstream data consuming led to frequent ingestion failures when the source data format changed. Uber’s data was often stored in flexible JSON formats, which made it hard to enforce schema consistency and caused frequent breakdowns in data pipelines.

[![](https://substackcdn.com/image/fetch/$s_!UjMf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1bbfecc-f711-414f-8583-6ba2ecc33e0a_777x356.png)](https://substackcdn.com/image/fetch/$s_!UjMf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1bbfecc-f711-414f-8583-6ba2ecc33e0a_777x356.png)

Image created by the author.

Furthermore, the lack of standardization in ingestion jobs led to the same data being ingested multiple times with different transformations, putting extra pressure on upstream data sources and increasing storage costs with duplicate data.

[![](https://substackcdn.com/image/fetch/$s_!rWTF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88c4d2d8-1baf-4431-ba1b-ac65d8dcc524_777x356.png)](https://substackcdn.com/image/fetch/$s_!rWTF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88c4d2d8-1baf-4431-ba1b-ac65d8dcc524_777x356.png)

Image created by the author.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=148723247)

---

## Hadoop as the Data Lake

> *Generation 2*

[![](https://substackcdn.com/image/fetch/$s_!ANM2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1ef562c-8b85-42a8-8611-eb16dbb7db3f_1278x681.png)](https://substackcdn.com/image/fetch/$s_!ANM2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1ef562c-8b85-42a8-8611-eb16dbb7db3f_1278x681.png)

Image created by the author.

Uber needed a new solution. They chose Hadoop as the heart of their next data platform generation; instead of loading data directly to the Vertica data warehouse, raw data is ingested into a Hadoop-based data lake.

This brought a whole new paradigm for Uber’s Big Data platform, allowing Uber to ingest and store vast amounts of raw data from various sources without transformation when ingestion.

This shift reduced the load on Uber’s source data stores, as data could now be ingested into Hadoop in its native format without pre-processing. Once the data was in Hadoop, it could be transformed and analyzed using various tools.

For the data consumption, the option is not only limited with the Vertica:

* For interactive queries, Uber used Presto, an open-source distributed SQL engine allowing fast querying of large datasets.
* Apache Spark was introduced for more complex data processing tasks, allowing teams to run large-scale jobs using SQL or programming languages.
* Apache Hive was also deployed to handle large queries.

Uber ensured all data transformations happened in Hadoop; only critical tables for real-time SQL queries were carried in the data warehouse. This allows fast backfilling and recovery; if these operations are required, they only need to process data already in Hadoop, avoiding touching data from the source.

The most critical aspect of Uber’s transition to Hadoop was the adoption of Apache Parquet, a columnar storage format that offered significant storage savings and compute resource efficiency. Parquet’s columnar nature allowed Uber to compress data more effectively, reducing storage costs and speeding up query performance for analytical workloads.

By the time the second generation of the data platform was fully onboarded, the company was ingesting tens of petabytes of data into its Hadoop data lake.

### Challenges of the Second Generation

While Hadoop enabled Uber to scale its data operations, it wasn’t perfect. One of the biggest challenges was the large number of small files in the HDFS, from ingestion or ad hoc batch jobs batch job or ETL process. The accumulation of these files began to put pressure on the HDFS NameNode, which is responsible for managing the file system’s metadata. As the number of files grew into the millions, the NameNode struggled to keep up.

[![](https://substackcdn.com/image/fetch/$s_!aiEg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9697009-59c8-4d15-9d2f-0ca4f2fd157e_692x496.png)](https://substackcdn.com/image/fetch/$s_!aiEg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9697009-59c8-4d15-9d2f-0ca4f2fd157e_692x496.png)

Image created by the author.

Another major issue was data latency. At the time, Uber’s data was only made available to users once every 24 hours, which was far too slow for many of the company’s real-time business needs. This delay limited Uber’s ability to make timely decisions in many cases, such as demand forecasting and fraud detection.

[![](https://substackcdn.com/image/fetch/$s_!25F5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b19cbbc-80c2-40a8-b66b-f18b5fcb0ee9_775x386.png)](https://substackcdn.com/image/fetch/$s_!25F5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b19cbbc-80c2-40a8-b66b-f18b5fcb0ee9_775x386.png)

Image created by the author.

Finally, while Hadoop solved many scalability issues, it didn’t support data updates or deletes. For example, rider and driver ratings, trip fare adjustments, and other real-time data must be updated frequently to ensure accurate reporting and analysis. However, Hadoop’s snapshot-based ingestion model meant that Uber had to re-load entire datasets from the source every time a minor update was made, which was inefficient and time-consuming.

---

## The Introduction of Hudi

> *Generation 3*

[![](https://substackcdn.com/image/fetch/$s_!g7WF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda265342-9fd2-4dfc-9259-b9477a51e910_980x555.png)](https://substackcdn.com/image/fetch/$s_!g7WF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fda265342-9fd2-4dfc-9259-b9477a51e910_980x555.png)

Image created by the author.

To address these challenges from the 2nd generation, they spent quite an amount of time identifying four primary pain points that need to be resolved in the next generation:

* **HDFS scalability limitation:** HDFS’s NameNode struggles when data exceeds 10 petabytes, worsening beyond 50-100 petabytes. Solutions like [ViewFS](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ViewFs.html) and [HDFS NameNode Federation](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/Federation.html), along with moving data to separate clusters, mitigated these issues.

  > ***HDFS ViewFS**: ViewFS provides a virtual filesystem in Hadoop, allowing users to access multiple HDFS clusters or directories through a unified namespace. It simplifies working with various HDFS locations by creating a seamless, single point of access.*
  >
  > ***HDFS NameNode Federation**: NameNode Federation improves HDFS scalability by using multiple independent NameNodes, each managing a portion of the namespace. This reduces bottlenecks, enhances fault tolerance, and supports larger deployments.*
* **Faster data in Hadoop:** Uber’s second-generation platform's 24-hour data latency was too slow for real-time needs. To speed up delivery, Uber had to re-design their pipeline for incremental ingestion of only updated and new data instead of loading full snapshots.
* **Support for updates and deletes in Hadoop/Parquet:** Uber’s data involves frequent updates, but snapshot-based ingestion wasn’t efficient.
* **Faster ETL and modeling:** Like raw data ingestion, ETL and modeling jobs rebuilt entire tables with each run. They shifted to incremental updates, pulling only changed data and updating derived tables without full rebuilds, reducing latency.

With that in mind, Uber developed an open-source project called Hudi (Hadoop Upserts and Incremental), which fundamentally transformed how data was ingested and managed in the Hadoop ecosystem.

Hudi introduced the ability to perform upserts (update-inserts) and incremental data ingestion, allowing Uber to move away from the snapshot-based ingestion approach. Instead of reloading entire datasets daily, Hudi enabled Uber to ingest only the changes—new records, incremental updates, and deletes—reducing data latency from 24 hours to under an hour.

This incremental approach improved data freshness and reduced the computational resources required to process updates. For example, instead of reprocessing an entire 100-terabyte dataset every time new data was added, Uber could now update only the relevant partitions, leading to significant efficiency gains.

Besides the creation of Hudi, Uber also streamlined data change between storage using Apache Kafka. All upstream datastore events, including logs from various services, were sent to Kafka with a unified Avro encoding.

Marmaray, Uber’s data ingestion platform, runs in mini-batches and consumes changelogs from Kafka. It applies them to existing Hadoop data via Hudi, allowing records to be updated or deleted. Behind the scenes of Marmaray are Spark jobs that run every 10-15 minutes, ensuring data latency remains under 30 minutes.

By eliminating the need for transformations during the ingestion phase, Marmaray ensured that raw data could be ingested quickly and reliably, with any necessary transformations performed downstream in Hadoop. Data reliability has also improved because they could avoid error-prone transformations during ingestion.

### Generalizing Data Ingestion

Uber’s number of upstream data stores increased over time. They decided to build a unified ingestion platform to streamline raw data ingestion into Hadoop. With this platform, the updating process can update Hadoop tables ***incrementally*** with a latency of 10-15 minutes. Hudi plays a vital role here; it allows ETL jobs to fetch only the changed data from the source table. Transfomration/modeling jobs only need to pass a checkpoint timestamp to the Hudi reader during each run to receive a stream of new or updated records from the raw source table.

> *I might have a deep dive article on Hudi soon ! ;)*

---

## Looking Ahead

> *Generation 4*

With the third generation of its Big Data platform, Uber has reached a point where its data infrastructure is robust, scalable, and efficient. In the next phase of Uber’s data journey, they planned to focus on four key areas:

1. **Data Quality**: Uber was working to enforce stricter schema validation on upstream data sources.
2. **Faster Data Access**: They aimed to reduce data latency by bringing raw data latency down to five minutes and modeling data latency to ten minutes.
3. **Operational Efficiency**: Uber moved away from dedicated hardware and embraced containerization for its services. This would allow for greater flexibility in resource management and ensure that jobs can be scheduled and executed more efficiently across the company’s Hadoop and non-Hadoop services.
4. **Scalability and Reliability**: Uber continued optimizing its data ingestion platform to make it more resilient and scalable by standardizing changelogs across all upstream data sources and adopting a more unified approach to data ingestion.

In the [May 2024](https://www.uber.com/en-SG/blog/uber-big-data-platform/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0) and [early September](https://www.uber.com/en-VN/blog/datamesh/) articles, Uber shared that they are migrating their batch processing infrastructure to Google Cloud.

---

## **Outro**

In this article, we explore Uber’s data platform journey from the MySQL databases to the Hadoop cluster and the creation of Apache Hudi. By learning about Uber’s data platform revolution, I hope we can gain valuable insights that can be applied to our data projects, even if they don't yet reach Uber's scale.

See you in the next article.

---

## **References**

*[1] Reza Shiftehfar, [Uber’s Big Data Platform: 100+ Petabytes with Minute Latency](https://www.uber.com/en-SG/blog/uber-big-data-platform/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0) (2018)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/ubers-big-data-revolution-from-mysql/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
