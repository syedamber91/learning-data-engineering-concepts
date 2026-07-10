---
title: "A Closer Look Into Databricks's Photon Engine"
channel: vutr
author: "Vu Trinh"
published: 2024-04-13
url: https://vutr.substack.com/p/a-closer-look-into-databrickss-photon
paid: false
topics: ["Apache Spark", "Snowflake", "Databricks", "BigQuery", "Lakehouse", "Batch Processing"]
tags: [photon, https, spark, memory, auto, column]
---

# A Closer Look Into Databricks's Photon Engine

*Vectorization*

> Source: [Open post](https://vutr.substack.com/p/a-closer-look-into-databrickss-photon)

## Topics

[[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[batch-processing|Batch Processing]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=143028483)

[![](https://substackcdn.com/image/fetch/$s_!qBRL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b0c8312-3ac2-4fa7-9d0d-d893be1b3031_1402x1002.png)](https://substackcdn.com/image/fetch/$s_!qBRL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b0c8312-3ac2-4fa7-9d0d-d893be1b3031_1402x1002.png)

Image created by the author.

---

## Table of contents:

* Vectorized Execution In Photon
* Integration with Databricks runtime

---

## Intro

Last week, [we learned why Databricks built the Photon Engine](https://open.substack.com/pub/vutr/p/why-did-databricks-build-the-photon?r=2rj6sg&utm_campaign=post&utm_medium=web) for the Lakehouse and had a general view of the engine. This week, we will dive deeper into the Photon internals and design.

> *This is part 2 of my note after reading the paper [Photon: A Fast Query Engine for Lakehouse Systems](https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf). You can read the part 1 [here](https://vutr.substack.com/p/why-did-databricks-build-the-photon?r=2rj6sg&utm_campaign=post&utm_medium=web&triedRedirect=true).*

---

## Vectorized Execution In Photon

In this section, we will go through the implementation of the Photon engine.

### Batched Columnar Data Layout

[![](https://substackcdn.com/image/fetch/$s_!av-g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02591b21-bab1-4010-bfac-1827ca9b80f6_689x846.png)](https://substackcdn.com/image/fetch/$s_!av-g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02591b21-bab1-4010-bfac-1827ca9b80f6_689x846.png)

Image created by the author.

Photon represents data in a columnar format; it stores column value contiguously in memory. Groups of columns are divided and processed in batches to limit memory usage and achieve cache locality. The data unit in Photon is a single column that holds a batch of values called a *column vector*. Besides data values, column vectors contain a byte vector for NULL information. A column batch is a set of column vectors and represents rows.

[![](https://substackcdn.com/image/fetch/$s_!YCCx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ebe9390-f61b-4ef8-9aa3-9efde7284a53_1454x590.png)](https://substackcdn.com/image/fetch/$s_!YCCx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ebe9390-f61b-4ef8-9aa3-9efde7284a53_1454x590.png)

A column batch in Photon. Besides data values, column vectors contain a byte vector for NULL information. A position list includes the indices of the rows in the batch that are “active. “ Figure 2. Photon: A Fast Query Engine for Lakehouse Systems (2022). [Source](https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf)

A batch contains a position list data structure, which includes the indices of the rows in the batch that are “active. “ The active rows are rows that have not been filtered out or are valid for the expression. Accessing a row in the column batch requires going through the position list. Photon processes data in operators at the granularity of column batches. Each operator receives a column batch from its child and outputs one or more batches to their parent operators.

### Vectorized Execution Kernels

[![](https://substackcdn.com/image/fetch/$s_!uWnm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89581daf-c25a-4e9f-9d29-577458faa197_694x463.png)](https://substackcdn.com/image/fetch/$s_!uWnm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89581daf-c25a-4e9f-9d29-577458faa197_694x463.png)

Image created by the author. The pseudo-code used in this image is only for illustration purposes; it does not reflect the actual implementation.

Photon’s execution is based on the concept of execution kernels, which are functions that execute efficient loops over one or more batches of data. This idea was first proposed in the [MonetDB/X100 system](https://www.cidrdb.org/cidr2005/papers/P19.pdf). Databricks implements most of the data operations as kernels. Most of the time, they rely on the compiler to auto-vectorize the kernel. Kernels can be specialized according to input types using C++ templates. As said in the above section, Photon calls operators and expressions at the granularity of vectors. Each kernel accepts vectors and the column batch position list as input and produces output vectors.

### Filters and Conditionals

Databricks implements filter operation in Photon by modifying the position list of the column batch. The filter expression receives the column vectors and outputs the position list, which marks the position “active“ if the data satisfies the filter expression.

### Vectorized Hash Table

> *For join operation*

Photon’s hash table is optimized for vectorized access. Here are three steps of the hash table lookup process; each step benefits from vectorized execution:

* The hashing kernel applies the hash function on a batch of keys.
* The probe kernel uses the hash values to load pointers to hash table entries
* The entries in the hash table are compared against the lookup keys column-by-column, and a position list is output for non-matching rows.

### Vector Memory Management

Photon prevents OS-level memory allocations using an internal buffer pool for transient column batches. This pool allocates memory and caches allocations with the most frequently used mechanism, keeping hot memory in use for repeated allocations.

Data with dynamic size (e.g., buffers for strings) is managed using a dedicated append-only pool. The pool frees the memory before processing each new batch. A global tracker tracks the memory this pool uses so the engine can adjust the batch size if the data’s size is too large.

Photon tracks large allocations that live beyond any single batch processing (e.g., for aggregations) by the external memory manager. Databricks have found fine-grained memory allocation valuable because, unlike the Spark SQL engine, it can efficiently handle extensive input records in the Lakehouse workload.

### Adaptive Execution

> *You have to process data you have never seen before, right?*

Photon engines support batch-level adaptivity, which allows Photon to build metadata for the processing batch at runtime and use this metadata to optimize query execution. Photon’s kernels can adapt to at least two variables: NULLs appearance or inactive rows appearance in batch. The batch without NULLs helps Photon to remove [branching](https://en.wikipedia.org/wiki/Branch_(computer_science)), which improves performance. Similarly, Photon can avoid the extra position list lookup step if a batch has no inactive rows.

Photon also specializes in several other kernels on a case-by-case basis:

* *Many string expressions can be executed with an optimized code path if the strings are all ASCII-encoded.*
* *Photon can selectively compact sparse batches at runtime to improve performance.*
* *Adaptive shuffle encoding by finding patterns in user data at runtime.*

## Integration with Databricks runtime

> Photon shares resources with other workloads that execute over DBR and the Lakehouse storage architecture. It also coexists with the old Spark SQL engine for queries with operators that are not yet supported in the new execution engine.

### Converting Spark Plans to Photon Plans

Photon converts a physical plan that represents execution using the legacy engine into one that represents execution with Photon to integrate with the legacy Spark SQL-based engine. The [Spark’s Catalyst optimizer](https://www.databricks.com/glossary/catalyst-optimizer) is responsible for this process. The optimizer’s rule is *“a list of pattern-matching statements and corresponding substitutions applied to a query plan.”*

[![](https://substackcdn.com/image/fetch/$s_!bY1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb15050a7-5ba7-47b8-a47c-825a98a111ab_864x492.png)](https://substackcdn.com/image/fetch/$s_!bY1K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb15050a7-5ba7-47b8-a47c-825a98a111ab_864x492.png)

Image created by the author.

The rule proceeds as follows:

* It starts at the bottom with the scan nodes and maps the supported legacy node to a Photon node.
* When a node is not supported by Photon, a transition node is inserted to convert the columnar Photon format to the Spark SQL engine’s row-wise format.
* They don’t transform middle nodes to avoid regressions from too many column-to-row pivots.
* They add an adapter node between the file scan and the first Photon node; this maps the legacy scan input to Photon columnar batches.

### Executing Photon Plans

After forming the physical plan, DBR launches tasks to execute the plan’s stages. With the Photon task, the execution node first serializes the Photon part of the plan into a [Protobuf](https://protobuf.dev/) message. This message is passed via the [Java Native Interface (JNI)](https://en.wikipedia.org/wiki/Java_Native_Interface#:~:text=Java%20Native%20Interface%20(JNI%2C%20ti%E1%BA%BFng,C%2B%2B%20v%C3%A0%20h%E1%BB%A3p%20ng%E1%BB%AF.) to the Photon C++ library, deserializing the Protobuf and converting it into a Photon-internal plan. The plan is quite the same as the DBR’s; they implement each operator using a node with a `HasNext()`/`GetNext()` interface. Photon runs in the JVM process and communicates with the Java runtime using JNI. If the plans end with a data exchange, Photon writes a shuffle file that follows Spark’s shuffle protocol and passes the shuffle’s metadata to Spark. Spark then performs the shuffle using this metadata, and a new Photon task reads the relevant partitions from the shuffle in a new stage.

[![](https://substackcdn.com/image/fetch/$s_!TEcC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3a68b9-c297-42a5-a7cf-c191537dd2fe_831x369.png)](https://substackcdn.com/image/fetch/$s_!TEcC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3a68b9-c297-42a5-a7cf-c191537dd2fe_831x369.png)

Image created by the author.

The leaf node in a Photon plan is always an “adapter.” It takes columnar data produced by Spark’s scan node and passes the data’s pointers to Photon. Within Photon, the adapter node’s `GetNext()` method makes a JNI call that passes the pointers list to the JVM. Two pointers per column are passed: one for the column values and one for the NULL values. On the Java side, the scan node directly produces columnar data stored in [off-heap memory](https://docs.oracle.com/en/java/javase/21/core/heap-and-heap-memory.html) via the open-source [OffHeapColumnVector](https://github.com/apache/spark/blob/master/sql/core/src/main/java/org/apache/spark/sql/execution/vectorized/OffHeapColumnVector.java) class in Spark. Like Photon, this class stores values as primitives in off-heap memory and stores NULLs as an off-heap byte array. Thus, the adapter node only needs to take the pointers provided by Photon and point them to the off-heap column vector memory without copying.

The last node in a Photon plan is a “transition” node. In contrast with the adapter, the transition node must convert columnar data to row data so the legacy Spark SQL engine can process it.

Databricks realizes that the more they change the query plan to Photon, the more pivots (column-to-row or row-to-column) they need to process. At the time of the paper’s writing, they approached Photon’s plan converting process conservatively. They wanted to understand more about the tradeoff of Photon’s performance boost vs. the slowdown caused by adding pivots.

### Unified Memory Management

Because of sharing the same cluster, Photon and Spark must have a consistent memory and disk usage view. Thus, Photon hooks into Apache Spark’s memory manager. Databricks separates the concept of memory reservations from allocations in Photon:

[![](https://substackcdn.com/image/fetch/$s_!MSAI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1368781f-1d76-42a2-9170-59112e615e82_862x589.png)](https://substackcdn.com/image/fetch/$s_!MSAI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1368781f-1d76-42a2-9170-59112e615e82_862x589.png)

Image created by the author.

* A memory reservation asks for memory from Spark’s [unified memory manager.](https://community.cloudera.com/t5/Community-Articles/Spark-Memory-Management/ta-p/317794) This can cause a spill like all requests to the memory manager. The spill happens when Spark asks some consumers to release memory to satisfy a new request. Photon uses memory consumer API to make the reservation, so Spark can ask Photon to spill data. Similarly, Photon can make reservations that cause other Spark operators to spill. This differs from other database engines, where operators are given a fixed memory budget and can only “self-spill.” Spilling is dynamic because Databricks often do not know how much data an operator will consume. They use the same spill-determined policy as Spark open-source. If they need to spill N bytes of memory, they sort the consumers from least to most allocated memory and spill the first consumer with at least 𝑁 bytes. They want to minimize the number of spills and avoid spilling more data than needed.
* Photon can allocate memory safely without spilling after making the memory reservation. Photon handles the allocation locally; Spark is only responsible for the memory that Photon requests. With spilling operators like hash join, the processing is split into two phases: a reservation phase where memory is acquired for the new input batch and spilling is handled, and an allocation phase where transient data can be produced since no spilling can occur.

### Managing On-heap vs. Off-heap memory

DBR and Apache Spark support requesting off-heap and on-heap memory from the memory manager. To manage off-heap memory, the Spark cluster is configured with a static “off-heap size” per node, and the memory manager is responsible for this allocation. If memory consumers overuse the allocated memory, it can lead to [out-of-memory (OOM)](https://en.wikipedia.org/wiki/Out_of_memory) errors.

The JVM performs garbage collection when it detects high on-heap memory usage. However, most memory usage with Photon is off-heap, so garbage collection rarely happens. This can cause considerable problems if Photon relies on on-heap memory for parts of the query. Databricks adds a listener that cleans up the Photon-specific state after the query ends: this ties the Photon state to the lifetime of a query instead of a GC generation.

### Interaction with Other SQL Features

* Photon participates in adaptive query execution, in which runtime statistics are used to re-partition and re-plan a query at runtime.
* Photon’s operators implement the interfaces required to export statistics for such decisions (e.g., the size of shuffle files).
* Photon can use optimizations, such as shuffle/exchange/subquery reuse and dynamic file pruning, to enable efficient data skipping.
* Photon supports integration with Spark’s metrics system and can provide live metrics appearing in the Spark UI during execution.

### Ensuring Semantics Consistency

Databricks also needed to deal with consistency problems, ensuring that Photon’s behavior was identical to Apache Spark’s. This is because the same query expression can run in either Photon or Spark, depending on whether some other part of the query can execute in Photon. Databricks uses three kinds of testing to check results against Spark:

[![](https://substackcdn.com/image/fetch/$s_!0zcD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4eabbf8-281f-4552-a751-65651055d299_877x485.png)](https://substackcdn.com/image/fetch/$s_!0zcD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4eabbf8-281f-4552-a751-65651055d299_877x485.png)

Image created by the author.

* **Unit tests**: They use two kinds of unit tests. They have built a unit testing framework for SQL expressions in native code, which lets the testers input and output values for any expression in a table. The framework then loads the table into column vectors, evaluates the expression on all the available specializations (e.g., no NULLs, with NULLs, etc.), and compares the result to the expected output. They also leverage Spark’s existing open-source expression unit tests. These tests hook in with the function registry to check if the test case is supported in Photon. If yes, they compile a query for the unit test, execute it in Spark and Photon, and finally compare the results.
* **End-to-end tests**: These test query operators by submitting a query against Spark and Photon and comparing the results. They have a unique set of tests that run only when Photon is enabled (e.g., to test out-of-memory behavior or certain Photon-specific plan transformations). They also allow Photon to use the full suite of Spark SQL tests for additional coverage.
* **Fuzz tests:** They test random queries against Spark and Photon. Their testing consists of a fully general random data and query generator.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=143028483)

---

## Experimental Evaluation

> *We will see some of Photon’s evaluations from Databricks in this section.*

### Which Queries Will Photon Benefit?

Photon improves the performance of queries that spend most of their execution time on CPU-heavy operations such as joins, aggregations, and SQL expression evaluation. Queries with these operations are most impacted by Photon’s differences over DBR: native code, columnar, vectorized execution, and runtime adaptivity. Photon can also provide speedups on other operators, such as data exchanges and writes, by either speeding up the in-memory execution of these operators or by using a better encoding format when transferring data over the network. Here are some benchmarks from Databricks:

* **Hash Joins:** Databricks compared Spark’s sort-merge join and hash join to Photon’s hash join. The benchmark was carried out using two artificial tables with 1GB of integer data each, which performed an inner equal join over the integer columns. They observed that Photon’s vectorized hash table outperforms DBR 3.5 times, primarily due to better memory hierarchy utilization by parallelizing loads.
* **Aggregations:** Databricks ran the benchmark on grouping aggregation on a string column on various integer groups with the [CollectList](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.collect_list.html) aggregation function. DBR implements this function using Scala collections to perform the aggregation and does not support code generation in large part. Photon uses a custom vectorized implementation of the expression. They observed that Photon outperforms DBR on this microbenchmark by up to 5.7×. Like the join, Photon benefits from a vectorized hash table while determining the aggregate groups.
* **Parquet Writes:** Photon supports writing Parquet/Delta files. Users use this operation to create new tables or append to existing ones. DBR performs this operation using the open-source Java-based [Parquet-MR](https://github.com/apache/parquet-mr) library. Databricks ran the benchmark that writes a 200M row Parquet table with six columns (integers, longs, dates, timestamps, strings, and booleans) to compare Photon and DBR Parquet write performance. Photon outperforms DBR by 2× end-to-end, with the main improvement coming from the column encoding.

### Overhead of JVM Transitions

Photon uses the JNI to communicate with Spark and transition operators to pass data between Spark and Photon. Databricks ran a query that reads a single integer column from an in-memory table to measure the overhead. They observed that 0.06% of the execution time was spent in JNI-internal methods and 0.2% in the adapter node feeding into Photon. The rest of the profile was the same for Photon and DBR: about 95% of the time was spent serializing rows into Scala objects, and the remaining time went into various Spark iterators. They also found no additional overhead from the column-to-row operation since Spark must apply this operation, too. In conclusion, the JNI or the transition nodes did not cause significant overhead, primarily when these calls were handled in batch.

---

## Outro

That’s all for this week. Databricks’s Photon is an interesting case when it’s not a standalone database system like BigQuery, Redshift, or Snowflake. In turn, it acts like the enhancement component of the existing SparkSQL engine when dealing with the Lakehouse workload.

I hope my works bring some value. See you next blog.

> *Speaking of which, I will write a blog on why we need the lakehouse paradigm, so stay tuned.*

---

***References**:*

*[1] Databricks, [Photon: A Fast Query Engine for Lakehouse Systems](https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf) (2022).*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/a-closer-look-into-databrickss-photon/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
