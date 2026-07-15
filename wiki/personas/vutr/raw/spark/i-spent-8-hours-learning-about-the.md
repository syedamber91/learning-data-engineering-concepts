---
title: "I spent 8 hours learning about the Spark Out-Of-Memory (OOM) errors"
channel: vutr
author: "Vu Trinh"
published: 2026-06-09
url: https://vutr.substack.com/p/i-spent-8-hours-learning-about-the
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [https, auto, spark, substackcdn, image, fetch]
---

# I spent 8 hours learning about the Spark Out-Of-Memory (OOM) errors

*What actually causes them and how to fix them*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-about-the)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=200072168)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!UJkL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17c640c4-a87c-4c77-9c0e-964b2918dc10_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!UJkL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17c640c4-a87c-4c77-9c0e-964b2918dc10_2000x1429.png)

---

# Intro

If you’ve ever run Spark in production, you might encounter the OOM error once.

You might simply increase the executor memory, and the problem will be fixed. However, naively allocating more resources to your Spark job won’t be sustainable in the long term.

Instead, understanding the nature of the OOM is the better approach.

In this article, I deliver my understanding of the OOM errors so you can operate Spark more robustly in production.

> ***Note 1**: This article assumes you have a basic understanding of Spark. I highly recommend you [read this article](https://vutr.substack.com/p/the-fastest-way-to-learn-spark-is?utm_source=publication-search) for that purpose.*
>
> ***Note 2**: This article only discusses **OOM on Spark executors.***

---

# How Spark works?

> In brief

If you want to run Spark, you must have a cluster of machines that provide the resources for the Spark cluster.

[![](https://substackcdn.com/image/fetch/$s_!t1Fv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F294bf882-ac59-4dba-b4b9-445d988be2a1_1612x846.png)](https://substackcdn.com/image/fetch/$s_!t1Fv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F294bf882-ac59-4dba-b4b9-445d988be2a1_1612x846.png)

A Spark cluster is a set of JVM processes, including a Driver and Executors. Those processes run on the cluster of machines (with communication with the Cluster Manager).

[![](https://substackcdn.com/image/fetch/$s_!4mrr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa76d9018-c55b-487c-832f-2526669cf89e_1824x952.png)](https://substackcdn.com/image/fetch/$s_!4mrr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa76d9018-c55b-487c-832f-2526669cf89e_1824x952.png)

Every Spark cluster is associated with a Spark application.

Below the application is the Spark job. A job represents a series of transformations applied to data: the entire workflow from start to finish. The series of transformations (e.g, filter, map…) can be triggered only by an action (e.g., show, count,…). We can say that a job is associated with an action. An application can have multiple jobs.

[![](https://substackcdn.com/image/fetch/$s_!D37O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4b9de28-cc3e-4de4-8001-0422ad99c09a_1364x710.png)](https://substackcdn.com/image/fetch/$s_!D37O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4b9de28-cc3e-4de4-8001-0422ad99c09a_1364x710.png)

A job is split into different stages when a transformation requires shuffling data across partitions. (e.g., groupBy, join). A stage is a job segment executed without data shuffling.

A stage has a set of tasks. A task is the smallest unit of execution within Spark. Each stage is divided into multiple tasks, each handling a partition, a portion of data from an external source or from the upstream stage.

[![](https://substackcdn.com/image/fetch/$s_!B0KW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638b2e1a-21a5-4082-a4a8-c287e1b97c02_852x786.png)](https://substackcdn.com/image/fetch/$s_!B0KW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638b2e1a-21a5-4082-a4a8-c287e1b97c02_852x786.png)

At a given stage, tasks can run in parallel; the parallelism depends on the executor's CPUs. You can understand that tasks are handled in parallel in an executor using the multithreading paradigm. By default, a task is handled by an executor core (controlled by the “spark.task.cpus” setting); if the executor has 4 cores, 4 tasks can run in parallel within the executor.

---

# Why do OOM errors happen?

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=200072168)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

However, the executor memory cannot be clearly separated like the cores; you might be aware of this: in multi-thread processing, all threads share the memory. With task-processing in an executor, all the tasks share the executor’s memory used for processing.

[![](https://substackcdn.com/image/fetch/$s_!M5q0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba3810c-e852-4560-abdc-844063215625_860x768.png)](https://substackcdn.com/image/fetch/$s_!M5q0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba3810c-e852-4560-abdc-844063215625_860x768.png)

Assuming an executor with 4 cores and 8 GB of RAM available for processing and storing data, the executor can handle 4 tasks in parallel, and the executor expects each task to use as much as 2 GB of RAM.

[![](https://substackcdn.com/image/fetch/$s_!sISY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F274a59b4-e8ce-4133-b4b1-311e25c48f2c_914x584.png)](https://substackcdn.com/image/fetch/$s_!sISY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F274a59b4-e8ce-4133-b4b1-311e25c48f2c_914x584.png)

If a task needs 5GB of RAM to handle, it causes OOM.

Thus, there are two main reasons why OOM errors happen:

* A task requires more memory to handle a partition.
* The memory portion of a single task shrinks.

For the first one, many factors could cause this: a task is assigned a skewed partition, the input data volume increases, an operation, such as aggregation, requires memory to hold aggregated values, and it is somehow exploited.

For the latter, the most common root cause is increasing the parallelism of an executor but keeping the memory the same (increase the spark.executor.cores but not change the spark.executor.memory)

An annoying thing is that the OOM might not be deterministic. Back to the example above, a task that handles 5GB of data causes OOM when running alongside three other 3 tasks that only need at most 2GB of memory. There is a case when the OOM won’t happen: when the heavy task runs alone or with at most a single normal task at the same time in the executor:

[![](https://substackcdn.com/image/fetch/$s_!yxK7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1d68365-ce40-4f6b-bd0f-8edbb38aecb2_936x628.png)](https://substackcdn.com/image/fetch/$s_!yxK7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1d68365-ce40-4f6b-bd0f-8edbb38aecb2_936x628.png)

* If the heavy task runs alone, all 8GB of memory is available for it, and it only needs 5GB to do well.

  [![](https://substackcdn.com/image/fetch/$s_!IRYG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb8544d9-1477-4269-8454-eb0a35daf9ac_914x632.png)](https://substackcdn.com/image/fetch/$s_!IRYG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb8544d9-1477-4269-8454-eb0a35daf9ac_914x632.png)
* If the heavy task runs with only one normal task, both only require 7GB of data, still below the 8GB cap.

If the Spark cluster has two executors, each has 4 cores, this means 8 tasks can run at the same time. If the stage’s total task is not divided by 8, for example, 19 or 20, there is a point in time where the total 3 or 4 tasks are run at the same time; each executor could handle 1 or 2 tasks at a time. If the heavy task somehow ends up in these runs, OOM won’t occur.

---

# The partition size

When discussing an OOM error, we must discuss the partition size because a task used most of the memory for loading the partition.

* The larger the partition, the smaller the number of partitions. The time to handle a single task might be longer, and there is a higher chance of the OOM
* The smaller the partition, the larger the number of partitions. Increasing the number of partitions reduces the workload per task and lowers the chance of OOM. However, the total number of tasks is higher.

There are two phase you can control the partition size:

[![](https://substackcdn.com/image/fetch/$s_!jmUD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdadaf56-f5ee-4da1-a55a-b47cc0dc7b9b_1286x740.png)](https://substackcdn.com/image/fetch/$s_!jmUD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdadaf56-f5ee-4da1-a55a-b47cc0dc7b9b_1286x740.png)

* When reading from the file: the spark.sql.files.maxPartitionBytes controls the max bytes to pack into a Spark partition when reading files. If the files are 20GB and you set the spark.sql.files.maxPartitionBytes to 200MB, you will have a total of 100 partitions.

[![](https://substackcdn.com/image/fetch/$s_!yjDt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b362191-80e1-485c-9090-74fb2312509c_842x566.png)](https://substackcdn.com/image/fetch/$s_!yjDt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b362191-80e1-485c-9090-74fb2312509c_842x566.png)

* After the shuffling phase: By default, you will have 200 partitions during the shuffle partitions unless you change the “spark.sql.shuffle.partitions“ setting. If your total data after shuffling is 2 TB and you leave “spark.sql.shuffle.partitions” at its default, a partition is roughly 10 GB, if no data skew happens.

The bigger your partition, the higher your chance of OOM.

---

# Data skew

In the section above, I mentioned: “a partition is roughly 10 GB, **if no data skew happens.”** That sentence can be understood to mean that the partitions have the same size if the data is evenly distributed. However, in real-life, that is not always true.

Skewing happens.

To understand data skew, we must first understand the data shuffle. In Spark, the stage boundary only appears when data shuffling occurs, and it appears when there are wide-dependency transformations:

[![](https://substackcdn.com/image/fetch/$s_!u7Uj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d1bf6d8-2bcd-4fd2-b403-6fe159f3133b_972x524.png)](https://substackcdn.com/image/fetch/$s_!u7Uj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d1bf6d8-2bcd-4fd2-b403-6fe159f3133b_972x524.png)

* Transformations with **narrow dependencies** are those where each partition in the downstream has a limited number of dependencies on partitions in the parent RDD. These partitions may depend on a single parent (e.g., the map operator) or on a specific subset of parent partitions known beforehand (e.g., with coalesce).
* Transformations with **wide dependencies** require data to be partitioned in a specific way, where a single partition of an upstream RDD contributes to multiple partitions of the child RDD. This typically occurs with operations such as groupByKey or join. These operators require that data with similar attributes (e.g., join keys or aggregation columns) be moved to the same place for processing together. The process is called data shuffling.

Data skew occurs when, during the shuffling process, a partition ends up with far more data than the others because it contains data from a dominant attribute value.

[![](https://substackcdn.com/image/fetch/$s_!uOxb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81f323aa-68ff-42fa-b5a5-8431bb9544d4_1640x768.png)](https://substackcdn.com/image/fetch/$s_!uOxb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81f323aa-68ff-42fa-b5a5-8431bb9544d4_1640x768.png)

For example, if you Group by country, all other countries have only 200 records, but the US has 100,000 records, so the partition store for US data will be skewed. That oversized partition needs far more memory than the others. If the executor doesn’t have enough, it runs out because the shared memory pool is already split across concurrent tasks. This skew task crashes, causing the OOM.

---

# Spark Scheduler behavior

You might wonder, “Why doesn’t Spark scheduler check the partition’s size to allocate it more cleverly, e.g., run the heavy task alone? “

This is because the scheduler wasn’t designed like that. It is built to maximize the Spark cluster resource utilization.

When there is a ready-to-run task set, the scheduler looks at available task slots (executor’s cores) and fills them as quickly as possible without leveraging the partition’s size information.

[![](https://substackcdn.com/image/fetch/$s_!QIIE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4113ef49-442d-4484-bc55-1f93e83ee780_732x944.png)](https://substackcdn.com/image/fetch/$s_!QIIE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4113ef49-442d-4484-bc55-1f93e83ee780_732x944.png)

Back to the above example with an executor with 4 cores and 8GB of memory. The scheduler sees 4 open slots and assigns 4 tasks. 3 tasks are normal, one of them has a skewed partition and needs 5GB on its own.

The scheduler’s assumption about resource usage is fine when all tasks require the same CPU and memory. However, when a small percentage of tasks require 3x or 5x as much memory as the rest, the assumption no longer holds.

Neither the scheduler nor the executor knows about this beforehand. So all 4 tasks start running together, sharing the 8GB memory pool. The heavy task keeps asking for more. At some point, the pool runs out. The task failed first, then the executor.

[![](https://substackcdn.com/image/fetch/$s_!yM1e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98b93436-6fab-4291-9e41-2eef3aaa2328_1536x558.png)](https://substackcdn.com/image/fetch/$s_!yM1e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98b93436-6fab-4291-9e41-2eef3aaa2328_1536x558.png)

When a task fails, if the number of failures is still within the threshold (spark.task.maxFailures; default: 4), the scheduler resets the task’s state and places it in the pending queue. Later, the failed task is executed again, but the problem is not resolved if it’s still run with other tasks. If you are lucky, the task is re-run when the number of tasks is exhausted.

[![](https://substackcdn.com/image/fetch/$s_!MNka!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64c2ffc9-b498-4085-a5b1-efd11e88b93a_1572x602.png)](https://substackcdn.com/image/fetch/$s_!MNka!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64c2ffc9-b498-4085-a5b1-efd11e88b93a_1572x602.png)

As I mentioned above, if you have two executors with 4 cores each, 8 tasks can run in parallel. If the total number of tasks is not divisible by 8, such as 19 or 20, some of the last tasks will run with only 3 or 4 tasks at a time instead of 8. This means that if you retry the task, there's a high chance it will succeed.

This is why the same job can pass on Monday and fail on Thursday. It’s not the data volume that changed. A different scheduling order, a different outcome. That’s the root of why Spark OOM errors sometimes feel unpredictable.

---

# How to debug and fix Spark OOM

> *Only discuss the **org.apache.spark.memory.SparkOutOfMemoryError** here. This is purely from my experience. Feel free to give feedback.*

As I said at the beginning of the article, throwing resources is not sustainable in the long term. Especially when increasing memory, we usually double it as a habit: 4 GB becomes 8 GB, 8 GB becomes 16 GB, 16 GB becomes 32 GB, and 32 GB becomes 64 GB. And memory is very expensive; doubling it every time you get an OOM will cause your company to go broke. So, when the OOM, what do you need to do?

## Investigate

The first thing is to locate the one that has the OOM.

Open the Spark UI and go to the Stages tab.

Find the failed stage and jump into it.

There is a summary metric like this:

[![](https://substackcdn.com/image/fetch/$s_!ul00!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb08c1509-558f-4b26-a460-be0fb3c8304d_2836x404.png)](https://substackcdn.com/image/fetch/$s_!ul00!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb08c1509-558f-4b26-a460-be0fb3c8304d_2836x404.png)

Example Summary Metrics

If the duration or input size’s max is way larger than the median, a high chance that the skew happened.

Next, scroll through the task list with these metrics in mind:

[![](https://substackcdn.com/image/fetch/$s_!YUq7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09adde5-f2af-4917-85d8-eec7e1dd2fdd_2776x1252.png)](https://substackcdn.com/image/fetch/$s_!YUq7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09adde5-f2af-4917-85d8-eec7e1dd2fdd_2776x1252.png)

Example Stage’s task list

* **Input Size**: The partition size when data is read from the source. If the stage only has “Input Size”, you can assume it is one of the first stages that read data from the source.
* **Shuffle Read**: The amount of shuffled that this data read. This means the task is at a stage with at least one upstream stage, as it consumes shuffle data from that stage.
* **Shuffle Write**: The amount of shuffled data written for the next stage.
* **Spill (Memory) and Spill (Disk)**: those track the same amount of spill data; the first is the size of the spilled data in RAM, and the latter is the size on disk (after being compressed). Normally, the latter will be smaller than the first.
* **Duration**: The amount of time that this task processes the partition in this stage.

There are usually two cases here:

* All tasks’ statuses are FAILED: the partition size is too big.

[![](https://substackcdn.com/image/fetch/$s_!NsBj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d1771d2-d66c-4a21-acbd-15efa7981343_636x412.png)](https://substackcdn.com/image/fetch/$s_!NsBj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d1771d2-d66c-4a21-acbd-15efa7981343_636x412.png)

* Some tasks’ statuses are FAILED with the input size/shuffle read way higher than other tasks: data skew. If one task reports 4GB while the other reports 500MB, you have a skew problem.

[![](https://substackcdn.com/image/fetch/$s_!pvrC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F979f82ce-d149-4829-8a04-ed8e4ed93e06_814x528.png)](https://substackcdn.com/image/fetch/$s_!pvrC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F979f82ce-d149-4829-8a04-ed8e4ed93e06_814x528.png)

When looking further into the Spill metrics, in most OOM cases, the spill is quite high; however, there is a case when you don’t see a spill in OOM.

—

In Spark, there are two main approaches to join: **Sort Merge Join (SMJ) and Shuffle Hash Join (SHJ).** Both require all rows with the same join keys from both tables to end up on the same physical partition.

SMJ then sorts each partition locally. Now that both sides are partitioned identically and sorted. Spark iterates through both sorted streams simultaneously and “merges “ the records from the streams if they match.

[![](https://substackcdn.com/image/fetch/$s_!WUyN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a608e75-b564-4830-8167-276b7f961b3b_860x398.png)](https://substackcdn.com/image/fetch/$s_!WUyN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a608e75-b564-4830-8167-276b7f961b3b_860x398.png)

With SHJ, for each partition, Spark uses the smaller side to build an in-memory hash table. The join keys are used as the hash keys in this table, mapping to the actual row data.

[![](https://substackcdn.com/image/fetch/$s_!-qNg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5987551b-44a4-43e0-9bc9-f39ce9cce003_1458x576.png)](https://substackcdn.com/image/fetch/$s_!-qNg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5987551b-44a4-43e0-9bc9-f39ce9cce003_1458x576.png)

Once the hash table is ready, Spark begins “probing” it using the larger dataset. Spark reads through the larger dataset. For each row, it hashes the join key and looks up for a match in the previously built hash table. If there is a match, the rows are combined (following the user’s defined logic).

If the hash table doesn’t fit the memory, you will get OOM without spill.

[![](https://substackcdn.com/image/fetch/$s_!EG0i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5853f1a0-956d-40dd-af79-4971169f1aee_1104x636.png)](https://substackcdn.com/image/fetch/$s_!EG0i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5853f1a0-956d-40dd-af79-4971169f1aee_1104x636.png)

The same thing can happen in aggregation; Spark uses HashAggregate or SortAggregate to calculate the aggregation. The first will sort the input data by the aggregation column (e.g., Group By “user\_id”), then iterate over the sorted data to group records with the same key. The second will build a hash table for the aggregation column. The key will be the aggregation column, and the value is the aggregation buffer.

However, the difference is that you won’t see OOM due to the aggregation here, as Spark will fall back to the SortAggregate if it sees the HashAggregate’s hash table can’t fit in the memory.

# Fix

### The partition is too big for all tasks.

You can:

* Decrease the partition size:

  [![](https://substackcdn.com/image/fetch/$s_!T2f9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38535730-052f-49df-b53c-a39fa84c907b_1294x574.png)](https://substackcdn.com/image/fetch/$s_!T2f9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38535730-052f-49df-b53c-a39fa84c907b_1294x574.png)

  + Decreasing the partition size here by lowering the **spark.sql.files.maxPartitionBytes**
  + Increasing the **spark.sql.shuffle.partitions** to increase the number of partitions after shuffling so each partition holds smaller data.
* Increase the executor pool by increasing the spark.executor.memory.

  [![](https://substackcdn.com/image/fetch/$s_!69hn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15f39064-7ddd-41db-b09d-b745ec46ad07_942x348.png)](https://substackcdn.com/image/fetch/$s_!69hn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15f39064-7ddd-41db-b09d-b745ec46ad07_942x348.png)
* Decrease the executor’s parallelism; fewer tasks share the memory pool, making each task have a larger portion.

  [![](https://substackcdn.com/image/fetch/$s_!SRMv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a5f7e9-e5f6-4d43-b847-909969802b14_1466x470.png)](https://substackcdn.com/image/fetch/$s_!SRMv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a5f7e9-e5f6-4d43-b847-909969802b14_1466x470.png)

For the case of increasing the **spark.sql.shuffle.partitions**, if you are concerned that the high number of partitions could impact the performance, you can leverage Adaptive Query Execution (AQE) to reduce the number of partitions at runtime by coalescing them:

[![](https://substackcdn.com/image/fetch/$s_!1hF8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1462fe7-11df-463c-824f-1673f1ca8755_902x680.png)](https://substackcdn.com/image/fetch/$s_!1hF8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1462fe7-11df-463c-824f-1673f1ca8755_902x680.png)

```
spark.sql.adaptive.enabled = true
spark.sql.adaptive.coalescePartitions.enabled = true
```

> *In Apache Spark 3, released in 2020, Adaptive Query Execution (AQE) was introduced to optimize the query plans, including the number of partitions, based on runtime statistics collected during execution.*

### Skew

Adding more memory won’t help here. The skewed partition will still land on one task. The task will still require more memory than you can provide.

The right fix is to break the skewed partition apart.

AQE has a feature to handle this called skewJoin. Enable it with:

```
spark.sql.adaptive.skewJoin.enabled = true
```

[![](https://substackcdn.com/image/fetch/$s_!c5yZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9625ce2c-1889-44ae-8595-e1c007eb97ac_842x786.png)](https://substackcdn.com/image/fetch/$s_!c5yZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9625ce2c-1889-44ae-8595-e1c007eb97ac_842x786.png)

Once enabled, AQE splits skewed partitions into smaller ones. There are two related parameters here:

* spark.sql.adaptive.skewJoin.skewedPartitionFactor (default: 5): a partition is considered skewed if its size is larger than this factor multiplied by the median partition size. At a default of 5, a partition needs to be 5x the median before AQE acts.
* spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes (default: 256MB): a partition must also exceed this absolute size to be marked as skewed.

Both conditions must be true to tell AQE that a partition is skew.

If the AQE can’t help you here (though it usually can in most cases), you can consider “salting” the join key, which adds a random suffix to distribute the dominant key to smaller partitions, then Spark strips the suffix after the join.

### OOM without Spill

This one is different.

No spill means the operation can’t spill; it must fit entirely in memory or fail. The size of the hash table in the shuffle hash join is typically the problem here.

For the shuffle hash join, this strategy has not been the default for a long time. The reason is the OOM concern: the hash table must fit entirely in memory.

This means you don’t deal with OOM because of the shuffle hash join (SHJ) most of the time. However, SHJ was sometimes needed because it is helpful when the build-side partitions fit in memory, allowing sorting to be skipped on both sides. To enable SHJ, you must do so explicitly:

* Set the “spark.sql.join.preferSortMergeJoin“ to False
* Increase the “spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold”; this setting indicates the maximum size in bytes per partition that can be allowed to build a hash table locally. By default, this setting is 0, which means Spark will ***always*** skip the ShuffleHashJoin.

[![](https://substackcdn.com/image/fetch/$s_!fatZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6ac8799-88ec-4680-9515-24e5bf7b0705_770x268.png)](https://substackcdn.com/image/fetch/$s_!fatZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6ac8799-88ec-4680-9515-24e5bf7b0705_770x268.png)

If the SHJ causes you the OOM, simply switch back to Sort Merge Join by setting spark.sql.join.preferSortMergeJoin and spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold to the default values (True and 0)

---

# Outro

In this article, I discuss my understanding of Spark OOM errors. We start by understanding the way Spark handles execution. Then we move on to understanding why OOM occurs and the factors that affect it, such as partition size and data skew. Next, we examine the Spark scheduler's behavior to understand why it can’t prevent the OOM error. Lastly, I show my experience in investigating and fixing OOM errors.

Thank you for reading this far. See you in my next articles.
