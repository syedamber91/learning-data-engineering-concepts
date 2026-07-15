---
title: "I spent 8 hours learning about vector databases"
channel: vutr
author: "Vu Trinh"
published: 2025-11-11
url: https://vutr.substack.com/p/i-spent-8-hours-learning-about-vector
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Lakehouse"]
tags: [https, auto, vector, image, good, substackcdn]
---

# I spent 8 hours learning about vector databases

*From their typical workload, how it stores to how it serves the data*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-about-vector)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[lakehouse|Lakehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=177093996)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!UwnL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F541d9adb-cf12-41ca-a158-dcd81718955f_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!UwnL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F541d9adb-cf12-41ca-a158-dcd81718955f_2000x1428.png)

---

## Intro

Cursor, Gemini, ChatGPT, and many other AI tools are dominating the world.

They work and serve humans based on existing data. And, the data must be stored somewhere so that the LLM models behind these applications can access it. The database seems a strong candidate, just like your company backend needs to be stateful with the help of a transactional database.

However, traditional OLTP and OLAP databases are not designed to work with AI.

A new kind of database is emerging.

In this article, we will explore vector databases, the data management systems designed for AI workloads. At the end of this article, you will understand the general idea and fundamentals of a vector database.

## Vector embedding

Since the early 2000s, the speed of data proliferation has not slowed down. It’s not only about the volume, but also the variety of the data; from documents, text, images, to videos, the demand is not only to collect and analyze tabular data, but also the unstructured one.

