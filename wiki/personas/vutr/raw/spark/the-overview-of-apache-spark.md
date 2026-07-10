---
title: "The Overview Of Apache Spark"
channel: vutr
author: "Vu Trinh"
published: 2024-09-07
url: https://vutr.substack.com/p/the-overview-of-apache-spark
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [spark, https, auto, image, application, substackcdn]
---

# The Overview Of Apache Spark

*The infamous data processing engine*

> Source: [Open post](https://vutr.substack.com/p/the-overview-of-apache-spark)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=148486041)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!4KVP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29e82657-edf1-4197-9c15-5845b5b329ec_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!4KVP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29e82657-edf1-4197-9c15-5845b5b329ec_2000x1429.png)

Image created by the author.

---

## Intro

This week, we’ll explore Apache Spark. Given the vast scope of this processing engine, starting with an overview seems like the best approach to streamlining my learning process.

In this article, I’ll provide a high-level introduction to Apache Spark. We’ll begin with some background on Spark and then explore the typical architecture of a Spark application. Following that, we’ll examine its core data abstraction, the RDD, and conclude by walking through the flow of a Spark application.

---

## Background

At its core, Apache Spark is an open-source distributed computing system designed to quickly process large volumes of data that can hardly accomplished by operating on a single machine. Spark distributes data and computations across multiple machines, allowing for parallel processing.

[![](https://substackcdn.com/image/fetch/$s_!bYmO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ee48a30-9f92-41be-a462-b424a2efa248_751x461.png)](https://substackcdn.com/image/fetch/$s_!bYmO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ee48a30-9f92-41be-a462-b424a2efa248_751x461.png)

Image created by the author.

It was first developed at UC Berkeley’s AMPLab in 2009. At that time, Hadoop MapReduce was the leading parallel programming engine for processing massive datasets across multiple machines. AMPLab collaborated with early MapReduce users to identify its strengths and limitations, driving the creation of more versatile computing platforms. They also worked closely with Hadoop users at UC Berkeley, who focused on large-scale machine learning requiring iterative algorithms and multiple data passes.

These discussions highlighted some insights. Cluster computing had significant potential. However, MapReduce made building large applications inefficient, especially for machine learning tasks requiring multiple data passes. For example, the machine learning algorithm might need to make many passes over the data. With MapReduce, each pass must be written as a separate job and launched individually on the cluster.

To address this, the Spark team created a functional programming-based API to simplify multistep applications and developed a new engine for efficient in-memory data sharing across computation steps.

---

## The Spark Application Architecture

A typical Spark application consists of several key components:

[![](https://substackcdn.com/image/fetch/$s_!jht9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd9823a5-00b5-4359-86c6-dcd3c5f3acf2_474x469.png)](https://substackcdn.com/image/fetch/$s_!jht9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd9823a5-00b5-4359-86c6-dcd3c5f3acf2_474x469.png)

Image created by the author.

* **Driver:** This JVM process manages the Spark application, handling user input and distributing work to the executors.
* **Cluster Manager:** This component oversees the cluster of machines running the Spark application. Spark can work with various cluster managers, including YARN, Apache Mesos, or its standalone manager.
* **Executors:** These processes execute tasks the driver assigns and report their status and results. Each Spark application has its own set of executors. A single worker node can host multiple executors.

> ***Note**:* *You might find some confusion here. The cluster manager will have its own “driver” (sometimes called master) and “worker” abstractions. The main difference is that these are tied to physical machines rather than Spark processes.*

[![](https://substackcdn.com/image/fetch/$s_!dMyK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62d362d8-e1b4-4806-a6f8-25b41631d84a_915x850.png)](https://substackcdn.com/image/fetch/$s_!dMyK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62d362d8-e1b4-4806-a6f8-25b41631d84a_915x850.png)

Physical Cluster. Image created by the author.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=148486041)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Job, Stage, and Task

* **Job:** In Spark, a job represents a series of transformations applied to data. It encompasses the entire workflow from start to finish.
* **Stage:** A stage is a job segment executed without data shuffling. Spark splits the job into different stages when a transformation requires shuffling data across partitions.
* **Task:** A task is the smallest unit of execution within Spark. Each stage is divided into multiple tasks, running the same code on a separate data partition executed by individual executors.

In Spark, a job is divided into stages wherever data shuffling is necessary. Each stage is further broken down into tasks and executed parallel across different data partitions. A single Spark application can have more than one Spark job.

---

## Resilient Distributed Dataset (RDD)

RDD is the primary data abstraction. Whether DataFrames or Datasets are used, they are compiled into RDDs behind the scenes. It represents an immutable, partitioned collection of records that can be operated on in parallel. Data inside RDD is stored in memory for as long and as much as possible.

### Properties

Internally, each RDD in Spark has five key properties:

[![](https://substackcdn.com/image/fetch/$s_!KQXz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb213561d-fb8e-4d37-8eaf-7ab0c97499da_673x487.png)](https://substackcdn.com/image/fetch/$s_!KQXz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb213561d-fb8e-4d37-8eaf-7ab0c97499da_673x487.png)

Image created by the author.

* **List of Partitions:** The RDD is divided into partitions, which are the units of parallelism in Spark.
* **Computation Function:** A function determines how to compute the data for each partition.
* **Dependencies:** The RDD keeps track of its dependencies on other RDDs, which describes how it was created.
* **Partitioner (Optional):** For key-value RDDs, a partitioner specifies how the data is partitioned, such as using a hash partitioner.
* **Preferred Locations (Optional):** This property lists the preferred locations for computing each partition, such as the data block locations in the HDFS.

### Lazy Evaluation

When you define the RDD, its inside data is not available or transformed immediately until an action triggers the execution. This approach allows Spark to determine the most efficient way to execute the transformations.

[![](https://substackcdn.com/image/fetch/$s_!J7nv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cbdb0b8-0869-4fcf-b346-9f9db8816656_777x367.png)](https://substackcdn.com/image/fetch/$s_!J7nv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cbdb0b8-0869-4fcf-b346-9f9db8816656_777x367.png)

Image created by the author.

* **Transformations**, such as `map` or `filter`, are operations that define how the data should be transformed, but they don't execute until an action forces the computation. Spark doesn't modify the original RDD when a transformation is applied to an RDD. Instead, it creates a new RDD that represents the result of applying the transformation because RDD is immutable.
* **Actions** are the commands that Spark runs to produce output or store data, thereby driving the actual execution of the transformations.

### Partitions

When an RDD is created, Spark divides the data into multiple chunks, known as partitions. Each partition is a logical data subset and can be processed independently with different executors. This enables Spark to perform operations on large datasets in parallel.

> ***Note**: I’ll explore the Spark partiions in detail in an upcoming article*

### Fault Tolerance

Spark RDDs achieve fault tolerance through ***lineage***. Spark forms the dependency lineage graph by keeping track of each RDD’s dependencies on other RDDs, which is the series of transformations that created it.

Suppose any partition of an RDD is lost due to a node failure or other issues. In that case, Spark can reconstruct the lost data by reapplying the transformations to the original dataset described by the lineage. This approach eliminates the need to replicate data across nodes. Instead, Spark only needs to recompute the lost partitions, making the system efficient and resilient to failures.

### Why RDD immutable

You might wonder why Spark RDDs are immutable. Here’s the gist:

* **Concurrent Processing:** Immutability keeps data consistent across multiple nodes and threads, avoiding complex synchronization and race conditions.
* **Lineage and Fault Tolerance:** Each transformation creates a new RDD, preserving the lineage and allowing Spark to recompute lost data reliably. Mutable RDDs would make this much harder.
* **Functional Programming:** RDDs follow functional programming principles that emphasize immutability, making it easier to handle failures and maintain data integrity.

---

## The journey of the Spark application

Before diving into the flow of a Spark application, it’s essential to understand the different execution modes Spark offers. We have three options:

* **Cluster Mode:** In this mode, the driver process is launched on a worker node within the cluster alongside the executor processes. The cluster manager handles all the processes related to the Spark application.

[![](https://substackcdn.com/image/fetch/$s_!kN3z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03f2ca61-6b9a-4519-8eff-7714961197be_914x853.png)](https://substackcdn.com/image/fetch/$s_!kN3z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03f2ca61-6b9a-4519-8eff-7714961197be_914x853.png)

Image created by the author.

* **Client Mode:** The driver remains on the client machine that submitted the application. This setup requires the client machine to maintain the driver process throughout the application’s execution.

[![](https://substackcdn.com/image/fetch/$s_!4SW9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a680eaf-1c3a-4b48-b8e8-2890f416601b_902x827.png)](https://substackcdn.com/image/fetch/$s_!4SW9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a680eaf-1c3a-4b48-b8e8-2890f416601b_902x827.png)

Image created by the author.

* **Local mode**: This mode runs the entire Spark application on a single machine, achieving parallelism through multiple threads. It’s commonly used for learning Spark or testing applications in a simpler, local environment.

Now, we will learn the Spark application flow with the cluster mode. Suppose the application leverages DataFrame API to process data. Here are the steps from the beginning to the end:

[![](https://substackcdn.com/image/fetch/$s_!sFWK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544b8586-2280-4db8-a51b-de0a4bc94b86_1141x815.png)](https://substackcdn.com/image/fetch/$s_!sFWK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F544b8586-2280-4db8-a51b-de0a4bc94b86_1141x815.png)

Image created by the author.

* First, the user defines the Spark Application using their chosen programming language. Every application must include the SparkSession object. This object is the entry point to programming with Apache Spark, which serves as the central gateway for interacting with all of Spark's functionalities.
* Then, the client submits a Spark application, which is a pre-compiled JAR, to the cluster manager. At this step, the client also requests for the driver resource.
* When the cluster manager accepts this submission, it places the driver process in one of the worker nodes.
* Next, the SparkSession from the application code asks the cluster manager to launch the executors. The user can define the number of executors and related configurations.
* If things go well, the cluster manager launches the executor processes and sends the relevant information about their locations to the driver process.
* Before execution begins, it formulates an execution plan to guide the physical execution. This process starts with the **logical plan**, which outlines the intended transformations. It generates the physical plan through several refinement steps, specifying the detailed execution strategy for processing the data.

  > ***Note**: I’ll explore the Spark planning process in detail in an upcoming article.*
* The driver starts scheduling tasks on executors, and each executor responds to the driver with the status of those tasks.
* After a Spark Application is completed, the driver exits with either success or failure. The cluster manager then shuts down the executors for this application.
* Then, the client can check the status of the Spark application by asking the cluster manager.

---

## Outro

Thank you for reading this far!

In this article, we've covered the basics of Apache Spark. I'm excited to dive deeper into this processing engine and will share more insights in future articles.

Stay tuned, and I look forward to seeing you in the next post!

---

## Reference

*[1] Bill Chambers, Matei Zaharia, [Spark: The Definitive Guide: Big Data Processing Made Simple](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/) (2018)*

*[2] Jacek Laskowski, [The Internals of Spark Core](https://books.japila.pl/apache-spark-internals/)*

*[3] Spark By Example, [Spark Internal Execution plan](https://sparkbyexamples.com/spark/spark-execution-plan/)*

*[4] luminousmen, [Why Apache Spark RDD is immutable?](https://luminousmen.com/post/why-apache-spark-rdd-is-immutable) (2024)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/the-overview-of-apache-spark/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
