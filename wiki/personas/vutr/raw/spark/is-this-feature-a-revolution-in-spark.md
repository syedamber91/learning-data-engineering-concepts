---
title: "Is this feature a revolution in Spark?"
channel: vutr
author: "Vu Trinh"
published: 2025-09-18
url: https://vutr.substack.com/p/is-this-feature-a-revolution-in-spark
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [spark, https, auto, connect, substackcdn, image]
---

# Is this feature a revolution in Spark?

*Process data in Spark by making an API request instead of submitting an application. Everything you need to know about Spark Connect.*

> Source: [Open post](https://vutr.substack.com/p/is-this-feature-a-revolution-in-spark)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=171801244)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!XoMb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb62fa026-dda6-4b48-9a43-23d05ae95a0b_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!XoMb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb62fa026-dda6-4b48-9a43-23d05ae95a0b_2000x1428.png)

---

## Intro

Apache Spark has introduced a new approach for developing data processing applications, promising reduced operational overhead compared to traditional methods.

It is [Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html).

I heard about this feature a few months ago and spent time examining it more closely when I wrote an article about PySpark. However, I did not fully understand this feature at that time, so I only left some highlights [in that article](https://vutr.substack.com/p/i-spent-6-hours-learning-pyspark?r=2rj6sg).

This time, I’m confident in providing you with more details about this feature after spending a considerable amount of time playing with it and reading the code from the Spark GitHub repo.

In this article, I aim to explain Spark Connect in the most straightforward way possible. I found that resources on the Internet (even the Spark official documentation) cannot provide me with all the answers I want when researching Spark Connect. So, I hope my work here can save others time who are learning about this feature.

First, let’s revisit some Spark fundamentals.

---

## Spark cluster vs Resource cluster

[![](https://substackcdn.com/image/fetch/$s_!NTfY!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc203c558-946c-47e3-8fb9-b65b8eb0be96_1042x524.png)](https://substackcdn.com/image/fetch/$s_!NTfY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc203c558-946c-47e3-8fb9-b65b8eb0be96_1042x524.png)

A Spark application consists of

* **Driver:** This JVM process manages the entire Spark application, from handling the user application, planning the execution, to distributing tasks to the executors.
* **Executors:** These processes execute tasks the driver assigns and report their status and results. Each Spark application has its own set of executors.

I will refer to the Driver-Executors as the Spark cluster. Each Spark cluster is associated with a Spark application.

There is another cluster that is responsible for providing physical resources for the Spark cluster's operation. I will refer to this as the resource cluster. This cluster is a set of physical servers that are managed by the cluster manager. Spark can work with several resource clusters such as YARN, Mesos, or Kubernetes. The driver will communicate with the cluster manager to allocate resources to the executors.

## Cluster Mode vs. Client Mode vs. Local Mode

Spark has different modes of execution, which are distinguished by the location of the driver process.

[![](https://substackcdn.com/image/fetch/$s_!0NjV!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb4c2e2f-2e0f-4f4d-9c9e-b1ba622e1df2_2298x590.png)](https://substackcdn.com/image/fetch/$s_!0NjV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb4c2e2f-2e0f-4f4d-9c9e-b1ba622e1df2_2298x590.png)

* **Cluster Mode:** The driver process is launched on the resource cluster alongside the executor processes in this mode.
* **Client Mode:** The driver remains on the client machine. This setup requires the client machine to maintain the driver process throughout the application’s execution.
* **Local mode**: This mode runs the entire Spark application on a single machine, achieving parallelism through multiple threads. It’s commonly used for learning or testing.

---

## Anatomy

It’s crucial to understand how Spark manages the workload:

[![](https://substackcdn.com/image/fetch/$s_!8oUw!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19dff907-ead2-4468-9a81-b4a3be44a49d_1344x450.png)](https://substackcdn.com/image/fetch/$s_!8oUw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19dff907-ead2-4468-9a81-b4a3be44a49d_1344x450.png)

* A **Spark Application** consists of a driver program and a set of executors on a cluster. As discussed earlier, a Spark application is associated with a Spark cluster.
* **Job**: In Spark, a job represents a series of transformations applied to data and is only triggered by an action such as count(), collect(), or show(). A single Spark application can have more than one Spark job.
* **Stage:** A stage is a job segment executed without data shuffling. Spark splits the job into different stages when a transformation requires shuffling data across partitions.
* **Task:** A task is the smallest unit of execution within Spark. Each stage is divided into multiple tasks, which execute processing in parallel across different data partitions.

> *After revisiting some Spark basics, we will continue with Spark Connect. I will delve into the details of this feature, using the knowledge we’ve discussed to ensure everything connects seamlessly.*

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=171801244)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Spark Connect

### Overview

Traditionally, the Spark driver process must perform a significant amount of work, ranging from running the client application to scheduling the actual data processing. In client mode, users must maintain the full Spark dependencies and ensure they are compatible with those running on the submit destination.

[![](https://substackcdn.com/image/fetch/$s_!KW4i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c01c54c-023d-4573-b3d8-4b79e2149615_1000x564.png)](https://substackcdn.com/image/fetch/$s_!KW4i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c01c54c-023d-4573-b3d8-4b79e2149615_1000x564.png)

Spark Connect offers a decoupled client-server architecture for Spark by separating the driver process from the client and making the client thinner. There will be a dedicated server that hosts a long-running Spark application (Spark cluster) and exposes a gRPC endpoint to accept client requests. The ultimate goal is to make the client far thinner compared to the traditional approach.

### High-level flow

At the high level, here are things that happen with Spark Connect:

[![](https://substackcdn.com/image/fetch/$s_!IWdD!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde1046f8-c9a0-48f0-bbd8-79f57a0dff6d_1110x476.png)](https://substackcdn.com/image/fetch/$s_!IWdD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde1046f8-c9a0-48f0-bbd8-79f57a0dff6d_1110x476.png)

* When the Spark Connect server is started, a Spark cluster is created here. The resource for this Spark cluster can be configured like any other cluster when users run the command to start the Connect Server. The Spark cluster is kept running as long as the server is alive.
* There is a gRPC connection between the client and the Spark Connect Server (the Spark driver). Each client will have its own session when communicating with the server.

  > ***Note**: The session here is not the Spark Session object.*
* For each Spark job (e.g., df.show(), df.collect()…), the client converts its DataFrame query to an unresolved logical plan that describes the intent of the operation. An important note is that the client can’t adjust the CPUs or RAMs for the remote Spark application. They will share the resource with other clients
* This plan is encoded using protocol buffers (so it can be language agnostic) and sent to the server.
* When the server receives the plan, the driver analyzes, optimizes, and converts it to a physical plan, and schedules the execution on the executors.
* The results are sent back to the client as Apache Arrow record batches (also via the gRPC connection)

## Thinner Client

The clients no longer need to maintain the full Spark dependencies, as they don’t need to initiate the driver process. The client library only needs to embed the Spark Connect API, which is built on the DataFrame API and enables communication via gRPC, allowing it to convert user input into an unresolved logical plan and send it to the remote driver for execution.

For example, the [Python Spark Connect client](https://spark.apache.org/docs/latest/api/python/getting_started/install.html#python-spark-connect-client) only requires the Python library and does not rely on any non-Python dependencies, such as jars and JRE for Spark.

[![](https://substackcdn.com/image/fetch/$s_!PG79!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d7f79c5-3f47-4cfe-8999-e14338ffe929_394x306.png)](https://substackcdn.com/image/fetch/$s_!PG79!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d7f79c5-3f47-4cfe-8999-e14338ffe929_394x306.png)

In simple terms, Spark Connect to me is running the Spark application in client mode, except that we don’t need to manage the driver process ourselves; we send the Spark jobs to a shared, remote driver managed by the Connect server.

## How it help

The driver lives separately, so we need to allocate **much fewer resources** for the client, who now only needs to implement the lightweight Spark Connect API.

[![](https://substackcdn.com/image/fetch/$s_!1iYb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05fb7bd1-ab1d-4540-a385-4a7493faed4b_426x322.png)](https://substackcdn.com/image/fetch/$s_!1iYb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05fb7bd1-ab1d-4540-a385-4a7493faed4b_426x322.png)

The thin Spark Connect API also enables developers to accelerate support for Spark applications in other programming languages.

[![](https://substackcdn.com/image/fetch/$s_!dNB9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3b854c-50a1-4d6e-9f75-49cd0b3c7abb_438x356.png)](https://substackcdn.com/image/fetch/$s_!dNB9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3b854c-50a1-4d6e-9f75-49cd0b3c7abb_438x356.png)

It’s also more straightforward for developers to debug the Spark job in their IDE, as the process now resembles calling a backend server.

[![](https://substackcdn.com/image/fetch/$s_!xfGy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faac9715e-fcdb-40a3-b6de-41dea4579404_460x162.png)](https://substackcdn.com/image/fetch/$s_!xfGy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faac9715e-fcdb-40a3-b6de-41dea4579404_460x162.png)

The Spark Connect design is well-suited for use cases that **require a low warm-up time or an interactive experience**. The driver initiation process clearly impacts the warm-up time, and the way to achieve interactiveness is by maintaining the long-running driver process on our laptop. With Spark Connect, the server manages the life cycle of the driver process on our behalf.

[![](https://substackcdn.com/image/fetch/$s_!PxKa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90543f91-6d48-49c5-ae36-e5b6539117da_546x404.png)](https://substackcdn.com/image/fetch/$s_!PxKa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90543f91-6d48-49c5-ae36-e5b6539117da_546x404.png)

The Spark driver can now be **upgraded independently of the client applications**. This means the server can receive performance improvements and security fixes without requiring all applications to be updated simultaneously, as long as the communication protocols remain compatible between the client and the server.

[![](https://substackcdn.com/image/fetch/$s_!-ihM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ac46e05-1847-4b5c-b934-05cafbad4ef5_514x256.png)](https://substackcdn.com/image/fetch/$s_!-ihM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ac46e05-1847-4b5c-b934-05cafbad4ef5_514x256.png)

## Limitation

The first limitation is that Spark Connect supports fewer APIs compared to traditional Spark, as it’s built around the DataFrame API; notable exceptions include the RDD and Spark Context APIs.

The second limitation I observed is that the user can only specify the resource for the remote Spark cluster at the time the Spark Connect server is run. The client communicating with the server via gRPC can’t adjust the CPUs or RAMs according to their needs.

All Spark jobs running on the Spark cluster have to share the resources of the server's Spark cluster. A heavy job will undoubtedly affect other jobs. This could be the problem if you need a higher isolation level or a more customized resource profile for your Spark application.

## Playground

To experiment with the Spark Connect, I prepared a Docker Compose script. You can use it to test yourself with the [Git repo here](https://github.com/vutrinh274/spark_connect).

When you run the Docker Compose file, here are the components that will be created:

[![](https://substackcdn.com/image/fetch/$s_!LgPX!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feccce99f-59c3-4930-a06f-bb1fa3305654_878x428.png)](https://substackcdn.com/image/fetch/$s_!LgPX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feccce99f-59c3-4930-a06f-bb1fa3305654_878x428.png)

* A [standalone Spark resource cluster](https://spark.apache.org/docs/latest/spark-standalone.html#installing-spark-standalone-to-a-cluster) with the master is started with the script `start-master.sh`, and a set of 3 workers is started with the script `start-worker.sh`. Each worker will have the capacity of 2 CPUs and 1 GB RAM.

  [![](https://substackcdn.com/image/fetch/$s_!B7-7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4caddbd8-9640-4f89-9e98-eaabfcd7b314_1208x882.png)](https://substackcdn.com/image/fetch/$s_!B7-7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4caddbd8-9640-4f89-9e98-eaabfcd7b314_1208x882.png)
* A Spark connect server that is started with the script `start-connect-server.sh` with some configurations for the Spark cluster: the resource cluster master (cluster manager), and the desired executor resource. The connect server is exposed to two ports: port 4040 is used for the UI, and port 15002 is used to accept client requests.

After all the services are running, you can visit the `localhost:8080` for the Spark resource master UI and `localhost:4040` for the Spark Connect server UI. You can see that there is a running Spark application in the Spark master UI; this is the one initiated by the Spark Connect server.

[![](https://substackcdn.com/image/fetch/$s_!YWTi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a0dacaf-866d-47c9-8887-7971655a9c73_1808x838.png)](https://substackcdn.com/image/fetch/$s_!YWTi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a0dacaf-866d-47c9-8887-7971655a9c73_1808x838.png)

Now, you can connect to the Connect server (port 15002) via PySpark. This is very similar to when you work with the traditional Spark application, except that you can’t call the `master` method and set the resource configuration (CPUs, RAMs) when constructing the SparkSession object; instead, we must call the `remote` method to set the Spark Connect URI.

[![](https://substackcdn.com/image/fetch/$s_!quqY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1afd3031-9399-4d62-a8ae-abb543bb9e0e_982x586.png)](https://substackcdn.com/image/fetch/$s_!quqY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1afd3031-9399-4d62-a8ae-abb543bb9e0e_982x586.png)

An important note is that although we still use the SparkSession class for the Spark Connect, the return object is not actually the SparkSession object when we run the Spark application. You can still use this object to create the dataframe and display the result, but the underlying processes are pretty different. The SparkSession no longer needs to be initialized. Instead, a session is created for us to work with the Spark Connect server. Each client can have a separate session.

When we run a command like this:

[![](https://substackcdn.com/image/fetch/$s_!eIs2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fed62d9-4269-4a40-8d37-918eb213ee70_1224x228.png)](https://substackcdn.com/image/fetch/$s_!eIs2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fed62d9-4269-4a40-8d37-918eb213ee70_1224x228.png)

The library will transform the logic into an unresolved logical plan, encode it using protobuf, and utilize the session to transfer it to the Connect server. The result is transferred back to the user by using this session as well.

I believe the creators behind the Python Spark Connect client aim to provide a better development experience, as we only need to modify a small amount of code when working with Spark Connect.

## Outro

In this article, we first revisit some Spark fundamentals. Then, we delve into Spark Connect, exploring what it is and how it differs from the traditional Spark application. Next, I list out aspects it could help with and things we need to consider when deciding to adopt this feature. Finally, I'd like to share a small experiment to try with Spark Connect.

For me, Spark Connect won’t replace the way we have developed Spark applications over the last 10 years any time soon; however, it opens the doors to more use cases (such as an IoT device that can send requests to the server). Spark Connect also enables support for additional programming languages more quickly, as developers only need to embed the lightweight Spark Connect API.

Thank you for reading this far. See you next time.

---

## Reference

*[1] [Spark GitHub Repo](https://github.com/apache/spark)*

*[2] Sergey Kotlov, [Adopting Spark Connect](https://towardsdatascience.com/adopting-spark-connect-cdd6de69fa98/), 2024*
