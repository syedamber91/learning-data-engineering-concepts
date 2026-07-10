---
title: "A small hands-on project to 2× your Apache Spark learning process"
channel: vutr
author: "Vu Trinh"
published: 2026-03-17
url: https://vutr.substack.com/p/the-fastest-way-to-learn-spark-is
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Databricks"]
tags: [https, auto, spark, image, substackcdn, fetch]
---

# A small hands-on project to 2× your Apache Spark learning process

*Validate the theory yourself with the available code you can run along with*

> Source: [Open post](https://vutr.substack.com/p/the-fastest-way-to-learn-spark-is)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[databricks|Databricks]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=190480784)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!_fSb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49471f9d-5077-47a4-b561-17c8b45a1533_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!_fSb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49471f9d-5077-47a4-b561-17c8b45a1533_2000x1429.png)

---

# Intro

I received some feedback that, although my Spark articles are very informative, they lack hands-on experience. Because of that, they usually forget what they read a few days later. I agree. The fastest way to learn something new is to learn enough theory, try it yourself, and validate your understanding.

I decided to do a project using Spark to process some data and share my notes in this article. We will process 20GB of data using Apache Spark.

I hear you. “Only 20GB? On Spark?“

My intention is much more than 1TB or even 10TB of data. Although we can now process “big data” with Spark, that volume of data barely fits on most laptops. Renting cloud virtual machines could be an option; however, with that volume of data, we need to request that the cloud vendor increase the VM’s CPU quota (free cloud trials don’t let you run a VM with many CPUs) and carefully manage costs.

So, 20GB of parquet data is more feasible.

The goal of this project is to have a closer look at how the data will be processed in a distributed manner in Spark. We also tune some configurations to adjust the parallelism and monitor what actually happens behind the scenes via the Spark UI.

Of course, the details delivered in this article won’t cover every single thing you need to tune your Spark production workload. However, I hope my work can clear the mist, boost your motivation (there is code so you can run along), and provide the fundamentals to handle your future Spark workload.

> ***Disclaimer**: The results I’m gonna show in this article come from the Spark application submissions on my laptop, and the results might be different when you run it, as the performance of the Spark application might be affected by the current status of the laptop, such as resource contention due to running other applications.*
>
> *Based on my experience, if you want a more isolated setup, you could spin up a VM instance with 12 cores and 36 GB of RAM to experiment. That spec won’t cost you more than $1 per hour, and the cloud free credit trial could cover the VM cost.*

---

# tl;dr

* You will be guided to prepare the 20GB of data, set up the Spark Standalone cluster via Docker, and submit the application.
* A Spark job will be divided into multiple stages. A stage will have multiple tasks, which are the smallest unit of work in Spark. A task will handle a partition, a piece of data. Tasks could be run in parallel in an executor.
* You can understand that tasks are handled in parallel in an executor using the multithreading paradigm.
* Increasing the number of executor cores will increase the parallelism. As a task is executed on a defined number of cores (1 by default, controlled by the “spark.task.cpus” setting).

  + However, increasing executor cores but keeping the executor’s memory the same will shrink the memory portion of each task because more tasks now share the same memory pool.
* Increasing the executor memory will give the task a larger memory portion, which helps reduce the chance of spilling data and improve the overall performance.

  + The memory portion used for the task’s processing and storage is not all the “spark.executor.memory”. It’s calculated by:

    ```
    (spark.executor.memory - reserved memory (300MB in default) ) * spark.memory.fraction (0.6 default)
    ```

* The size of the partition is important as it determines the workload for a single task and the total number of tasks:

  + The larger the partition, the smaller the number of partitions.
  + The time to handle a single task might be longer, and there is a higher chance that the task spills data to disk
  + Although a lower partition size might increase the number of partitions, it reduces the workload for a single task and lowers the chance of data spilling.
* The data type affect the way Spark do aggregation. For example, if you aggregates String, Spark will choose to go with SortAggregate, which is as not as efficient as the HashAggregate.

---

# Prepare data

For all the code and the logic, you can clone this [repo](https://github.com/vutrinh274/spark_small_project) and follow along.

Make sure you run the following commands inside the repo folder. First, install the Python packages:

```
pip install -r requirements.txt
```

To generate the data, we need the “initial“ data file so we can duplicate it until we get 20GB of data. This parquet data file (part of the tpc-ds dataset) will be generated via the [ibis-bench](https://pypi.org/project/ibis-bench/) library:

```
bench tpch gen -s 10
```

Then we copy this file into the ./data folder. We will mount this folder into the Spark standalone cluster on Docker containers, more on this later.

```
cp ./tpch_data/parquet/sf=10/n=1/lineitem/0000.parquet ./data/0000.parquet
```

There is also the “duplicate.sh” script, which accepts the target data size as a parameter. The script will duplicate 0000.parquet to reach the target. To generate 20GB of parquet data, run this:

```
chmod +x duplicate.sh && ./duplicate.sh 20
```

The processing logic is in the .data/main.py file.

It simply reads the folder of generated Parquet files and does simple aggregations. **An important note**: I tried to select and operate on all the fields in the Parquet files so we can actually process 20GB of data. Because Parquet is a columnar format (hybrid), selecting only a few columns will significantly reduce the data scan. However, we don’t want that in this project. We want a solid 20GB.

[![](https://substackcdn.com/image/fetch/$s_!q5LO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe015b655-ae3e-45f1-b4ae-da71e142be9a_900x662.png)](https://substackcdn.com/image/fetch/$s_!q5LO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe015b655-ae3e-45f1-b4ae-da71e142be9a_900x662.png)

# Start the cluster

Next, we will start the Standalone Spark Cluster via Docker.

[![](https://substackcdn.com/image/fetch/$s_!wbUO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d8f363c-b67f-4e9c-8abc-b129da3a70a6_1090x588.png)](https://substackcdn.com/image/fetch/$s_!wbUO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d8f363c-b67f-4e9c-8abc-b129da3a70a6_1090x588.png)

This is not a Spark cluster.

This is a cluster of machines that provide resource for the Spark cluster, which is a set of JVM processes (driver and executors). The Spark cluster will ask the cluster manager resource from the cluster of machines. There are different managers, such as YARN, Kubernetes, or, in our case, the standalone one.

I prepared the “docker-compose.yaml“ file so you can simply run:

```
docker compose up -d
```

For the Spark master (the cluster manager), we use the official Spark 4.0.0 image, expose ports 8080 and 7077, set the necessary environment variables, and run the “start-master.sh” script to start the master process. I also mount the “data” and “spark-events” volumes into this Docker container. The first stores the PySpark file and the Parquet data; the latter stores monitoring information used by the Spark History server.

[![](https://substackcdn.com/image/fetch/$s_!T2zN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3920fcfa-a131-4728-bdf0-77bdaf2a1d17_1490x694.png)](https://substackcdn.com/image/fetch/$s_!T2zN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3920fcfa-a131-4728-bdf0-77bdaf2a1d17_1490x694.png)

For the worker, we also use the same image, set the worker capacity in the environment variable, and run the script to start the worker process. We also mount the data and spark-events volumes for the worker.

[![](https://substackcdn.com/image/fetch/$s_!nsxv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ddcf57f-b228-49d5-a976-0be0e249870b_1486x728.png)](https://substackcdn.com/image/fetch/$s_!nsxv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ddcf57f-b228-49d5-a976-0be0e249870b_1486x728.png)

The last component is the Spark History Server, where we can observe metrics from our Spark application. The service is exposed on port 18080.

[![](https://substackcdn.com/image/fetch/$s_!5aDR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a874982-d890-41bb-b3a4-252c016cf4b7_1178x516.png)](https://substackcdn.com/image/fetch/$s_!5aDR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a874982-d890-41bb-b3a4-252c016cf4b7_1178x516.png)

# Let’s run our application

Here is the PySpark logic. It simply initiates a Spark session, reads a folder of Parquet files, and performs a simple GroupBy that touches all the columns.

[![](https://substackcdn.com/image/fetch/$s_!g9jF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdddec10a-0f6b-4bd3-bb0f-63bcc5163163_890x1374.png)](https://substackcdn.com/image/fetch/$s_!g9jF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdddec10a-0f6b-4bd3-bb0f-63bcc5163163_890x1374.png)

## The resource request

Let’s walk through the SparkSession initialization code block:

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=190480784)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

* We will submit this application inside the Spark master container, so we can note “spark-master:7077“ for the “master” value here. (We’ve already named the host of the master container “spark-master“)
* We will let the driver’s resource as default.
* All the configurations related to the “eventLog” are simply used for logging.
* We don’t use dynamic resource allocation here to monitor the application’s resource easier.
* The “spark.executor.instances” indicates the number of executors that will be spawned for this application.

  [![](https://substackcdn.com/image/fetch/$s_!DjtE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e68de74-3ef7-49cc-bf29-b2bcfdea6683_742x514.png)](https://substackcdn.com/image/fetch/$s_!DjtE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e68de74-3ef7-49cc-bf29-b2bcfdea6683_742x514.png)
* The “spark.executor.cores“ indicates the number of CPU cores for an executor. This determines the application's parallelism capacity, as a task is executed on a defined number of cores (1 by default, controlled by the “spark.task.cpus” setting).

  [![](https://substackcdn.com/image/fetch/$s_!9Fn_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3c814cc-67f8-4ce0-8ea4-d07f6d27fc6f_532x418.png)](https://substackcdn.com/image/fetch/$s_!9Fn_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3c814cc-67f8-4ce0-8ea4-d07f6d27fc6f_532x418.png)

  + In our case, we set “spark.executor.instances” to 2 and “spark.executor.cores” to 2, which means there are 4 tasks that can run in parallel, 2 per executor. You can think that tasks are processed in multiple threads in a single executor.
* The “spark.executor.memory“ indicates the amount of JVM heap memory for an executor. In our case, we set it to 2GB.

  [![](https://substackcdn.com/image/fetch/$s_!4egJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc9182b-a8f3-471a-af0c-76b0e3404df6_784x502.png)](https://substackcdn.com/image/fetch/$s_!4egJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc9182b-a8f3-471a-af0c-76b0e3404df6_784x502.png)

  However, this does not mean an executor could use the whole 2GB for data processing. As discussed in [my article about Spark memory management](https://vutr.substack.com/p/i-spent-8-hours-understanding-apache?utm_source=publication-search), the memory zone used for processing and storage is calculated by:

  ```
  (spark.executor.memory - reserved memory) * spark.memory.fraction
  ```

  With reserved memory of 300, and spark.memory.fraction is 0.6 by default, the actual memory an executor could use for processing and storage is:

  ```
  (2048 -300) * 0.6 = 1048.8MB
  ```
* The “spark.cores.max” configuration is an interesting one, as in a standalone cluster, a Spark application tries to wrap as many cores as possible across all clusters, we set “spark.cores.max” equal to the “spark.executor.instances” \* “spark.executor.cores” to prevent the application from asking for resource.

---

# Running the application

## What if we request Spark resources more than the cluster’s capacity

In our initial setup, each worker container only provides 4 cores and 4GB of RAM. We have two workers, so the hard limits for the CPU and memory are 8 cores and 8GB.

[![](https://substackcdn.com/image/fetch/$s_!pbOJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc25f83f9-e948-4ef2-82bb-c7b251c503c1_360x74.png)](https://substackcdn.com/image/fetch/$s_!pbOJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc25f83f9-e948-4ef2-82bb-c7b251c503c1_360x74.png)

This means if we request more than 8 CPU cores or more than 8GB RAM:

[![](https://substackcdn.com/image/fetch/$s_!_5Vf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44284ba7-d441-4d71-954a-3c2e8ba3a5ca_430x122.png)](https://substackcdn.com/image/fetch/$s_!_5Vf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44284ba7-d441-4d71-954a-3c2e8ba3a5ca_430x122.png)

Total of 10 cores and 10GB RAM

When we run the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

We will receive the error like this:

[![](https://substackcdn.com/image/fetch/$s_!-_Hg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc20290f1-50ae-4f09-a1c2-45072ad06347_1696x70.png)](https://substackcdn.com/image/fetch/$s_!-_Hg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc20290f1-50ae-4f09-a1c2-45072ad06347_1696x70.png)

## The data size in the memory

Although we read 20GB of Parquet data, the total memory usage will surely exceed 20GB. This is because Parquet is compressed when writing to disk (using SNAPPY in most cases). When reading data from disk into RDDs, Spark must deserialize and uncompress it.

[![](https://substackcdn.com/image/fetch/$s_!Cr-Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57edcdad-a3f4-4f94-a31b-9f43aa49cc69_908x516.png)](https://substackcdn.com/image/fetch/$s_!Cr-Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57edcdad-a3f4-4f94-a31b-9f43aa49cc69_908x516.png)

To see the real memory usage of the parquet data, we can cache the dataframe and observe the storage tab in the Spark History UI (localhost:18080).

> *Caching is storing the results of a Spark object such as the DataFrame, in the memory (or disk) of worker nodes so executor can quickly read it for next operations without re-computing that object.*

To cache the data, adjust the PySpark logic to:

[![](https://substackcdn.com/image/fetch/$s_!0vD8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f1b05d1-27af-40bb-8a8a-11f76c850816_1126x264.png)](https://substackcdn.com/image/fetch/$s_!0vD8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f1b05d1-27af-40bb-8a8a-11f76c850816_1126x264.png)

* Read a single 0000.parquet (2.6GB) file in the data folder.
* Cache the df
* Because cache is a transformation, we need an action, in this case, the count, to trigger the transformation.

, and comment out the agg logic:

[![](https://substackcdn.com/image/fetch/$s_!Y7L7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc79c9f8f-8fe7-467c-afe6-b68ad414deb6_924x724.png)](https://substackcdn.com/image/fetch/$s_!Y7L7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc79c9f8f-8fe7-467c-afe6-b68ad414deb6_924x724.png)

Then, we run the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

After that, we can visit the Spark history server (localhost:18080), choose your application, and switch to the storage type:

[![](https://substackcdn.com/image/fetch/$s_!HOSx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a5ff2-315c-46d5-808c-33db4d46c67a_2868x522.png)](https://substackcdn.com/image/fetch/$s_!HOSx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c7a5ff2-315c-46d5-808c-33db4d46c67a_2868x522.png)

As you can see, the parquet file might use more memory than its on-disk size (2.6GB). The memory size is 3.7GB, and part of it is spilled to disk (530.8MB).

Being aware that the data memory size is always greater than the disk size is very important for the task's resource consumption and performance. We will revisit this point later.

## The partition size

There is a configuration I did not mention previously: “spark.sql.files.maxPartitionBytes”. This configuration controls the max bytes to pack into a Spark partition when reading files. In our case, we set it to 256 MB, which means Spark will try to pack no more than 256MB of Parquet data into a partition. The higher the “spark.sql.files.maxPartitionBytes”, the larger the partition.

[![](https://substackcdn.com/image/fetch/$s_!2BMu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe5178c4-5b92-4c25-9b76-bcc161eafc94_1166x686.png)](https://substackcdn.com/image/fetch/$s_!2BMu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe5178c4-5b92-4c25-9b76-bcc161eafc94_1166x686.png)

Speaking of partition, let’s visit a bit of the Spark anatomy:

[![](https://substackcdn.com/image/fetch/$s_!vu58!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23eb70ef-9fab-44f0-a0f2-7e9c713e9211_1014x608.png)](https://substackcdn.com/image/fetch/$s_!vu58!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23eb70ef-9fab-44f0-a0f2-7e9c713e9211_1014x608.png)

* **Application:** Every Spark application is associated with a Spark cluster, which comprises a driver and a set of executors.
* **Job:** A job represents a series of transformations applied to data. It encompasses the entire workflow from start to finish. The series of transformations can be triggered only by an action. In our case, the transformations are the aggregations, and the action is the “show“. So we can safely say that a job is associated with an action.
* **Stage:** A stage is a job segment executed without data shuffling. A job is split into different stages when a transformation requires shuffling data across partitions. In our case, the GroupBy surely result in the shuffle.
* **Task:** A task is the smallest unit of execution within Spark. Each stage is divided into multiple tasks, each of which handles a partition. At a given stage, tasks can run in parallel; the degree of parallelism depends on the executor's resources.

Back to our case, if a partition is 256 MB, there will be roughly 80 partitions for 20GB of data (20 \* 1024 / 256). We are configuring each executor with 2 cores. This means that at any given time, an executor can process up to 2 tasks in parallel.

## Submit the application

After code adjustment to cache the data in the “The data size in the memory“ section, make sure to adjust the code:

[![](https://substackcdn.com/image/fetch/$s_!Y2QK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6eca7249-32f5-4e14-8ff4-d750d7a02901_1084x996.png)](https://substackcdn.com/image/fetch/$s_!Y2QK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6eca7249-32f5-4e14-8ff4-d750d7a02901_1084x996.png)

* Change 0000. parquet to \*.parquet in the input\_path so we can process 20GB of data.
* Uncomment the aggregation
* Comment on the persist and count
* Make sure the resource request is 2 executor instances, each has 2 CPU cores and 2G RAM, the max partition is 256 MB.

[![](https://substackcdn.com/image/fetch/$s_!Jdfk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F193fb94f-c965-462c-a01d-c82807f59732_962x196.png)](https://substackcdn.com/image/fetch/$s_!Jdfk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F193fb94f-c965-462c-a01d-c82807f59732_962x196.png)

Then, we can submit the application.

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

Visiting the master UI (localhost:8080), we could see the information about the executors:

[![](https://substackcdn.com/image/fetch/$s_!rs-d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd1e1ba5-3866-4477-9338-9e879bc01d99_1482x184.png)](https://substackcdn.com/image/fetch/$s_!rs-d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd1e1ba5-3866-4477-9338-9e879bc01d99_1482x184.png)

After 11 minutes, the process completes.

[![](https://substackcdn.com/image/fetch/$s_!8apM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55eb7f4e-48df-4f82-98af-4489cb5b1985_414x158.png)](https://substackcdn.com/image/fetch/$s_!8apM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55eb7f4e-48df-4f82-98af-4489cb5b1985_414x158.png)

We can visit the Spark History Server to understand what happened behind the scenes.

For the physical execution plan, we can choose the application, switch to the “SQL/Dataframe“ tab, choose the completed query, and click “Details“, we can see the plan:

[![](https://substackcdn.com/image/fetch/$s_!JzpG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a33815b-1d99-49e0-a57a-74bb7bb63438_1160x466.png)](https://substackcdn.com/image/fetch/$s_!JzpG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a33815b-1d99-49e0-a57a-74bb7bb63438_1160x466.png)

* From the bottom up, first, the executors scan parquet and convert the data from columnar format to Spark’s row format.
* Then there are the Sort and SortAggregate. This is the partial aggregation step in the Map phase
* Then there is a shuffle at the Exchange.
* Then, there are ShuffleQueryStage and AQEShuffleRead in the Reduce phase; these are AQE features that use runtime statistics to optimize the plan. Let me show the role of AQE here:

  [![](https://substackcdn.com/image/fetch/$s_!I_gD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3691ad4-9242-49dc-9ddc-0c2e353159df_1418x602.png)](https://substackcdn.com/image/fetch/$s_!I_gD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3691ad4-9242-49dc-9ddc-0c2e353159df_1418x602.png)

  + In the Exchange step, we see that data is hash-partitioned to shuffle the data. The data will be hashed and routed to 200 partitions. In Spark, by default, you will have 200 partitions during the shuffle partitions unless you adjust the “spark.sql.shuffle.partitions“ setting.

    [![](https://substackcdn.com/image/fetch/$s_!jmc0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefbfcc1c-2110-48af-9771-c423eb94ce13_1042x212.png)](https://substackcdn.com/image/fetch/$s_!jmc0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefbfcc1c-2110-48af-9771-c423eb94ce13_1042x212.png)
  + However, the Adaptive Query Execution (AQE) doesn’t see the need for 200 partitions and decides to coalesce them into a single partition.

    > *In Apache Spark 3, released in 2020, Adaptive Query Execution (AQE) was introduced to optimize the query plans, including the number of partitions, based on runtime statistics collected during execution.*

    [![](https://substackcdn.com/image/fetch/$s_!qput!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d17bdb9-f070-4eea-994e-ca9811e23ff5_1076x566.png)](https://substackcdn.com/image/fetch/$s_!qput!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d17bdb9-f070-4eea-994e-ca9811e23ff5_1076x566.png)
  + To learn more about Spark shuffle and the role of AQE in this process, you can read this [article](https://vutr.substack.com/p/a-9-minute-simple-explanation-of?utm_source=publication-search).
* Next, we have another round of Sort and SortAggregate. This is the final aggregation step. Partial aggregation, final aggregation, and SortAggregate will be discussed in detail later.
* Finally, there is the collect limit associated with the action “.show(10)“ in our code.

Switching to the stage tab, there are a total of three stages:

[![](https://substackcdn.com/image/fetch/$s_!gNsh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38ba82d7-ec99-43c1-a2f5-5cdd33c4ce03_2862x222.png)](https://substackcdn.com/image/fetch/$s_!gNsh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38ba82d7-ec99-43c1-a2f5-5cdd33c4ce03_2862x222.png)

The first stage is for reading the data from disk. The longest stage is where the partial SortAggregate happens. We also observe that this stage is the Map phase as it writes the shuffle data to disk. The final stage is the Shuffle stage, assisted by AQE, where we can see that it reads the shuffle records from the last stage.

Let’s zoom in on the longest stage and expand the “event timeline“. We can see that at any given time, the executor can handle only two tasks in parallel.

[![](https://substackcdn.com/image/fetch/$s_!jsMf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81badbf1-831e-45fa-99ed-fdcfdda235de_872x754.png)](https://substackcdn.com/image/fetch/$s_!jsMf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81badbf1-831e-45fa-99ed-fdcfdda235de_872x754.png)

Scrolling a bit to the “Tasks“ section, we can see that:

[![](https://substackcdn.com/image/fetch/$s_!PZBK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F216cb724-3542-4b19-99ab-8856f8c45683_2782x594.png)](https://substackcdn.com/image/fetch/$s_!PZBK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F216cb724-3542-4b19-99ab-8856f8c45683_2782x594.png)

* There are total of 84 tasks
* Each task will handle ~250MB of data (the Input size)
* Each task need ~35s to finish.
* Each task spills 832MB of data (in memory). The spill data is written to disk as 358.7 MB. This Spill data comes from the two factors. The 250MB of Parquet data is the size on disk; it will expand when the executor deserializes it in memory (as we discussed in the “The data size in the memory” section). Secondly, there is memory overhead in the Sort step.

## Aggregation

When you perform an aggregation (like SUM or AVG), Spark tries to be efficient. Instead of sending every raw record across the network during the shuffle process, it first performs a “pre-aggregation” locally on each partition in the Map phase (partial aggregation) and writes out the aggregation result as shuffle files.

[![](https://substackcdn.com/image/fetch/$s_!cLpS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe643ec08-f908-4e29-97ce-6962b3020e3f_1194x914.png)](https://substackcdn.com/image/fetch/$s_!cLpS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe643ec08-f908-4e29-97ce-6962b3020e3f_1194x914.png)

Then, the reduce tasks will read these files and make the final aggregation to retrieve the result. This helps Spark reduce **network I/O** because executors will exchange the "summary" of the data rather than the raw data.

[![](https://substackcdn.com/image/fetch/$s_!3Qw2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30a18f4e-8a84-4f49-a24f-fc9c4672246a_1110x452.png)](https://substackcdn.com/image/fetch/$s_!3Qw2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30a18f4e-8a84-4f49-a24f-fc9c4672246a_1110x452.png)

That’s why in our case, we saw the SortAggregate happen twice. The first is partial aggregation, which occurs in the Map stage, and the latter is final aggregation, which occurs in the Reduce stage.

Speaking of SortAggregate, Spark provides two main approaches to aggregation: SortAggregate and HashAggregate.

The first will sort the input data based on the aggregation column (e.g., Group By “user\_id“), then iterate over it to group records with the same key.

[![](https://substackcdn.com/image/fetch/$s_!WUyN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a608e75-b564-4830-8167-276b7f961b3b_860x398.png)](https://substackcdn.com/image/fetch/$s_!WUyN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a608e75-b564-4830-8167-276b7f961b3b_860x398.png)

The second will build a hash table for the aggregation column. The key will be the aggregation column, and the value is the aggregation buffer. This buffer is updated based on the aggregation expression (e.g., SUM or COUNT) whenever the same key appears.

[![](https://substackcdn.com/image/fetch/$s_!-qNg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5987551b-44a4-43e0-9bc9-f39ce9cce003_1458x576.png)](https://substackcdn.com/image/fetch/$s_!-qNg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5987551b-44a4-43e0-9bc9-f39ce9cce003_1458x576.png)

The HashAggregate is way more preferred compared to the SortAggregate because the it doesn’t require sorting data beforehand. However, Spark sometimes has to switch to SortAggregate. The first case is the hash table growing too large and not fitting into the memory. The second case relates to the type of data being aggregated.

For Spark to use a HashAggregate efficiently, it prefers to use the UnsafeRow format.

> *UnsafeRow format is a way Spark represents data in off-heap memory, bypassing the JVM garbage collector. It is the core of “[Project Tungsten](https://www.databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html),” the initiative to improve Spark memory management and CPU efficiency*

This format works best when the data for the aggregation buffer has a fixed size. Integers, Longs, and Doubles always take up the same number of bytes. Spark can update these "in-place" within the hash table quickly. However, with dynamic types such as String, they aren't easily "mutable" in a fixed-size memory slot. Thus, to validate for the HashAggregate, the data type must belong to this list:

[![](https://substackcdn.com/image/fetch/$s_!wZFo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee7c2fb9-3c04-4bb4-82e2-d18e08076e2e_403x301.png)](https://substackcdn.com/image/fetch/$s_!wZFo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee7c2fb9-3c04-4bb4-82e2-d18e08076e2e_403x301.png)

Source: Data Ninjago, [Spark SQL Query Engine Deep Dive (9) – SortAggregateExec](https://dataninjago.com/2022/01/06/spark-sql-query-engine-deep-dive-9-sortaggregateexec/)

In our case, because we do aggregation for all of the fields, and some fields are String, such as the “l\_comment“ or the “l\_returnFlag“, Spark choose to go with SortAggregate instead of the HashAggregate.

[![](https://substackcdn.com/image/fetch/$s_!-fdC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2a901ec-98c4-4d68-acf9-7127069d0a8d_1422x566.png)](https://substackcdn.com/image/fetch/$s_!-fdC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2a901ec-98c4-4d68-acf9-7127069d0a8d_1422x566.png)

So, be mindful about the data type when you aggregation on Spark next time.

## Adjust the partition size

Let's make it more fun.

We’re gonna twist the resource request to see what it's gonna affect our application. To make it easier to observe, I change only one factor per application. As the physical plan will be the same as our initial submission, I won't deliver it again. We will only observe the overall duration, task parallelism, and the workload of a single task.

First, we adjust the partition size. We lower the spark.sql.files.maxPartitionBytes to 128MB to 256MB. This means a task could handle a smaller partition; however, it will have 2x number of partitions.

[![](https://substackcdn.com/image/fetch/$s_!5FVs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb2cf18-ce51-4043-b80e-9da3cceaf779_1240x272.png)](https://substackcdn.com/image/fetch/$s_!5FVs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb2cf18-ce51-4043-b80e-9da3cceaf779_1240x272.png)

After changing the spark.sql.files.maxPartitionBytes, we simply re-submit the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

Surprisingly, the application only takes 6.5 minutes.

[![](https://substackcdn.com/image/fetch/$s_!B2a3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a85fdd3-5bb2-40c7-8fc5-beedcf1c380e_402x156.png)](https://substackcdn.com/image/fetch/$s_!B2a3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a85fdd3-5bb2-40c7-8fc5-beedcf1c380e_402x156.png)

Let’s also zoom into the second stage, where the SortAggregate happens. The parallelism doesn’t change; each executor can handle only 2 tasks at a time.

[![](https://substackcdn.com/image/fetch/$s_!EIc-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc67a6663-e0a7-4e56-8160-051e7f5eda0f_894x748.png)](https://substackcdn.com/image/fetch/$s_!EIc-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc67a6663-e0a7-4e56-8160-051e7f5eda0f_894x748.png)

What changes is the total number of tasks the executor needs to handle:

[![](https://substackcdn.com/image/fetch/$s_!iem9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9cbbf7de-2f5e-49f3-95ec-0469537a1bd8_2682x604.png)](https://substackcdn.com/image/fetch/$s_!iem9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9cbbf7de-2f5e-49f3-95ec-0469537a1bd8_2682x604.png)

* There will be a total of 168 tasks, doubling from 84 tasks.
* This is because a task now only handles a ~128MB partition.
* The cool thing is that we see a 2x decrease in data spill, which means each task can handle more data processing in memory. Thus, it only takes ~12s for a task to complete, reduce 65.7 % compare to the initial submission (35s)

A task that handles a partition faster is an important factor in reducing the overall application’s duration, despite the 2x increase in the number of partitions.

## Adjust the executor’s number of cores

Next, we roll back the spark.sql.files.maxPartitionBytes to 256MB and increase the number of cores per executor. Make your resource variables look like this:

[![](https://substackcdn.com/image/fetch/$s_!DkRU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4fb3fecd-da27-407c-81ce-85df2efa0ff8_1262x258.png)](https://substackcdn.com/image/fetch/$s_!DkRU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4fb3fecd-da27-407c-81ce-85df2efa0ff8_1262x258.png)

Then, re-submit the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

Visiting the localhost:8000, we can now see each executor has 4 cores:

[![](https://substackcdn.com/image/fetch/$s_!ysFW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F073758ed-1f35-4faf-a455-456cee46e3de_1562x186.png)](https://substackcdn.com/image/fetch/$s_!ysFW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F073758ed-1f35-4faf-a455-456cee46e3de_1562x186.png)

The duration is 7.9 mins, it is faster than the first submission and slower than the second submission.

[![](https://substackcdn.com/image/fetch/$s_!9t_s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cff5157-5ebc-4f3e-a3ec-4bdf32867abe_416x128.png)](https://substackcdn.com/image/fetch/$s_!9t_s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cff5157-5ebc-4f3e-a3ec-4bdf32867abe_416x128.png)

We also zoom in on the second stage, where the Sort Aggregate occurs.

The parallelism increases because we increased the executor’s core; each executor can now handle 4 tasks at a time.

[![](https://substackcdn.com/image/fetch/$s_!ZUHD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2595ca5c-e9dd-4f7a-a6d2-93b0a47e1b48_942x950.png)](https://substackcdn.com/image/fetch/$s_!ZUHD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2595ca5c-e9dd-4f7a-a6d2-93b0a47e1b48_942x950.png)

The total number of tasks is now back to 84 as we roll back the spark.sql.files.maxPartitionBytes to 256MB:

[![](https://substackcdn.com/image/fetch/$s_!1g-k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2008189f-79c1-4128-ad2a-946cda79f825_2794x690.png)](https://substackcdn.com/image/fetch/$s_!1g-k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2008189f-79c1-4128-ad2a-946cda79f825_2794x690.png)

* The time to process a task is now ~40 seconds. This is because more tasks can be handled by an executor at a given time, but the memory doesn’t increase, so the portion of memory for a task shrinks.
* The memory spill is increase compare to the first submission (1GB vs 832MB). Align to my point about the portion of memory for a task shrinks when more task can be run on an executor.

## Adjust the executor’s memory

Finally, we roll back the spark.executor.cores to 2 and increase the executor’s memory to 4G RAM:

[![](https://substackcdn.com/image/fetch/$s_!7itN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc81c46d0-469c-4cec-badf-2edccf467c98_1250x250.png)](https://substackcdn.com/image/fetch/$s_!7itN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc81c46d0-469c-4cec-badf-2edccf467c98_1250x250.png)

Next, we submit the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/main.py
```

When visiting the localhost:8080, we see that each executor now has 4G RAM:

[![](https://substackcdn.com/image/fetch/$s_!doC3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdf75fc0-e4c9-43f7-9788-36096b04ea40_1562x176.png)](https://substackcdn.com/image/fetch/$s_!doC3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdf75fc0-e4c9-43f7-9788-36096b04ea40_1562x176.png)

The application duration is 8.1 minutes. Faster than the first submission.

[![](https://substackcdn.com/image/fetch/$s_!GmIS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa39b380-87cf-434c-8699-09025f15c0b4_420x160.png)](https://substackcdn.com/image/fetch/$s_!GmIS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa39b380-87cf-434c-8699-09025f15c0b4_420x160.png)

The task parallelism is still 2, but a single task is now completed faster compare the first submission as the task has more memory now:

[![](https://substackcdn.com/image/fetch/$s_!jXCN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48716f31-ea04-4606-87b0-66979cc5b0c4_2798x600.png)](https://substackcdn.com/image/fetch/$s_!jXCN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48716f31-ea04-4606-87b0-66979cc5b0c4_2798x600.png)

* A task only need 25s to complete (the first submission is ~35s)
* Spill memory is the same as the first submission

  + This is quite counterintuitive to me. As I discussed above, the portion of memory allocated to a task improves, so I expect the Spill volume to be smaller than in the first submission. However, it’s the same
  + My best guess at the moment is that it’s related to the SortAggregate mechanism; I might need more time to dive deeper into this observation.

---

# Outro

In this article, I set up a small Spark application that runs on a Docker-based Spark Standalone cluster. During the process, I discuss Spark’s data size in memory and the partition size before running the application, and observe different runs with varying resource profiles. I also explore the approaches Spark uses to perform aggregation behind the scenes.

Thank you for reading this far. See you in my next articles.
