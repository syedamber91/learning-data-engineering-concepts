---
title: "How is Databricks' Spark different from Open-Source Spark?"
channel: vutr
author: "Vu Trinh"
published: 2025-03-06
url: https://vutr.substack.com/p/how-is-databricks-spark-different
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse"]
tags: [https, spark, databricks, auto, engine, image]
---

# How is Databricks' Spark different from Open-Source Spark?

*Why don't they just use the open-sourced Apache Spark?*

> Source: [Open post](https://vutr.substack.com/p/how-is-databricks-spark-different)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=156976428)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!6sgM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F568aa09c-1a49-4d6a-8a84-4d5ef37aaa3b_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!6sgM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F568aa09c-1a49-4d6a-8a84-4d5ef37aaa3b_2000x1429.png)

Image created by the author.

---

## Intro

This week, we will explore the differences between open-source Spark and Databricks Spark, why the creators originally developed Spark, why Spark alone is insufficient for Databricks' Lakehouse solution, and how Databricks makes Spark significantly more efficient.

---

## Apache Spark

### Why it was created

[![](https://substackcdn.com/image/fetch/$s_!t_H3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5fc448d-eb0b-4307-9528-c5f9b82e2858_640x490.png)](https://substackcdn.com/image/fetch/$s_!t_H3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5fc448d-eb0b-4307-9528-c5f9b82e2858_640x490.png)

Image created by the author.

Apache Spark is an open-source distributed computing system designed to quickly process large volumes of data that can hardly accomplished by operating on a single machine. Spark distributes data and computations across multiple machines.

It was first developed at UC Berkeley’s AMPLab in 2009.

At the time, Hadoop MapReduce was the popular choice for processing big datasets across multiple machines. AMPLab collaborated with early MapReduce users to identify its strengths and limitations. They also worked closely with Hadoop users at UC Berkeley, who focused on large-scale machine learning requiring iterative algorithms and multiple data passes.

[![](https://substackcdn.com/image/fetch/$s_!yS5J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb9953d0-e5fd-4c1d-864d-5e12c7d4b582_586x476.png)](https://substackcdn.com/image/fetch/$s_!yS5J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb9953d0-e5fd-4c1d-864d-5e12c7d4b582_586x476.png)

Hadoop was famous back then—Image created by the author.

These discussions highlighted some insights. Cluster computing had significant potential. However, MapReduce made building large applications inefficient, especially for machine learning tasks requiring multiple data passes. For example, the machine learning algorithm might need to make many passes over the data. With MapReduce, each pass must be written as a separate job and launched individually on the cluster.

To address this, the Spark team created a functional programming-based API to simplify multistep applications and developed a new engine for efficient in-memory data sharing across computation steps.

### SparkSQL

Spark was intended to focus more on a general-purpose cluster computing engine than a specified database’s query engine. Realizing the need for relation processing over big datasets, the people behind Apache Spark presented the new model Spark SQL in 2014. This new module lets Spark programmers leverage the benefits of relational processing (e.g., declarative queries and optimized storage). Spark SQL introduces two significant enhancements.

[![](https://substackcdn.com/image/fetch/$s_!zBOo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c9865cb-aa88-466d-a6ef-49075dcaf57a_508x516.png)](https://substackcdn.com/image/fetch/$s_!zBOo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c9865cb-aa88-466d-a6ef-49075dcaf57a_508x516.png)

Image created by the author. [Reference](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf)

* First, it integrates relational and procedural processing through a declarative DataFrame API.
* Second, it incorporates a highly extensible optimizer, Catalyst, which leverages Scala's features to facilitate the addition of composable rules and manage code generation.

The goals of SparkSQL are:

* Support relational processing of Spark’s native RDDs and external data sources using a convenient API.
* Offering high performance using DBMS techniques.
* Efficiently supporting new data sources,
* Enabling extension with advanced analytics algorithms such as graph processing and machine learning.

The people behind Spark aim to make it a viable option as a query engine.

---

## Databricks

The Apache Spark team founded Databricks in 2013. The company aims to simplify the process of building and deploying Spark applications for organizations. In 2019, Databricks introduced Delta Lake, a table format that provides the warehouse capability to the data lakes.

In 2021, they [released a paper](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) introducing the new data management paradigm, the Lakehouse. This paradigm combines the best of both worlds: the warehouse's robust management features with the lake's theoretically unlimited scalability.

[![](https://substackcdn.com/image/fetch/$s_!R3Oj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e7c61f6-1431-4efe-b45e-c563de9612e1_1496x1040.png)](https://substackcdn.com/image/fetch/$s_!R3Oj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e7c61f6-1431-4efe-b45e-c563de9612e1_1496x1040.png)

Lakehouse. Image created by the author.

Databricks aimed to solve some problems with the two-tier data architecture, such as **t**he stale data in the warehouse compared to the lake’s, the difficulty and cost of consolidating the data lake and warehouse, and users being billed twice the storage cost for data duplication in the data lake and warehouse**.**

They have been offering the managed lakehouse solution with Delta Lake for the storage layer and Spark for the query engine.

## The challenges

Databricks does not just want to offer a data management system; it must also ensure high performance to compete with other solutions in the market, such as Snowflake, BigQuery, and Redshift.

At that time, all the above solutions primarily positioned themselves as cloud data warehouse solutions—the lakehouse paradigm caused Databricks some problems because Spark was initially not developed to be a native query engine:

* The Lakehouse query engines deal with a greater variety of data than traditional warehouses. From organized datasets to raw data with messy layouts, many small files, many columns, and no valuable statistics, the execution engine must be flexible enough to deliver good performance on a wide range of data.
* Databricks initially offered Spark as the lakehouse engine. To enhance the query engine, they must ensure that many customers using Spark do not experience disruptions.

They need a more efficient query engine but can’t replace Spark. So, what did they do? Simple—they enhanced Spark in place.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=156976428)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Their effort

An important thing to note is that before this effort to enhance Apache Spark, Databricks already built their own Spark runtime, the Databricks Runtime (DBR), which is a [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) of Apache Spark that provides the same interface but has enhancements for reliability and performance.

[![](https://substackcdn.com/image/fetch/$s_!XmZS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07aa832-0aa2-4bfb-8c16-73d66c501506_936x258.png)](https://substackcdn.com/image/fetch/$s_!XmZS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07aa832-0aa2-4bfb-8c16-73d66c501506_936x258.png)

Image created by the author.

But they need a little more than that.

They built the Photon engine, a library that integrates closely with the DBR. The engine acts as a new set of physical operators inside the DBR. The query plan can use these operators like any other Spark. Databricks’s customers can continue to run their workloads without any changes and still benefit from Photon.

The system can run the queries partially in Photon; if it needs unsupported operations, they are switched back to SparkSQL. Databricks tests Photon to ensure its semantics are consistent with Spark SQL’s

Databricks built Photon using a [vectorized model](https://www.youtube.com/watch?v=FrspnYbFSxQ) instead of [the code generation](https://www.youtube.com/watch?v=UPQ53hM6AWE) approach that Apache Spark implements. Vectorized execution enabled support runtime adaptivity; Photon discovers, maintains, and leverages micro-batch data characteristics with specialized code paths to adapt to the properties of Lakehouse data.

Another essential design that Databricks made when developing Photon is writing it in [C++](https://vi.wikipedia.org/wiki/C%2B%2B) instead of following the Spark approach, which used the [Java Virtual Machine (JVM)](https://en.wikipedia.org/wiki/Java_virtual_machine). Databricks observed that *“the Spark applications were hitting performance ceilings with the existing JVM-based engine.”* Moreover, they found that the performance of native code was more effortless to explain than that of the JVM engine, as they can explicitly control aspects like [memory management](https://isocpp.org/wiki/faq/freestore-mgmt) and [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) in C++.

---

## The Photon Designs

### JVM vs. Native Execution

[![](https://substackcdn.com/image/fetch/$s_!Wpr1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1443b02b-96e4-4fc8-a5dc-f93477f1f4a9_554x338.png)](https://substackcdn.com/image/fetch/$s_!Wpr1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1443b02b-96e4-4fc8-a5dc-f93477f1f4a9_554x338.png)

Image created by the author.

Databricks decided to move away from the JVM and implement a native code execution engine. Integrating the new engine with the existing JVM-based runtime is challenging for Databricks. Here are several reasons that led Databricks to the decision to develop a new native execution engine:

* The Lakehouse paradigm demands processing a wide range of workloads that stresses the JVM engine's in-memory performance.
* Improving the JVM engine performance requires deep knowledge of JVM internals.
* Databricks found they lack control over lower-level optimizations such as custom [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) kernels.
* They also observed that garbage collection performance degraded on heap memory larger than 64GB. Databricks had to manually manage off-heap memory in the JVM-based engine, which made the codebase more complex.

### Interpreted Vectorization vs. Code Generation

Modern OLAP systems build high-performance engines predominantly using two approaches: interpreted vectorized design inspired by the MonetDB/X100 system or code-generated design used in systems like [Spark SQL](https://spark.apache.org/docs/latest/sql-programming-guide.html) or [Apache Impala](https://impala.apache.org/).

Vectorized engines use a dynamic dispatch mechanism like [virtual function calls](https://www.geeksforgeeks.org/virtual-function-cpp/) to choose the code block for the execution; then, the system will process data in batches and enable SIMD to amortize virtual function call overhead. On the other hand, code generation uses a compiler at runtime to generate specific code for each query; this way, the approach doesn’t have to deal with virtual function call overhead. Databricks tries to implement both of the above methods; here are their observations:

* Code generation is more complicated to build and debug because the approach generates executing code at runtime; Databricks engineers need to add extra code manually to find issues. In contrast, the interpreted approach only deals with native C++ code; print debugging was much more manageable. As a result, their engineers only needed a couple of weeks to prototype the vectorized approach, while it took them two months with the code-generated approach.
* Code generation removes interpretation and function call overheads by collapsing and inlining operators into a few functions. Despite the performance boost, this makes observability difficult. Operator collapsing prevents the engineers from observing metrics on how much time is spent in each operator, “given that the operator code may be fused into a row-at-a-time processing loop.” In contrast, the vectorized approach maintains clear boundaries between operators.
* Photon can adapt to data properties by choosing a code path at runtime based on the input’s type. This is critical in the Lakehouse context because constraints and statistics may not be available for all queries.
* Databricks found they can achieve code-generated specialization with vectorized engines by creating [specialized fused operators](https://dl.acm.org/doi/10.14778/3151113.3151114) for the most common cases.

For these reasons, Databricks chose the vectorized approach for the Photon engine.

> *If you want to learn more about vectorization and code generation, here are the two resources you should check out:*

### Row vs. Column-Oriented Execution

Traditionally, Spark SQL represents records in memory with a row-oriented format. Since the Lakehouse execution engine mainly deals with columnar files like Parquet, scanning data from disk to memory requires expensive column-to-row pivoting when using the Spark SQL engine.

[![](https://substackcdn.com/image/fetch/$s_!dgKh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6478278-2536-4ba8-818d-d40f34a2432c_1156x614.png)](https://substackcdn.com/image/fetch/$s_!dgKh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6478278-2536-4ba8-818d-d40f34a2432c_1156x614.png)

Image created by the author.

In contrast, Photon adopts columnar in-memory data representation; the system stores values of a particular column contiguously in memory. This layout is more convenient for SIMD and enables more efficient data [pipelining](https://en.wikipedia.org/wiki/Pipeline_(computing)) and [pre-fetching](https://en.wikipedia.org/wiki/Prefetching). Moreover, it allows for the efficient working of columnar data on disks, eliminating the column-to-row pivoting process and making it easier to write data to disks with the columnar engine.

---

## Outro

Based on my observation, many solutions are out there that try to do the same things as Datbricks has done with Spark: they tried to make Spark more efficient as a query engine by implementing state-of-the-art techniques for OAN LAP systems while keeping it compatible with Spark.

* [Apache DataFusion Comet](https://datafusion.apache.org/comet/) implements Apache Datafusion as a runtime for Spark to achieve improvement in terms of query efficiency and query runtime.
* [Apache Gluten(incubating)](https://gluten.apache.org/) is a middle layer that offloads JVM-based SQL engines’ execution to native engines.

Even with the community versions, contributors actively work to make Spark more efficient as an OLAP query engine. One significant improvement is the introduction of Adaptive Query Execution (AQE), which allows query plans to be adjusted based on runtime statistics collected during execution.

Your turn: What’s your experience with Databricks’ Spark? Do you think the open-source version of Spark will catch up with Databricks’ version at any point in the future?

—

Thank you for reading this far. If you notice any logical gaps, please let me know.

It’s time to say goodbye—see you in my next article! ;)

---

## Reference

*[1] Databricks, [Photon: A Fast Query Engine for Lakehouse Systems](https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf) (2022).*

[2] *Michael Armbrust, Reynold S. Xin, Cheng Lian, Yin Huai, Davies Liu, Joseph K. Bradley, Xiangrui Meng, Tomer Kaftan, Michael J. Franklin, Ali Ghodsi, Matei Zaharia [Spark SQL: Relational Data Processing in Spark](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf) (2015)*

[3] Liz Elfman, [A brief history of Databricks](https://www.bigeye.com/blog/a-brief-history-of-databricks) (2023)
