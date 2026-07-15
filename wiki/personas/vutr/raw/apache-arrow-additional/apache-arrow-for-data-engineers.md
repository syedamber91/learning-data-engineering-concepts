---
title: "Apache Arrow For Data Engineers"
channel: vutr
author: "Vu Trinh"
published: 2025-08-05
url: https://vutr.substack.com/p/apache-arrow-for-data-engineers
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "BigQuery"]
tags: [https, auto, arrow, substackcdn, image, fetch]
---

# Apache Arrow For Data Engineers

*Everything you need to know, from what it is, its motivation, and how it provides value?*

> Source: [Open post](https://vutr.substack.com/p/apache-arrow-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=169655500)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!KBQ0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5e11054-b4e4-4b64-9a3c-8ef270206d44_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!KBQ0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff5e11054-b4e4-4b64-9a3c-8ef270206d44_2000x1428.png)

---

## Intro

Polars, Pandas, Spark, Snowflake, BigQuery, DuckDB, DataFusion, Clickhouse.

Besides the fact that all of these are solutions for handling analytics data, do you know what one thing they have in common?

They all leverage Apache Arrow.

From improving data transfer (BigQuery, Snowflake, Clickhouse…) to in-memory data representation (Pandas, Polars, DataFusion)

Fairly speaking, the data engineering field will be different if we don’t have Arrow.

This article will delve into Apache Arrow, exploring what it is, its motivation, how it organizes data, and finally, how it can help us.

---

## Overview

The Apache Arrow format project began in February 2016, focusing on columnar in-memory analytics workloads. Unlike Parquet or CSV, which specify how data is organized on disk, Arrow focuses on how data is organized in memory.

[![](https://substackcdn.com/image/fetch/$s_!uG0a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff35ace1c-12a3-46e2-8367-4d9afcedb8c3_964x372.png)](https://substackcdn.com/image/fetch/$s_!uG0a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff35ace1c-12a3-46e2-8367-4d9afcedb8c3_964x372.png)

The creators try to build Arrow as a community standard in-memory format for workload analytics. These foundations attract many contributors from projects such as Pandas, Spark, Cassandra, Apache Calcite, Dremio, and Ibis.

Beyond a standard for organizing data in memory, the [Apache Arrow project](https://arrow.apache.org/) offers libraries that implement the format in various languages, including C++, Java, Python, Rust, Go, C#, and R, enabling developers to create, manipulate, and share Arrow data natively.

## How does it organize the data for a single column?

### Terminology

To understand how Arrow organizes data, let’s check out some terminology in the Arrow:

* An **array** is a logical sequence of values with a defined length, all sharing the same type. Array is immutable.
* A **chunked array** is a list of arrays.
* A **slot** is a single logical value within an array.
* The **Buffer** is a sequential virtual address space with a fixed length, where any byte can be accessed via a pointer offset within the region’s length. You can think of a buffer as a physical container for the array.

### Inside an array

Arrow represents a single column of values using the array object, which is defined by a few pieces of metadata and data:

[![](https://substackcdn.com/image/fetch/$s_!FaJS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1041191d-6315-4c42-b552-1908ba8f9a1d_642x246.png)](https://substackcdn.com/image/fetch/$s_!FaJS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1041191d-6315-4c42-b552-1908ba8f9a1d_642x246.png)

* The array’s length: A 64-bit signed integer, and the null count
* The null count: Also a 64-bit signed integer.
* The data type
* Buffers:

  + **Validity bitmap**: Almost all array types have a validity bitmap memory buffer, which encodes the null information for each array's slot value.
  + **Offset Buffer**: Some array types, such as Variable-size Binary Layout, have offset buffers to locate the start position of each slot in the data buffer.
  + **Value Buffer**: The buffers containthearray’s data
  + There are more buffers for some complex types, such as Size Buffer ([ListView Layout](https://arrow.apache.org/docs/format/Columnar.html#listview-layout)) or Types Buffer ([Union Layout](https://arrow.apache.org/docs/format/Columnar.html#union-layout))

Next, we will explore some examples to understand how Arrow represents the three types of arrays: arrays of fixed-size primitive values and arrays of variable-size binary values.

#### Fixed-size primitive

This is the most straightforward one, as all values have the same size, thus each will be stored in the same slot width.

Given an integer column: [1, 2, Null, 3, 4]. Here is the Arrow layout of this data:

[![](https://substackcdn.com/image/fetch/$s_!kPcj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73c6be44-7b0b-4f98-8428-527de82806df_812x552.png)](https://substackcdn.com/image/fetch/$s_!kPcj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73c6be44-7b0b-4f98-8428-527de82806df_812x552.png)

#### Variable-size binary

A variable-size binary has an additional buffer, called an offset, in addition to the data buffer. The offset buffer’s length equals the value array’s length + 1. This buffer encodes the start position of each slot in the data buffer.

The value length in each slot is the difference between the offset at that slot’s index and the subsequent offset.

Offsets must increase monotonically, even for null slots, ensuring that all values are well-defined and accessible via their corresponding offsets. Typically, the first slot in the offsets array is 0, and the last slot is the length of the values array.

Given a column [“vu“, null, null, “trinh“]

The array will be organized as follows:

[![](https://substackcdn.com/image/fetch/$s_!-fCE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d4b228c-8a0b-4bbb-ba02-c03a563cd9ef_1080x642.png)](https://substackcdn.com/image/fetch/$s_!-fCE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d4b228c-8a0b-4bbb-ba02-c03a563cd9ef_1080x642.png)

The not-null values will be stored continuously in the value buffer. To locate the value for each array slot, the reader can utilize the offset buffer. In this case, it is [0, 2, 2, 2, 7].

To read each slot, we begin with its start offset, which corresponds to the position in the offset buffer. Then the length of this value is calculated by the difference between the next offset and the current offset from the offset buffer.

* 1st value slot:

  [![](https://substackcdn.com/image/fetch/$s_!DHiA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b303628-29d6-4bb3-b274-677f5826b9b6_444x370.png)](https://substackcdn.com/image/fetch/$s_!DHiA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b303628-29d6-4bb3-b274-677f5826b9b6_444x370.png)

  + Start offset: offset\_buffer[0] = 0
  + Length = next offset - current offset = 2 - 0 =2
  + → Value = “vu“
* 2nd value slot:

  [![](https://substackcdn.com/image/fetch/$s_!tAeM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdee88df1-ce20-4b35-9dbe-8d6dc1e81fc2_466x362.png)](https://substackcdn.com/image/fetch/$s_!tAeM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdee88df1-ce20-4b35-9dbe-8d6dc1e81fc2_466x362.png)

  + Start offset: offset\_buffer[1] = 2
  + Length = next offset - current offset = 2 - 2 = 0
  + → Value = Null
* 3rd value slot:

  [![](https://substackcdn.com/image/fetch/$s_!inJk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ccd4c2e-1bb9-41dc-8995-9b8667653d80_446x330.png)](https://substackcdn.com/image/fetch/$s_!inJk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ccd4c2e-1bb9-41dc-8995-9b8667653d80_446x330.png)

  + Start offset: offset\_buffer[2] = 2
  + Length = next offset - current offset = 2 - 2 = 0
  + → Value = Null
* 4th value slot:

  [![](https://substackcdn.com/image/fetch/$s_!q9cC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8259cd54-2677-4dfb-8aac-508618966b46_450x328.png)](https://substackcdn.com/image/fetch/$s_!q9cC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8259cd54-2677-4dfb-8aac-508618966b46_450x328.png)

  + Start offset: offset\_buffer[3] = 2
  + Length = next offset - current offset = 7 - 2 = 5
  + → Value = “trinh“

The above are only two examples of how Arrow organizes different data types. It supports a wide range of types, including complex ones such as Map or Struct. All are suited to the array abstraction. You can check more [here](https://arrow.apache.org/docs/format/Columnar.html#data-types).

### A Record Batch

To represent tabular data, the Arrow specification introduces the Record Batch abstraction. It is used in many serialization and computation functions. It has:

[![](https://substackcdn.com/image/fetch/$s_!hIRI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33263c07-47f7-49f3-9fdc-cee8c303fb62_530x330.png)](https://substackcdn.com/image/fetch/$s_!hIRI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33263c07-47f7-49f3-9fdc-cee8c303fb62_530x330.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=169655500)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

* Schema: Every RecordBatch is associated with a Schema object. The Schema describes each column’s name and type.
* A list of Arrays: Each Array object corresponds to one column defined in the Schema.

The record batch is immutable (the arrays are immutable), ensuring that concurrent access is safe and eliminating the need for data copying for sharing.

### A Table

There is a Table to help users manage their datasets more conveniently. It is the higher-level abstraction that has one or more RecordBatches (or their underlying Array chunks) to form a complete dataset. All columns in a table must have the same rows.

[![](https://substackcdn.com/image/fetch/$s_!lDj-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89d77df0-436e-431d-91dc-fd5c775590d5_764x350.png)](https://substackcdn.com/image/fetch/$s_!lDj-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89d77df0-436e-431d-91dc-fd5c775590d5_764x350.png)

The Table’s column is a Chunked Array, which combines multiple arrays to provide a unified view for users. Unlike a record batch, we can append new data to the table by instructing the chunked array to include a new pointer that points to the new array, which can come from a record batch.

An example of a Table is that users receive multiple record batches and need a way to combine them so they can process them conveniently. Arrow Table can help in this case without excessive data copying. (Thanks to its pointer operations)

### Observation on the Arrow’s columnar format

Arrow positions itself for adoption in data analytics workloads that access subsets of attributes (columns) rather than the whole data records.

From what we’ve learned, Arrow stores values for each column contiguously in memory using the Array abstraction. This design is highly advantageous for data analytics workloads, which often focus on a subset of columns when processing large datasets.

Additionally, by storing data in this way, Arrow enables:

* **CPU Cache Efficiency:** Columnar storage improves data locality. When processing a column, the CPU can load contiguous blocks into its cache, leading to fewer cache misses and faster access.

  + With the row-oriented format, the system must load the entire record into the cache before extracting the required columns, thereby increasing cache misses.

    [![](https://substackcdn.com/image/fetch/$s_!Uc78!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c02c68e-c4ae-42cd-bd14-fb3f07de0c56_998x420.png)](https://substackcdn.com/image/fetch/$s_!Uc78!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c02c68e-c4ae-42cd-bd14-fb3f07de0c56_998x420.png)
* **SIMD (Single Instruction, Multiple Data) Optimization:** Some modern CPUs can perform the same operation on multiple data points simultaneously. Arrow also [performs memory alignment](https://arrow.apache.org/docs/format/Columnar.html#buffer-alignment-and-padding), allowing the system to leverage SIMD for operations on Arrow's in-memory data.

  [![](https://substackcdn.com/image/fetch/$s_!vXVd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0881899d-b359-4f57-8906-cb5a82a3f0dc_586x238.png)](https://substackcdn.com/image/fetch/$s_!vXVd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0881899d-b359-4f57-8906-cb5a82a3f0dc_586x238.png)

The way Arrow organizes the data reminds me of the approach used in a hybrid file format, such as Parquet. Data from a Table is horizontally split into portions (record batches vs. row groups), and then the columns are stored close together in a portion (array vs. column chunks). However, Arrow record batches don’t need to stay close together like Parquet’s row group.

[![](https://substackcdn.com/image/fetch/$s_!Ijsi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F138c8d52-3ade-42fa-8893-103385afdc29_1044x418.png)](https://substackcdn.com/image/fetch/$s_!Ijsi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F138c8d52-3ade-42fa-8893-103385afdc29_1044x418.png)

## The data transfer

Besides the performance, the Arrow creators also aim to make it a standard in-memory data representation format for analytics workloads, thereby improving data exchange between systems.

In this section, we will learn how Arrow can achieve that goal. First, we explore three data exchange scenarios to understand the challenges. Then, we will see how Arrow could solve them.

The three scenarios are: between two libraries in the same process, between two processes on the same machine, and between two processes on two different machines.

> ***Note**: The approach I take to delivering insights here is heavily inspired by **[Dunith Danushka](https://www.linkedin.com/in/dunithd/),** who wrote an excellent article on this topic. I also refer to this article to validate my research. You can check the [article here](https://www.linkedin.com/pulse/apache-arrow-missing-deep-dive-series-part-1-dunith-danushka-rhame/?trackingId=dr7DGgg%2FkAd9qAzsROq82g%3D%3D).*

### Between 2 libraries

#### Challenges

Imagine we process the same piece of data using two libraries in the same Python program. One library creates the dataset with its internal memory layout. To enable another library to work with this data, the layout must be converted into a format that the receiving library understands.

[![](https://substackcdn.com/image/fetch/$s_!4Mor!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde89ccdd-c668-4644-95bf-06270f896c5a_1046x410.png)](https://substackcdn.com/image/fetch/$s_!4Mor!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde89ccdd-c668-4644-95bf-06270f896c5a_1046x410.png)

In other words, the data must be serialized and deserialized between libraries. This raises some challenges:

* Each library must maintain its own copies of the same data.
* The cost of data serialization and deserialization (e.g., CPU…)
* In some cases, this process can’t be executed safely as data type systems from both libraries are not compatible.

#### Arrow comes to rescue

[![](https://substackcdn.com/image/fetch/$s_!YeID!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b789273-21db-4321-a386-94d57496116e_1408x460.png)](https://substackcdn.com/image/fetch/$s_!YeID!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b789273-21db-4321-a386-94d57496116e_1408x460.png)

If both libraries use Apache Arrow, things are much easier, as both libraries can leverage this Arrow format. As a result, there is no need for serialization and deserialization.

### Between two processes on the same machine

#### Challenges

Because the computing process is designed with high isolation, where each process has a separate memory region, one can access another process’s memory only with special mechanisms called IPC.

> ***[Inter-Process Communication (IPC)](https://en.wikipedia.org/wiki/Inter-process_communication)** is a set of mechanisms that allow independent computer processes to communicate with each other and share data, including shared memory, message passing, pipes, or sockets.*

To exchange data, the first process must also **serialize** its in-memory data into an intermediate format, such as JSON. This serialized data is then passed to the second process using an IPC mechanism, such as a socket or shared memory. The second process then **deserializes** this data in the internal format of the library it’s using.

[![](https://substackcdn.com/image/fetch/$s_!Dy3j!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f100063-048a-4f7a-b3e5-32fe1723d583_1372x576.png)](https://substackcdn.com/image/fetch/$s_!Dy3j!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f100063-048a-4f7a-b3e5-32fe1723d583_1372x576.png)

Again, this has some challenges, similar to those mentioned above, including the cost of data serialization and deserialization, memory wastage, and incompatible data type systems. In addition, both may need to implement IPC mechanisms to exchange data if no support is available.

#### Arrow comes to rescue

Arrow supports a highly efficient **IPC mechanism.**

[![](https://substackcdn.com/image/fetch/$s_!0jkh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2fceb7b-c4c4-40fe-b100-c7cd09f95f48_1342x486.png)](https://substackcdn.com/image/fetch/$s_!0jkh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2fceb7b-c4c4-40fe-b100-c7cd09f95f48_1342x486.png)

One process writes its data into an Arrow memory buffer in shared memory. The remaining process can **directly access and use the data from that shared region**, without any serialization, deserialization, or data copying.

> *Shared memory is an IPC mechanism in which multiple processes can access the same memory segment.*

### Between two processes on two different machines

#### Challenges

This is similar to the inter-process exchange on a single machine, but data must be sent over the network. The sending machine's process **serializes** the data, sends the resulting byte stream over the network, and the receiving machine's process **deserializes** it.

[![](https://substackcdn.com/image/fetch/$s_!ALF_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f4d8bcb-23c2-416f-82a4-d83a5634e276_1180x378.png)](https://substackcdn.com/image/fetch/$s_!ALF_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f4d8bcb-23c2-416f-82a4-d83a5634e276_1180x378.png)

JSON is often the preferred choice for network serialization, thanks to its widespread adoption in various systems. This could affect the latency of the data exchange as the format is [verbose and redundant](https://vutr.substack.com/p/file-formats-for-data-engineers), where every single record repeats the attribute keys. This could eat up more network bandwidth.

Additionally, the JSON format lacks a rich data type system, which can lead to data integrity issues when serializing/deserializing data from/to richer data type formats.

#### Arrow comes to rescue

For network data transferring, Arrow provides the **[Arrow Flight](https://arrow.apache.org/docs/format/Flight.html)**, a high-performance RPC framework. It organizes the data as a network stream of record batches.

[![](https://substackcdn.com/image/fetch/$s_!6f9q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28baf654-a09f-4f0f-9c09-156b8e5e9153_1592x502.png)](https://substackcdn.com/image/fetch/$s_!6f9q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28baf654-a09f-4f0f-9c09-156b8e5e9153_1592x502.png)

Instead of costly JSON serialization, data is sent over the network in its native, highly compressed Arrow format. The receiver gets a stream of bytes that is already in the exact memory layout it needs for processing.

This approach also ensures data integrity, as the data schema is preserved in the arrow type system. Additionally, thanks to the columnar format, the bandwidth required can be reduced by selecting only the necessary columns to transfer.

### Observation on how Arrow improves data exchange

Systems are encouraged to adopt Arrow at some level to achieve the benefits of data exchange. In return, Arrow must give them some value. And, in fact, the format provides:

* The performant columnar format, which is designed for analytics workload.
* The rich data type systems that allow systems to represent complex data structures.

[![](https://substackcdn.com/image/fetch/$s_!Fd5g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e893584-7419-4c6d-9665-97a6161c15b6_1192x772.png)](https://substackcdn.com/image/fetch/$s_!Fd5g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e893584-7419-4c6d-9665-97a6161c15b6_1192x772.png)

This makes Arrow an attractive option for any analytics system. Using Arrow is not only for interoperability, but also because Arrow is a very robust solution for organizing data in memory. Whatever reason a system chooses at first, whether interoperability or robustness, it will ultimately achieve both.

---

## Outro

In this article, we first explore the motivation behind Arrow, then dive deep into how its in-memory columnar format is implemented. Next, we discuss how this format can aid in analytics workloads and examine its role in enhancing data exchange between systems.

Most data engineers may not work directly with Arrow due to its low-level nature. However, I believe understanding this standard is helpful, given that one of our goals is to ensure that data moves reliably through systems.

(Your next company might require you to build a custom data application that involves reading/writing from multiple systems. Who knows?)

—

Thank you for reading this far. See you next time.

---

## Reference

*[1] Danielle Navarro, [Arrays and tables in Arrow](https://blog.djnavarro.net/posts/2022-05-25_arrays-and-tables-in-arrow/), 2022*

*[2] Dunith Danushka**,** [Apache Arrow - The Missing Deep Dive Series - Part 1](https://www.linkedin.com/pulse/apache-arrow-missing-deep-dive-series-part-1-dunith-danushka-rhame/?trackingId=dr7DGgg%2FkAd9qAzsROq82g%3D%3D), 2025*

*[3] [Arrow Official Documentation](https://arrow.apache.org/docs/format/Columnar.html)*

*[4] Jacques Nadeau, CTO of Dremio, [Apache Arrow: Theory & Practice Explained // Apache Arrow Meetup](https://www.youtube.com/watch?v=33s7Qs-e0gQ), 2017*
