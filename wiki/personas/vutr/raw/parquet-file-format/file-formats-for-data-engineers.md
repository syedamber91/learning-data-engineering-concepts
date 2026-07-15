---
title: "I spent 8 hours learning CSV, JSON, Avro, and Parquet"
channel: vutr
author: "Vu Trinh"
published: 2025-07-29
url: https://vutr.substack.com/p/file-formats-for-data-engineers
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Streaming"]
tags: [https, auto, file, good, image, substackcdn]
---

# I spent 8 hours learning CSV, JSON, Avro, and Parquet

*File Formats for Data Engineers*

> Source: [Open post](https://vutr.substack.com/p/file-formats-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=169049694)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!4vTf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b4d4edc-20dd-4480-8b33-e11705fcd61f_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!4vTf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b4d4edc-20dd-4480-8b33-e11705fcd61f_2000x1428.png)

---

## Intro

We, data engineers, work with data nearly every day. We capture and consolidate digital data from multiple sources, transform it, and store it.

For every data interaction, we:

* Write data to disk
* Or, read data from disk.

From pulling data from a remote server via API to appending data to a table, we interact with digital records persisted on physical disks. However, we don’t work directly with the raw device, such as an HDD or SSD, most of the time. We work with the file abstraction instead

Not every file is the same. They differ in the way the data is organized, making data writing and reading ideal for specific use cases.

A photographer might not care how his image is stored in a PNG file. However, data engineers should pay attention to how data is organized and ensure that data read-write operations are as efficient as possible.

This article explores the most common file formats that data engineers may encounter: CSV, JSON, Parquet, and Avro.

---

## Text-based format vs binary format

It’s helpful to understand the difference between text and binary formats.

All data stored on a disk is a sequence of 0s and 1s. However, the way these 0s and 1s are interpreted distinguishes the "text-based" file from a "binary" format.

Text-based formats rely on **character encoding** to serve as a dictionary between binary numbers and the characters displayed on the screen.

Every single character—a letter like 'A', a number like '9', or a symbol like ','—is assigned a unique numerical code by a standard like **ASCII** or **Unicode**. When you save a text file, the computer converts each character into its corresponding binary representation.

The most important benefit of text-based files is that they are human-readable. We can read and edit the text files using Notepad or collaborate on Google Docs. It will be a nightmare if you open a .py file and try to adjust a function by editing bits 0 and 1.

However, this approach creates a crucial inefficiency, especially for numbers. To store the number `256`, the computer stores the binary codes for three separate characters: '2', '5', and '6'. This takes up more space and requires the computer to perform an extra step of parsing these characters back into a single number during processing.

Not caring much about whether humans can understand it or not, the binary format is designed for machine efficiency. While strings within a binary file are still encoded (typically using UTF-8), other data types are stored in their raw, native binary form.

The number `256`, in a binary format, stores the direct mathematical representation of that integer. For example, as a 16-bit integer, it would be stored as `00000001 00000000`.

This approach is far more compact and faster for a computer to process. There is no need to parse three separate characters and convert them into a number; the CPU can interpret the binary value directly.

---

## CSV

### Characteristics

At its core, Comma-Separated Values (CSV) is a plain-text format designed to store data in a structured manner. When opening a CSV file in any text editor, you will see text that is separated by **newline characters**.

[![](https://substackcdn.com/image/fetch/$s_!PuEl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98298a39-4b4d-49e3-b51a-2464a491b094_644x366.png)](https://substackcdn.com/image/fetch/$s_!PuEl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98298a39-4b4d-49e3-b51a-2464a491b094_644x366.png)

Each line in a file represents a data record or row. The values within that record are separated by a delimiter, which is typically a comma. Every line should have the same fields. (The exact number of commas.).

[![](https://substackcdn.com/image/fetch/$s_!3apq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ef07487-4e27-4f14-82c7-389fc6a58ff4_612x198.png)](https://substackcdn.com/image/fetch/$s_!3apq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ef07487-4e27-4f14-82c7-389fc6a58ff4_612x198.png)

The format's simplicity makes it universally understood by nearly every data application, from spreadsheet programs like Microsoft Excel to relational databases. This factor makes it the widely adopted option for data exchange, especially with non-technical stakeholders.

The primary advantage of CSV is its compatibility and ease of use. Users can display the contents in the CSV file in a well-organized table via Google Sheets, edit, and update it with their keyboard.

### Challenges

However, some things must be considered:

* A CSV file **has no built-in mechanism for defining a schema or enforcing data types**. This put the responsibility on the reading system to parse and interpret the data.

  [![](https://substackcdn.com/image/fetch/$s_!GwM5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06dbbd76-89c5-48a2-b1cf-639b8252400c_570x212.png)](https://substackcdn.com/image/fetch/$s_!GwM5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06dbbd76-89c5-48a2-b1cf-639b8252400c_570x212.png)

  + This process is not only computationally intensive but also a common source of critical errors, such as “1“ should be a string, not a number.
  + To ensure a reliable parsing process, it is recommended that the reader tell the system about the column’s data type and schema beforehand.
* The format's **lack of a standard** leads to numerous potential failure points that make ingestion pipelines brittle. Common issues include:

  + **Delimiter Conflicts:** Data fields that naturally contain the delimiter (e.g., a text description containing a comma) can break the structure if not properly escaped.
  + **Inconsistent Quoting:** There is no universal rule for when to quote fields, leading to ambiguity that parsers must resolve.
  + **Varying Encodings:** While UTF-8 is a best practice, it is not guaranteed. Files may arrive in different encodings, which can lead to data corruption if not handled explicitly.
* **Not good for analytics:** As a row-oriented text format, CSV is fundamentally **inefficient for large-scale analytics.** To access a single column, the entire row must be read from disk and processed, leading to excessive I/O.
* An uncompressed CSV file is splittable and can be read in parallel. Because each line in the file represents a complete, independent record, different workers can handle a set of lines.

  [![](https://substackcdn.com/image/fetch/$s_!m7i8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423653f9-4c4c-4d62-a96a-baa9bcdfbca3_576x306.png)](https://substackcdn.com/image/fetch/$s_!m7i8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423653f9-4c4c-4d62-a96a-baa9bcdfbca3_576x306.png)

  + However, if we use a non-splittable compression algorithm, such as **Gzip**, the entire file becomes a single, continuous compressed stream. A processing engine can’t divide the work.

    [![](https://substackcdn.com/image/fetch/$s_!voFG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2d808ce-892b-455e-86be-e11e8199b93b_1330x432.png)](https://substackcdn.com/image/fetch/$s_!voFG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2d808ce-892b-455e-86be-e11e8199b93b_1330x432.png)
* CSV lacks support for nested and repeated data.

---

## JSON

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=169049694)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

### Characteristics

JSON emerged from the world of web development as a lightweight, text-based data interchange format. Its structure is built on human-readable key-value pairs, with native support for nested objects and arrays. JSON is widely used in web development

[![](https://substackcdn.com/image/fetch/$s_!INw7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbb66117-a77f-462a-b7b8-dacbc085859e_564x440.png)](https://substackcdn.com/image/fetch/$s_!INw7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbb66117-a77f-462a-b7b8-dacbc085859e_564x440.png)

This hierarchical nature makes it well-suited for representing complex or semi-structured data, a capability that CSV lacks. Additionally, JSON has native support for various [data types](https://www.json.org/json-en.html) by enforcing a set of rules:

* **Boolean:** Represented by two keywords: `true` or `false`.
* **Null:** unquoted keyword `null`
* **String:** A sequence of zero or more Unicode characters enclosed in double quotes. For example: `"hello"`.
* **Number:** A signed decimal number, possibly with a fraction and/or exponent. Examples: `123`, `-3.14`, `2.5e-2`.
* **Object:** An unordered collection of key-value pairs, where keys are strings and values can be any JSON data type. Objects are enclosed in curly braces { }. For example: `{"name": "Clark", "age": 26}`.
* **Array:** An ordered list of JSON values, which can be of different types. Arrays are enclosed in square brackets [ ]. For example: `[1, "apple", true, null]`.

JSON's strength is its flexibility. It does not require a predefined schema, allowing developers to easily evolve data structures and represent complex relationships.

### Challenges

However, this flexibility also imposes its own challenges:

* **Verbosity and Redundancy:** Every single record repeats the attribute keys, leading to redundancy. This significantly increases storage footprint and network transfer costs.

  [![](https://substackcdn.com/image/fetch/$s_!IqOD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdab9dcbf-f320-469b-a7f2-30fd7966ad40_490x328.png)](https://substackcdn.com/image/fetch/$s_!IqOD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdab9dcbf-f320-469b-a7f2-30fd7966ad40_490x328.png)
* **Slow Parsing:** JSON allows objects and arrays to be nested within one another, which means that parsers must use a recursive approach most of the time to traverse the structure.

  [![](https://substackcdn.com/image/fetch/$s_!IQvb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b5af2d6-5e10-4220-9fa4-f691be9a00f6_800x476.png)](https://substackcdn.com/image/fetch/$s_!IQvb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b5af2d6-5e10-4220-9fa4-f691be9a00f6_800x476.png)

  + For an object, the parser processes all of its children; if a child is another object, the parser must recursively jump into that object and process its children, and so on.
  + This process incurs computational overhead for each level of nesting, as the parser must manage the context and state of each layer within the hierarchy. The deeper your JSON data is, the more overhead the parser must have.
* **No schema:** Like CSV, standard JSON lacks native support for schema enforcement. However, clients can leverage [JSON Schema](https://json-schema.org/), an external vocabulary, to validate the structure of JSON data.
* **Not good for analytics**: Like CSV, fields from the same record are stored close together, making it not ideal for analytics workload.
* **Hard to parallelize**: A standard JSON file, especially one that contains a large array of objects, is treated as a single, continuous document.

  [![](https://substackcdn.com/image/fetch/$s_!gvzb!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47f31fd7-7f3a-4ce7-9b70-dbb0c7e2da33_990x232.png)](https://substackcdn.com/image/fetch/$s_!gvzb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47f31fd7-7f3a-4ce7-9b70-dbb0c7e2da33_990x232.png)

  + To be parsed correctly, the entire structure—from the opening bracket `[` to the closing bracket `]`—must be read and understood. With a standard JSON file, a worker can't simply start reading from the middle of the file because it lacks the context of the preceding structure.
  + With a JSON variant called **Newline Delimited JSON (NDJSON)**, each line is a complete, self-contained JSON object (like how a record is represented in CSV). This structure enables each line to be processed independently, allowing it to be handled by multiple workers.

---

## Avro

### Characteristics

Now we come to the binary formats.

Apache Avro is a data serialization framework that originated within the Apache Hadoop ecosystem. It is a **row-oriented** format with language-independent **schema definition**. Avro supports [more data types than JSON](https://avro.apache.org/docs/1.11.1/specification/#primitive-types), which also includes complex types such as unions, Enums, or Maps.

It is optimized for data exchange and serialization with the ability to evolve schema over time, making it the dominant format for streaming data pipelines, particularly with Apache Kafka. Avro is also leveraged for the optimized write workload, such as [Hudi log files](https://hudi.apache.org/tech-specs/).

### Schema evolution

The schema is typically defined using JSON, while the data is in binary format. Avro doesn't store the field names in every record. It just stores the values in the order defined by the schema. As a result, the data part is more compact, reducing the storage footprint and network transfer overhead.

[![](https://substackcdn.com/image/fetch/$s_!w-3k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf45c8b7-4ff0-4605-b3f9-83b5cfe9d75a_838x608.png)](https://substackcdn.com/image/fetch/$s_!w-3k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf45c8b7-4ff0-4605-b3f9-83b5cfe9d75a_838x608.png)

When writers want to write Avro data, they do so with a known schema, which is referred to as the writer’s schema. When the readers want to read Avro data, they expect the data to follow a schema, which is referred to as the reader’s schema. The key is that these two schemas don’t need to be exactly the same; they must only be compatible.

[![](https://substackcdn.com/image/fetch/$s_!zZUR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63d180b8-5b0a-4c11-a5ce-510c88df695c_922x324.png)](https://substackcdn.com/image/fetch/$s_!zZUR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63d180b8-5b0a-4c11-a5ce-510c88df695c_922x324.png)

When the reader reads the data, Avro attempts to resolve the conflict between the writer's and reader's schemas, then it translates the data using the writer’s schema into one that conforms to the reader’s schema. [For schema resolution, you can refer to Avro’s official documentation for more details](https://avro.apache.org/docs/1.11.1/specification/#call-format).

### Parallel processing

An Avro data file is designed to be easily processed in parallel. Let’s dive into the way it organizes data in more detail:

[![](https://substackcdn.com/image/fetch/$s_!efkS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F365321c7-4d86-4162-9c9d-3570a0c28137_554x314.png)](https://substackcdn.com/image/fetch/$s_!efkS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F365321c7-4d86-4162-9c9d-3570a0c28137_554x314.png)

* **File Header**: An Avro file begins with a header that contains the schema for the data stored in the file. This ensures that any process reading the file is aware of the data's structure.
* **Data Blocks**: Following the header, there is a series of data blocks. Each block is compressed independently. Each block consists of the object count, the size of those objects, and the objects themselves.
* **Sync Markers**: There are **[16-byte sync markers](https://avro.apache.org/docs/1.11.1/specification/)** [that separate each data block](https://avro.apache.org/docs/1.11.1/specification/). This marker is a randomly generated sequence of bytes that is unique to the file and is stored in the file header.

Thanks to these sync markers, readers can split the files into multiple parts for parallel processing, as each worker can handle a set of data blocks.

[![](https://substackcdn.com/image/fetch/$s_!6J8H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2ea7033-f22c-47c4-9358-d75662d07e28_778x504.png)](https://substackcdn.com/image/fetch/$s_!6J8H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2ea7033-f22c-47c4-9358-d75662d07e28_778x504.png)

From the official [Avro document](https://avro.apache.org/docs/1.11.1/specification/):

> *Objects are stored in blocks that may be compressed. Syncronization markers are used between blocks to permit efficient splitting of files for MapReduce processing.*

Additionally, Avro utilizes block size, object counts, and sync markers to detect block corruption and ensure data integrity.

### Disadvantages

The most obvious disadvantage of Avro is that its row-oriented format is not suitable for analytics workload.

---

## Parquet

### Characteristics

Parquet is a binary format that was designed with analytics workloads in mind.

> *The analytics workload only requires a subset of columns most of the time, and query performance relies mostly on the amount of skipped data.*

It stores data in a hybrid format, where the data is first horizontally divided into portions called “row groups.” Within each group, column data is stored in close proximity. This allows the query engine to read only the required row groups and columns, significantly reduce I/O.

[![](https://substackcdn.com/image/fetch/$s_!nAke!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3a3a597-be04-4ced-b5f5-ba4c4dbc801f_786x458.png)](https://substackcdn.com/image/fetch/$s_!nAke!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3a3a597-be04-4ced-b5f5-ba4c4dbc801f_786x458.png)

A Parquet file is composed of:

* **Row Groups:** Each row group contains a subset of the rows in the dataset. Data is organized into columns within each row group, with each column stored in a separate **column chunk**.
* **Column Chunk:** A chunk is the data for a particular column in the row group. Data for a column is stored continuously, offering an opportunity for data compression, as data in the same column may have a higher likelihood of repetition compared to data from the same row.
* **Pages:** Column chunk is further divided into pages. A page is the smallest data unit in Parquet. There are several types of pages, including data pages (which contain the actual data), dictionary pages (which contain dictionary-encoded values), and index pages (used for faster data lookup).

Like Avro, Parquet is also a self-contained format in which the schema and other metadata are stored inside the file.

[![](https://substackcdn.com/image/fetch/$s_!sbOD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c45841e-3344-4d00-8fbf-a519e3e4a8cf_956x452.png)](https://substackcdn.com/image/fetch/$s_!sbOD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c45841e-3344-4d00-8fbf-a519e3e4a8cf_956x452.png)

* **Magic number**: The magic number is a specific sequence of bytes (`PAR1`) located at the beginning and end of the file. It is used to verify whether it is a valid Parquet file.
* **FileMetadata:** Parquet stores FileMetadata in the footer of the file. This metadata provides information like the number of rows, data schema, and row group metadata. Each row group metadata contains information about its column chunks (ColumnMetadata), including the encoding and compression scheme, size, page offset, minimum and maximum values of the column chunk, and other relevant details. The application can utilize the information in this metadata to eliminate unnecessary data.
* **PageHeader:** The page header metadata is stored with the page data and includes information such as value, definition, and repetition encoding. Parquet also stores definition and repetition levels to handle nested data. The application uses the header to read and decode the data.

You can check the [Parquet official documentation for more details](https://parquet.apache.org/docs/file-format/metadata/).

### Schema evolution

Parquet enables us to modify the schema of our data over time without requiring the rewriting of existing data. These are non-breaking changes that are generally safe to make

* **Adding a New Column:** This is the most common and safest change. Old files that don't have the new column will simply return `null` for that column when queried.
* **Removing an Existing Column:** When querying the data, the client can choose not to select the old column. The data for that column will remain in the old files but will be ignored by the query, which is highly efficient due to Parquet's columnar nature.
* **Reordering Columns:** The order of columns doesn't matter because Parquet reads columns by name, not by their position.
* **Renaming an Existing Column:** Renaming a column is effectively the same as deleting the old column and adding a new one. The query engine will see them as two distinct columns.

### Parallel processing

[![](https://substackcdn.com/image/fetch/$s_!jCva!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbaec397-7eef-4bf0-af51-783f9feacb6a_1668x500.png)](https://substackcdn.com/image/fetch/$s_!jCva!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbaec397-7eef-4bf0-af51-783f9feacb6a_1668x500.png)

#### Row Group-Level Parallelism

As discussed, Parquet data is horizontally partitioned into **row groups**. A row group contains a set of rows from the dataset.

Since each row group is an independent unit within the file, a processing engine can assign different tasks or threads to read multiple row groups from the *same file* in parallel.

#### Column Chunk-Level Parallelism

The parallel reading can also happen at the column chunks level. Different workers can be assigned to read different chunks concurrently within the same row group.

### Disadvantages

Parquet’s hybrid format is ideal for analytics; read operations can rely on metadata to skip unneeded data portions (row groups or columns). However, it is slower at write operations compared to row-oriented formats like Avro or JSON, as Parquet requires writing data in multiple columns separately in a row group.

Compared to the columnar format, where column data is completely separated into different files, a hybrid format like Parquet maintains the locality of data within the same record by storing it in the same row group. This helps the writing process of the hybrid format faster than the columnar format.

However, it can’t beat the advantage of a row-oriented format when data from the same record is written continuously, without jumping around.

---

## Outro

In this article, we first explore the CSV format, which is the most human-friendly due to its text-based nature and simple scheme; however, its downside is that it is error-prone, lacking support for data types and schema enforcement.

Then we explore the next text-based format, JSON. Compared to CSV, it supports data types, as well as nested and repeated data. The format is also human-readable. However, it might have a high overhead in the parsing process and is not splittable.

Next, we explore the binary formats, starting with Avro. It decouples the schema (JSON) from the data (binary). It also decouples the reader and writer schema to provide excellent schema evolution. Compared to the above text-based format, Avro is more lightweight. Avro file is splittable thanks to the implementation of the sync marker.

We conclude this article with Parquet, the one designed for analytics-intensive reading workloads. Data in this format is divided into row groups; in each group, column data is stored close together. This nature helps the query engine effectively skip unwanted data portions. Parquet also supports schema evolution and is splittable by default. However, compared to the row-oriented format, Parquet can’t bear the write operation speed.

Now, see you next time.

---

## Reference

[1] Vaishnav Manoj, [JSON is incredibly slow: Here’s What’s Faster!](https://medium.com/data-science-community-srm/json-is-incredibly-slow-heres-what-s-faster-ca35d5aaf9e8) (2023)

[2] [Avro Documentation](https://avro.apache.org/docs/)

[3] Martin Kleppmann, Chapter 4, JSON, XML, and Binary Variants section, [Designing Data-Intensive Applications](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)

[4] Martin Kleppmann, Chapter 4, Avro Section, [Designing Data-Intensive Applications](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) (2017)

[5] [Parquet Official Docs](http://parquet.apache.org/docs/)

[6] Michael Berk, [Demystifying the Parquet File Format](https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705) (2022)

[7] [fastparquet source code GitHub repo](https://github.com/dask/fastparquet)
