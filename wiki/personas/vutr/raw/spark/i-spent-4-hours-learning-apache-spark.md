---
title: "I spent 4 hours learning Apache Spark Resource Allocation"
channel: vutr
author: "Vu Trinh"
published: 2024-10-19
url: https://vutr.substack.com/p/i-spent-4-hours-learning-apache-spark
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [https, auto, image, spark, fetch, substackcdn]
---

# I spent 4 hours learning Apache Spark Resource Allocation

*Spark's resource allocation mechanism and the two scheduling modes.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-4-hours-learning-apache-spark)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=150143866)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!_h4y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9eccf68-5ed7-43a3-a43a-0138f36f6b18_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!_h4y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9eccf68-5ed7-43a3-a43a-0138f36f6b18_2000x1429.png)

Image created by the author.

---

## Intro

This week, we will explore Spark's resource allocation mechanism and the two scheduling modes: FIFO and scheduling.

---

## Resource Allocation

As you might know, when running on a physical cluster, a Spark application gets an isolated set of executors (JVM processes) that are only responsible for processing and storing data for that application.

Spark provides two ways of allocating resources for Spark applications: static allocation and dynamic allocation.

* **Static allocation**: Each application is allocated a finite maximum amount of resources on the cluster, which are reserved for the duration of the application as long as the SparkContext is running. Users can define the resource configuration.

