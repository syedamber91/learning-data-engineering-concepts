---
title: "The internal of BigQuery, Snowflake, Databricks and Redshift"
channel: vutr
author: "Vu Trinh"
published: 2025-04-17
url: https://vutr.substack.com/p/the-internal-of-bigquery-snowflake
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Lakehouse"]
tags: [https, auto, good, image, media, substackcdn]
---

# The internal of BigQuery, Snowflake, Databricks and Redshift

*4 famous cloud data warehouses in an article*

> Source: [Open post](https://vutr.substack.com/p/the-internal-of-bigquery-snowflake)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=161157477)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!xNC5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55f58fc2-f867-4184-9645-bff8708f0dc7_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!xNC5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55f58fc2-f867-4184-9645-bff8708f0dc7_2000x1429.png)

Image created by the author.

---

## Intro

I spent a lot of time researching and learning about OLAP systems, especially cloud data warehouse solutions like BigQuery, Snowflake, Databricks, and Redshift. This article acts as a summary of what I researched. Each section will give you the main ideas for each cloud warehouse solution.

In the world where you might work with Databricks today and then later have to learn Snowflake for your next job tomorrow, I hope this article could give you a good starting point when you begin to learn an entirely new cloud data warehouse.

> ***Note:** I organized this article so you can consume it however you want. You can read the whole article to get the big picture or focus only on your interested warehouse solution.*

---

## Cloud data warehouse

The 2010s witnessed [the emergence of the cloud-native shared-disk architecture](https://youtu.be/5J-I8Mj8tss?list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ) OLAP system with pioneers like Google BigQuery (2010) and Snowflake (2012).

Like traditional data management systems, these have a query engine and a place to store data. However, they store data separately in object storage (except for Redshift, at least for its initial design). The vendors manage the storage layer; the data can be in the system's proprietary format. (BigQuery, Snowflake, Redshift) or “quite“ open one (Databricks with Delta Lakes)

[![](https://substackcdn.com/image/fetch/$s_!ZiPu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc187c864-2f0b-4892-bc5b-0eae3a7620ec_268x300.png)](https://substackcdn.com/image/fetch/$s_!ZiPu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc187c864-2f0b-4892-bc5b-0eae3a7620ec_268x300.png)

Besides the paradigm shift (from share-nothing to shared disk), these OLAP systems also had more advanced query power processing; many workers can efficiently process and distribute data, and more importantly, users can benefit from this without needing to manage infrastructure.

—

Before diving into each warehouse solution, we must agree on some terms. You might have heard about column format before, which can help analytics workload more efficiently by allowing the engines to scan only the necessary columns. I want to make it more straightforward a little bit:

[![](https://substackcdn.com/image/fetch/$s_!HZyr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c11f4a9-c41c-4c6a-97d7-e22b410f47c9_404x388.png)](https://substackcdn.com/image/fetch/$s_!HZyr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c11f4a9-c41c-4c6a-97d7-e22b410f47c9_404x388.png)

* **Column Format**. I will use this to refer to the format where columns are stored completely separated
* **Hybrid Format**: I will use this to refer to the formats with the same characteristic as Parquet: it groups data into "row groups," each containing a subset of rows. (horizontal partition.) Within each row group, data for each column is called a “column chunk." (vertical partition)

Now, let’s first start with my favorite one: BigQuery.

---

## Google BigQuery

[BigQuery](https://cloud.google.com/blog/products/bigquery/bigquery-under-the-hood) combines many technologies. It uses [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system) for storage, [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) for computing management (think Kubernetes), and [Dremel](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf) for query processing engines.

[![](https://substackcdn.com/image/fetch/$s_!Se2S!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f1be63e-9f73-4f66-aec1-cac0f91782d7_336x518.png)](https://substackcdn.com/image/fetch/$s_!Se2S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f1be63e-9f73-4f66-aec1-cac0f91782d7_336x518.png)

### Compute

[Google introduced Dremel in 2010](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf). It is a processing query engine inspired by the MapReduce shuffle implementation.

[![](https://substackcdn.com/image/fetch/$s_!9sWP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31de7dcf-a21f-4ae1-bfa9-3988557636b9_466x346.png)](https://substackcdn.com/image/fetch/$s_!9sWP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31de7dcf-a21f-4ae1-bfa9-3988557636b9_466x346.png)

In the beginning, Dremel operated on a few hundred shared-nothing servers. Each server kept a subset of the data on local disks. This led to several disadvantages:

* Data must be shifted when the cluster’s membership changes (e.g., add a node, remove a node,…).
* Storage and computing can not scale independently.

They gradually shifted to a shared-disk architecture, which leverages the Google File System (GFS), and later migrated to [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system), the successor to the GFS. You can think of it as S3 or GCS object storage. This shift allowed Google to scale the computing and storage layer independently. However, it came with a price: performance degradation due to interacting with the storage layer via the network. They put a lot of effort into improving the query latency.

Later, they also faced challenges with data shuffling because of the coupling architecture of compute nodes and the intermediate shuffle.

> *In the first phase of MapReduce, each worker applies the* `map` *function to the data assigned and writes the output to temporary storage (worker’s local RAM or hard disk). Then, in the reduce phase, each worker pulls data with the key it’s responsible for (shuffling) and processes the data based on the* `reduce` *logic.*

[![](https://substackcdn.com/image/fetch/$s_!8_cV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc942e383-a1c3-4b0c-a162-5b1f19708dd8_692x466.png)](https://substackcdn.com/image/fetch/$s_!8_cV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc942e383-a1c3-4b0c-a162-5b1f19708dd8_692x466.png)

When dealing with large data, the scaling of “mapper“ and “reducer” is not predictable. The shuffle output depends on the characteristics of the input data. In addition, the compute and the shuffle storage can not be scaled independently.

To deal with this, Google separated the shuffle layer. Instead of colocating shuffle storage with the worker, they stored shuffle data separately in a distributed storage system.

[![](https://substackcdn.com/image/fetch/$s_!FlUy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32315f47-5324-4d3b-a449-7d7a9fbcee2b_710x476.png)](https://substackcdn.com/image/fetch/$s_!FlUy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32315f47-5324-4d3b-a449-7d7a9fbcee2b_710x476.png)

Because of storage and compute separation, Dremel often needs to process unseen data. It encounters challenges in the planning phase since it is hard to produce an optimal execution plan when the nature of the data is unknown. Google overcame this by allowing Dremel to dynamically change the query execution plan at runtime based on the statistics collected during query execution.

### Storage

As mentioned, Google stored BigQuery’s data separately in [Colossus](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system).

They developed an internal data format called [Capacitor](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format). From a high level, it organizes data in a hybrid format, like Parquet. In fact, the Capacitor format inspired the design of Parquet in the first place, especially with the way [it handles nested and repeated fields.](https://vutr.substack.com/p/lesson-learned-after-reading-bigquery?r=2rj6sg&utm_campaign=post&utm_medium=web&triedRedirect=true)

Capacitor has metadata to help query engines prune unnecessary data (e.g., min-max values of a column) and applies techniques like Run Length Encoding (RLE) or Dictionary encoding to optimize storage space.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=161157477)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Databricks

The Apache Spark team founded Databricks in 2013. The company aims to simplify the process of building and deploying Spark applications for organizations. In 2019, Databricks introduced Delta Lake, a table format that provides the warehouse capability to the data lakes.

In 2021, they [released a paper](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) introducing the new data management paradigm, the Lakehouse. This paradigm combines the best of both worlds: the warehouse's robust management features with the lake's theoretically unlimited scalability.

[![](https://substackcdn.com/image/fetch/$s_!TE5l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cde78b1-7916-463b-9bb8-dcb5ada16e76_790x502.png)](https://substackcdn.com/image/fetch/$s_!TE5l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cde78b1-7916-463b-9bb8-dcb5ada16e76_790x502.png)

They have been offering the managed Lakehouse solution, which uses Delta Lake for the storage layer and Spark for the query engine.

### Compute

Databricks must ensure high performance to compete with other solutions in the market, such as Snowflake or BigQuery.

At that time, all the above solutions primarily positioned themselves as cloud data warehouse solutions—the lakehouse paradigm caused Databricks some problems because Spark was initially not developed to be a native query engine:

* The Lakehouse query engines deal with a greater variety of data than traditional warehouses. From organized datasets to raw data with messy layouts, many small files, many columns, and no valuable statistics, the execution engine must be flexible enough to deliver good performance on a wide range of data.
* Databricks initially offered Spark as the query engine. To enhance the query engine, they must ensure that many customers using Spark do not experience disruptions.

They needed a more efficient query engine but couldn’t replace Spark.

So, they enhanced Spark.

Databricks already built the Databricks Runtime (DBR), a [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) of Apache Spark with enhancements for reliability and performance. But they need a little more than that.

[![](https://substackcdn.com/image/fetch/$s_!XmZS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07aa832-0aa2-4bfb-8c16-73d66c501506_936x258.png)](https://substackcdn.com/image/fetch/$s_!XmZS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07aa832-0aa2-4bfb-8c16-73d66c501506_936x258.png)

They built the Photon engine, a library that integrates closely with the DBR. The engine acts as a new set of physical operators inside the DBR. The query plan can use these operators like any other Spark. The customers can continue to run their workloads without any changes and still benefit from Photon. Databricks tests Photon to ensure its semantics are consistent with Spark SQL’s. The system can run the queries partially in Photon; if it needs unsupported operations, they are switched back to SparkSQL.

Databricks built Photon using a [vectorized model](https://www.youtube.com/watch?v=FrspnYbFSxQ) instead of [the code generation](https://www.youtube.com/watch?v=UPQ53hM6AWE) approach that Apache Spark implements. Vectorized execution enabled support runtime adaptivity; Photon discovers, maintains, and leverages micro-batch data characteristics with specialized code paths to adapt to the properties of Lakehouse data.

[![](https://substackcdn.com/image/fetch/$s_!Wpr1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1443b02b-96e4-4fc8-a5dc-f93477f1f4a9_554x338.png)](https://substackcdn.com/image/fetch/$s_!Wpr1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1443b02b-96e4-4fc8-a5dc-f93477f1f4a9_554x338.png)

Another essential design that Databricks made when developing Photon is writing it in [C++](https://vi.wikipedia.org/wiki/C%2B%2B) instead of following the Spark approach, which used the [JVM](https://en.wikipedia.org/wiki/Java_virtual_machine). With C++, Databricks can explicitly control aspects like [memory management](https://isocpp.org/wiki/faq/freestore-mgmt) or [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data).

Traditionally, Spark SQL represents records in memory with a row-oriented format. Since the Lakehouse execution engine mainly deals with columnar files like Parquet, scanning data from disk to memory requires expensive column-to-row pivoting when using the Spark SQL engine.

[![](https://substackcdn.com/image/fetch/$s_!YmyZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d1249bf-0763-4bd7-92f3-f3ded43e0028_1056x548.png)](https://substackcdn.com/image/fetch/$s_!YmyZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d1249bf-0763-4bd7-92f3-f3ded43e0028_1056x548.png)

Photon adopts columnar in-memory data representation; the system stores values of a particular column contiguously in memory. This layout allows for the efficient working of columnar data on disks. It eliminates the column-to-row pivoting process and makes writing data to disks with the columnar engine easier.

In short, you can think that when you’re running a query on Databricks, you’re submitting a Spark application to a Spark cluster with the benefit of Databricks Run Time and the Photon acceleration engine.

### Storage

Databricks suggests users store data in Delta Lake, an ACID table storage layer on cloud object storage. Databricks served it to the customers in 2017 and open-sourced it in 2019. The core idea of Delta Lake is simple: keeping information about which objects belong to a table in an ACID manner, using a write-ahead log in the cloud object store.

[![](https://substackcdn.com/image/fetch/$s_!ztP2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79972a7c-71cb-4dd3-b13a-9132dfb3a50c_590x350.png)](https://substackcdn.com/image/fetch/$s_!ztP2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79972a7c-71cb-4dd3-b13a-9132dfb3a50c_590x350.png)

A Delta Lake table is the cloud object storage directory or file system that consists of the table’s data objects and a log of transaction operations. The data in a table is stored in Apache Parquet objects, which can be organized into directories using [Hive’s partition](https://delta.io/blog/pros-cons-hive-style-partionining/) convention. The Parquet format is widely adopted in many processing engines, thus simplifying the connector development process for Databricks.

[![](https://substackcdn.com/image/fetch/$s_!QTQK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8298d2b6-3afc-45e1-8a10-e0c3956db8f2_626x394.png)](https://substackcdn.com/image/fetch/$s_!QTQK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8298d2b6-3afc-45e1-8a10-e0c3956db8f2_626x394.png)

Delta Lake identifies which object belongs to which table’s version using the transaction log. Every data file in the delta table must be referenced from the transaction log. It is unreadable if a file can’t be referenced from a log.

You can learn the Delta Lake format in more detail here:

---

## Snowflake

Snowflake was founded in July 2012 by [Benoit Dageville](https://www.linkedin.com/in/benoit-dageville-3011845/) and [Thierry Cruanes](https://www.linkedin.com/in/thierry-cruanes-3927363/), two ex-Oracle engineers, and Vectorwise co-founder [Marcin Zukowski](https://www.linkedin.com/in/marcinzukowski/).

[![](https://substackcdn.com/image/fetch/$s_!H8hC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04f606f5-688e-4b82-9b66-5c742cd9a169_518x512.png)](https://substackcdn.com/image/fetch/$s_!H8hC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04f606f5-688e-4b82-9b66-5c742cd9a169_518x512.png)

Traditional data warehouses (DWHs) operated on static local clusters, where data volume and structure were predictable. However, the big data era introduced enormous, unstructured data flows from diverse sources. Those DWHs struggled to keep pace, leading to the birth of big data platforms like Spark and Hadoop. However, they required significant engineering effort to implement. Snowflake's creators saw the need for a solution that:

* Replaced traditional data warehouses.
* Leveraged the scalability of cloud platforms.

They built a new OLAP database in C++. Like BigQuery, their solution separates computing and storage. Compute power comes from Snowflake’s proprietary shared-nothing engine, which uses cloud virtual machines. For storage, Snowflake relies on services like Amazon S3 or Google Cloud Storage. Snowflake uses local disk for data caching to enhance query performance by reducing API calls to object storage.

Unlike Photon from Databricks or Dremel from Google, Snowflake avoids shuffle-based execution. Instead, workers can exchange data directly with one another.

### Compute

[![](https://substackcdn.com/image/fetch/$s_!MhX8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52d5d906-f90e-44bd-8148-0ae938176fb9_596x588.png)](https://substackcdn.com/image/fetch/$s_!MhX8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52d5d906-f90e-44bd-8148-0ae938176fb9_596x588.png)

Snowflake hides users from complex worker configurations. They offer Virtual Warehouses in abstract “T-shirt sizes,” ranging from X-Small to XX-Large, simplifying service management and pricing on cloud platforms.

[![](https://substackcdn.com/image/fetch/$s_!MhX8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52d5d906-f90e-44bd-8148-0ae938176fb9_596x588.png)](https://substackcdn.com/image/fetch/$s_!MhX8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52d5d906-f90e-44bd-8148-0ae938176fb9_596x588.png)

Nodes in a VW are essentially virtual machines. Since data is stored in S3, VWs are stateless, allowing them to scale up or down on demand without affecting the data. Each query runs on exactly one VW, and nodes are not shared across VWs, ensuring performance isolation. When a new query arrives, each worker node in a VW spawns a new worker process, which lives only for the duration of its associated query.

[![](https://substackcdn.com/image/fetch/$s_!hMjB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181375eb-1c26-41b7-ae9b-7059be0f6bf0_554x284.png)](https://substackcdn.com/image/fetch/$s_!hMjB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181375eb-1c26-41b7-ae9b-7059be0f6bf0_554x284.png)

Snowflake employs vectorized execution, processing data in batches of thousands of rows in column format. Unlike systems such as MapReduce, Snowflake's vectorized approach avoids materializing intermediate results. Instead, data is processed pipelined, handling a batch of rows at a time. This method, pioneered by [VectorWise (MonetDB/X100)](https://www.cidrdb.org/cidr2005/papers/P19.pdf), significantly reduces I/O and boosts cache efficiency.

[![](https://substackcdn.com/image/fetch/$s_!cQEi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d5e7a5e-ed3b-4272-8ff8-acdd1f1f0854_576x316.png)](https://substackcdn.com/image/fetch/$s_!cQEi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d5e7a5e-ed3b-4272-8ff8-acdd1f1f0854_576x316.png)

Each worker node in a VW maintains a local cache of table data on its disk, composed of previously accessed table files (S3 objects). Instead of caching entire files, the cache stores file headers and specific columns, as queries only download the necessary columns. This cache persists for the lifetime of the worker node and is shared among all queries running on that node. The cache operates under a simple least-recently-used (LRU) replacement policy.

Snowflake uses consistent hashing to improve cache hit rates and minimize redundant caching across multiple worker nodes within a VW. This process assigns table files to worker nodes based on file names, ensuring that queries accessing the same data will likely hit the same node.

[![](https://substackcdn.com/image/fetch/$s_!iywi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff71313b2-e3a1-488f-baa2-f619e88e4900_670x380.png)](https://substackcdn.com/image/fetch/$s_!iywi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff71313b2-e3a1-488f-baa2-f619e88e4900_670x380.png)

Snowflake uses file stealing to address performance skew, which occurs when certain worker nodes process data more slowly than others.

[![](https://substackcdn.com/image/fetch/$s_!S9ww!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a1cf078-7d18-4e41-ba0a-03ec2053f0dc_432x404.png)](https://substackcdn.com/image/fetch/$s_!S9ww!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a1cf078-7d18-4e41-ba0a-03ec2053f0dc_432x404.png)

When a worker finishes scanning its assigned files, it can request additional files from other worker nodes. If a peer has many files left, it will transfer ownership of one file to the requesting node, which downloads the file directly from S3. This approach ensures that file stealing doesn't burden slower nodes and keeps the system running efficiently.

### Storage

When it came to storage, the team behind Snowflake had to choose between using object storage like S3 or building their solution on HDFS (or similar systems). After some experiments, they concluded that S3 excelled in availability and durability despite its unpredictable performance; they opted for object storage and focused on improving the performance of local caching in the Virtual Warehouse and optimizing it with their proprietary storage format.

Snowflake partitions table data into large, immutable files, similar to blocks or pages in a traditional database. Column values are grouped and heavily compressed in each file, equivalent to the hybrid file format.

> *It's important to note that when Snowflake was built in 2012, formats like Parquet and ORC, which were introduced in 2013, did not yet exist.*

The file contains a header, which includes metadata such as the offsets for each column. Since S3 supports retrieving specific file ranges, queries only need to download the file headers and the required columns.

Snowflake uses min-max-based pruning, storing the minimum and maximum values for each chunk of data. Based on these values, queries can skip unnecessary chunks. For example, if a query needs data with values between 8 and 15, chunks with a max of 7 or a min of 16 are excluded from scanning.

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

---

## Redshift

Amazon Redshift is a column-oriented massively parallel processing data warehouse designed for the cloud. The system is built on top of technology from [ParAccel](https://en.wikipedia.org/wiki/ParAccel) (later acquired by [Actian](https://en.wikipedia.org/wiki/Actian)). It is based on an older version of [PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL) [8.0.2](https://en.wikipedia.org/wiki/PostgreSQL#Release_history), and Redshift has made changes to that version. An initial [preview beta](https://en.wikipedia.org/wiki/Software_release_life_cycle#Stages_of_development) was released in November 2012, and a full release was made available on February 15, 2013.

Redshift is a special case because it was initially designed with a share-nothing architecture. Later, they introduced Redshift Managed Storage (RMS), which leverages Amazon S3 behind the scenes. Thanks to data being offloaded from the compute node, RMS allows customers to scale computing and storage independently. RMS is only available **in the RA3 cluster and serverless Redshift service**.

This section will focus only on Redshift with RMS offering.

### Compute

A Redshift cluster consists of multiple compute instances that handle query execution. Each cluster has a single coordinator node (a.k.a. leader) and multiple worker nodes. Data is offloaded to RMS, making the compute node stateless.

In the OLAP world, there are two main ways to enhance query performance: [Vectorization](https://www.youtube.com/watch?v=yU1S8gwjGEw&list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&index=7) and [Code Specialization](https://www.youtube.com/watch?v=UPQ53hM6AWE&t=687s).

> ***Note**: These approaches are not mutually exclusive.*

The main idea of Vectorization is that instead of processing one record, the engine will process a batch (vector) of values. BigQuery, Snowflake, and Databricks’s Photon do this.

> ***Note**: It has nothing to do with the vector database here.*

For the latter approach, the engine generates the code for each query to reduce the CPU instructions. In a system that doesn’t apply code specialization, each operator has to go through a condition block (switch) to check for the data type and then choose the appropriate function for the input data type. The code generation approach avoids this because all operators for a specific query are generated during execution.

Redshift has applied the code generation approach. The system generates C++ code specific to the query plan and the executed schema. The generated code is then compiled, and the binary is delivered to the compute nodes for execution.

[![](https://substackcdn.com/image/fetch/$s_!69br!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1585db9-7e94-4d2d-963f-8fae410bca2e_704x346.png)](https://substackcdn.com/image/fetch/$s_!69br!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1585db9-7e94-4d2d-963f-8fae410bca2e_704x346.png)

Redshift will use the compiled optimized objects for the query execution. These objects will be cached in the local cluster cache, so whenever the same or similar queries are executed, the compiled objects are reused. This results in faster runtime because Redshift doesn’t need to re-compile the query. This strategy only boosts the performance of the necessary compiled objects in the local cache; if not, Redshift must generate the code.

[![](https://substackcdn.com/image/fetch/$s_!T3p5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99367ec9-2277-4077-8d4f-b92d2c3f7a46_548x334.png)](https://substackcdn.com/image/fetch/$s_!T3p5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99367ec9-2277-4077-8d4f-b92d2c3f7a46_548x334.png)

[In 2020, Redshift introduced compilation services](https://aws.amazon.com/about-aws/whats-new/2020/06/amazon-redshift-now-delivers-better-cold-query-performance/). The service uses separate resources instead of cluster resources. The compilation service caches the compiled objects in the external cache so that Redshift can serve the cache objects for multiple clusters.

### Storage

As mentioned, data is offloaded to RMS, which is based on Amazon S3. To identify which worker node is in charge of which subset of data in RMS, Redshift partitions the table’s data into multiple buckets distributed to all worker nodes. Redshift can apply the partition scheme based on the data’s characteristics, or the user can explicitly declare the desired partition scheme, such as round-robin or hash.

[![](https://substackcdn.com/image/fetch/$s_!pUBR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c8320b1-f433-4742-a546-cc4b23a075e5_402x528.png)](https://substackcdn.com/image/fetch/$s_!pUBR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c8320b1-f433-4742-a546-cc4b23a075e5_402x528.png)

Like Snowflake, Redshift caches data on worker nodes’ local SSD to improve query performance. The cluster maintains its working data set locally based on the information on the number of accesses of data blocks in each data block. The tiered cache is in charge of keeping track of this information. The cache has two-level:

[![](https://substackcdn.com/image/fetch/$s_!cr7D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2481f31b-588d-4b03-93a2-c633f46c819e_498x398.png)](https://substackcdn.com/image/fetch/$s_!cr7D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2481f31b-588d-4b03-93a2-c633f46c819e_498x398.png)

* **Low level**: This level stores cold data blocks. Every time the query accesses a data block, the system increases the block’s reference count.
* **High level**: the cold blocks become hot (after being accessed multiple times), and the policy promotes data blocks to a high level.

During eviction, the reference count of each block is decremented. When the reference count reaches zero, the block will be moved down to the low level or entirely evicted from the cache.

Regarding storage format, instead of storing data in a hybrid format like the three data warehouses above, Redshift stores data in column format. This allows Redshift to pack data and apply compression to minimize disk I/O during query execution. A row can be stitched together by utilizing the offset of a specific value.

---

## Outro

Thank you for reading this far. It was such a long article.

In the article, we observed that from the 10,000-foot views, these systems are the same. They separate storage and computing. The compute are virtual machines that can leverage [vectorization](https://www.youtube.com/watch?v=yU1S8gwjGEw&list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&index=7) or [code specialization](https://www.youtube.com/watch?v=UPQ53hM6AWE&t=687s) for the query execution. The storage is an object store with a hybrid or column file format. In more detail, vendors have different approaches to optimizing their service:

* BigQuery with worker node and shuffle storage separation.
* Databricks with in-place Spark improvement with Photon library.
* Snowflake with cache and file-stealing mechanism
* Redshift with the compilation service, which caches the compiled queries.

—

Feel free to drop comments if you see anything I need to correct.

Now, it’s time to say goodbye; see you in my following articles.

---

## Reference

*[1] Google, [Dremel: A Decade of Interactive SQL Analysis at Web Scale](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf) (2020)*

*[2] Databricks, [Photon: A Fast Query Engine for Lakehouse Systems](https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf) (2022).*

*[3] Michael Armbrust, Reynold S. Xin, Cheng Lian, Yin Huai, Davies Liu, Joseph K. Bradley, Xiangrui Meng, Tomer Kaftan, Michael J. Franklin, Ali Ghodsi, Matei Zaharia [Spark SQL: Relational Data Processing in Spark](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf) (2015)*

*[4] Liz Elfman, [A brief history of Databricks](https://www.bigeye.com/blog/a-brief-history-of-databricks) (2023)*

*[5] Andy Pavlo, [S2024 #19 - Snowflake Data Warehouse Internals (CMU Advanced Database Systems)](https://www.youtube.com/watch?v=NhWp1bTG0Cw&t=1875s) (2024)*

*[6] Snowflake Computing, [The Snowflake Elastic Data Warehouse](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf) (2016)*

*[7] Snowflake Computing, [Building An Elastic Query Engine on Disaggregated Storage](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf) (2020)*

*[8] Amazon, [Amazon Redshift Re-invented](https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf) (2022)*

*[9] [Amazon Redshift Official Document](https://docs.aws.amazon.com/redshift/)*
