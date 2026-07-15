---
title: "Why there are so many Parquet's alternative file formats?"
channel: vutr
published: 2026-04-07
url: https://vutr.substack.com/p/why-there-are-so-many-parquets-alternative
paid: true
topics: ["Data Engineering", "Lakehouse"]
tags: [https, auto, parquet, image, fetch, good]
---

# Why there are so many Parquet's alternative file formats?

*Parquet's weakness and how the new formats resolved.*

> Source: [Open post](https://vutr.substack.com/p/why-there-are-so-many-parquets-alternative)

## Topics

[[data-engineering|Data Engineering]] · [[lakehouse|Lakehouse]]

---

> *I invite you to join my paid membership list to read this writing and **150+ high-quality** data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this **[30% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)***
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *You can also claim this post for free (one post only).*

[![](https://substackcdn.com/image/fetch/$s_!m5xH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4907abc-e8bb-4476-b4c4-1c28738837bb_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!m5xH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4907abc-e8bb-4476-b4c4-1c28738837bb_2000x1429.png)

This image is created with the help of Google Nano Banana.

---

# Intro

Parquet has been the core pillar in data engineering infrastructure.

From landing raw data to object storage to build a complete lakehouse solution.

It’s the most open-source implementation of the hybrid file format, where the dataset is partitioned into portions (called row groups in Parquet), and data for each column is stored continuously in a portion.

—

Recently, new file formats, such as Lance, Nimble, and Vortex, have emerged that promise to outperform Parquet. In this week's article, I take a deep dive into the motivations behind these formats. We first revisit the pros and cons of Parquet and then explore how these new formats differ.

**Note 1**: To keep this article concise, I won’t dive too much into Parquet architecture. So I assume you have a basic understanding of the file format. You can read [my previous article](https://vutr.substack.com/p/the-overview-of-parquet-file-format) to learn more.

**Note 2**: I won’t try to dive too deep into Lance, Nimble, and Vortex as [I did with Parquet](https://vutr.substack.com/p/the-overview-of-parquet-file-format). We see how they do things differently, mostly in how they organize metadata, control I/O, and encode data.

**Note 3**: This article is not sponsored by any of the mentioned file formats.

---

# Parquet

## Revisit

The Parquet format organizes data using the Partition Attributes Across (PAX) layout, commonly referred to as the hybrid format. It first groups data into “row groups,” each containing a subset of rows (horizontal partition)

[![](https://substackcdn.com/image/fetch/$s_!j-0_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bbaf009-837b-4bbc-b35a-c0343a4d3c8b_1610x814.png)](https://substackcdn.com/image/fetch/$s_!j-0_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bbaf009-837b-4bbc-b35a-c0343a4d3c8b_1610x814.png)

Within each row group, data is stored column by column; values from a column are stored together. Each column is stored as a column chunk. Each chunk is composed of pages, which are the unit for encoding and compression.

Metadata plays a crucial role in Parquet. The file format contains the information the application needs to consume the file.

[![](https://substackcdn.com/image/fetch/$s_!MAN4!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c6283e0-7894-4a4b-b262-e3eac34a2027_1658x824.png)](https://substackcdn.com/image/fetch/$s_!MAN4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c6283e0-7894-4a4b-b262-e3eac34a2027_1658x824.png)

* **Magic number**: It is used to verify if it is a valid Parquet file.
* **FileMetadata:** Parquet stores FileMetadata in the footer of the file. This metadata includes information such as the number of rows, the data schema, and row group metadata.

  + Each row group metadata contains information about its column chunks (ColumnMetadata), including the encoding and compression scheme, size, page offset, and min/max value of the column chunk. The application can use information in this metadata to prune unnecessary data.
* **PageHeader:** The page header metadata is stored with the page data and includes information such as value, definition, and repetition encoding. Parquet also stores definition and repetition levels to handle nested data. The application uses the header to read and decode the data.

## Pros

* Columnar storage makes it I/O cheaper for the engine to read a few columns.

  [![](https://substackcdn.com/image/fetch/$s_!sOfc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdccea6b1-b525-4787-b566-6b85797560df_862x290.png)](https://substackcdn.com/image/fetch/$s_!sOfc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdccea6b1-b525-4787-b566-6b85797560df_862x290.png)
* As data in the same column is stored next to each other. This helps Parquet encode the data more efficiently because data in the same column tends to be more homogeneous and repetitive.

  [![](https://substackcdn.com/image/fetch/$s_!_ond!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71cdb522-8d1a-4db9-8640-dadb9736ea0b_1018x284.png)](https://substackcdn.com/image/fetch/$s_!_ond!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71cdb522-8d1a-4db9-8640-dadb9736ea0b_1018x284.png)
* Parquet is a self-described format, including information such as schema and statistics to help the engine skip the data at multi-level (row-group and column)

  [![](https://substackcdn.com/image/fetch/$s_!UAyR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79551d6c-f3fc-41de-bf47-be234c535a99_1038x392.png)](https://substackcdn.com/image/fetch/$s_!UAyR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79551d6c-f3fc-41de-bf47-be234c535a99_1038x392.png)
* It’s the most adopted columnar file format. This means it received robust support from many systems.

## Cons

Parquet is great. But it has several disadvantages, especially in today's context, where hardware is not the same as it was 10 years ago and AI workloads dominate. These shortcomings also motivate the new formats, which we will discuss shortly.

### Random access

Parquet is not optimized for random access.

Parquet’s page is the unit of encoding/compression; to read a value in a page, the engine must fetch the entire page and decode the surrounding data before reaching the value. In addition, the page is compressed (by default), so the engine needs to decompress the entire page before entering the decoding process.

[![](https://substackcdn.com/image/fetch/$s_!ydHe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F570d459d-33ae-4db4-9361-29dfbe263e65_1216x796.png)](https://substackcdn.com/image/fetch/$s_!ydHe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F570d459d-33ae-4db4-9361-29dfbe263e65_1216x796.png)

Besides the latency of the processing of a page, if the random access needs more column values, the latency is increased by the time spent processing other columns’ pages.

Random-access latency is important in the context of AI, as organizations might store vector embeddings in Parquet. When the LLM needs to retrieve an embedding (e.g., a document), the speed of the random access will affect the latency of the AI response.

### The row-group constraint

[![](https://substackcdn.com/image/fetch/$s_!zpk2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3167ee-2da6-4a22-9872-446e291e0311_452x384.png)](https://substackcdn.com/image/fetch/$s_!zpk2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3167ee-2da6-4a22-9872-446e291e0311_452x384.png)

The row group in Parquet is tied directly to the physical I/O unit. The write engine cannot flush a partial column chunk, so it must buffer the entire row group in memory before writing. This is a common cause of out-of-memory (OOM) failures, especially with large column values like AI vector embeddings.

### FileMetadata bloat with wide tables (tables with many columns)

A table with many columns could bloat the FileMetadata, which is encoded using Apache Thrift or Protocol Buffer. However, Thrift and Protocol Buffers do not support random access. This means the engine must deserialize the entire FileMetadata object to obtain the schema, even though it might only require a schema for a single column.

[![](https://substackcdn.com/image/fetch/$s_!B_zI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0675b106-d31c-442f-8e70-cc9adc9aa0e1_1418x506.png)](https://substackcdn.com/image/fetch/$s_!B_zI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0675b106-d31c-442f-8e70-cc9adc9aa0e1_1418x506.png)

This is a serious problem when storing a feature table (for AI model training) with thousands of columns.

## Encoding flexibility

More advanced encoding methods have been developed that can present and compact data more effectively. Although Parquet supports a [robust set of encodings](https://vutr.substack.com/p/i-spent-8-understanding-how-parquet?utm_source=publication-search), it does not keep up with state-of-the-art ones.

Since Parquet was created, storage and network performance have improved significantly. Still, the CPUs have not. This means you can pull more Parquet data (via I/O), but decoding speed (via CPU) might not keep up due to the dated encoding schemes.

---

As we can see, most of Parquet’s shortcomings stem from two factors: AI workloads and hardware evolution. This motivates the birth of the new formats such as Lance, Nimble, and Vortex. All are columnar formats, but promise to do better with Parquet for AI workloads and to follow the state of the art in encoding methods.

Saying that doesn’t mean these formats will resolve all the problems I listed above.

---

> *I invite you to join my paid membership list to read this writing and **150+ high-quality** data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this **[30% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)***
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *You can also claim this post for free (one post only).*

---

# Lance

## Overview

[Lance](https://github.com/lance-format/lance) is a modern, open-source columnar data format designed for machine learning and multimodal AI, launched around 2022 by LanceDB (a YC W22 startup) to address Apache Parquet's performance limitations in AI workloads.

[![](https://substackcdn.com/image/fetch/$s_!brVo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a911a67-43b3-49bf-a0ed-a97e2b643395_992x938.png)](https://substackcdn.com/image/fetch/$s_!brVo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a911a67-43b3-49bf-a0ed-a97e2b643395_992x938.png)

The Lance file structure ***abandons row groups completely***. The column’s data is stored across multiple disk pages. A page will have some rows of a column. Different columns can have different numbers of pages, so columns don’t need to be the same length. Each column data writer will have its own buffer to write the page. Lance doesn’t require the pages in the same column to be contiguous.

The metadata that describes each page is located near the end of the file. It includes a set of protobuf messages, each column will have its own message. This means the engine can only read the protobuf messages for the required columns and skip the others. At the end of the file are the offset array and the footer. The array contains the offset to the column metadata, and the footer contains the offset to the array.

Let's see, with this specification, how Lance solves the Parquet problem’s list above.

## Random access

Lance addresses the random access differently depending [on the data size](https://lancedb.com/blog/columnar-file-readers-in-depth-structural-encoding/).

For **small values** (integers, short strings), Lance uses “miniblock” encoding, which is conceptually similar to Parquet pages; the engine still reads and decodes a small chunk. But Lance keeps these chunks very small, so the decode time spent on a chunk is dramatically reduced.

[![](https://substackcdn.com/image/fetch/$s_!nqDn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53943ce1-178f-4999-93db-32f9aa59bd56_476x226.png)](https://substackcdn.com/image/fetch/$s_!nqDn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53943ce1-178f-4999-93db-32f9aa59bd56_476x226.png)

For **large values** (vector embeddings, images, large text, 128 bytes per value as threshold), Lance uses “full-zip” encoding, which interleaves each value’s metadata directly with its data. The compression used is restricted to “transparent” encodings, meaning you can decompress a single value without affecting neighboring values. So if you need embedding #48, you jump directly to it and decompress just that one value.

[![](https://substackcdn.com/image/fetch/$s_!xBrx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa93a1992-2c1f-4646-a5a3-937b4eb0d58b_2316x454.png)](https://substackcdn.com/image/fetch/$s_!xBrx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa93a1992-2c1f-4646-a5a3-937b4eb0d58b_2316x454.png)

In brief, Lance aims to achieve effective random access by doing less than Parquet (decompression + decoding of surrounding data) while using more robust encoding schemes.

## The row-group constraint

As Lance skipped the concept of row-group entirely, each column can be written at its own speed.

## FileMetadata bloat with wide tables

[![](https://substackcdn.com/image/fetch/$s_!URbr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31ebe5cf-ef4c-4dda-9310-daa7cf4c906f_1564x538.png)](https://substackcdn.com/image/fetch/$s_!URbr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31ebe5cf-ef4c-4dda-9310-daa7cf4c906f_1564x538.png)

As each column is described by a separate protobuf message. The engine can retrieve the metadata for the required columns without loading metadata for the other columns (using the offset from the offset array)

## Encoding flexibility

Lance allows for encoding extensibility. However, because the Lance file format is a spec, the fragmentation seen in Parquet persists, and more implementations of the spec in different languages will make it difficult to keep things in sync.

However, when a specification is extensible, there is a high chance it will become fragmented; keeping everything aligned across implementations (e.g., Rust, C++, Java library) requires significant effort.

---

# Nimble

[Nimble](https://github.com/facebookincubator/nimble/), originally known as [Alpha](https://www.cidrdb.org/cidr2023/papers/p77-chattopadhyay.pdf), is a file format introduced by Meta around 2024. They aim to replace Parquet and ORC internally with Nimble. Its focus is on decode speed for sequential reads across wide tables, the workload Meta sees in feature engineering and model training.

Unlike Lance, Nimble specification still horizontally partitions data into row groups like Parquet.

[![](https://substackcdn.com/image/fetch/$s_!-mH1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee6a9cc3-fcbb-4587-bb95-e5230a62d286_1144x778.png)](https://substackcdn.com/image/fetch/$s_!-mH1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee6a9cc3-fcbb-4587-bb95-e5230a62d286_1144x778.png)

In each row group, data is stored as "streams"; each column is decomposed into one or more streams (e.g., a nullable string column produces a nullability stream, a length stream, and a data stream). Nimble store encodes information directly within each data stream, reducing the file footer to only essential offset data.

The footer metadata uses FlatBuffers instead of Thrift (Parquet). FlatBuffers can be accessed without full deserialization. This means the query engine could read information of a column without deserializing the whole footer metadata.

## Random access

As I understand, Nimble was **not designed for random access**. Its main target is sequential scan-and-decode performance for ML training. Its encodings are optimized for fast sequential decoding rather than point lookups.

## The row-group constraint

As Nimble still retains the row-group concept, the row-group sizing dilemma persists. Nimble relocates stripe footers to the end of the file (an improvement over ORC, which places them inline, but Parquet already stores row group metadata in the file footer). The means Nimble still inherits the fundamental tension of choosing a row group size that works across all columns.

## FileMetadata bloat with wide tables

[![](https://substackcdn.com/image/fetch/$s_!U66i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18de9a35-b325-4939-98ed-3c8fd53c500f_1568x546.png)](https://substackcdn.com/image/fetch/$s_!U66i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18de9a35-b325-4939-98ed-3c8fd53c500f_1568x546.png)

As mentioned, Nimble uses FlatBuffers for footer metadata, which does not require fully deserializing the entire structure to read a single piece of data.

## Encoding flexibility

[![](https://substackcdn.com/image/fetch/$s_!XuoA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb29047aa-fa33-44f8-ad06-e3e7923c37d3_660x318.png)](https://substackcdn.com/image/fetch/$s_!XuoA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb29047aa-fa33-44f8-ad06-e3e7923c37d3_660x318.png)

Nimble supports many encodings. The developer can extend the encoding methods if needed. An important note is that where Lance is a spec that encourages multiple implementations (accepting fragmentation as a trade-off), Nimble is a single canonical C++ library. [Meta explicitly discourages reimplementation](https://github.com/facebookincubator/nimble/).

---

# Vortex

[Vortex](https://github.com/vortex-data/vortex) is the youngest of the three formats. It was introduced last year and was created at [SpiralDB](https://github.com/spiraldb). It is said to be 100x faster for random-access reads than modern Apache Parquet.

The encoding and the physical data layout can be extensible. This means the same Vortex file spec can express a Parquet-like layout (row groups → chunks → pages), a Lance-like layout (no row groups, per-column chunking), or something entirely different.

[![](https://substackcdn.com/image/fetch/$s_!4f5p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F171c8f44-2352-4933-b4ef-616ae54f49ab_1048x744.png)](https://substackcdn.com/image/fetch/$s_!4f5p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F171c8f44-2352-4933-b4ef-616ae54f49ab_1048x744.png)

The file structure is organized like this: data segments, followed by per-column statistics, then a schema FlatBuffer, a layout FlatBuffer, and a postscript FlatBuffer (providing location of other sections), and an 8-byte end-of-file marker. The layout FlatBuffer provides the physical organization of the data as a tree of composable “layouts”. This tree provides information about the physical data layout.

A core concept in Vortex is the separation of [in-memory arrays](https://docs.vortex.dev/concepts/arrays) representation from [on-disk layouts](https://docs.vortex.dev/concepts/layouts). For the layout, Vortex offers [out-of-the-box layouts](https://docs.vortex.dev/concepts/layouts#built-in-layouts) (the user can introduce their own layouts), such as:

* FlatLayout: a single Vortex array
* StructLayout: a collection of child layouts
* ChunkedLayout: a collection of row-wise partitioned child layouts
* DictionaryLayout: a dictionary of values for dictionary encoding
* ZonedLayout: a zone-map of statistics to help the engine skip data

The user can combine these layouts to achieve the desired composed layout, for example, the row-group Parquet-style layout.

The [default Vortex layout](https://spiraldb.com/post/towards-vortex-10) splits struct arrays into fields, repartitions each field into 8k-row chunks with zone map statistics, repartitions again until chunks measure 1MB uncompressed, then passes each 1MB chunk to a BtrBlocks-inspired sampling compressor.

## Random access

[![](https://substackcdn.com/image/fetch/$s_!BunY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07aedffd-37c5-41e6-858b-a44aeb8f383a_916x542.png)](https://substackcdn.com/image/fetch/$s_!BunY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07aedffd-37c5-41e6-858b-a44aeb8f383a_916x542.png)

Vortex chooses encoding schemes that are navigable without full decompression, and then provides compute kernels that can operate directly on compressed data. Vortex selects encodings that are "transparent"; individual values remain addressable within the compressed data. The encoding methods include FastLanes bit-packing (for integers), ALP (for floating-point), FSST (for strings),…

## The row-group constraint

Vortex doesn’t have a fixed opinion on row groups.

The layout implementation can use the Parquet-style layout with row groups and aligned pages. Alternatively, it can chunk columns differently based on their data (like Lance). With the default Vortex layout, there are no row groups. Each column is independently split into chunks based on its own data characteristics.

## FileMetadata bloat with wide tables

[![](https://substackcdn.com/image/fetch/$s_!N6O5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c8a1d78-a7bc-4b76-8001-ab643035cbfd_1646x644.png)](https://substackcdn.com/image/fetch/$s_!N6O5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c8a1d78-a7bc-4b76-8001-ab643035cbfd_1646x644.png)

By leveraging FlatBuffer, Vortex can read a single piece of data without deserializing the entire metadata.

## Encoding flexibility

As discussed, Vortex offers the highest level of extensibility. Not only the encoding, but also the physical layout. However, it takes a different approach compared to Lance and Nimble.

[Vortex plans (based on their official documentation, the feature is not implemented yet)](https://docs.vortex.dev/specs/file-format#forward-compatibility) to address the fragmentation by embedding [WebAssembly](https://webassembly.org/) decompression kernels into the file itself, so even if a reader doesn’t natively support a new encoding, it can still decode the data using the embedded WASM logic. If it works, it would allow Vortex to evolve the encoding schemes without breaking any reader implementations, a problem that has plagued Parquet for years.

---

# The Parquet’s future

We took a short trip to explore how Lance, Nimble, and Vortex differ in their approaches to solving Parquet problems. It’s oriented around these things:

* O(1) metadata access: All three can access the metadata for required columns, thanks to the usage of FlatBuffer (Nimble, Vortex) or the separation of column metadata (Lance)
* Leveraging more advanced encoding/compression techniques to reduce the decoding/decompression data, which also improves the performance of random access.
* More freedom in physical layout (Lance and Vortex).

That said, I believe Parquet won’t go anywhere soon. For these formats to completely replace Parquet, they would require a lot of time and hope that Parquet won’t evolve. Despite its limitations, Parquet is still a solid columnar format supported by nearly any data system, and not everybody requires Parquet to be good at random access or to contain thousands of columns (e.g., AI workloads).

[![](https://substackcdn.com/image/fetch/$s_!yrKa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd35780b2-2718-4c8a-ab27-a029937af9da_850x652.png)](https://substackcdn.com/image/fetch/$s_!yrKa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd35780b2-2718-4c8a-ab27-a029937af9da_850x652.png)

For use cases that do not work well with Parquet, such as AI workloads, more organizations will recognize Parquet’s limitations (given that everybody wants AI power nowadays) and seek alternative formats that better support their needs, such as the three formats we discussed. The problem that needs to be solved now is fragmentation across storage formats. For example, a data scientist runs an ad hoc query on a Parquet dataset and trains on the Lance format.

Another approach is to … wait for the Parquet to evolve. There are ongoing efforts to bring more state-of-the-art encoding schemes to Parquet:

[![](https://substackcdn.com/image/fetch/$s_!sw0t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11bd609d-9220-45d1-aa7b-3d85a4355e0c_1532x1348.png)](https://substackcdn.com/image/fetch/$s_!sw0t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11bd609d-9220-45d1-aa7b-3d85a4355e0c_1532x1348.png)

[Column Storage for the AI Era](https://sympathetic.ink/2025/12/11/Column-Storage-for-the-AI-era.html), by Julien Le Dem

There is also a proposal in progress to implement [FlatBuffer (which was not available at the time when Parquet was first developed) for Parquet’s footer metadata](https://lists.apache.org/thread/j9qv5vyg0r4jk6tbm6sqthltly4oztd3). If those proposals are implemented, Parquet can access the metadata and encode and decode data more efficiently.

The columnar file format race will be more and more excited.

---

# Outro

In this article, we revisit the Parquet specification and its pros/cons. From there, we understand the motivation behind new formats such as Lance, Nimble, and Vortex, which aim to outperform Parquet in leveraging advanced encoding and serving AI workloads.

We then dive into how Lance, Nimble, and Vortex solve random access, the row-group constraint, file metadata bloat in many-column tables, and encoding extensibility. Finally, we look into the future to see whether Parquet still exists or not (the answer is yes).

Thank you for reading this far.

See you in my next articles.

---

# Reference

*[1] Xinyu Zeng, Ruijun Meng, Martin Prammer, Wes McKinney, Jignesh M, Andrew Pavlo, Huancheng Zhang, [F3: The Open-Source Data File Format for the Future](https://db.cs.cmu.edu/papers/2025/zeng-sigmod2025.pdf), 2025*

*[2] [Lance v2: A columnar container format for modern data](https://blog.lancedb.com/lance-v2/), 2024*

*[3] [Lance Specification](https://lance.org/format/file/)*

*[4] Weston Pace, Chang She, Lei Xu, Will Jones, Albert Lockett, Jun Wang, Raunak Shah, [Lance: Efficient Random Access in Columnar Storage through Adaptive Structural Encodings](https://arxiv.org/abs/2504.15247), 2025*

*[5] Yoav Helfman, Nimble, [A New Columnar File Format](https://www.youtube.com/watch?v=bISBNVtXZ6M), 2024*

*[6] [Vortex Official Documentation](https://docs.vortex.dev/concepts/#).*

*[7] Julien Le Dem, [Column Storage for the AI Era](https://sympathetic.ink/2025/12/11/Column-Storage-for-the-AI-era.html), 2025*
