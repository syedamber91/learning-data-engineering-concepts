---
title: "\"It's time to replace Parquet\""
channel: vutr
author: "Vu Trinh"
published: 2025-10-21
url: https://vutr.substack.com/p/its-time-to-replace-parquet
paid: true
topics: ["Data Engineering", "Lakehouse"]
tags: [https, auto, parquet, fetch, substackcdn, image]
---

# "It's time to replace Parquet"

*Parquet's limitations, what motivates the need for new file formats in analytics and AI, and will Parquet be replaced soon?*

> Source: [Open post](https://vutr.substack.com/p/its-time-to-replace-parquet)

## Topics

[[data-engineering|Data Engineering]] · [[lakehouse|Lakehouse]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!59Oj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F222f4ae7-cd35-4837-a556-d5b6e4801723_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!59Oj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F222f4ae7-cd35-4837-a556-d5b6e4801723_2000x1429.png)

---

## Intro

(about the title, I don’t say it; someone on the internet did)

Parquet is great. From my [previous article](https://open.substack.com/pub/vutr/p/the-overview-of-parquet-file-format?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false), we learn that Parquet is perfect for analytics workload. The query engine can choose to read the column it wants and skip irrelevant rows thanks to statistics.

However, Parquet was created over a decade ago.

Things have changed, especially with the analytics workload pattern. AI workloads are getting popular.

In this article, we first revisit the detailed implementation of a Parquet file. From that, we will try to understand the typical workload that the format was initially designed for. Then we will see how that design might not work well for the common analytics workload these days, which results in some file formats being created to solve the problems.

The goal is to provide a clearer understanding of Parquet, not only from its strengths but also from its limitations.

## History

[Apache Parquet was created in the early 2010s](https://en.wikipedia.org/wiki/Apache_Parquet) from a collaboration between engineers at Twitter and Cloudera, who looked for a more efficient and performant columnar storage format for large-scale data processing within the **Apache Hadoop ecosystem**.

[![](https://substackcdn.com/image/fetch/$s_!Ahef!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F684fa3e8-7a62-4c66-85d5-27940476de25_344x370.png)](https://substackcdn.com/image/fetch/$s_!Ahef!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F684fa3e8-7a62-4c66-85d5-27940476de25_344x370.png)

It was designed as an improvement over the Trevni ([now it’s a part of Apache Avro](https://avro.apache.org/docs/1.9.2/trevni/spec.html)), a columnar storage format created by [Doug Cutting](https://en.wikipedia.org/wiki/Doug_Cutting), the creator of Hadoop. Notably, Parquet incorporated concepts from Google’s Dremel paper to handle complex, nested data structures. The format’s goal was to provide an open-source, columnar standard that offered superior data compression, encoding schemes, and query performance by only reading necessary columns.

The first version, Apache Parquet 1.0, was released in July 2013.

The rest is history.

## Architecture

### Overview

Parquet is well-known as a columnar format. People often assume that data from a column is stored together. It’s only half of the story.

[![](https://substackcdn.com/image/fetch/$s_!S_vs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F318d8277-d142-4b68-9f3c-f7fa3a69dacc_658x294.png)](https://substackcdn.com/image/fetch/$s_!S_vs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F318d8277-d142-4b68-9f3c-f7fa3a69dacc_658x294.png)

The format organizes the data in the Partition Attributes Across (PAX) layout, which is commonly referred to as the hybrid format. It first groups data into “row groups,” each containing a subset of rows. (horizontal partition.)

[![](https://substackcdn.com/image/fetch/$s_!8HJW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43dffdc5-b343-4b57-bd39-0ed426d2dbce_636x462.png)](https://substackcdn.com/image/fetch/$s_!8HJW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43dffdc5-b343-4b57-bd39-0ed426d2dbce_636x462.png)

Within each row group, data is stored column by column; values from a column are stored together. Each row group’s column is called the column chunk. Each chunk is composed of pages, which are the unit for encoding and compression.

[![](https://substackcdn.com/image/fetch/$s_!Oi3y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cb04281-7152-4fc3-a396-e12abf5a4cc9_560x236.png)](https://substackcdn.com/image/fetch/$s_!Oi3y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cb04281-7152-4fc3-a396-e12abf5a4cc9_560x236.png)

This approach enables query engines to read only the desired columns and amortize the cost of writing data and reconciling a record; it is distributed only within a row group.

Metadata also plays a crucial role in Parquet. The file format contains information needed for the application to consume the file.

[![](https://substackcdn.com/image/fetch/$s_!MYLM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a8cea41-7550-42a7-9c92-b0454d10764a_876x692.png)](https://substackcdn.com/image/fetch/$s_!MYLM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a8cea41-7550-42a7-9c92-b0454d10764a_876x692.png)

* **Magic number**: It is used to verify if it is a valid Parquet file.
* **FileMetadata:** Parquet stores FileMetadata in the footer of the file. This metadata provides information like the number of rows, data schema, and row group metadata.

  + Each row group metadata contains information about its column chunks (ColumnMetadata), including the encoding and compression scheme, size, page offset, and min/max value of the column chunk. The application can use information in this metadata to prune unnecessary data.
* **PageHeader:** The page header metadata is stored with the page data and includes information such as value, definition, and repetition encoding. Parquet also stores definition and repetition levels to handle nested data. The application uses the header to read and decode the data.

### Write process

When writing data, the engine:

[![](https://substackcdn.com/image/fetch/$s_!sd9i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F594f0b76-1d80-4957-8481-2ad2139b56a8_1634x1156.jpeg)](https://substackcdn.com/image/fetch/$s_!sd9i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F594f0b76-1d80-4957-8481-2ad2139b56a8_1634x1156.jpeg)

* Collects information, such as the data schema, the null appearance, the encoding scheme, and all the column types, which are recorded in FileMetadata.
* Writes the magic number at the beginning of the file
* Calculates the number of row groups based on the row group’s max size (configurable) and the data’s size
* For each row group, iterates through the column list to write each column chunk for the row group. The engine typically buffers the entire row group data before flushing to disk.
* Writes each column chunk page by page sequentially

  + Each page has a header that includes the page’s number of rows, the page’s encoding for data, repetition, and definition.
* After writing all the pages for the column chunk, constructs the column chunk metadata for that chunk, including the min/max of the column (if it has), total\_uncompressed\_size, total\_compressed\_size, and the first data page offset.
* Continues until all columns in the row group are written to disk.
* Writes all row groups’ metadata in the FileMetadata after writing all the row groups.
* Writes the FileMetadata to the footer.
* Writes the magic number at the end of the file.

### Read process

When reading data, the engine:

[![](https://substackcdn.com/image/fetch/$s_!Y7L1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbc1c95-739e-49c4-a42d-1e56dad0bd2f_1398x990.jpeg)](https://substackcdn.com/image/fetch/$s_!Y7L1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbc1c95-739e-49c4-a42d-1e56dad0bd2f_1398x990.jpeg)

* Checks the magic number to see if it’s a valid Parquet file.
* Reads the FileMetadata from the footer. It extracts information for later use, such as the whole schema and the row group metadata.
* Retrieves the list of row groups to be read. If filters are specified, the engine iterates over every row group metadata and checks the filters against the statistic. If it satisfies the filters, this row group is appended to the list of row groups, which is later used to read.

  + If there are no filters, the list contains all the row groups.
* Defines the column list:

  + If the engine specifies a subset of columns it wants to read, the list only contains these columns.
* Iterates through the row group list and reads each one.
* Reads the column chunks for each row group based on the column list. It uses ColumnMetadata to locate the position of the first data page and decode the data.
* Continues until all row groups are read.

## Strengths

The section above highlights two obvious advantages of the Parquet file: Column Pruning and Predicate Pushdown. With the former, thanks to the column layout in row groups, the engine can read the required columns and skip irrelevant ones.

[![](https://substackcdn.com/image/fetch/$s_!1ANF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e709e1a-2dd4-40da-bbb1-1214ff7614fe_556x336.png)](https://substackcdn.com/image/fetch/$s_!1ANF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e709e1a-2dd4-40da-bbb1-1214ff7614fe_556x336.png)

For the latter, Parquet’s statistics can help the engine apply the query filter down to the physical file level. A query to filter for a value of 5 can skip all the row groups and the column chunk’s page, which has the data ranges that do not include 5. Similar to Column Pruning, this approach reduces the amount of data read from the file, decreases disk I/O, and enables faster data reading.

[![](https://substackcdn.com/image/fetch/$s_!W-Wm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d231bc9-3e38-4483-a6b0-a6b4efaf367d_598x262.png)](https://substackcdn.com/image/fetch/$s_!W-Wm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d231bc9-3e38-4483-a6b0-a6b4efaf367d_598x262.png)

> *In the following sections, I will first list out some Parquet limitations (based on my research), then we will move on to see why these limitations matter in today's analytics and AI workload.*

## Limitations

### Random Access

Parquet is not ideal for random access, where a small set of rows needs to be read.

This is because Parquet stores data by column. To rebuild a single logical row, the engine must perform multiple reads—one for each column’s data—from different physical locations within the file.

[![](https://substackcdn.com/image/fetch/$s_!BIO1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67cee9b9-10c1-43c2-8407-96cf01ae15e2_630x302.png)](https://substackcdn.com/image/fetch/$s_!BIO1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67cee9b9-10c1-43c2-8407-96cf01ae15e2_630x302.png)

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

This turns one logical row lookup into N separate operations (N is the number of columns). Although the location of all column data in a row stays close together in a row group, the cost of reading and stitching columns for a row is high, compared to a row-oriented format, which would require only a single read operation for the entire row. Plus, recall that a page is the unit of encoding/compression; to read a value in a page, the engine must bring the whole page.

[![](https://substackcdn.com/image/fetch/$s_!yqYq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee869f76-45ad-4c7e-85a7-3bc125641388_592x382.png)](https://substackcdn.com/image/fetch/$s_!yqYq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee869f76-45ad-4c7e-85a7-3bc125641388_592x382.png)

So, to read the data of a row, the engine must read a whole row group, locate, read, decompress, and decode the entire chunk’s page. That’s only for one column. The process is repeated until all column values are read.

#### Why does it matter

Wasn’t Parquet created to make large data scans efficient, not for random access?

You’re right. Parquet was not designed for random access. However, organizations require that capability nowadays. To provide interoperability for sub-teams in the data division, such as the data engineering team or the data science team, data must be present in a common format, and Parquet is widely chosen in the analytics world.

[![](https://substackcdn.com/image/fetch/$s_!VUEo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dbdcc08-7744-4b7c-85eb-09835aabdec6_338x362.png)](https://substackcdn.com/image/fetch/$s_!VUEo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dbdcc08-7744-4b7c-85eb-09835aabdec6_338x362.png)

The workloads that Parquet serves don’t stop at large-data-scan anymore—more to come, especially from the AI field. In modern AI, feature stores often need to store vector embeddings (e.g., a 768-dimensional array of floats) representing items, users, or documents/

[![](https://substackcdn.com/image/fetch/$s_!1JqO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9af75f23-2c40-43ff-aa64-edf1b347c3ed_718x190.png)](https://substackcdn.com/image/fetch/$s_!1JqO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9af75f23-2c40-43ff-aa64-edf1b347c3ed_718x190.png)

When an AI model needs to perform a semantic search (e.g., find documents similar to a query vector), it first searches a specialized index, which will return a list of documents.

> ***Note**: This article won’t dive much into the AI workload, such as semantic search*

To retrieve the actual document features, the system then executes a burst of random access against the data store. If data is stored in Parquet, you're likely aware of the inefficiency of the operation.

### Large column value

The goal of a Parquet Row Group is to be large—typically 128 MB to 1 GB —to ensure the data aligns with large disk blocks (like in HDFS) and to maximize sequential I/O. The size of the row group affects these things:

* Because the engine must buffer the entire row group in memory before flushing to disk, a too-big row group will put pressure on memory.

  [![](https://substackcdn.com/image/fetch/$s_!zpk2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3167ee-2da6-4a22-9872-446e291e0311_452x384.png)](https://substackcdn.com/image/fetch/$s_!zpk2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd3167ee-2da6-4a22-9872-446e291e0311_452x384.png)

  + In return, large row groups provide a larger sample size of data for each column, allowing compression and encoding algorithms to be more effective.
* We can adjust the row group size to be smaller. However, it must be done with caution, as small row groups also translate to small, non-sequential I/O requests.

  + The encoding and compression might be less effective.
* Row groups can be used to parallelize the read operations. The size of the row group determines the total number of row groups in a file, which in turn affects the efficiency of read operations.

  [![](https://substackcdn.com/image/fetch/$s_!6gOs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64fe6a1f-6c3b-4fc0-b826-fa0ffb95552e_456x362.png)](https://substackcdn.com/image/fetch/$s_!6gOs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64fe6a1f-6c3b-4fc0-b826-fa0ffb95552e_456x362.png)
* Besides that, the number of row group also impact the amount of metadata (as Parquet manages metadata for each row group)

  [![](https://substackcdn.com/image/fetch/$s_!MzuN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa67b1b-66ff-4c3a-99ba-bdbf4e4e44b4_354x288.png)](https://substackcdn.com/image/fetch/$s_!MzuN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa67b1b-66ff-4c3a-99ba-bdbf4e4e44b4_354x288.png)

That said, the row-group size is crucial. One of the factors that impacts the row-group size is the column size. Assume a table with **one column** stored in Parquet:

[![](https://substackcdn.com/image/fetch/$s_!Dw5t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea0397a3-49f6-4198-973b-0fb11806feae_548x250.png)](https://substackcdn.com/image/fetch/$s_!Dw5t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea0397a3-49f6-4198-973b-0fb11806feae_548x250.png)

> *These numbers are just [back-of-the-envelope](https://systemdesign.one/back-of-the-envelope/).*

* With a small column (e.g., 8 bytes), a 512 MB Row Group could contain 64 million rows (512,000,000/8).
* With one large column like with 4KiB values (e.g., 4,096 bytes), a 512 MB Row Group would contain only 125,000 rows (512,000,000/4,096).

In the large column value case, because the number of rows in a row group will be small, the Parquet file must contain a large number of row groups. As discussed right above, this is inefficient; more metadata to manage (due to more row groups), non-sequential I/O requests, and ineffective encoding/compression (due to the small row group)

So, will increasing the size of the row group solve the problem? Yes, it could hold more rows with large column values. However, recall that the engine buffers the row group in the memory before writing to disk; a large row group will put more pressure on the memory.

In conclusion, a large column value is the problem here. It makes the application harder to tune the row-group size.

#### Why does it matter

[![](https://substackcdn.com/image/fetch/$s_!H0Eb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F982f399f-2f9d-4c57-8d17-609990d83592_774x228.png)](https://substackcdn.com/image/fetch/$s_!H0Eb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F982f399f-2f9d-4c57-8d17-609990d83592_774x228.png)

When it comes to the AI workload, a large column value is not rare. Users typically want to store embeddings, documents, or images in a single column in Parquet, which easily exceeds the 4KiB value in this section’s example.

### Wide tables

As we discussed, every Parquet file contains a FileFooter that holds the critical FileMetadata object. Before a query engine can read any data, it must:

[![](https://substackcdn.com/image/fetch/$s_!W6Vk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6c1366a-14ef-4eb0-8aa9-6c5e6332bbe7_972x274.png)](https://substackcdn.com/image/fetch/$s_!W6Vk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6c1366a-14ef-4eb0-8aa9-6c5e6332bbe7_972x274.png)

* **Read the Footer:** Perform I/O operation(s) to find and fetch the entire FileMetaData.
* **Deserialize:** Decode the metadata ([which is encoded using Apache Thrift](https://parquet.apache.org/docs/file-format/metadata/) or Protocol Buffer) into the internal memory structures so that the engine can understand the dataset’s metadata, including its schema

Here is the thing: Thrift and Protocol Buffers do not support random access. This means the engine must deserialize the entire FileMetadata object to get the schema, although it might only require a schema of a single column.

[![](https://substackcdn.com/image/fetch/$s_!mL-J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b074b1c-cdb9-4682-857f-5e66af2b5c6a_766x268.png)](https://substackcdn.com/image/fetch/$s_!mL-J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b074b1c-cdb9-4682-857f-5e66af2b5c6a_766x268.png)

This problem is even worse when the table has thousands of columns. The FileMetadata object size is now bigger, and the operations that only require a few column metadata are even more inefficient.

#### Why does it matter

You might wonder, what on earth a table might have thousands of columns?

Machine Learning models, particularly in recommendation systems, require numerous descriptive attributes, or **features**, to make predictions. ML models perform best when all the necessary features are available in a single row for a specific entity (e.g., a user, an item, a click).

[![](https://substackcdn.com/image/fetch/$s_!uNvV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff6c5874-fd0b-4ed9-9a27-dedf3694fda1_826x242.png)](https://substackcdn.com/image/fetch/$s_!uNvV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff6c5874-fd0b-4ed9-9a27-dedf3694fda1_826x242.png)

> *I don’t know much about AI workloads, so my delivery about the wide tables in AI workloads might not be precise. Feel free to correct me here.*

This is the common input format for model training; features are **stitched** into a single, massive table. That said, this table won’t be efficient on Parquet due to the reasons discussed in this section.

### Encoding Extensibility

More advanced encoding methods have been developed that can compact data more effectively. Although Parquet supports a robust set of encodings, it does not keep up with state-of-the-art ones. Developers can add a custom encoding method for Parquet; however, maintaining consistency across different Parquet implementations (e.g., Java, Python, C++, Go) is complicated.

#### Why does it matter

Since Parquet was created, storage and network performance have improved significantly. Still, the CPUs have not. The rise of the lakehouse paradigm means more organizations are moving toward storing data in object storage, which provides high-bandwidth properties. I/Os are no longer the problem; the CPU is.

## So, will Parquet be replaced soon?

> ***Short answer**: No*

There are efforts to offer a new table format that can do better than Parquet. Meta introduced [Nimble](https://github.com/facebookincubator/nimble). LanceDB introduced [Lance](https://lancedb.github.io/lance/). Both projects are trying to address the challenges discussed above.

Recently, researchers have introduced a file format called [F3](https://db.cs.cmu.edu/papers/2025/zeng-sigmod2025.pdf), which puts the focus on interoperability, extensibility, and efficiency. Its ultimate goal is to eliminate the need for custom file formats in new use cases “by providing a data organization structure and a general-purpose API to allow developers to add new encoding schemes easily. “

However, I think that for these formats to replace Parquet, they need time, as all these projects are young and Parquet has been there for over a decade, despite its limitations (some don’t recognize them as Parquet still gives what they need; not everybody uses Parquet for AI workloads).

To replace Parquet, a new format must provide at least the same interoperability level as Parquet: most query engines and data processing frameworks natively support Parquet readers and writers.

That said, Parquet won’t be replaced any time soon.

For use cases that do not work well on Parquet, such as AI workloads, I believe more organizations will recognize Parquet’s limitations (given the fact that everybody wants the AI power nowadays) and seek alternative formats that can better support their needs, such as Nimble or Lance. A data team now might use two different formats:

[![](https://substackcdn.com/image/fetch/$s_!hUUH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5efdae5c-b78a-4c5b-87b5-9f7e398877a0_440x408.png)](https://substackcdn.com/image/fetch/$s_!hUUH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5efdae5c-b78a-4c5b-87b5-9f7e398877a0_440x408.png)

* Original analytics workloads can still go with Parquet (why not?)
* AI workloads will go with Nimble, Lance, or something else; the one that can do better than Parquet in this area.

To enable interoperability and ease the management overhead, a middle layer, such as a library, could abstract the complexity of translating between the two formats.

Saying that doesn’t mean I’m not excited about the future, where a new format could do the thing Parquet has been doing since its release: becoming the go-to choice for analytics workload. Still, this time, the new one could do better at providing greater interoperability and extensibility, allowing it to evolve to (any) new use cases.

(I bet on the production-ready implementation of F3; the format is currently a research prototype)

> *What you’ve just read in this section is based on my naive observation and personal experience. Feel free to discuss or correct me.*

## Outro

In this article, we revisit Parquet’s history and architecture to understand its role in supporting analytics workloads. We then discover its limitations, given that analytics workloads have evolved (e.g., AI), and the assumption about the hardware has become obsolete since the time Parquet was developed. Finally, I deliver some of my naive answers to the question “Will Parquet be replaced soon? “

Thank you for reading this far. See you in my next articles.

## Reference

*[1] Anastassia Ailamaki, David J. DeWitt, Mark D. Hill, Marios Skounakis, [Weaving Relations for Cache Performance](https://www.vldb.org/conf/2001/P169.pdf)*

*[2] [Parquet Official Docs](http://parquet.apache.org/docs/)*

*[3] Wes McKinney, [Extreme IO performance with parallel Apache Parquet in Python](https://wesmckinney.com/blog/python-parquet-multithreading/) (2017)*

*[4] Michael Berk, [Demystifying the Parquet File Format](https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705) (2022)*

*[5] [fastparquet source code GitHub repo](https://github.com/dask/fastparquet)*

*[6] [Lance v2: A columnar container format for modern data](https://blog.lancedb.com/lance-v2/), 2024*

*[7] Xinyu Zeng, Ruijun Meng, Martin Prammer, Wes McKinney, Jignesh M, Andrew Pavlo, Huancheng Zhang, [F3: The Open-Source Data File Format for the Future](https://db.cs.cmu.edu/papers/2025/zeng-sigmod2025.pdf), 2025*