[![](https://substackcdn.com/image/fetch/$s_!xI8N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe28ed957-59d5-402c-9640-0780e96d511f_1534x1028.png)](https://substackcdn.com/image/fetch/$s_!xI8N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe28ed957-59d5-402c-9640-0780e96d511f_1534x1028.png)

Static allocation. Image created by the author.

* **Dynamic allocation** (enabled by setting `spark.dynamicAllocation.enabled` to `True`): Since version 1.2, Spark offers dynamic resource allocation. The application may return resources to the cluster if they are no longer used and can request them later when there is demand. Let’s dive into this approach in more detail.

[![](https://substackcdn.com/image/fetch/$s_!74Sl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f4d63da-f05d-4730-b653-6d52706cc6c3_1482x1020.png)](https://substackcdn.com/image/fetch/$s_!74Sl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f4d63da-f05d-4730-b653-6d52706cc6c3_1482x1020.png)

Dynamic allocation. Image created by the author.

---

## **Dynamic allocation**

Spark should generally release executors when no longer needed and acquire new executors when necessary. Because it's impossible to predict whether an executor about to be removed will soon run a task or whether a newly added executor will remain idle, Spark uses a set of heuristics to decide when to remove and request executors.

### **Request Policy**

An application with dynamic allocation enabled requests more executors when pending tasks are waiting to be scheduled. It only requests when the tasks have been pending for a defined interval.

> *The request is triggered when there have been pending tasks for **spark.dynamicAllocation.schedulerBacklogTimeout** seconds, and then triggered again every **spark.dynamicAllocation.sustainedSchedulerBacklogTimeout** seconds thereafter if the queue of pending tasks persists. [—Source—](https://spark.apache.org/docs/latest/job-scheduling.html#request-policy)*

The requests are made in rounds, and the number of executors in each round increases exponentially from the previous round. For example, an application will request 1 executor in the first round and then 2, 4, 8, etc.

[![](https://substackcdn.com/image/fetch/$s_!OfNy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19f990e1-6bb6-447a-b2ca-b5b2638df654_2348x882.png)](https://substackcdn.com/image/fetch/$s_!OfNy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19f990e1-6bb6-447a-b2ca-b5b2638df654_2348x882.png)

Image created by the author

There are two reasons behind this approach:

* First, an application should request a small number of executors at first to ensure that only a few additional executors are used if they are sufficient.
* Second, the application should be able to accelerate its resource usage if many executors are actually needed.

### **Remove Policy**

The policy for removing executors is straightforward. A Spark application removes an executor when idle for a predefined interval (***spark.dynamicAllocation.executorIdleTime***).

[![](https://substackcdn.com/image/fetch/$s_!fBwY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe15669b-8ce6-45c5-87ac-37ab831174a1_1520x1312.png)](https://substackcdn.com/image/fetch/$s_!fBwY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe15669b-8ce6-45c5-87ac-37ab831174a1_1520x1312.png)

Image created by the author.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=150143866)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

### **Graceful Decommission of Executors**

In static resource allocation, an executor only exits when its associated application has also been completed; this implies that the executor can be safely discarded.

However, when an executor is removed, the application still runs with dynamic allocation. If the application attempts to access data stored in or written by the executor, it must perform data recomputing.

Thus, a mechanism exists to gracefully remove an executor by preserving its data before removing it. In other words, we will try to make the executor stateless a bit.

During a shuffle, the executor writes its map outputs locally to disk and then serves as the entry point for other executors to fetch those files.

The solution is to use an external shuffle service. This service runs as a long-running process on each cluster node, independently of Spark applications and their executors.

[![](https://substackcdn.com/image/fetch/$s_!Fhy6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e6e0280-2d82-43f8-ac52-42039ad54f07_2022x1300.png)](https://substackcdn.com/image/fetch/$s_!Fhy6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e6e0280-2d82-43f8-ac52-42039ad54f07_2022x1300.png)

Image created by the author.

Spark executors fetch shuffle files from the service rather than from each other. This means that shuffle data produced by an executor can continue to be served even after the executor has been terminated.

Besides outputting shuffle data, executors also cache data on disk or in memory. However, when an executor is removed, all cached data is gone. Users can configure executors containing cached data that are never removed by default.

In the future, cached data may be stored off-heap and managed independently from the executor's lifetime. This is similar to how Spark handles shuffle data with the external service.

---

## Schedule Mode

### First In First Out (FIFO)

[![](https://substackcdn.com/image/fetch/$s_!oX7-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc82bee7a-b0ee-4996-8b51-2ce3c9a07d89_990x1182.png)](https://substackcdn.com/image/fetch/$s_!oX7-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc82bee7a-b0ee-4996-8b51-2ce3c9a07d89_990x1182.png)

Image created by the author.

> ***Note**: The above image is just meant to convey the general idea. It may not reflect the exact implementation.*

By default, jobs are run in FIFO order. The first job gets priority on all available resources, followed by the next jobs. If the first job doesn’t consume all of the cluster’s resources, later jobs can start running immediately. However, if some of the first jobs use up all the resources, later jobs may remain pending for a while.

### Fair

Since Spark 0.8, the user can configure fair scheduling between jobs. With this mode, Spark assigns tasks between jobs in a round-robin fashion to ensure equal resource sharing between jobs. This implies that short jobs submitted while a long job is running can start receiving resources immediately without waiting for the long job to finish.

[![](https://substackcdn.com/image/fetch/$s_!saL5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4585789c-dae7-4953-89ed-434aeb3b2b98_1062x1278.png)](https://substackcdn.com/image/fetch/$s_!saL5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4585789c-dae7-4953-89ed-434aeb3b2b98_1062x1278.png)

Image created by the author.

> ***Note**: The above image is just meant to convey the general idea. It may not reflect the exact implementation.*

The approach is modeled after the [Hadoop Fair Scheduler](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html). The fair scheduler supports grouping jobs into *pools* and setting various scheduling options for each pool, such as the weight.

[![](https://substackcdn.com/image/fetch/$s_!rw1e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1f6d6c1-63c7-4744-9ca8-9b315855239a_1246x1066.png)](https://substackcdn.com/image/fetch/$s_!rw1e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1f6d6c1-63c7-4744-9ca8-9b315855239a_1246x1066.png)

Image created by the author.

This can help isolate workload so critical jobs can be executed on a more resource pool. (User can configure which jobs can be run on which pools.)

Here are some pool properties that user can configure:

* **Scheduling Mode (default is FIFO)**: This option controls the scheduling behavior in a specific pool. This can be FIFO or FAIR.

[![](https://substackcdn.com/image/fetch/$s_!lYx1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02e6cfd9-11fc-4279-9f06-d24e893a52f4_1364x992.png)](https://substackcdn.com/image/fetch/$s_!lYx1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02e6cfd9-11fc-4279-9f06-d24e893a52f4_1364x992.png)

Image created by the author.

* **Weight (default is 1):** This controls the pool’s cluster share relative to other pools. By default, all pools have a weight of 1, which means they will have the same amount of resources. However, if a pool has a weight of 2, it will have double the resources of other pools.

[![](https://substackcdn.com/image/fetch/$s_!3GVd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2bce96f-77eb-4f57-b4eb-51a5268f6285_1852x1114.png)](https://substackcdn.com/image/fetch/$s_!3GVd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2bce96f-77eb-4f57-b4eb-51a5268f6285_1852x1114.png)

Image created by the author.

* **minShare (default is 0)**: Each pool can be given a minimum share (e.g., minimum number of CPU cores). The scheduler always tries to meet all active pools’ minimum shares before redistributing extra resources according to the weights.

[![](https://substackcdn.com/image/fetch/$s_!mOuZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7180306-c4e8-4526-b91f-15c178d8ab6a_1178x1186.png)](https://substackcdn.com/image/fetch/$s_!mOuZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7180306-c4e8-4526-b91f-15c178d8ab6a_1178x1186.png)

Image created by the author.

---

## Outro

Thank you for reading this far.

In this article, we explored Spark's resource allocation behavior and its scheduling modes, including FIFO and Fair scheduling.

Now it’s time to say goodbye. See you in my next blog!

---

## Reference

*[1] [Apache Spark Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html)*

*[2] Holden Karau, Rachel Warren, [High Performance Spark: Best Practices for Scaling and Optimizing Apache Spark](https://www.amazon.com/High-Performance-Spark-Practices-Optimizing/dp/1491943203) (2017)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-4-hours-learning-apache-spark/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
