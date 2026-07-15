---
title: "8.2 minutes, and you will understand how most data systems execute joins."
channel: vutr
author: "Vu Trinh"
published: 2025-06-17
url: https://vutr.substack.com/p/fundamentals-that-help-you-understand
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "BigQuery"]
tags: [join, https, table, auto, hash, substackcdn]
---

# 8.2 minutes, and you will understand how most data systems execute joins.

*From Spark, Snowflake, to BigQuery, here is how joins are built on*

> Source: [Open post](https://vutr.substack.com/p/fundamentals-that-help-you-understand)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=165857165)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!8rsC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3344d6ef-7f67-442a-b71d-a38379433d95_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!8rsC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3344d6ef-7f67-442a-b71d-a38379433d95_2000x1429.png)

---

## Intro

If you need to write SQL for the paycheck (:D), you might be familiar with the join operations. From the left join to the full outer join, data is normalized into separate tables to streamline the ingest, store, and manage process. When insight needs to be gathered from multiple tables, we join them.

The from clause, the join kind (e.g., LEFT JOIN), the join conditions, and 10 minutes later, the result is returned to us.

The beauty of SQL is that you don’t need to care much about the physical implementation of how SQL is executed. The optimizer will do it.

However, understanding how things work behind the scenes will help us, especially data engineers, to debug and optimize our data workload more efficiently.

And, I think understanding joins is worth our time, given that we encounter them almost daily.

This article will outline the fundamental approach most systems implement for join operations. Then, we will see how these approaches are optimized for OLAP systems, which typically require executing the join on a large amount of data from both tables.

> ***Note:** This article focuses on the physical implementation of the join operations, so you won’t find the details of logical join operations like LEFT JOIN or RIGHT JOIN. I believe there are tons of excellent resources on the internet that elaborate on this topic.*

---

## Before we move on

This article will only cover the equi-join, which combines rows from two tables, using the “=“ operator to compare column values.

I will present the table from the left of the join as the left table and the table from the right as the right table, as I found it intuitive. When reading other resources, you might find that the terms outer table and inner table are widely used.

---

## Nested loop join

The basic idea of nested loop join (NLJ) is to have two loops.

The first loop will loop through every record in the left table. For each record, we loop through the right table to compare using the join condition. If the condition is met, the combined row is produced as part of the join result.

[![](https://substackcdn.com/image/fetch/$s_!esdH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd992c957-5f2d-4ea4-afcf-5d1da6de4a2b_792x496.png)](https://substackcdn.com/image/fetch/$s_!esdH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd992c957-5f2d-4ea4-afcf-5d1da6de4a2b_792x496.png)

The advantage of NLJ is its simplicity and ability to be used without requiring auxiliary data structures like hash tables or data to be sorted.

However, the naive NLJ can be inefficient due to scanning the right table repeatedly.

The Block-Nested Loop (BNL) join is an enhancement that aims to reduce the I/O cost of the naive approach. Instead of processing the left table row by row, BNL reads a block of the left table into a memory buffer.

[![](https://substackcdn.com/image/fetch/$s_!EdSV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa48c3ead-f052-40ff-aefd-a37d69185b61_906x604.png)](https://substackcdn.com/image/fetch/$s_!EdSV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa48c3ead-f052-40ff-aefd-a37d69185b61_906x604.png)

> *In the context of databases, a block typically refers to the smallest unit of data that a database management system (DBMS) reads or writes from storage.*

Then, the entire right table is scanned once for this left table’s block. All rows within the buffered block are compared against each row of the right table, significantly reducing the I/Os.

Besides the BNL join, we can use an index to optimize performance. For every record from the left, instead of sequentially scanning the whole right table, the system can check the index to find the location of the matched rows in the right table.

[![](https://substackcdn.com/image/fetch/$s_!eFug!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F546f33da-c124-42ab-8ce2-dc3583bd52b1_1058x618.png)](https://substackcdn.com/image/fetch/$s_!eFug!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F546f33da-c124-42ab-8ce2-dc3583bd52b1_1058x618.png)

### Key takeaways

NLJ can perform reasonably well when the left table is small, which keeps the number of repeat scans of the right table small. In addition, if the right table has an index on the join column(s), the second loop can perform an index lookup instead of a full table scan for each left table row, drastically improving performance.

---

## Sort-merge join

The next approach we will explore is the sort-merge join (SMJ)

With SMJ, the system must carry out two phases.

[![](https://substackcdn.com/image/fetch/$s_!uIkv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13bb1551-56e5-403d-885a-11f9e5a575da_1076x586.png)](https://substackcdn.com/image/fetch/$s_!uIkv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13bb1551-56e5-403d-885a-11f9e5a575da_1076x586.png)

* In the first phase, the system sorts the two tables based on the join columns.
* In the second phase, the system walks through the tables with associated pointers:

  + If the join conditions match, the rows are combined. If duplicates exist in one or both tables for the current join key value, all combinations of matching rows must be generated. This might involve moving the pointer from one table backward while moving the pointer from another forward.
  + If the join values from the left are less than those of the right, the left’s pointer is moved forward.
  + If the join values from the right are less than those of the left, the right’s pointer is moved forward.
  + This process continues until one or both tables are exhausted.

Compared to the NLJ, the system must perform extra sort operations on the two tables. SMJ is particularly efficient when one or both input tables are already sorted on the join columns, or if they have clustered indexes on these attributes, as this can eliminate or reduce the cost of the sort phase.

> *With a clustered index, the database sorts and stores the rows physically using the values from the index columns.*

It is also convenient if the query output must be sorted by the join key ( `ORDER BY` clause on the join key), as the merge phase naturally produces sorted output.

---

## Hash join

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=165857165)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

The following algorithm is the hash join. It works based on the simple idea that if the rows from two tables match, they have the same join column values, thus having the same result after applying the hash function on these column values.

The classic in-memory Hash Join algorithm consists of two phases:

[![](https://substackcdn.com/image/fetch/$s_!GCa8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe6137ff-a66a-4552-b6fc-ed2216315ada_1370x488.png)](https://substackcdn.com/image/fetch/$s_!GCa8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe6137ff-a66a-4552-b6fc-ed2216315ada_1370x488.png)

1. **Build Phase:** The database system will construct an in-memory hash table using the smaller table. The goal is to fit the entire hash table in memory. Each row’s join column(s) are hashed to determine its bucket.
2. **Probe Phase:** After the hash table is built, the system scans the second table. For each row in this table, its join column(s) are hashed using the same hash function applied during the build phase. This hash value is then used to look up matching rows in the hash table. If a match (or matches, in case of non-unique join keys) is found, the corresponding rows are combined and returned.

> *From now on, I will use the build table to refer to the table used to build the hash table, and the probe table to refer to the one scanned and used to look up the hash table.*

Hash Join is effective for equi-joins, especially when one of the tables (the build table) is small enough to fit into memory. It won’t require data to be sorted beforehand or a pre-built index to optimize the performance.

However, it requires building an in-memory hash table during runtime. If this hash table exceeds available memory, the classic Hash Join algorithm's performance degrades significantly as it may spill to disk. Imagine the hash table has two parts: part A, which fits in memory, and part B, which spills to the disk.

[![](https://substackcdn.com/image/fetch/$s_!_ysI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26184009-2bc5-43e1-abe1-2c22c0862815_484x392.png)](https://substackcdn.com/image/fetch/$s_!_ysI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26184009-2bc5-43e1-abe1-2c22c0862815_484x392.png)

When looping through the probe table, for each row, after checking for matching rows from part A, the system needs to check part B on the disk. This requires loading part B into memory and storing part A to disk. The loading of data back and forth from disks like this degrades the performance of the hash join.

This is where the [Grace Hash Join (named after the Grace database machine from Tokyo in the 1980s)](https://youtu.be/MFazkaZKs1s?list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&t=3323) comes to rescue. This algorithm can sometimes be called a partitioned hash join. This variant is employed when the hash table does not fit into available memory:

* **Partitioning Phase:** Both tables are scanned, the same hash function is applied to their join columns, and rows are distributed into buckets on disk. The number of buckets is chosen so that each bucket of the build table (ideally, the probe table) is small enough to be processed in memory during the next phase. If any partition bucket of the hash table is too large for memory, it can be recursively partitioned using a different hash function until all resulting sub-buckets fit in memory.

  [![](https://substackcdn.com/image/fetch/$s_!j9IM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe21980cd-b48e-4577-b506-231223d8b46a_1338x574.png)](https://substackcdn.com/image/fetch/$s_!j9IM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe21980cd-b48e-4577-b506-231223d8b46a_1338x574.png)
* **Probing Phase (Join Phase):** For each pair of corresponding buckets (build bucket i/probe bucket i), the system brings these buckets to memory and creates a hash table from the build bucket i, and a classic in-memory hash-join is executed between this hash table and the associated probe bucket.

  [![](https://substackcdn.com/image/fetch/$s_!6vuB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a15c898-d4ba-449c-abe2-816471726842_586x372.png)](https://substackcdn.com/image/fetch/$s_!6vuB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a15c898-d4ba-449c-abe2-816471726842_586x372.png)

Although this approach requires two rounds of hashing, it limits the number of disk I/Os as each bucket will be brought into memory once to execute the hash join.

---

## Joins in OLAP systems

The algorithms listed above are the three most popular approaches to implementing a join operation for most databases.

> ***Note**: There are undoubtedly other algorithms than the three above. However, I believe these are the most popular and the fundamentals for most algorithms.*

During the planning phase, the query optimizer will use statistics from both tables to identify the most efficient join algorithm. [The metric for this purpose is the number of I/O operations to execute the join](https://youtu.be/MFazkaZKs1s?list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&t=995) for each algorithm.

Although the three approaches are reasonable to apply to the OLTP systems (e.g., PostgreSQL [supports all three above](https://www.timescale.com/learn/postgresql-join-type-theory)), the nested loop join might not be suitable for the OLAP workload, given that the performance of this algorithm relies on the left table’s size (to reduce the number of right table scans) and the index (to eliminate the right table sequential scans). OLAP systems usually deal with large tables on both sides and don’t maintain an index for point look-up, as the OLTP system usually does.

So, two algorithms are left: the sort-merge join and the hash join.

What OLAP systems try to do differently is execute the join algorithm simultaneously to adapt to the nature of their typical workload: processing large tables that need the help of more than one machine.

[![](https://substackcdn.com/image/fetch/$s_!zyF3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2597f198-db56-4145-822d-568e50553b4b_782x632.png)](https://substackcdn.com/image/fetch/$s_!zyF3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2597f198-db56-4145-822d-568e50553b4b_782x632.png)

Although the detailed implementation varies on systems, the high-level idea is quite the same: the data from the two tables is divided into smaller chunks so multiple workers can execute the join simultaneously. Inside each worker, a typical hash-join or sort-merge join is executed.

The process of dividing the data into smaller chunks looks quite similar to the Grace Hash Join described above. The system applies the same hash function to both tables’ join columns to split them into buckets, which are then distributed to workers. Thus, the distribution of the join keys is crucial; if a join key has a dominant number of rows, it can put much pressure on a single worker. In this case, most of the system will try another round of hashing to re-partition this giant partition and re-distribute it to the workers.

[![](https://substackcdn.com/image/fetch/$s_!SS33!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ed535e4-4ee2-4a62-9768-882ab523f6c3_676x406.png)](https://substackcdn.com/image/fetch/$s_!SS33!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ed535e4-4ee2-4a62-9768-882ab523f6c3_676x406.png)

### A note on hash join

Compared to the sort-merge join, I personally found that hash-join has been more widely used for the OLAP system. (Feel free to correct me.)

Snowflake uses [hash join for most cases](https://medium.com/snowflake/the-basics-of-joins-in-snowflake-3da7736075f9).

BigQuery [only supports hash joins](https://youtu.be/VOZax1tbvxw?list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&t=1221).

Spark supports [sort-merge join](https://www.waitingforcode.com/apache-spark-sql/sort-merge-join-spark-sql/read) and [hash join](https://www.waitingforcode.com/apache-spark-sql/shuffle-join-spark-sql/read).

For the hash join, most systems employ an interesting optimization if one of the tables is small enough to fit entirely into memory. In this scenario, this table is broadcast to all workers who execute the join. Each worker builds the hash table using this broadcast table and handles the join locally with the assigned partition of the probe table.

[![](https://substackcdn.com/image/fetch/$s_!kwYc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82709508-13d6-409e-8b08-4fab72f46a2b_1408x918.png)](https://substackcdn.com/image/fetch/$s_!kwYc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82709508-13d6-409e-8b08-4fab72f46a2b_1408x918.png)

Unlike a typical distributed hash join, when data from both the build and probe tables needs to be exchanged over the network, a broadcast join only moves the small build table around.

You can check how to leverage broadcast hash join in your favorite system.

[Spark lets you configure the threshold of the build table to detect a broadcast join and hint at the join strategy you want.](https://spark.apache.org/docs/latest/sql-performance-tuning.html#automatically-broadcasting-joins)

BigQuery can dynamically switch to broadcast join at runtime based on the size of your build table. However, users can’t configure the threshold like Spark does. [It only suggests you order your tables in the join statement to hint to the optimizer.](https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns)

> *In the case of broadcast vs. hash join, Dremel (BigQuery’s query engine) will start with the hash join by shuffling data on both sides, but if one side finishes fast and is below a broadcast data size threshold, Dremel will cancel the second shuffle and execute a broadcast join instead. — [Dremel: A Decade of Interactive SQL Analysis at Web Scale](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)*

Snowflake also [detects the opportunity for the broadcast join automatically](https://www.snowflake.com/en/engineering-blog/query-acceleration-smarter-join-decisions/).

---

## Outro

Few, that’s all for this article.

We first explore the three popular join algorithms: nested loop join, sort-merge join, and hash join. Then, we stand on the moon and see how the OLAP system handles the join operation.

I hope this article will give you enough insight to understand what you're looking at the next time you need to debug a slow query that joins a bunch of tables.

Now, it’s time to say goodbye.

Thank you for your support. That means the world to me.

---

## Reference

*[1] Andy Pavlo, [Join Algorithms: Hash, Sort-Merge, Nested Loop Joins (CMU Intro to Database Systems)](https://www.youtube.com/watch?v=MFazkaZKs1s&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=13)*

*[2] Andy Pavlo, [Parallel Hash Join Algorithms (CMU Advanced Database Systems)](https://www.youtube.com/watch?v=S40K8iGa8Ek&list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ&index=10)*

*[3] Timescale, [PostgreSQL Join Type Theory](https://www.timescale.com/learn/postgresql-join-type-theory)*