[![](https://substackcdn.com/image/fetch/$s_!HFRw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c010e9b-1bbb-4142-b84f-bdbccb60f9bb_702x154.png)](https://substackcdn.com/image/fetch/$s_!HFRw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c010e9b-1bbb-4142-b84f-bdbccb60f9bb_702x154.png)

Then comes the AI era, the time when we speak to Gemini or ChatGPT more than we spend time with our friends. Increasingly, companies want to feed data to LLM models, hoping to receive valuable insights in return. The thing is, these models don’t see the image or the videos the way we do.

[![](https://substackcdn.com/image/fetch/$s_!CQb9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8715da7b-2d37-4962-a198-6edb76ecb5d7_484x220.png)](https://substackcdn.com/image/fetch/$s_!CQb9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8715da7b-2d37-4962-a198-6edb76ecb5d7_484x220.png)

There must be a translator.

That’s where vector embedding shines. It translates complex, “unstructured” data—like a word, a sentence, a picture, or a song—into a list of numbers (a “vector”).

A simple text like: “The quick brown fox”

[![](https://substackcdn.com/image/fetch/$s_!HxCy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb12782da-37fb-4043-82d9-d54509035bcb_1060x206.png)](https://substackcdn.com/image/fetch/$s_!HxCy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb12782da-37fb-4043-82d9-d54509035bcb_1060x206.png)

Can be vectorized into a list of floating point numbers like this via specialized machine learning models: [0.12, -0.45, 0.98, ..., -0.22]

The cool thing is that this list of numbers (which can be hundreds or thousands of items long) captures the **semantic meaning** or **context** of the original data.

[![](https://substackcdn.com/image/fetch/$s_!blY8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fbdacaf-1d62-4297-b8b3-f3b5c43227eb_306x104.png)](https://substackcdn.com/image/fetch/$s_!blY8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fbdacaf-1d62-4297-b8b3-f3b5c43227eb_306x104.png)

A number is called a dimension; each is used to represent an aspect of the data. For example, the first dimension provides information about the color, the second tells us about the shape, and so on.

By representing the data in vector embedding, we can map the data in a high-dimensional “meaning space,” and use some mathematical magic to check the closeness of the data; for example, the vectors for “king” and “queen” would be very close to each other. The vector for “apple” and “orange” would also be close. But the vector for “king” would be very far away from the vector for “apple.”

[![](https://substackcdn.com/image/fetch/$s_!SMh3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F272840be-b8eb-417b-a062-97d502a23c61_532x460.png)](https://substackcdn.com/image/fetch/$s_!SMh3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F272840be-b8eb-417b-a062-97d502a23c61_532x460.png)

A simplified “meaning space“ with three dimensions. I don’t think I can draw a diagram with more than three dimensions.

Now, LLM models can understand the semantics of our data and can query for the related data based on the input. That fundamental backs a lot of use cases, from classification and clustering to recommendation engines and semantic search, as well as how ChatGPT or Gemini answers your questions.

[![](https://substackcdn.com/image/fetch/$s_!QNbT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5157f9c9-6341-4314-9a90-e56d57417dac_490x258.png)](https://substackcdn.com/image/fetch/$s_!QNbT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5157f9c9-6341-4314-9a90-e56d57417dac_490x258.png)

It’s no exaggeration to say the ability to store and retrieve vector embedding efficiently is the backbone of AI workloads.

## Vector databases

Because of that trend, more systems have emerged to give that ability. Some choose to build a dedicated vector database from scratch, such as [Weaviate](https://weaviate.io/). Others build a system to serve both vector embedding and traditional analytics workloads, such as [LanceDB](https://lancedb.com/). Some choose to extend an existing system with new capabilities, such as [pgvector](https://github.com/pgvector/pgvector).

[![](https://substackcdn.com/image/fetch/$s_!a9Br!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff20eb4fd-2a7a-40dd-860c-ffe7a4a81348_778x282.png)](https://substackcdn.com/image/fetch/$s_!a9Br!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff20eb4fd-2a7a-40dd-860c-ffe7a4a81348_778x282.png)

Despite the difference in how they approach, all the vendors try to offer two things:

* The ability to efficiently store vector embedding
* The ability to efficiently do neighbor search (input’s related vectors)

I believe three aspects need to be discussed here:

* How is the data stored? Does the vector system use row or column format?
* How does the system do the neighbor search, and what techniques can make it faster?
* Space efficiency when storing vector embedding data.

## How is the data stored?

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=177093996)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

As you might know, in a database management system, there are three main approaches to physically organizing the data: row, column, and hybrid.

The row stores all data for a row together, while the column stores data for a column separately. The hybrid approach also organizes data similarly to the column; however, data from the same row is kept close together in the concept of row groups.

[![](https://substackcdn.com/image/fetch/$s_!x0I2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60547560-632f-4024-96f6-a60feadb252d_1160x336.png)](https://substackcdn.com/image/fetch/$s_!x0I2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60547560-632f-4024-96f6-a60feadb252d_1160x336.png)

It is widely known that row format is best suited for OLTP, and the other two work well in OLAP.

OLTP workloads typically require point lookup, random access, and reading the entire row at a time; the row format can accommodate this. With the help of a point-lookup index, such as BTree, the query performance can be significantly boosted.

[![](https://substackcdn.com/image/fetch/$s_!JJTY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb76b7877-237d-428d-8849-917059a483b3_1172x442.png)](https://substackcdn.com/image/fetch/$s_!JJTY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb76b7877-237d-428d-8849-917059a483b3_1172x442.png)

On the other hand, OLAP requires processing large-scale data, but only a few columns are needed; column and hybrid approaches could be beneficial in this context. Skipping unneeded columns helps save I/Os.

A point-lookup index is useless here; maintaining a min-max index is preferred, as the ultimate goal is to limit the amount of data as much as possible when workers scan data to prepare for query processing.

So, I asked myself: which approach does vector embedding choose?

### The row

Recall that the typical workload related to vector embedding is to find related vectors based on the input vector. The result is usually required to be a whole, the complete document, or the image with associated metadata.

[![](https://substackcdn.com/image/fetch/$s_!xIJW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F270a66cc-dc24-4a83-bd9a-25292c5417e6_560x252.png)](https://substackcdn.com/image/fetch/$s_!xIJW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F270a66cc-dc24-4a83-bd9a-25292c5417e6_560x252.png)

That said, the row store format is a good fit here. All the data, alongside the vector embedding, are stored closely together. The search operation is carried out based on the column that stores the vector embedding, and the matching results are returned by simply loading the entire record and sending it to the client.

Many vector databases choose this approach.

Weaviate stores data as a key-value store and leverages the [LSM](https://vutr.substack.com/i/173554718/log-structured-storage) tree as the storage engine. In this architecture, data regarding updates, insertions, or deletions is first written sequentially into a structure in memory called a Memtable.

[![](https://substackcdn.com/image/fetch/$s_!zYE_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42969474-60fa-4dba-a93b-ff8f1972b671_1038x850.png)](https://substackcdn.com/image/fetch/$s_!zYE_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42969474-60fa-4dba-a93b-ff8f1972b671_1038x850.png)

When the memtable reaches a specific size, it is written to disk. The data from the Memtable is written out as a new, **immutable (read-only)**, sorted file called an SSTable. These SSTables are then later compacted on disk to produce larger SSTables, which improves the read performance.

[ChromaDB](https://github.com/chroma-core/chroma) also leverages SQLite, a row-oriented database engine behind the scenes. The cool thing is that ChromaDB decided to go with DuckDB, an OLAP system with column store at first, but they [had to admit that an OLTP-style system](https://github.com/chroma-core/chroma/issues/1133) is more suitable for their need.

### The column/hybrid

Random access and reading a record as a whole make row-store a strong approach to implement a vector database.

But here is the thing.

Most of the time, the end-users of the vector database are data scientists. They also need to handle other workloads, such as the traditional analytic ones, and nothing can beat an OLAP database at this type of workload.

So they have two databases to work with.

Recognizing these challenges, some vendors, such as LanceDB, offer a multi-purpose solution that enables users to perform both vector and traditional analytics workloads. The key is that their database is built on a brand new columnar format.

[![](https://substackcdn.com/image/fetch/$s_!FBYD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb401960-bd7c-4f85-8fac-b9cf6ed48d08_808x408.png)](https://substackcdn.com/image/fetch/$s_!FBYD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb401960-bd7c-4f85-8fac-b9cf6ed48d08_808x408.png)

The rise of the lakehouse paradigm imposes another challenge; standard columnar file formats, such as Parquet, don’t work well with vector embedding. Parquet is problematic for random access, and wide columns (such as those that store vector embeddings) make it difficult to adjust the row-group size.

[![](https://substackcdn.com/image/fetch/$s_!R9X4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F961a0911-510d-41b9-b73e-7147c0fe89d0_796x376.png)](https://substackcdn.com/image/fetch/$s_!R9X4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F961a0911-510d-41b9-b73e-7147c0fe89d0_796x376.png)

If users want better performance on vector workloads, they must load the data into a dedicated vector database, which eliminates one of the key properties of the lakehouse paradigm: shared storage, so users can use any query engine.

That’s one of the reasons why many new columnar formats are introduced.

[Lance from LanceDB](https://github.com/lancedb/lance)

[Nimble from Meta.](https://github.com/facebookincubator/nimble)

[F3 from famous researchers.](https://github.com/future-file-format/F3)

All of them are trying to offer a new columnar format that will outperform Parquet in vector or AI workloads in general.

So, to answer the question: which approach does vector embedding choose?

My answer at the moment is that it depends on your system. The vector database is a new system compared to OLTP and OLAP databases; time is needed to determine the best approach for this new kind of database.

## The index

As discussed, the primary workload in a vector database is searching for similar vectors.

The most straightforward way to do this is to use the input vector, compare it one by one to every vector stored in the database using a mathematical tool, such as Euclidean distance, and output the matched vectors.

[![](https://substackcdn.com/image/fetch/$s_!kh2T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc5f05f8-8cd4-40d4-8dae-7b23c3fd2235_932x468.png)](https://substackcdn.com/image/fetch/$s_!kh2T!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc5f05f8-8cd4-40d4-8dae-7b23c3fd2235_932x468.png)

This actually works and is implemented in vector databases. It works if the number of vectors is not too large. However, if you have 10 million vectors, things gonna slow down as the algorithm is O(n) where n is the number of vectors.

To address this, a well-known approach utilizes an index to facilitate the search. However, this index is not what we are familiar with in OLTP and OLAP systems; it leverages the approximate nearest neighbor (ANN) approach to help with the vector workload.

[![](https://substackcdn.com/image/fetch/$s_!3a4S!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2554f9e-35fd-4070-ba44-02187b9edd58_1072x200.png)](https://substackcdn.com/image/fetch/$s_!3a4S!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2554f9e-35fd-4070-ba44-02187b9edd58_1072x200.png)

The core idea is to pre-calculate the distances between the vectors; then, the system can organize those that are close together using graphs or clusters. When searching, the system can skip vectors that are far apart, thereby reducing the search space. In return, the result will be slightly different compared to the brutal approach.

As I researched, two key approaches to approximate nearest neighbor are most commonly implemented in vector databases. Due to my limited mathematical knowledge, I will only grasp the high-level idea of these two approaches. Also, we won’t discuss the pros and cons of each approach in this article.

### Graph Based

The general idea is to construct a **graph** where each vector is a node. An edge (a link) is created between a node and its closest neighbors. When you search, you don’t check every vector; you “walk” this graph. You start at an entry point and greedily jump from node to node, always moving to the neighbor that is closest to your query vector, until you can’t find a closer one.

[![](https://substackcdn.com/image/fetch/$s_!4ddS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bec454c-f3cb-40e2-9230-c5d957ef4e85_574x238.png)](https://substackcdn.com/image/fetch/$s_!4ddS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bec454c-f3cb-40e2-9230-c5d957ef4e85_574x238.png)

The most common approach in the graph-based method is the HNSW (Hierarchical Navigable Small World). HNSW builds *multiple layers* of graphs, like a highway system. The top layer is very sparse, with only a few nodes and long-distance links. The bottom layer is a dense graph that connects all the vectors.

[![](https://substackcdn.com/image/fetch/$s_!jCFW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd443c254-2002-4894-b44d-d979c24e6edd_674x428.png)](https://substackcdn.com/image/fetch/$s_!jCFW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd443c254-2002-4894-b44d-d979c24e6edd_674x428.png)

When a search begins, the system starts at the top-most layer.

It quickly navigates this sparse graph to find the *approximate region* of the query. Once it finds the best point in that layer, it “drops down” to the next layer below, using the previous point as the starting position.

It refines its search on this denser graph and repeats the process, dropping layer by layer until the system reaches the bottom layer and finds the nearest vectors.

### Spatial Partitioning

This approach tries to put data into “partitions“. Each vector is stored near other vectors in the same partition. A point identifies a partition, usually the centroid of all the vectors in that partition. To clarify this point, some mathematical concepts are necessary.

[![](https://substackcdn.com/image/fetch/$s_!-hVu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1a3f4ff-a5c0-4eda-84b6-31859665adb8_658x572.png)](https://substackcdn.com/image/fetch/$s_!-hVu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1a3f4ff-a5c0-4eda-84b6-31859665adb8_658x572.png)

When the query is received, the system first identifies the closest representative point to the inputs and then loads the associated partitions to locate the related vectors.

[![](https://substackcdn.com/image/fetch/$s_!xX5E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d58eb12-5147-430f-89b9-458eee25f07f_880x626.png)](https://substackcdn.com/image/fetch/$s_!xX5E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d58eb12-5147-430f-89b9-458eee25f07f_880x626.png)

## A typical vector query life cycle

After learning some fundamentals of a vector database. We can imagine the query life cycle of a vector database will look like this:

[![](https://substackcdn.com/image/fetch/$s_!7W6l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52b70853-a792-4b52-97c9-0056b0717866_1162x846.png)](https://substackcdn.com/image/fetch/$s_!7W6l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52b70853-a792-4b52-97c9-0056b0717866_1162x846.png)

* Raw data goes through a model so it can be encoded in a vector embedding.
* The embedding is stored in the database; the system can use the new data to build or adjust the ANN index.
* The new query comes.
* The input must also be represented as vectors.
* Similar to traditional databases, the query may go through initial parsing and validation
* The optimizer then generates a plan.
* Next, the system uses the query vector to search the indexed vectors in the database
* Closest vectors are found
* Once potential candidate vectors are retrieved, post-processing steps may occur, such as ranking the output vectors based on their similarity to the query vector

## Compression

Retrieving vectors is complex; we need the help of the ANN index as discussed.

However, storing vectors has its own problems.

Imagine a tiny piece of text, such as “the red fox” (11 bytes, giving ASCII characters, requiring 1 byte in UTF8), being fed into an embedding model, and the resulting 1536-dimensional output vector is stored in the database.

A standard 32-bit floating-point number (FP32) requires **4 bytes** of storage.

Total space per vector = 4 bytes \* 1536 ~= 6KB.

That is a > 500x storage blow-up (6,000 / 11).

You might say 6 KB is nothing. But what if you’re indexing Wikipedia, every tweet ever, or your company’s entire document library?

* 1 billion vectors \* 6 KBs/vector = 6, 000,000,000,000 bytes
* That’s 6 TB of disk space.

**Vector Quantization (VQ)** is the core compression in vector databases. Instead of encoding the vector using 4 bytes (32 bits) for each number (dimension), VQ uses a smaller number of bits (such as 8 bits) to represent the floating number. Some quantizationtechniques also try to reduce the number of dimensions of the vector.

**Product Quantization** is a popular method for **Vector Quantization.**

First, the system will take your massive 1536-dimensional vector and chop it into, say, 32 smaller, independent 48-dimensional sub-vectors.

[![](https://substackcdn.com/image/fetch/$s_!0izs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19245748-705a-45e8-8fde-8931c26f3a44_1316x740.png)](https://substackcdn.com/image/fetch/$s_!0izs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19245748-705a-45e8-8fde-8931c26f3a44_1316x740.png)

After that, the system will train (applying a clustering algorithm such as k-means) to define a fixed number of centroids for sub-vectors. The centroids make up a codebook. Then, each sub-vector is assigned to its nearest centroid in the codebook.

[![](https://substackcdn.com/image/fetch/$s_!1VLO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16ad6f1-2077-45c8-9cce-240d4a7cffcb_1152x438.png)](https://substackcdn.com/image/fetch/$s_!1VLO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb16ad6f1-2077-45c8-9cce-240d4a7cffcb_1152x438.png)

A sub-vector is now represented as the centroid index in the codebook. The whole vector is now a concatenated code of indices.

## Outro

In this article, we first explore what vector embedding is; from that, we understand the motivation for the new kind of database. We then try to answer whether vector embedding data is stored in row or column format. Next, we highlight the importance of ANN indexing in vector databases for facilitating related vector searches.

Finally, we explore the challenges of storing vector embedding data, as simple text can occupy more than 500 times the space when encoded as a vector. From that, we learn about vector quantization, with product quantization being a common approach.

Thank you for reading this far, see you in future articles (about vector database again)

## Reference

*[1] Brian Hentschel, Xian Huang, [A Developer’s Guide to Approximate Nearest Neighbor (ANN) Algorithms](https://www.pinecone.io/learn/a-developers-guide-to-ann-algorithms/) (2024)*

*[2] Weaviate Documentation, [Compression (Vector Quantization)](https://docs.weaviate.io/weaviate/concepts/vector-quantization)*

*[3] [A Comprehensive Survey on Vector Database: Storage and Retrieval Technique, Challenge](https://arxiv.org/pdf/2310.11703)*
