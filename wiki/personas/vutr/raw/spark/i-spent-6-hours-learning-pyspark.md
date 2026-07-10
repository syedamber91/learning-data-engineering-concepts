---
title: "I spent 6 hours learning PySpark"
channel: vutr
author: "Vu Trinh"
published: 2025-08-26
url: https://vutr.substack.com/p/i-spent-6-hours-learning-pyspark
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Databricks", "Orchestration", "Streaming"]
tags: [spark, https, python, auto, process, pyspark]
---

# I spent 6 hours learning PySpark

*How it works behind the scenes.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-6-hours-learning-pyspark)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[databricks|Databricks]] · [[orchestration|Orchestration]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=171197171)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!HC0n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b1f7096-b1f5-49e0-9c47-62e4189732e7_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!HC0n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b1f7096-b1f5-49e0-9c47-62e4189732e7_2000x1428.png)

---

## Intro

For a long time, Apache Spark has become the leading choice for data processing in the data engineering world. The field we’re seeing would be very different if Spark hadn’t existed; the event when the creators decided to start the Spark project at UC Berkeley AMPLab in 2009 will always be an important milestone for the data analytics and processing field.

I believe there is one more event that has a huge impact on how we process data, which is when Spark officially supported Python in [version 0.7.0](https://spark.apache.org/releases/spark-release-0-7-0.html) in 2013. This enables users to harness the power of Spark with the intuitive syntax of Python.

This week, we delve into PySpark, exploring how it works behind the scenes, its significant impact, and its evolution over time.

## Spark Overview

In 2009, UC Berkeley’s AMPLab developed Apache Spark, a functional programming-based API designed to simplify multistep applications, and created a new engine for efficient in-memory data sharing across computation steps.

Unlike MapReduce, Spark relies heavily on in-memory processing. The creator introduced the Resilient Distributed Dataset (RDD) abstraction to manage Spark’s data in memory. RDD represents an **immutable**, **partitioned collection** of records that can be operated on in parallel. Data inside RDD is stored in memory for as long as possible.

A Spark application consists of:

[![](https://substackcdn.com/image/fetch/$s_!HaHQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd88e701b-0b7f-4cfb-a7f9-ef49fbdba1a6_458x410.png)](https://substackcdn.com/image/fetch/$s_!HaHQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd88e701b-0b7f-4cfb-a7f9-ef49fbdba1a6_458x410.png)

* **Driver:** This JVM process manages the entire Spark application, from handling user input to distributing tasks to the executors.
* **Cluster Manager:** This component manages the cluster of machines running the Spark application. Spark can work with various cluster managers, including YARN, Apache Mesos, or its standalone manager.
* **Executors:** These processes execute tasks the driver assigns and report their status and results. Each Spark application has its own set of executors.

The Spark Driver-Executors cluster differs from the cluster hosting your Spark application. To run a Spark application, there must be a cluster of machines or processes (if you’re running Spark locally) that provides resources to Spark applications. The cluster manager manages this cluster and the machines that can host driver and executor processes, referred to as workers.

To learn Apache Spark, I wrote an article that contains everything you need to know about this processing framework. Check out the article here:

## Why the support for Python is crucial

Besides SQL, Python is the preferred language for working in the field of data analytics. The language’s straightforward syntax makes it easy to learn and use, even for those with a non-technical background; data analysts and scientists, in particular, appreciate this.

Additionally, Python offers a vast collection of libraries for data analytics. Users can use pre-built tools to save time and effort. Some essential libraries include NumPy, Pandas, Matplotlib, and Scikit-learn, among others**.** The language can also be used to cover the whole data engineering pipeline, from orchestration (with Airflow) to building a robust data application for the stakeholders (with Streamlit)

If you build a tool for data engineers, data analysts, or data scientists that requires them to code, it must support Python as a first-class citizen. This is not the case with Apache Spark when it was first released. The framework was built with Scala, so the creators recommend using this functional programming language to work with Spark.

[![](https://substackcdn.com/image/fetch/$s_!LWgC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb8001e-5452-4520-a1cc-80df7c618fb0_540x308.png)](https://substackcdn.com/image/fetch/$s_!LWgC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb8001e-5452-4520-a1cc-80df7c618fb0_540x308.png)

Until 2013, Spark finally supported Python in [version 0.7.0](https://spark.apache.org/releases/spark-release-0-7-0.html) due to the emergence of this programming language in the data analytics field. Of course, the support for Python couldn’t compare to Scala at that time; it took Spark many versions from then to make Python one of the primary interfaces for users to work with Spark. Databricks provided [some numbers](https://youtu.be/-vJLTEOdLvA?t=80) to prove the PySpark position:

[![](https://substackcdn.com/image/fetch/$s_!UhzP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cf9634-37e5-46ec-94e4-5c94d29195d6_860x484.png)](https://substackcdn.com/image/fetch/$s_!UhzP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F97cf9634-37e5-46ec-94e4-5c94d29195d6_860x484.png)

[Source](https://www.youtube.com/watch?t=80&v=-vJLTEOdLvA&feature=youtu.be)

* In 2013, **92% of their users used Scala**, 5% used Python, and 3% used SQL for their Spark workload.
* In 2020, **47% used Python**, 41% used SQL, and 12% used Scala and other

In the next section, we delve into how PySpark works internally and discover how it has improved over time to overtake Scala - Spark’s native language.

## How PySpark works behind the scenes

### Revisiting the Spark application journey

Essentially, a Spark application will be in the same way, regardless of whether the logic is specified in Python or Scala:

[![](https://substackcdn.com/image/fetch/$s_!PLHO!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9a23c75-5ce2-4af8-889d-3dd803876574_1156x696.png)](https://substackcdn.com/image/fetch/$s_!PLHO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9a23c75-5ce2-4af8-889d-3dd803876574_1156x696.png)

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=171197171)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

* The user defines the Spark Application. It must include the definition of the SparkSession object.

> *The SparkContext object is the entry point for Spark core functionality.*
>
> *Before Spark 2.0, you needed separate entry points for different APIs (e.g., `SparkContext` for core functionality, 'SQLContext' for the SQL API, or' StreamingContext' for the streaming API).*
>
> *Since [version 2.0](https://spark.apache.org/releases/spark-release-2-0-0.html), Spark has introduced the SparkSession object, which serves as the modern, unified entry point for all Spark functionality. SparkSession is now the recommended entry point. When it is initiated, it will also automatically create the SparkContext internally.*

* The client submits a Spark application to the cluster manager. At this step, the client also requests the driver resource. The SparkContext will also be initialized in the driver.
* When the cluster manager accepts this submission, it places the driver process in one of the worker nodes.
* The driver asks the cluster manager to launch the executors. The user can define the number of executors and related configurations.
* If things go well, the cluster manager launches the executor processes and sends the information about their locations to the driver process.
* The driver formulates an execution plan to guide the physical execution. This process starts with the logical plan, which outlines the intended transformations.
* It generates the physical plan through several refinement steps, specifying the detailed execution strategy for processing the data.
* The driver starts scheduling tasks on executors, and each executor responds to the driver with the status of those tasks.
* Once the application finishes, the driver exits with either success or failure. The cluster manager then shuts down the application’s executors.
* The client can check the status of the Spark application by asking the cluster manager.

### PySpark Implementation

PySpark is simply a wrapper. When a developer executes a PySpark script, two separate processes are spawned: a Python process and a JVM process. The communication between those processes is handled via the [Py4j library](https://www.py4j.org/), which enables Python programs to access Java objects in a JVM.

Here are the details that happen behind the scenes:

[![](https://substackcdn.com/image/fetch/$s_!WKpH!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff134f938-e9a5-4d1c-aa7a-895ea1b9183c_1122x500.png)](https://substackcdn.com/image/fetch/$s_!WKpH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff134f938-e9a5-4d1c-aa7a-895ea1b9183c_1122x500.png)

* You write your PySpark application and run it. This Python process is the driver process.
* The SparkSession object is initiated in the Python process. The SparkContext (SC) object is also created at this time.
* During the process of creating SC, the JVM process is spawned with the help of Py4j. This JVM process is the actual Spark driver, which facilitates the data processing.
* In this JVM, the associated SparkSession and SparkContext object will be created here with the same config as the ones that live in Python.
* The Python process will communicate with the JVM via the Py4J library:

  + The Python process will listen on port with a default value of 25334
  + The created JVM process will listen on port with a default value of 25333
  + The two processes will communicate using the [Inter-Process Communication (IPC)](https://www.geeksforgeeks.org/operating-systems/ipc-technique-pipes/) mechanism. The data transfer requires serialization from the sender and deserialization from the receiver.
* Thanks to the IPC, the Python process can:

  + Send commands to the JVM
  + View the result from the JVM
* When calling any methods, such as `.read.load("yellow_tripdata_2024-01.parquet"`, the call will be routed to the JVM driver process.
* The rest of the process will look like the “Revisiting the Spark application journey”. Physical data processing still occurs in the Spark JVM executors.

As you can see, the whole data processing process has one more step, which is to initiate the Py4j JVM driver. The overhead is the data serialization/deserialization between the Python and the Py4j JVM. This overhead is not serious, given that the data to be transferred is the file path text; however, a large object, such as a Pandas DataFrame, surely affects performance.

### PySpark with Python UDF

In the above section, we assumed that the logic defined in the PySpark application could be handled entirely inside the JVM. In reality, that’s not always the case.

Spark allows users to define a User-Defined Function (UDF) to add a custom processing function. First, users specify the regular Python function that will operate on a data row. After that, users need to register the function as a UDF by wrapping the function with the [udf() function](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html). From then on, this UDF can be used to process the data.

With the Python UDF, things become a bit different when you run your PySpark application. The physical data execution doesn’t happen exclusively in the Spark JVM executor anymore:

[![](https://substackcdn.com/image/fetch/$s_!TwMi!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2073e37b-19c5-4ecf-8138-91c9a9729fc5_2158x1048.png)](https://substackcdn.com/image/fetch/$s_!TwMi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2073e37b-19c5-4ecf-8138-91c9a9729fc5_2158x1048.png)

* Besides the JVM executor process, there will be additional Python processes to be spawned to handle the Python function.
* When it comes to Python UDF, Spark serializes the data from the JVM and sends it to the Python process via the IPC mechanism.
* The Python process deserializes the data and executes the Python function.

  + Besides the data, the Python process also receives the information about the function from the driver.
* The result from the Python function is serialized again and sent back to the JVM process.

The overhead is now more significant compared to the scenario without the UDF; the performance impact increases based on the size of the data that needs to be exchanged between the JVM and Python processes.

Besides the effect of the serialized/deserialized process, UDF in general is slower compared to native Spark functions because those user-defined functions do not benefit from Spark optimized features such as the [Catalyst](https://vutr.substack.com/i/148600255/spark-sql) (Spark’s optimizer) and project [Tungsten](https://vutr.substack.com/i/165246693/off-heap) (the project to improve memory usage by operating directly against binary data rather than Java objects). Another factor that could impact the performance of the Python UDF is that it operates on a single data row at a time.

## How has PySpark improved over time

There was a time when many Spark gurus recommended using Scala for Spark applications to achieve the most robust performance. However, based on the statistics shown in the section “Why the support for Python is crucial“, PySpark is becoming the dominant programming language to work with Spark.

That requires a lot of effort from the community to make this work. In the following sections, I will walk you through some of the key improvements in PySpark.

## Catching up on supported features

Because Scala is Spark’s native language, it is no surprise that users can use all Spark features with Scala. Python is only supported in version 0.7.0, but it has been constantly adding features to catch up with Scala. Now, some Python-supported features are not available in Scala, such as [user-defined table functions (UDTF)](https://spark.apache.org/docs/latest/api/python/user_guide/udfandudtf.html#Python-UDTFs).

## Project Zen

Project Zen is a community initiative within Apache Spark, focused on making PySpark more Pythonic and user-friendly. These improvements are officially introduced in [Spark 3.0](https://spark.apache.org/releases/spark-release-3-0-0.html).

### PySpark documentation

Before the Zen project, PySpark's official documentation structure had not been updated for five years.

[![](https://substackcdn.com/image/fetch/$s_!MKzn!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfb8d4bd-01fd-4bbf-94bb-c9b2bb374aab_1046x564.png)](https://substackcdn.com/image/fetch/$s_!MKzn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfb8d4bd-01fd-4bbf-94bb-c9b2bb374aab_1046x564.png)

The documentation now includes more examples, a dedicated Getting Started guide, and improved organization, moving away from the previous Javadoc-style documentation that was often difficult to navigate.

### Type Hinting

[![](https://substackcdn.com/image/fetch/$s_!aoxf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F029dd299-accb-40e5-813a-3bb5ed800c44_2052x700.png)](https://substackcdn.com/image/fetch/$s_!aoxf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F029dd299-accb-40e5-813a-3bb5ed800c44_2052x700.png)

[Source](https://youtu.be/-vJLTEOdLvA?t=254)

With the project Zen, Spark has introduced official support for Python **type hints**. It enables IDEs to offer improved autocompletion, static analysis, and type checking, which can detect errors before a program even runs. It makes the code more readable and easier to maintain.

### Better Error Handling

In the past, when running PySpark and the application failed, users would receive a lengthy stack trace. Especially, with the UDF, the trace will be a mix of Python and Scala traces. Project Zen improves this by providing more concise and understandable Python tracebacks, making it easier to debug issues.

## Arrow supported UDF

Recall that when there is a Python UDF in the application, it requires the JVM executor to pass the execution of this UDF in a separate Python process. This process is costly because the data must be serialized and deserialized to be transferred between processes.

[![](https://substackcdn.com/image/fetch/$s_!GGAS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe704adf9-97f8-4eec-84f4-a869ee25c58c_490x374.png)](https://substackcdn.com/image/fetch/$s_!GGAS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe704adf9-97f8-4eec-84f4-a869ee25c58c_490x374.png)

In [Spark 3.5](https://spark.apache.org/releases/spark-release-3-5-0.html), Spark introduced Arrow-optimized Python UDFs. The Arrow optimization is optional; user can choose to use it or not based on their need. Both the JVM and Python processes handle data in the Arrow format, which helps bypass the costly serialized and deserialized process. You can read more [here on how Arrow](https://vutr.substack.com/i/169655500/between-two-processes-on-the-same-machine) facilitates the smooth exchange of data between different processes.

In addition, Arrow organized memory data in columnar fashion, which helps improve data processing time compared to Pickle, which serialized data in row-wise format.

## Pandas UDF

In Spark 2.3, Spark introduced Pandas UDFs (also known as Vectorized UDFs) with the promise of improving the performance of Python UDFs. The feature is supported by Arrow for data exchange and Pandas for data manipulation. Compared to Python UDFs, which operate row by row, Pandas UDFs can be executed in a vectorized manner.

[![](https://substackcdn.com/image/fetch/$s_!nu50!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf33d2e8-3a90-4231-9eeb-a60fba3d8701_530x408.png)](https://substackcdn.com/image/fetch/$s_!nu50!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf33d2e8-3a90-4231-9eeb-a60fba3d8701_530x408.png)

The Pandas UDF still needs to be handled by separate Python processes; Pandas now handles the computation, and the data serialization/deserialization is skipped thanks to Arrow.. The columnar format of Arrow also facilitates the vectorized execution of data.

## Python Native Source API

In version 4.0, Spark introduced the [Python Data Source API](https://spark.apache.org/docs/latest/api/python/tutorial/sql/python_data_source.html), which allows us to use Python to define custom data sources/sinks that Spark does not natively support. Before the PySpark Source API, users had to define custom data sources in **Scala or Java**. This approach was a significant barrier for many users who primarily worked with Python.

## Spark Connect

> ***Note 1:** This feature is not exclusively developed for PySpark; however, it promises to provide a better development experience for users, which could ultimately improve Python for Spark.*

> ***Note 2**: I must confess that I don’t feel strongly about the advantages of Spark Connect here, as there are a few things behind the scenes that I don’t fully understand. I will return with a separate Spark Connect article in the future to provide you with more details. Before that, let's take a high-level view of this feature.*

In version 3.4, Spark introduced the [Spark Connect](https://spark.apache.org/spark-connect/), a protocol that enables client applications to connect with the remote Spark server. This is quite similar to how we can connect to the database via the JDBC driver. The protocol is built on the DataFrame API (for data processing) and Arrow (for data exchange between the client and the server). The driver process is now live in the Spark server.

At the high level, here are things that happen with Spark Connect:

[![](https://substackcdn.com/image/fetch/$s_!vVDY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb41dbea6-e694-4de1-89c7-a403d79f45b5_770x386.png)](https://substackcdn.com/image/fetch/$s_!vVDY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb41dbea6-e694-4de1-89c7-a403d79f45b5_770x386.png)

* There is a gRPC connection between the client and the Spark Connect Server.
* The Client converts a DataFrame query to an unresolved logical plan that describes the intent of the operation.
* This plan is encoded using protocol buffers (so it can be language agnostic) and sent to the server.
* The server analyzes, optimizes, and converts it to a physical plan and then executes it. (The typical Spark process here)
* The results are sent back to the client as Apache Arrow record batches (also via the gRPC connection)

With SparkConnect, we no longer need Py4j to create the JVM driver in PySpark. Based on the official documentation, [here are the benefits of Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html#operational-benefits-of-spark-connect):

* Because each application runs in its own process on the client, an out-of-memory (OOM) error or other client-side issue will only impact that specific application.
* The Spark driver can now be upgraded independently of the client applications. This means the server can receive performance improvements and security fixes without requiring all applications to be updated simultaneously, as long as the communication protocols remain compatible between the client and the server.
* Developers can perform interactive, step-through debugging directly from the IDEs, a workflow that is much more intuitive than traditional methods

> As mentioned, I will be back with a future article to discuss about Spark Connect.

---

## Outro

In this article, we first revisit the Spark fundamentals, then we explore why Python support is crucial for “data developers”. Then we delve into how PySpark works internally, which is very similar to how a Scala Spark application runs, except for one thing: the Python SparkContext must communicate with the JVM SparkContext via Py4j.

If the application has a Python UDF, things will also be different as the JVM executors now need to hand over the execution of the UDF to a separate Python process. We finally discover some significant improvements that’ve made PySpark widely adopted, even more so than Spark’s native language, Scala.

Thank you for reading this far. See you next time.

---

## Reference

*[1] Hyukjin Kwon, Matei Zaharia, [An Update on Project Zen: Improving Apache Spark for Python Users](https://www.databricks.com/blog/2020/09/04/an-update-on-project-zen-improving-apache-spark-for-python-users.html) (2020)*

*[2] Spark Official Documentation, [Unleashing UDFs & UDTFs](https://spark.apache.org/docs/latest/api/python/user_guide/udfandudtf.html)*

*[3] Xinrong Meng, Hyukjin Kwon, Takuya Ueshin, Allan Folting, [Arrow-optimized Python UDFs in Apache Spark™ 3.5](https://www.databricks.com/blog/arrow-optimized-python-udfs-apache-sparktm-35) (2023)*

*[4] Edward S., [How does PySpark work? — step by step (with pictures)](https://medium.com/analytics-vidhya/how-does-pyspark-work-step-by-step-with-pictures-c011402ccd57) (2020)*

*[5] Jay Wei, [How PySpark Works as a Wrapper? Dive Into The Code](https://www.linkedin.com/pulse/how-pyspark-wrapper-works-dive-code-jay-wei-fbsse/) (2023)*

*[6] Databricks, [What's Next for Apache Spark™ Including the Upcoming Release of Apache Spark 4.0](https://www.youtube.com/watch?v=S1B0J-uzSDE&t=612s) (2024)*

*[7] Databricks, [Project Zen: Making Spark Pythonic](https://www.youtube.com/watch?v=-vJLTEOdLvA&t=786s) (2020)*

[8] StackOverflow, answer by Hristo Iliev, [Does PySpark code run in JVM or Python subprocess](https://stackoverflow.com/questions/61816236/does-pyspark-code-run-in-jvm-or-python-subprocess)? (2020)

*[9] [Official Spark Connect Documentation](https://spark.apache.org/spark-connect/)*

*[10] Databricks, [Python with Spark Connect](https://www.youtube.com/watch?v=QGUvjcrqj-U) (2023)*
