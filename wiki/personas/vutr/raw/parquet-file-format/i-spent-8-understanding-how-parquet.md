---
title: "I spent 8 hours understanding how Parquet actually stores the data."
channel: vutr
author: "Vu Trinh"
published: 2025-11-04
url: https://vutr.substack.com/p/i-spent-8-understanding-how-parquet
paid: true
topics: ["Data Engineering", "BigQuery", "Lakehouse"]
tags: [https, auto, parquet, substackcdn, image, fetch]
---

# I spent 8 hours understanding how Parquet actually stores the data.

*From logical data representation to data encoding and compression.*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-understanding-how-parquet)

## Topics

[[data-engineering|Data Engineering]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]]

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

[![](https://substackcdn.com/image/fetch/$s_!1vnV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7230b1b-4336-4153-a2ee-d001b0f8fb4b_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!1vnV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7230b1b-4336-4153-a2ee-d001b0f8fb4b_2000x1428.png)

---

## Intro

Parquet has become the standard file format in modern data analytics, thanks to its efficiency in both storage and query performance.

Everybody knows about Parquet's columnar layout, but few know how data is physically stored, especially how it is encoded and compressed. In this article, I will provide a deep dive into Parquet’s encoding capabilities, from its type system to how data is represented based on each type.

## The row groups and column chunks

The Parquet format organizes data using the Partition Attributes Across (PAX) layout, commonly referred to as the hybrid format. It first groups data into “row groups,” each containing a subset of rows. (horizontal partition.)

[![](https://substackcdn.com/image/fetch/$s_!8HJW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43dffdc5-b343-4b57-bd39-0ed426d2dbce_636x462.png)](https://substackcdn.com/image/fetch/$s_!8HJW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43dffdc5-b343-4b57-bd39-0ed426d2dbce_636x462.png)

Within each row group, data is stored column by column; values from a column are stored together. Each row group’s column is called the column chunk. Each chunk is composed of pages, which are the unit for encoding and compression.

Because data from the same column are stored back-to-back within a chunk, values of the same type remain close together. In addition, data in the same column tend to be more homogeneous and repetitive, which significantly benefits the encoding and compression processes, as these rely on data patterns.

[![](https://substackcdn.com/image/fetch/$s_!Oi3y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cb04281-7152-4fc3-a396-e12abf5a4cc9_560x236.png)](https://substackcdn.com/image/fetch/$s_!Oi3y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cb04281-7152-4fc3-a396-e12abf5a4cc9_560x236.png)

Before diving into these processes, we will first explore Parquet’s type system, as the input column’s type largely impacts the encoding and compression schemes.

## Type systems

Parquet distinguishes between logical and physical types:

[![](https://substackcdn.com/image/fetch/$s_!B33x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0776a4a5-5c87-493a-9921-a1f0dee8614a_496x106.png)](https://substackcdn.com/image/fetch/$s_!B33x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0776a4a5-5c87-493a-9921-a1f0dee8614a_496x106.png)

* **Logical Type:** What the data **semantically means**.
* **Physical Type:** How the data is **physically stored** on disk.

### Physical

These are the **only** few types Parquet actually knows how to write to a file. The creator keeps the options small to make the implementation of the Parquet reader and writer simpler:

* `BOOLEAN`: A single-bit true/false value.
* `INT32`: A 32-bit signed integer.
* `INT64`: A 64-bit signed integer.
* `FLOAT`: A 32-bit floating-point number.
* `DOUBLE`: A 64-bit floating-point number.
* `BYTE_ARRAY`: A variable-length array of raw bytes.
* `FIXED_LEN_BYTE_ARRAY`: A fixed-length array of raw bytes.
* `INT96`: (Deprecated) A 96-bit integer, primarily used for legacy timestamp formats.

The encoding and compression only work with physical types.

### Logical

However, your application might need to be represented with a richer type system. Parquet supports [logical types](https://github.com/apache/parquet-format/blob/master/LogicalTypes.md), which are wrappers around physical types with additional metadata to help the engine interpret the bytes correctly.

For example, a `STRING` is stored as a `BYTE_ARRAY`; the raw bytes are interpreted as a UTF-8-encoded string. A `DATE` logical type annotates an `INT32` that stores the number of days from the Unix epoch.

## Encoding scheme

### PLAIN

This scheme is the most straightforward. It serializes values back-to-back in a standardized, little-endian binary format with no complex transformations. `PLAIN` must be supported for all physical types defined in the Parquet specification.

* BOOLEAN: 1 bit per value, zero is false; one is true.
* INT32: 4 bytes each value.
* INT64: 8 bytes each value.
* FLOAT: 4 bytes each value.
* DOUBLE: 8 bytes each value.
* BYTE\_ARRAY: The length is stored in 4 bytes, followed by bytes.
* FIXED\_LEN\_BYTE\_ARRAY: it simply stored as bytes

This encoding is the default choice when no other scheme offers a clear advantage. It is best suited for data that lacks patterns, such as columns with high cardinality (many unique values), randomness, or unpredictability.

### RLE\_DICTIONARY

This one is one of Parquet’s most commonly used encodings. The writer first scans the data in a column chunk to build a “dictionary” of all unique values. This dictionary is stored once in a dedicated dictionary page. This page is encoded using the PLAIN scheme.

[![](https://substackcdn.com/image/fetch/$s_!Z8Sh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a8c301b-174f-4b1f-b4f2-df231b5f4bb0_738x720.png)](https://substackcdn.com/image/fetch/$s_!Z8Sh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a8c301b-174f-4b1f-b4f2-df231b5f4bb0_738x720.png)

---

> To celebrate Lunar New Year (the true New Year holiday in Vietnam), I’m offering ***50% off the annual subscription***. The offer ends soon; grab it now to get full access to nearly 200 high-quality data engineering articles.
>
> [50% off the annual subscription](https://vutr.substack.com/subscribe)

The data page is then rewritten as a stream of small integer indices, where each integer is associated with a value’s position in the dictionary. This stream of indices is itself highly compressible and is encoded using the `RLE/Bit-Packing Hybrid` scheme (covered later).

The effectiveness of this scheme is gone as the cardinality of the column values increases. Most Parquet writers implement a fallback mechanism. If the dictionary exceeds a specific size in bytes (e.g., 1 MB) or the number of unique values surpasses a threshold, the writer will fallback to a more suitable encoding.

### RLE/Bit-Packing Hybrid

The scheme analyzes the stream of integers and dynamically switches between two modes.

* For sequences of identical, consecutive values (a “run”), it uses Run-Length Encoding (RLE), storing the value once alongside a count of its repetitions.

  [![](https://substackcdn.com/image/fetch/$s_!jmj0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e7d7314-aa98-42a9-b3fd-249b8766a7cc_352x168.png)](https://substackcdn.com/image/fetch/$s_!jmj0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e7d7314-aa98-42a9-b3fd-249b8766a7cc_352x168.png)

  + For example, instead of writing [5, 5, 5, 5, 5], it writes (store the value 5, 5 times)
* For sequences of varying integers, it uses Bit-Packing, which stores each integer using the minimum number of bits required for its range of values, rather than a fixed 32- or 64-bit width.

  [![](https://substackcdn.com/image/fetch/$s_!-jl5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33ed4c85-1d83-445d-9b1f-661a810952db_516x336.png)](https://substackcdn.com/image/fetch/$s_!-jl5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F33ed4c85-1d83-445d-9b1f-661a810952db_516x336.png)

  + For example, if numbers in a run never exceed 7 (which only requires 3 bits), it’s wasteful to use a full 32-bit integer for each one.

In a stream, if the Parquet writer sees the same value ≥ 8 times consecutively, it uses RLE; if not, it uses bitpacking.

The scheme is used for three specific cases:

* Encoding the integer streams of Repetition and Definition Levels, which are how Parquet stores semi-structured data (covered later)
* Encoding the integer indices generated by `RLE_DICTIONARY` encoding
* Encoding for `BOOLEAN` values

### DELTA\_BINARY\_PACKED

This scheme is designed for sequences of INT32 or INT64 physical types. Instead of storing the absolute values, it stores the first value of a block, followed by a stream of “deltas” (the difference between each value and the preceding one).

[![](https://substackcdn.com/image/fetch/$s_!mkMG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ba6ef0d-6aaa-4679-8132-6455309f7192_508x318.png)](https://substackcdn.com/image/fetch/$s_!mkMG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ba6ef0d-6aaa-4679-8132-6455309f7192_508x318.png)

These deltas are (hopefully) much smaller than the original integers, allowing them to be stored with fewer bits. DELTA\_BINARY\_PACKED works best on sorted data, making it perfect for columns representing event timestamps (which are often stored as `INT64` milliseconds since epoch, auto-incrementing primary keys, or any other monotonically increasing series

### DELTA\_LENGTH\_BYTE\_ARRAY

This encoding offers a clever optimization for `BYTE_ARRAY` columns by decoupling the byte array lengths from the data itself. The writer first creates a stream of all byte array lengths and encodes it using `DELTA_BINARY_PACKED`. Following this encoded length block, it concatenates the raw byte array data of all values back-to-back into a single, contiguous block.

[![](https://substackcdn.com/image/fetch/$s_!UrnR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea565b2b-5c2f-45e7-9728-033ddbbe8507_950x426.png)](https://substackcdn.com/image/fetch/$s_!UrnR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea565b2b-5c2f-45e7-9728-033ddbbe8507_950x426.png)

In `PLAIN` encoding, `BYTE_ARRAY` is always encoded with a length of 4 bytes. For columns with many short strings (e.g., “NY”, “CA”, “TX”), the engine uses more space for the lengths than for the data itself.

`DELTA_LENGTH_BYTE_ARRAY` solves the problem by storing the length information together and applying DELTA\_BINARY\_PACKED to reduce its size further.

### DELTA\_BYTE\_ARRAY

This scheme is a specialized encoding for sequences of strings that share common prefixes. For each item in a sequence of strings, the engine stores the prefix length of the previous entry plus the suffix. Let’s use a list of URLs as an example:

```
“www.google.com/search”
“www.google.com/images”
“www.google.com/maps”
“www.yahoo.com/news”
```

Here is how `DELTA_BYTE_ARRAY` would store them:

[![](https://substackcdn.com/image/fetch/$s_!W3kt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc556b5ab-0389-4b35-a7de-7a910a94cd08_636x246.png)](https://substackcdn.com/image/fetch/$s_!W3kt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc556b5ab-0389-4b35-a7de-7a910a94cd08_636x246.png)

1. **String 1:** `“www.google.com/search”`

   * As it’s the first string, there is no previous string to compare to.
   * **Prefix Length:** `0`
   * **Suffix:** `“www.google.com/search”`
2. **String 2:** `“www.google.com/images”`

   * It shares a `17`-character prefix (`“www.google.com/”`) with the previous string.
   * **Prefix Length:** `17`
   * **Suffix:** `“images”`
3. **String 3:** `“www.google.com/maps”`

   * It also shares a `17`-character prefix (`“www.google.com/”`) with the *previous* string.
   * **Prefix Length:** `17`
   * **Suffix:** `“maps”`
4. **String 4:** `“www.yahoo.com/news”`

   * It shares a `4`-character prefix (`“www.”`) with the previous string.
   * **Prefix Length:** `4`
   * **Suffix:** `“yahoo.com/news”`

This approach significantly reduces the page size, especially for pages with values that share a prefix, as shown in the example above. To further reduce the size, the prefix lengths are bunched together and encoded using `DELTA_BINARY_PACKED`. For suffix values, they are encoded with `DELTA_LENGTH_BYTE_ARRAY`.

### BYTE\_STREAM\_SPLIT

This encoding is special because it does not directly reduce data size; instead, it tries to improve the effectiveness of the later compression process.

For a fixed-width data type of N bytes (e.g., 4 for `FLOAT`, 8 for `DOUBLE`), it reorganizes the data into N separate byte streams. The first stream contains the first byte of every value, the second stream includes the second byte of every value, and so on.

[![](https://substackcdn.com/image/fetch/$s_!T4NF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facdc9113-601a-4a6a-a77e-d70131d44cc7_306x532.png)](https://substackcdn.com/image/fetch/$s_!T4NF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facdc9113-601a-4a6a-a77e-d70131d44cc7_306x532.png)

These N streams are then concatenated at the end.

With `FLOAT` or `DOUBLE` numbers:

* The **first few bytes** usually represent the **exponent** and **sign**. These bytes often have similar values or recognizable patterns (e.g., the sign bit might be `0` for a long time).
* The **last few bytes** represent the precision. These bytes tend to be much more random.

In the `PLAIN` scheme, mixing random and pattern data makes it very difficult for the compressor to detect repeating patterns. `BYTE_STREAM_SPLIT` comes to the rescue here by grouping the first few bytes with recognizable patterns together. This provides the compression process with the opportunity to compress the data effectively.

## The typical encoding process

After discovering the available encoding schema, we will see how the writer encodes a Parquet data page:

[![](https://substackcdn.com/image/fetch/$s_!zzK6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff684896c-dd77-4dc5-9a36-3d0b6823c49d_798x412.png)](https://substackcdn.com/image/fetch/$s_!zzK6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff684896c-dd77-4dc5-9a36-3d0b6823c49d_798x412.png)

* The process starts by writing the magic number at the beginning of the files, calculating the number of row groups based on the row group’s max size (configurable) and the data’s size.
* For each row group, iterate through the column list to write each column chunk for the row group.
* For each column chunk, the engine writes page by page sequentially.
* The encoding process happens here.
* **Here is the catch**: although there are many available encoding schemes, Parquet **aggressively performs dictionary encoding (RLE\_DICTIONARY) for every column type except for the BOOLEAN** one, which will be encoded using the RLE scheme instead.

  [![](https://substackcdn.com/image/fetch/$s_!KAdO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86248556-9407-4ab5-8666-3578d2184d75_506x234.png)](https://substackcdn.com/image/fetch/$s_!KAdO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86248556-9407-4ab5-8666-3578d2184d75_506x234.png)
* There are cases when dictionary encoding doesn’t work: if the distinct values exceed a certain threshold, the writer will fall back to a more suitable scheme

  [![](https://substackcdn.com/image/fetch/$s_!zoky!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F75b9b710-1020-4ac9-bf07-cf528f193193_692x398.png)](https://substackcdn.com/image/fetch/$s_!zoky!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F75b9b710-1020-4ac9-bf07-cf528f193193_692x398.png)

  + As a page is the unit of encoding, if fallback happens, the rest of the pages in a chunk will be encoded in the fallback scheme.
* **Note:** Although the Parquet’s official document stated that PLAIN encoding will always be used, the [Java Parquet](https://issues.apache.org/jira/browse/PARQUET-2221) and the [Rust Parquet](https://arrow.apache.org/rust/parquet/file/properties/struct.WriterPropertiesBuilder.html) implementations allow for falling back to other encoding schemes. (Other Parquet implementations might allow this as well; it's just that I only spent time with the Java and Rust implementations.)

  [![](https://substackcdn.com/image/fetch/$s_!bIRQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49571865-5ad8-4d4f-810c-cb07491a3f9e_1466x156.png)](https://substackcdn.com/image/fetch/$s_!bIRQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49571865-5ad8-4d4f-810c-cb07491a3f9e_1466x156.png)

  [Source](https://parquet.apache.org/docs/file-format/data-pages/encodings/)

  + For example, [in the Java implementation, INT32 and INT64 will fall back to DELTA\_BINARY\_PACKED.](https://github.com/apache/parquet-java/blob/master/parquet-column/src/main/java/org/apache/parquet/column/values/factory/DefaultV2ValuesWriterFactory.java)
* Some implementations, such as Rust, allow users to [disable dictionary encoding and specify the encoding scheme for a particular column](https://arrow.apache.org/rust/parquet/file/properties/struct.ColumnProperties.html).

### How semi-structured data is encoded

Discussing Parquet without mentioning how semi-structured data is encoded would be incomplete.

Parquet encodes semi-structured data using a technique called record shredding, inspired by the approach in Dremel, [Google BigQuery’s processing engine](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf). The approach uses two concepts: nested and repeated.

#### Nested

Imagine you have a nested field like this:

[![](https://substackcdn.com/image/fetch/$s_!FeNF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17491c1d-1e72-44b3-8dc7-77cfb48e16ca_384x292.png)](https://substackcdn.com/image/fetch/$s_!FeNF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17491c1d-1e72-44b3-8dc7-77cfb48e16ca_384x292.png)

The challenge is to store `Country` as an independent column while also preserving the hierarchical information (i.e., that it belongs to the `Person` field). The record-shredding approach has introduced the concept of ***definition level*** to deal with this. From the definition from Google:

> *Each value of a field with path p, esp. every NULL, has a definition level specifying how many fields in p that could be undefined (because they are optional or repeated) are actually present in the record.*

In simple terms, it is the maximum level at which the path is defined.

Back to the example above, consider the full path of the field `Name` is:

> `Person.Info.Name`

The definition level of `Name` in the associated scenarios:

[![](https://substackcdn.com/image/fetch/$s_!3a-n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c56c0ba-6f10-4894-89a6-64423df290d8_1090x408.png)](https://substackcdn.com/image/fetch/$s_!3a-n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c56c0ba-6f10-4894-89a6-64423df290d8_1090x408.png)

* We can see there are a total of 3 levels here: `Person, Info,` and `Name`.
* If the level `Name` has a defined value, it will have the definition level of 3.
* In case the `Name` is NULL, but we have `an Info` level defined, the definition level of `Name` is 2. Because “*the maximum level at which the path is defined*” is at `Info`, which is level 2.
* With the same logic, if both `Info` and `Name` areNULL but `Person` is defined, the definition level of `Name` is now 1.
* When the `Person` is NULL, the definition level of `Name` is0.

#### Repeated

> *Array-alike*

The problem statement here is quite similar to nested fields.

How can you store an array as an independent column while also retaining information that the values belong to the same array?

Google introduced the ***repetition level***, which is:

> *It tells us at what repeated field in the field’s path the value has repeated.*
>
> *… level 0 denotes the start of a new record.*

With the example of the repeated field like this:

> [ [1,2,3],[4,5,6] ]

Based on the definition from Google, here is the manually encoded version of that example:

[![](https://substackcdn.com/image/fetch/$s_!qI14!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7d74c29-65b0-4641-bfc0-72a373d5db62_868x630.png)](https://substackcdn.com/image/fetch/$s_!qI14!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7d74c29-65b0-4641-bfc0-72a373d5db62_868x630.png)

## Bring it together

I will borrow (again) a complete example from a [Google paper](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf) to consolidate all the knowledge above.

Given nested records R1 and R2 with the below schema:

[![](https://substackcdn.com/image/fetch/$s_!hw95!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cc44905-b7c8-4f4e-9069-d2463f7ed202_602x386.png)](https://substackcdn.com/image/fetch/$s_!hw95!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cc44905-b7c8-4f4e-9069-d2463f7ed202_602x386.png)

Following the schema, here’s what we expect from the `Forward` field:

> * `Forward` *is nested inside the* `Links`
> * `Forward` is a repeated field.

Following the definition from above, this means:

> * Definition level of `Forward` with a range from 0 to 2
>
>   + 0 if `Links` is NULL
>   + 1 if `Forward` is NULL but `Links` is not NULL
>   + 2 if `Forward` is defined
> * Repetition level of `Forward` with a range from 0 to 1:
>
>   + 0 if this is a new record
>   + 1 if it repeated.

Now, apply the rules for the below data values; now we get the result as follows (I also borrowed from the paper):

[![](https://substackcdn.com/image/fetch/$s_!pWrn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F408afc1a-cfc2-4cb2-a3f1-7dde48ebf222_718x382.png)](https://substackcdn.com/image/fetch/$s_!pWrn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F408afc1a-cfc2-4cb2-a3f1-7dde48ebf222_718x382.png)

[Source](https://www.vldb.org/pvldb/vol13/p3461-melnik.pdf)

Let’s go through this result line by line to make sure we’re on the same page:

* Value 20:

  + repetition: 0 → because it’s a new record (beginning of record 1)
  + definition: 2→ because `Forward` is defined

* Value 40:

  + repetition: 1→ because it’s repeated
  + definition: 2→ because `Forward` is defined
* Value 60:

  + repetition: 1→ because it’s repeated
  + definition: 2→ because `Forward` is defined

* Value 80:

  + repetition: 0 → because it’s a new record (beginning of record 2)
  + definition: 2→ because `Forward` is defined

With this encoding system, Google can now store nested and repeated field values efficiently while still maintaining the hierarchical and array-like information. These integer data can now be further encoded using a scheme such as RLE.

## Compression

To further reduce the size of the dictionary and data pages, the writer can compress the encoded data to achieve even more space efficiency. Parquet supports a variety of compression schemes to balance the trade-off between **compression ratio** (smaller file size) and **decompression speed (**faster decompression speed**)** from **[SNAPPY, GZIP, to ZSTD.](https://parquet.apache.org/docs/file-format/data-pages/compression/)**

Since Parquet was created, storage and network performance have improved significantly. Still, the CPUs have not. The rise of the lakehouse paradigm means more organizations are moving toward storing data in object storage, which provides high-bandwidth properties. I/Os are no longer the problem; the CPU is.

From that, there are research papers ([here](https://dl.acm.org/doi/pdf/10.1145/3749163) and [here](https://www.vldb.org/pvldb/vol17/p148-zeng.pdf)) that suggest skipping general-purpose compression; the file size might be larger, but in return, the engine doesn’t have to decompress the file before reading any more.

## Outro

In this article, we first explore the decoupling of Parquet's physical and logical type systems, then examine the encoding scheme supported by this format, and finally discuss the typical encoding process and understand that Parquet aggressively uses dictionary encoding for all columns except bool.

Next, we see how Parquet encodes semi-structured data and how the writer can further reduce the size by applying compression on the pages.

Thank you for reading this far. See you in my next article.

## Reference

*[1] [Parquet Documentation](https://parquet.apache.org/docs/)*

*[2] [Java Parquet implementation](https://github.com/apache/parquet-java)*

*[3] [Rust Parquet Implementation](https://github.com/apache/arrow-rs)*

*[4] Xinyu Zeng, Yulong Hui, Jiahong Shen, Andrew Pavlo, Wes McKinney, Huanchen Zhang, [An Empirical Evaluation of Columnar Storage Formats](https://www.vldb.org/pvldb/vol17/p148-zeng.pdf), 2023*

*[5] Xinyu Zeng, Ruijun Meng, Martin Prammer, Wes McKinney, Jignesh M, Andrew Pavlo, Huancheng Zhang, [F3: The Open-Source Data File Format for the Future](https://db.cs.cmu.edu/papers/2025/zeng-sigmod2025.pdf), 2025*
