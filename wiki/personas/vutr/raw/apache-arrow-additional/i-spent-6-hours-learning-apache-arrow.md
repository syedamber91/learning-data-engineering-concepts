---
title: "I spent 6 hours learning Apache Arrow: Overview"
channel: vutr
author: "Vu Trinh"
published: 2024-10-12
url: https://vutr.substack.com/p/i-spent-6-hours-learning-apache-arrow
paid: false
topics: ["Data Engineering", "Apache Spark", "BigQuery", "Streaming"]
tags: [arrow, https, memory, format, apache, auto]
---

# I spent 6 hours learning Apache Arrow: Overview

*Why do we need a standard memory format for analytics workload?*

> Source: [Open post](https://vutr.substack.com/p/i-spent-6-hours-learning-apache-arrow)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[bigquery|BigQuery]] · [[streaming|Streaming]]

---

> *My name is Vu Trinh, and I am a data engineer.*
>
> *I’m trying to make my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!rW8x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee954c34-f168-4c87-a973-efea9b1e45ff_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!rW8x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee954c34-f168-4c87-a973-efea9b1e45ff_2000x1429.png)

[Apache Arrow Icon Source.](https://arrow.apache.org/powered_by/)

---

## Intro

This week, we will explore one of the most exciting data-related projects at the moment: Apache Arrow. The article will be structured as follows: first, we will understand what Arrow is and the motivation behind it. Then, we will learn about the physical data layout of the Arrow array and how Arrow data is serialized. Finally, we will explore how Arrow can bring immense value to the analytics world.

---

## What?

I will bring the definition from Arrow’s official documentation here:

> *The **Arrow columnar format** includes a language-agnostic in-memory data structure specification, metadata serialization, and a protocol for serialization and generic data transport. It provides analytical performance and data locality guarantees in exchange for comparatively more expensive mutation operations.*

The Apache Arrow format project began in February 2016, focusing on columnar in-memory analytics workload. Unlike file formats like Parquet or CSV, which specify how data is organized on disk, Arrow focuses on how data is organized in memory.

[![](https://substackcdn.com/image/fetch/$s_!CN3d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d15d894-4e7c-4205-a74c-a489d847fed3_1378x670.png)](https://substackcdn.com/image/fetch/$s_!CN3d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d15d894-4e7c-4205-a74c-a489d847fed3_1378x670.png)

Image created by Canva Image Generator.

The creators try to build Arrow as a community standard in-memory format for workload analytics. These foundations attract many contributors from projects such as Pandas, Spark, Cassandra, Apache Calcite, Dremio, and Ibis.

Apache Arrow tries to achieve:

* **Performance**: Efficient data processing for analytics workload by designing to take advantage of modern CPU characteristics.
* **Interoperability**: Sharing data between systems at a low cost or zero cost.

When two systems communicate, each converts its data into a standard format before transferring it. However, this process incurs serialization and deserialization costs. The idea behind Apache Arrow is to provide a highly efficient format for processing within a single system. As more systems adopt this data representation, they can share data at a very low cost, potentially even through shared memory at zero cost. This is the core of Arrow's design. It's a library that can be embedded in many systems, such as execution engines, analytics tools, or storage layers.

---

## Terminology

Before going further, let's check out some terminology in the Arrow world:

* An **array** is a sequence of values with defined lengths, all sharing the same type.
* A **slot** is a single logical value within a specific data type array.
* **Buffer** is a sequential virtual address space with a fixed length, where any byte can be accessed via a pointer offset within the region’s length.
* **Physical Layout** describes the underlying memory structure of an array without considering its value semantics.
* **The data type** represents an application-level value type implemented using a specific physical layout. For example, Decimal128 values are stored as 16 bytes in a fixed-size binary format, while a timestamp might be stored in a 64-bit fixed-size layout.
* A **primitive type** is a data type with no child types, such as fixed bit-width, variable-size binary, and null types.
* A **nested type** is a data type whose structure depends on one or more child types.

For the rest of this article, I will convey the information using arrays with primitive types. For other data types, you can check [Arrow's documentation](https://arrow.apache.org/docs/format/Columnar.html).

## Array Physical Memory Layout

A few pieces of metadata and data define arrays:

[![](https://substackcdn.com/image/fetch/$s_!-5St!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbbd50d7-7994-420b-a109-39618786caa6_1434x746.png)](https://substackcdn.com/image/fetch/$s_!-5St!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbbd50d7-7994-420b-a109-39618786caa6_1434x746.png)

Image created by the author.

* The array’s length is a 64-bit signed integer, and the null count is also a 64-bit signed integer.
* A data type.
* An optional **dictionary** for dictionary-encoded arrays.
* A sequence of buffers:

  + **Validity bitmap**: Almost all array types have a dedicated memory buffer, known as the validity bitmap, which encodes the null information for each array's slot value.
  + **Offset Buffer**: Some array types, such as Variable-size Binary Layout, have offset buffers to locate the start position of each slot in the data buffer.
  + **Value Buffer**: The buffers containthearray’s data
  + There are more buffers for some complex types, such as Size Buffer ([ListView Layout](https://arrow.apache.org/docs/format/Columnar.html#listview-layout)) or Types Buffer ([Union Layout](https://arrow.apache.org/docs/format/Columnar.html#union-layout))

### Memory Alignment

When working with Apache Arrow, memory should be allocated at aligned addresses—typically in multiples of 8 or 64 bytes. Additionally, padding (over-allocating memory) is encouraged to ensure the total length is a multiple of 8 or 64 bytes.

> **Aligned memory** refers to a memory address that is a multiple of a specific value, known as the alignment boundary, such as 4, 8, or 64 bytes. Aligned memory is crucial for performance because CPUs are optimized to handle data on these boundaries, allowing faster access. Misaligned data forces the CPU to perform extra operations, slowing things down.
>
> **Padding** in memory refers to the practice of adding extra, unused bytes between data elements or at the end of a data block to ensure proper alignment. This is often done to make sure that subsequent data starts at a correctly aligned memory address, adhering to alignment boundaries such as 8 or 64 bytes. Padding helps maintain efficient memory access. In return, padding increases the memory usage.

This alignment follows Intel's performance guidelines, which suggest matching memory alignment to SIMD register widths, particularly for the AVX-512 architecture.

> *SIMD (Single Instruction, Multiple Data) is a processing technique that allows a CPU to perform the same operation on multiple data points simultaneously. This is achieved through specialized instructions and registers that can handle multiple values at once.*

### An example layout of a Fixed-size Primitive Array Layout

A primitive value array represents values with the same slot width.

[![](https://substackcdn.com/image/fetch/$s_!zm4Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd851c7f4-7999-4e1f-bedd-809118c34543_1388x806.png)](https://substackcdn.com/image/fetch/$s_!zm4Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd851c7f4-7999-4e1f-bedd-809118c34543_1388x806.png)

Image created by the author.

### An example layout of a Variable-size Binary Array Layout

Each value in this layout consists of 0 or more bytes. A variable-size binary has an additional buffer called offset in addition to the data buffer.

The offset buffer’s length equals the value array’s length + 1. This buffer encodes each slot's start position in the data buffer. The value length in each slot is computed using the difference between the offset at that slot’s index and the subsequent offset.

[![](https://substackcdn.com/image/fetch/$s_!h6nX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde456d8e-d53d-483b-9f17-e73c69ad1017_1092x974.png)](https://substackcdn.com/image/fetch/$s_!h6nX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde456d8e-d53d-483b-9f17-e73c69ad1017_1092x974.png)

Image created by the author.

A null value may have a positive slot length and take non-empty memory space in the data buffer. In such cases, the content of the corresponding memory space is undefined. Offsets must increase monotonically, even for null slots, ensuring that all values' locations are valid and well-defined. Typically, the first slot in the offsets array is 0, and the last slot is the length of the values array.

For more layouts of different array types, you can check [Arrow Official Documentation](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc).

---

## Serialization and Interprocess Communication (IPC)

> *This section describes the Arrow protocol for efficiently transferring and processing data between processes.*

The unit of serialized data in the Arrow is the “record batch.” A record batch is a collection of arrays, known as its **fields**, each with potentially different data types. The field names and types collectively form the batch’s **schema**.

[![](https://substackcdn.com/image/fetch/$s_!9vtj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f18bf94-a5ed-43b4-b779-c69762e9a4f2_1298x620.png)](https://substackcdn.com/image/fetch/$s_!9vtj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f18bf94-a5ed-43b4-b779-c69762e9a4f2_1298x620.png)

Image created by the author.

The [Arrow protocol](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc) utilizes a one-way stream of binary messages of these types:

* **Schema message**: This defines the structure of the data. It consists of a list of fields, each with a name and a data type (int, float, string, etc.). A serialized Schema does not contain any data buffers.
* **RecordBatch message** contains the actual data buffers. A RecordBatch contains a collection of equal-length arrays, each corresponding to a column described in the schema. The metadata for this message provides the location and size of each buffer, allowing its array to be reconstructed using pointer arithmetic and, thus, avoid memory copying. The serialized form of the record batch has the body and data header. The body includes arrays’ memory buffers. The header contains the length and null count for each flattened field and the memory offset and size of each buffer within the record batch’s body.
* **DictionaryBatch message**: A DictionaryBatch is a specialized batch used for dictionary encoding, an efficient way to store categorical data. It contains a dictionary or lookup table where unique values are stored. Dictionary-encoded fields refer to indices in this dictionary rather than storing the total values directly, saving space and improving performance.

Arrow supports two types of binary formats for serializing RecordBatches:

* **Streaming format (IPC Streaming Format)**: Used for sending an arbitrary-length sequence of record batches. This format must be processed sequentially from start to end and does not support random access. The schema appears first in the stream. If any fields in the schema are dictionary-encoded, one or more DictionaryBatch messages will be included.
* **File format (IPC File Format)**: Used for serializing a fixed number of record batches, with support for random access. The file begins and ends with the magic string "ARROW1." The file contents are otherwise identical to the streaming format. At the end of the file is a footer containing a redundant copy of the schema and memory offsets and sizes for each data block. This allows for random access to any record batch within the file.

---

## How does Apache Arrow bring value?

### Performance

Arrow positions itself for adoption in data analytics workloads that access subsets of attributes (columns) rather than individual data records.

As mentioned, Arrow organizes data in a column-by-column format within a record batch. This design is highly advantageous for data analytics workloads, which typically focus on a subset of columns at a time and scan through large numbers of rows to aggregate values. Storing data in a columnar fashion enables high-performance, sequential access patterns ideal for these tasks.

Additionally, storing data column-by-column offers further benefits for analytical workloads, such as enabling SIMD acceleration and improving compression rates. One additional factor that ensures Arrow provides processing efficiency is memory alignment.

### **Interoperability**

Initially, when moving data from one system to another, we had to rewrite the data within the system into a more straightforward representation. This representation would then be passed to the other system, where it would be rewritten to fit its proprietary format. Rewriting data before export is called "serialization," and rewriting it back before import is called "deserialization." These serialization and deserialization CPU costs were unavoidable when moving data between systems.

Before Arrow, each system used its internal memory format, which wasted many CPU resources on serialization and deserialization. With Arrow, everything changes. All systems now utilize the same memory format, eliminating cross-system communication overhead.

[![](https://substackcdn.com/image/fetch/$s_!MWV5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94914839-5e7a-4fe2-abaf-cebbcc523363_2274x822.png)](https://substackcdn.com/image/fetch/$s_!MWV5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94914839-5e7a-4fe2-abaf-cebbcc523363_2274x822.png)

Image created by the author.

Apache Arrow promises to provide low-cost or zero-cost data sharing between systems by providing an IPC format ([IPC stream](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format) and [IPC file](https://arrow.apache.org/docs/format/Columnar.html#ipc-file-format)) that allows data to be seamlessly passed between processes without re-serialization, making inter-process communication faster and more efficient.

Arrow [IPC files](https://arrow.apache.org/docs/format/Columnar.html#ipc-file-format) can be memory-mapped, allowing us to work with datasets that exceed the memory capacity. This enables seamless data sharing across different languages and processes.

> *A **memory-mapped file** is a segment of virtual memory that has been assigned a direct byte-for-byte correlation with some portion of a file or file-like resource. The benefit of memory mapping a file is increasing I/O performance, especially when used on large files.*
>
> *— [Wikipedia](https://en.wikipedia.org/wiki/Memory-mapped_file) —*

Arrow also excels at moving data over the network. The format supports serializing and transferring columnar data across the network or other streaming transports. Apache Spark, for instance, uses Arrow as a data interchange format. Big names like Google BigQuery, TensorFlow, and AWS Athena also use Arrow to streamline data operations.

Moreover, the Arrow project defines **Flight**, a client-server RPC framework. Flight helps users build robust services for exchanging data based on application-specific needs, making data handling even more efficient and customizable.

To see Arrow's ubiquity, you can visit the list of projects that leverage Apache Arror [here](https://arrow.apache.org/powered_by/). Some notable projects include Spark, AWS Data Wrangler, Clickhouse, Dask, Dremio, InfluxDB IOx, MATLAB, pandas, Polars, and Ray.

---

## Outro

In this article, we explored the Apache Arrow’s overview, from its definition and motivation to its physical memory layout and how data is serialized.

Thank you for reading this far. If you notice any points needing correction or want to discuss more about Arrow, feel free to leave a comment.

Now, it’s time to say goodbye. See you in the next blog!

---

## Reference

*[1] [Arrow Official Documentation](https://arrow.apache.org/docs/format/Columnar.html)*

*[2] Jacques Nadeau, CTO of Dremio, [Apache Arrow: Theory & Practice Explained // Apache Arrow Meetup 2017](https://www.youtube.com/watch?v=33s7Qs-e0gQ)*

*[3] Daniel Abadi, [An analysis of the strengths and weaknesses of Apache Arrow](https://dbmsmusings.blogspot.com/2018/03/an-analysis-of-strengths-and-weaknesses.html) (2018)*

---

## Before you leave

If you want to discuss this further, please comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-6-hours-learning-apache-arrow/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
