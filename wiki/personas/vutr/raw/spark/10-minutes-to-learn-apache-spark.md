---
title: "10 Minutes to Learn Apache Spark JOINs with a Hands-On Project"
channel: vutr
author: "Vu Trinh"
published: 2026-03-24
url: https://vutr.substack.com/p/10-minutes-to-learn-apache-spark
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark"]
tags: [https, spark, auto, join, image, substackcdn]
---

# 10 Minutes to Learn Apache Spark JOINs with a Hands-On Project

*How do JOIN operations work in Spark?*

> Source: [Open post](https://vutr.substack.com/p/10-minutes-to-learn-apache-spark)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=191115067)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!Hwi6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc50390c1-9d12-43ed-ac74-4c51d3f08e3c_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Hwi6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc50390c1-9d12-43ed-ac74-4c51d3f08e3c_2000x1429.png)

---

# Intro

Apache Spark was designed to solve the problem of processing large volumes of data during data movement from A to B.

It has evolved.

In [2015](https://people.csail.mit.edu/matei/papers/2015/sigmod_spark_sql.pdf), the creator introduced the new Spark SQL model, which let users leverage the benefits of relational processing. That means the user can express the processing logic using “SELECT“, “GROUP BY“, “SUM“, “AVG“, and especially “JOIN”.

The ability to work with multiple datasets is the backbone of many business transformations.

JOINs are among the most commonly used operations in Spark. Although I shared how Spark JOINs work [here](https://vutr.substack.com/i/166248471/join), it is still theories.

We need to validate them, as I did with Spark’s fundamentals [here](https://vutr.substack.com/publish/post/190480784?r=2rj6sg&utm_campaign=post&utm_medium=web).

In this article, we will walk through a simple project with (a quite dummy) Spark JOIN logic to understand what actually happens behind the scenes.

> ***Prerequisite:** I expect you to have some Spark fundamentals, such as Spark clusters, Spark jobs/stages/tasks, or data shuffling. You can read my Spark series [here](https://vutr.substack.com/t/spark).*

---

# Prepare the data

First, clone this [repo](https://github.com/vutrinh274/spark_join_project) and enter that repo for the rest of the project.

Then, install the Python packages:

```
pip install -r requirements.txt
```

For this project, we will join two datasets from the TPC-H: the “lineitem” (~2.6GB) and the “order” (~600MB) using the “o\_orderkey” column. To generate these two tables:

```
cd data && bench tpch gen -s 10
```

---

# The logic

The processing logic is in the .data/join.py file. It simply reads these two datasets and joins them together.

[![](https://substackcdn.com/image/fetch/$s_!CrZ4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe55fd363-1dac-4355-9d0f-eeb7721b0b65_1404x808.png)](https://substackcdn.com/image/fetch/$s_!CrZ4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe55fd363-1dac-4355-9d0f-eeb7721b0b65_1404x808.png)

For the Spark cluster resource:

[![](https://substackcdn.com/image/fetch/$s_!IBUf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35c0e070-ce8b-4b28-bb08-2574eda42375_630x338.png)](https://substackcdn.com/image/fetch/$s_!IBUf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35c0e070-ce8b-4b28-bb08-2574eda42375_630x338.png)

* There will be 2 executor instances. Each will have 2 cores and 4GB RAM. This means the application’s parallelism is 4, where a task could be handled by a CPU core (controlled by spark.task.cpus, which is 1 by default)
* We will let the driver’s resource be the default.
* All the configurations related to the “eventLog” are simply used for logging.
* We ignore dynamic resource allocation here to monitor the application’s resource easier.
* The “spark.sql.files.maxPartitionBytes” is 256 MB, which means Spark will try to pack no more than 256MB of Parquet data into a partition when reading from files. The higher the “spark.sql.files.maxPartitionBytes”, the larger the partition.

---

# The Spark Standalone Cluster

We need a cluster of machines to launch our Spark cluster. In this project, we start a Spark Standalone cluster in Docker:

```
docker compose up -d
```

[![](https://substackcdn.com/image/fetch/$s_!wbUO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d8f363c-b67f-4e9c-8abc-b129da3a70a6_1090x588.png)](https://substackcdn.com/image/fetch/$s_!wbUO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d8f363c-b67f-4e9c-8abc-b129da3a70a6_1090x588.png)

Docker will pull the official Spark 4.0.0 image and run scripts to start a master container (exposed on port 8080), a history server (for debugging, exposed on port 18080), and two workers (each with 4 CPU cores and 4 GB of RAM).

---

# Sort Merge Join (SMJ)

After the done with the preparation, let’s submit our app:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/join.py
```

After the application completes, we can visit the Spark History server (localhost:18080) to see what actually happened. In this article, we focus only on the JOIN operation. For other details, such as the input stage, partition size, and parallelism, please see my [previous article](https://vutr.substack.com/p/the-fastest-way-to-learn-spark-is).

—

For the physical execution plan, we can choose the just finished application, switch to the “SQL/Dataframe“ tab, choose the completed query, and click “Details “

[![](https://substackcdn.com/image/fetch/$s_!jH0c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb94263e-9a43-4e4b-9c53-1de8185fe467_1160x648.png)](https://substackcdn.com/image/fetch/$s_!jH0c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb94263e-9a43-4e4b-9c53-1de8185fe467_1160x648.png)

For our inner join operation, we see that Spark applied the SMJ for us.

> ***Note:** SortMergeJoin is not an exclusive technique in Spark; it has long existed in the database field.*

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=191115067)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## The shuffle

[![](https://substackcdn.com/image/fetch/$s_!TAOl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad7b68fb-50dd-40e5-82e4-431d6a1d03bf_1076x578.png)](https://substackcdn.com/image/fetch/$s_!TAOl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad7b68fb-50dd-40e5-82e4-431d6a1d03bf_1076x578.png)

Before the join can happen, Spark ensures that rows with the same join keys from both tables end up on the same physical partition.

* **Exchange (4 & 11):** Spark performs a “Shuffle” to redistribute data across the cluster.
* **AQEShuffleRead (6 & 13):** Adaptive Query Execution (AQE) optimizes this read, coalescing small partitions to ensure the join is efficient.

## The Sort Phase

[![](https://substackcdn.com/image/fetch/$s_!PPMe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa11be2bb-5cbb-4c19-b084-d9e83a3644d1_1232x384.png)](https://substackcdn.com/image/fetch/$s_!PPMe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa11be2bb-5cbb-4c19-b084-d9e83a3644d1_1232x384.png)

Once the data is partitioned by the join key, each partition must be sorted locally.

* **Sort (7 & 14):** Both branches of the join tree show an explicit `Sort` operator.

## The Merge Phase

[![](https://substackcdn.com/image/fetch/$s_!8JY5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeb95299-c07f-4416-8015-033743f10ad6_420x536.png)](https://substackcdn.com/image/fetch/$s_!8JY5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbeb95299-c07f-4416-8015-033743f10ad6_420x536.png)

Now that both sides are partitioned identically and sorted, the join itself occurs at node **(15)**.

* **Linear Scan:** Spark iterates through both sorted streams simultaneously.
* **Pointer Comparison:** It compares the keys at the current “pointer” of each stream.

  + If the keys match, it produces a joined row.
  + If the left key is smaller, it moves the left pointer forward.
  + If the right key is smaller, it moves the right pointer forward.
* Because the data is sorted, Spark only needs to pass through each dataset **once** (O(n + m) complexity).

---

# Shuffle Hash Join

SMJ is the preferred join strategy at the moment. However, the crown used to belong to the ShuffleHashJoin (SHJ).

### 1. The Shuffle Phase

As with SortMergeJoin, Spark routes the records with the same join keys to the same partition. This results in the shuffle processes.

[![](https://substackcdn.com/image/fetch/$s_!TAOl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad7b68fb-50dd-40e5-82e4-431d6a1d03bf_1076x578.png)](https://substackcdn.com/image/fetch/$s_!TAOl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad7b68fb-50dd-40e5-82e4-431d6a1d03bf_1076x578.png)

### 2. The Build Phase

[![](https://substackcdn.com/image/fetch/$s_!GE4V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c3f17e0-f22d-482e-ae64-5333857475f4_1268x554.png)](https://substackcdn.com/image/fetch/$s_!GE4V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c3f17e0-f22d-482e-ae64-5333857475f4_1268x554.png)

Once the data is partitioned, Spark identifies the **smaller** of the two datasets within each partition.

* For every partition, Spark takes the smaller side and builds an in-memory hash table.
* The join keys are used as the hash keys in this table, mapping to the actual row data.

### 3. The Probe Phase

[![](https://substackcdn.com/image/fetch/$s_!N68n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa601f677-969a-4ca9-8722-124808f4c794_1436x764.png)](https://substackcdn.com/image/fetch/$s_!N68n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa601f677-969a-4ca9-8722-124808f4c794_1436x764.png)

Once the hash table is ready, Spark begins “probing” it using the larger dataset.

* Spark reads through the larger dataset.
* For each row in the large dataset, it hashes the join key and looks up for a match in the previously built hash table.
* If there is a match, the rows are combined (following the user’s defined logic).

SHJ was removed in [Spark 1.6](https://issues.apache.org/jira/browse/SPARK-11675) and reintroduced in [Spark 2.0](https://issues.apache.org/jira/browse/SPARK-13977). The main reason is that the SHJ requires the “build side” (the smaller table) of every partition to fit entirely in memory so it can build the hash table. If a partition is large and can fit (e.g., due to skew), the executor will throw an OutOfMemoryError (OOM).

In contrast, SMJ can safely spill to disk if the partition is too big to fit in memory. Make the processing more reliable.

In Spark 2.0, SHJ was reintroduced because it is helpful when the build-side partitions fit in memory, allowing sorting to be skipped on both sides. However, to enable SHJ, you must do so explicitly:

* Set the “spark.sql.join.preferSortMergeJoin“ to False
* Increase the “spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold”; this setting indicates the maximum size in bytes per partition that can be allowed to build a hash table locally. By default, this setting is 0, which means Spark will ***always*** skip the ShuffleHashJoin.

Back to our application, we set the “spark.sql.join.preferSortMergeJoin” to False and set the “spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold” to 256MB:

[![](https://substackcdn.com/image/fetch/$s_!V-C-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c803951-4d47-49dc-8933-89a6f0f6ab6a_1288x80.png)](https://substackcdn.com/image/fetch/$s_!V-C-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c803951-4d47-49dc-8933-89a6f0f6ab6a_1288x80.png)

By setting the “spark.sql.files.maxPartitionBytes“ to 128 MB, we can ensure that the input partition sizes are no larger than 128MB, which, of course, is smaller than the ShuffledHashJoinLocalMapThreshold threshold of 256 MB.

Then, we submit the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/join.py
```

After it finishes, visit the physical execution plan on the “SQL/Dataframe“ tab in localhost:18080:

[![](https://substackcdn.com/image/fetch/$s_!XYku!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F767d8d1c-cef8-412a-9edc-39e1ddf94757_1410x1502.png)](https://substackcdn.com/image/fetch/$s_!XYku!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F767d8d1c-cef8-412a-9edc-39e1ddf94757_1410x1502.png)

We now see that ShuffleHashJoin was applied.

In a production Spark application, make sure you know what you’re doing when enabling the SHJ; it’s only efficient when the build-side partitions fit in memory. If they get larger for some reason, your application will likely get an OOM error.

---

# Broadcast Join

For SHJ, there is an interesting optimization called broadcast hash join (BHJ). Suppose one of the tables is small enough to fit entirely into memory; this table is sent to all executors who execute the join.

[![](https://substackcdn.com/image/fetch/$s_!SD2Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a8003c-ff6e-48a3-abb1-3c0850247e09_944x626.png)](https://substackcdn.com/image/fetch/$s_!SD2Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a8003c-ff6e-48a3-abb1-3c0850247e09_944x626.png)

Each executor builds the hash table using this broadcast table and handles the join locally. This avoids the expensive shuffle process.

The BHJ is enabled by default, but with a condition: one of the tables must be smaller than the “spark.sql.autoBroadcastJoinThreshold” (10MB by default)

In our application, let’s generate a much smaller “order“ (~60M) table:

```
cd data && bench tpch gen -s 1
```

Then, we adjust the “spark.sql.autoBroadcastJoinThreshold” to 65MB:

[![](https://substackcdn.com/image/fetch/$s_!n7p2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff86a853c-4794-496f-9fa8-544a55b46ebb_992x36.png)](https://substackcdn.com/image/fetch/$s_!n7p2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff86a853c-4794-496f-9fa8-544a55b46ebb_992x36.png)

Adjust the “order\_path” to point to the smaller “order“ dataset (“sf=10 → “sf=1”)

[![](https://substackcdn.com/image/fetch/$s_!RaIE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8462db6-d4cb-4271-b4e6-9bdbcf53b11b_1362x48.png)](https://substackcdn.com/image/fetch/$s_!RaIE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8462db6-d4cb-4271-b4e6-9bdbcf53b11b_1362x48.png)

Then, we submit the application:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/join.py
```

If it works accordingly, you will feel the application finish much faster.

And the physical plan will look like this:

[![](https://substackcdn.com/image/fetch/$s_!dIGD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11cd4e7a-9e96-45ef-acbe-ce08ef414c17_1152x1490.png)](https://substackcdn.com/image/fetch/$s_!dIGD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11cd4e7a-9e96-45ef-acbe-ce08ef414c17_1152x1490.png)

The entire order input table will be broadcast.

There aren’t any “Exchange“ steps (Shuffles) before the broadcast join

[![](https://substackcdn.com/image/fetch/$s_!K3r-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b9b590c-bd83-4856-899d-3e4002bb2c71_1406x674.png)](https://substackcdn.com/image/fetch/$s_!K3r-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b9b590c-bd83-4856-899d-3e4002bb2c71_1406x674.png)

---

# Bucket Join

In addition to these join strategies, Spark supports the bucket join.

As discussed, in Spark, data is partitioned and shuffled by the join keys. If somehow the data from both tables is physically organized in “buckets” defined by the join keys, Spark can keep the shuffle phase when performing the joins.

Bucketing is a technique that distributes data across multiple buckets based on the hash of a column value.

In other words, a bucket join is when you shuffle the data during write time rather than during join time, which is helpful when you know how the tables are joined and aggregated beforehand. However, this might increase data write time because the engine needs to do more to organize the data into buckets.

[![](https://substackcdn.com/image/fetch/$s_!QgUu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb56c055-f586-4321-9af6-a6d676b8562b_596x768.png)](https://substackcdn.com/image/fetch/$s_!QgUu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb56c055-f586-4321-9af6-a6d676b8562b_596x768.png)

Back to our application, we can stimulate the bucket join by:

* Write the lineitem and order into the bucket tables, using the join key “orderkey”. The logic is in the ./data/write\_bucket.py
* Join these bucketed tables using the orderkey. The logic is in ./data/bucket\_join.py

In the write\_bucket.py, compared to the previous logic, we must add these settings:

[![](https://substackcdn.com/image/fetch/$s_!5RFy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe39a441d-2dc5-448b-99bc-19dfaf7779bd_1186x78.png)](https://substackcdn.com/image/fetch/$s_!5RFy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe39a441d-2dc5-448b-99bc-19dfaf7779bd_1186x78.png)

, and save the lineitem and the orders as tables:

[![](https://substackcdn.com/image/fetch/$s_!efGA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F909a7b3e-3d6c-4765-9550-ffd7433da6ed_832x924.png)](https://substackcdn.com/image/fetch/$s_!efGA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F909a7b3e-3d6c-4765-9550-ffd7433da6ed_832x924.png)

This is because:

* bucketBy() only works with saveAsTable(); it doesn’t work with write.parquet(). Bucketing metadata (which column, how many buckets) needs to be stored somewhere so Spark can use it later (when we join them). That “somewhere” is the Hive metastore.
* We activate the Hive metastore (enableHiveSupport), which is a local [Derby DB](https://db.apache.org/derby/) by default (here is where metadata is physically stored)
* With the “spark.sql.warehouse.dir“, tells Spark where to physically store the table files.
* The saveAsTable(”orders\_bucketed”) — writes the data AND registers the bucketing info in the metastore.

Later, in the bucket\_join.py:

[![](https://substackcdn.com/image/fetch/$s_!zFDC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b766aab-910e-4df1-ab9f-e59fbcf8456a_1426x842.png)](https://substackcdn.com/image/fetch/$s_!zFDC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b766aab-910e-4df1-ab9f-e59fbcf8456a_1426x842.png)

* We also leverage the Hive metastore to read the two tables: “lineitem\_bucketed“ and “order\_bucketed. “
* Then, we join them as we did previously.

By doing this, the executor will see that those tables are bucketed by the join key and will attempt to apply the bucket join.

Before the submission, we must set some configurations, following this [guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html#storage-partition-join):

[![](https://substackcdn.com/image/fetch/$s_!GfsG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F315c172d-527e-4c71-a85b-03a8f5d5c0f0_1290x188.png)](https://substackcdn.com/image/fetch/$s_!GfsG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F315c172d-527e-4c71-a85b-03a8f5d5c0f0_1290x188.png)

After the preparation, we can start writing those bucket tables:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/write_bucket.py
```

Then, we read those tables and join them:

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/spark-warehouse/data/bucket_join.py
```

Visiting the Spark UI history, we can see the plan:

[![](https://substackcdn.com/image/fetch/$s_!VUwt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F021f498d-d556-4357-b6f5-2cbea3b0899b_1376x1172.png)](https://substackcdn.com/image/fetch/$s_!VUwt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F021f498d-d556-4357-b6f5-2cbea3b0899b_1376x1172.png)

There aren’t the exchange steps (shuffle) here before the join here.

[![](https://substackcdn.com/image/fetch/$s_!nuD6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a5501c1-9c43-4b22-a02e-85fd81506b01_730x48.png)](https://substackcdn.com/image/fetch/$s_!nuD6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a5501c1-9c43-4b22-a02e-85fd81506b01_730x48.png)

Because we also aggregate on the orderkey (which is the join key and the key for bucketing), we won’t see shuffle later in the aggregation. The data was already “shuffled“ when we wrote these tables.

[![](https://substackcdn.com/image/fetch/$s_!TF3F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5622e4b-ea45-412f-a999-66b8df481400_1386x696.png)](https://substackcdn.com/image/fetch/$s_!TF3F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5622e4b-ea45-412f-a999-66b8df481400_1386x696.png)

---

# Join Strategy Hints

In addition to tuning the application’s settings, the user can “hint” Spark JOIN strategies. A hint can be provided for both tables participating in the join.

[![](https://substackcdn.com/image/fetch/$s_!YVxD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2c514fe-195f-4864-9062-a0e861881ec0_1200x482.png)](https://substackcdn.com/image/fetch/$s_!YVxD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2c514fe-195f-4864-9062-a0e861881ec0_1200x482.png)

Example of Spark join hints. Screenshot from the [Spark SQL Guide - Hints.](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html)

Before Spark 3.0, users could only hint at the `BROADCAST` (broadcast join). Since version 3.0, Spark allows hints for other strategies.

When different join strategy hints are specified on both sides of a join, Spark prioritizes hints in the following order:

* `BROADCAST`
* `MERGE` (sort-merge join)
* `SHUFFLE_HASH` (hash join)

For the hash join type (`BROADCAST` and `SHUFFLE_HASH` hint), Spark will choose the table to build the hash table based on the tables’ sizes.

You can give the hint; however, the optimizer makes the decision at the end of the day. Your hint is not guaranteed to be picked, because a strategy may not support all logical join types (e.g., LEFT, RIGHT, INNER, …).

---

# Outro

In this article, we set up a small Spark application to validate Spark's theories, from sort-merge join, shuffle-hash join, and broadcast join to bucket join. For each strategy, I note the pros and cons and the conditions/settings that enable it. We also explore the true physical plan of each strategy via the Spark UI.

Thank you for reading this far.

See you in my next articles.
