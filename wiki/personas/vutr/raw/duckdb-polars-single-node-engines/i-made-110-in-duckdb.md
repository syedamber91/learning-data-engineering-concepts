---
title: "I made 1+1=0 in DuckDB"
channel: vutr
author: "Vu Trinh"
published: 2024-02-03
url: https://vutr.substack.com/p/i-made-110-in-duckdb
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery"]
tags: [https, duckdb, auto, image, fetch, substackcdn]
---

# I made 1+1=0 in DuckDB

*How I did it and cool stuff I found about DuckDB.*

> Source: [Open post](https://vutr.substack.com/p/i-made-110-in-duckdb)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=140881637)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

[![](https://substackcdn.com/image/fetch/$s_!QxNB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff40e1b4e-892f-489c-a9dc-776407fc71da_1456x1048.png)](https://substackcdn.com/image/fetch/$s_!QxNB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff40e1b4e-892f-489c-a9dc-776407fc71da_1456x1048.png)

---

> *TL, DR:  
> 🔵 How I made it 1+1=0 in DuckDB  
> 🔵 Some exciting things about DuckDB's internal:  
> 👉 Embedded analytics  
> 👉 Execution engine  
> 👉 File Formats  
> 👉 Vector Format  
> 👉 ACID*

---

## Intro

> *This is a 20% “How-To“ and 80% “Introduction“ article.*

When setting the title: “I made 1+1=0 in DuckDB”, I didn’t intend to make it like a click-bait.

This is actually how I started playing around with [DuckDB](https://duckdb.org/).

This idea is inspired by the [modifying operator logic in PostgreSQL database](https://www.aadhav.me/posts/pg-experiments-part-1) blog post I read months ago.

### 1+1=0, How?

[![](https://substackcdn.com/image/fetch/$s_!kLkq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3aa67f2c-c84b-4f61-8043-7225bbb68f1c_824x376.gif)](https://substackcdn.com/image/fetch/$s_!kLkq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3aa67f2c-c84b-4f61-8043-7225bbb68f1c_824x376.gif)

A GIF for more trust.

The action needed to make 1+1=0 is quite simple.

The hard part is finding the source code (C++) where the add operator is implemented.

Thanks to [Github Copilot](https://github.com/features/copilot) and half a day of sitting in front of the laptop, I finally found that [piece of code](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/operator/add.hpp#L18C1-L23C3):

[![](https://substackcdn.com/image/fetch/$s_!cA93!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb1455cf-71a6-41db-ae6e-a0f68cfccfbd_824x224.png)](https://substackcdn.com/image/fetch/$s_!cA93!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb1455cf-71a6-41db-ae6e-a0f68cfccfbd_824x224.png)

[DuckDB source code is viewed from my code editor.](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/common/operator/add.hpp#L18C1-L23C3)

Following Copilot:

> *The active selection is a struct named* `AddOperator` *that contains a templated static method called* `Operation`*. This method is designed to operate on two values of any type,* `TA` *and* `TB`*, and return a result of type* `TR`*.*

From my understanding, AddOperator is an abstract method that all the “+“operators must implement.

Knowing precisely the code, I only need to change `left + right` to `left - right`, then compile the source code to get an executable binary file.

Finally, I ran that binary file, inputting SELECT 1+1, and the result returned was 0, as I expected.

Now that’s all for my weird intro.

The following sections are some cool features of DuckDB (to me) that I discovered when playing around with this database.

---

## Embedded analytics

> *Client, server, no?*

Unlike traditional database management systems with a client-server model, DuckDB aligns itself with the philosophy of simplicity and embedded operation, drawing inspiration from the widely embraced SQLite.

From the user’s point of view, DuckDB is simply an SQL interface run beside other applications on the same computer.

DuckDb’s embedded nature eliminates the need for a separate DBMS server, seamlessly integrating the analytical database within the host process.

This eliminates the complexities of installing, updating, and maintaining separate server software.

[![](https://substackcdn.com/image/fetch/$s_!UJVo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e773545-6136-4b36-9217-aa8adc9762f5_935x616.png)](https://substackcdn.com/image/fetch/$s_!UJVo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e773545-6136-4b36-9217-aa8adc9762f5_935x616.png)

---

## Execution engine

### Vectorization

> *Amount of records being processed at a time*

Pay attention here; you might think the term “Vectorization“ will draw some connection to a vector database.

But it’s not.

Let me explain here. (From my perspective)

Unlike traditional systems like PostgreSQL, MySQL, or SQLite, which process each row sequentially behind the scenes…

[![](https://substackcdn.com/image/fetch/$s_!A8NF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f1297b2-d678-4d50-a62b-8d48d1391c6d_980x268.png)](https://substackcdn.com/image/fetch/$s_!A8NF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f1297b2-d678-4d50-a62b-8d48d1391c6d_980x268.png)

…DuckDB processes data in a vectorized style.

[![](https://substackcdn.com/image/fetch/$s_!aa0P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b9d065b-d9de-4087-9c36-36467b8e1980_981x282.png)](https://substackcdn.com/image/fetch/$s_!aa0P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b9d065b-d9de-4087-9c36-36467b8e1980_981x282.png)

Said DuckDB processes a “batch of values” at once.

This approach isn’t exclusively developed in DuckDB; the vectorized execution engine is inspired by the paper [MonetDB/X100: Hyper-Pipelining Query Execution by Peter Boncz, Marcin Zukowski, and Niels Nes.](https://www.cidrdb.org/cidr2005/papers/P19.pdf)

The paper released in 2005 points out that the “volcano“ processing model (which indicates the model where each parent operator requests a single record at a time) does not leverage the full power of modern CPUs.

The paper's authors suggest an innovative vectorization model where records are batched into a vector and processed at once; this way can enhance the performance significantly.

This paper has a very important impact on the design of many OLAP databases.

You might not notice, but BigQuery, Databricks (Photon Engine), and Snowflake all apply vectorized execution engines.

### Pull and Push

> *The direction of dataflow between internal operators.*

In the past, DuckDB’s execution model operates in a pull-based fashion.

An operator will expose a function that allows fetching a result chunk from another operator.

The parent operators will fetch result chunks from its children using this interface until it reaches a source node.

[![](https://substackcdn.com/image/fetch/$s_!5VIV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64c6a670-8caf-4a76-b761-92e9c41237a5_960x333.png)](https://substackcdn.com/image/fetch/$s_!5VIV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64c6a670-8caf-4a76-b761-92e9c41237a5_960x333.png)

Following the DuckDB author, this approach works fine at the beginning but soon encounters [some problems](https://github.com/duckdb/duckdb/issues/1583) like code duplication or operators not being able to be executed separately from the tree plan.

To solve this, DuckDB changed the model to a push-based fashion where child operators actively push their output data to the parent instead of passively waiting for the parent operators to call to emit the data.

[![](https://substackcdn.com/image/fetch/$s_!ERG_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F556ce449-1b4d-4f59-94bc-92d85abf8f8e_966x322.png)](https://substackcdn.com/image/fetch/$s_!ERG_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F556ce449-1b4d-4f59-94bc-92d85abf8f8e_966x322.png)

If you'd like to get to know more about this, you can [check here](https://www.youtube.com/watch?v=bZOvAKGkzpQ&t=1701s).

> *My intention is just an introductory blog post, so I might release another post that deep dives into the OLAP execution engine, like vectorization or push-pull dataflow, in the near future.*

To end this section, I will give you some facts about other OLAP database’s execution engine:

* OLAP databases with vectorization engines: [BigQuery](https://cloud.google.com/bigquery/?utm_source=google&utm_medium=cpc&utm_campaign=japac-VN-all-en-dr-BKWS-all-all-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_658171083000-ADGP_Hybrid+%7C+BKWS+-+BRO+%7C+Txt+~+Data+Analytics_BigQuery_bigquery_main-KWID_43700076364598924-aud-1640178259900:kwd-33969409261&userloc_1028581-network_g&utm_term=KW_bigquery&gad_source=1&acs_info=ZmluYWxfdXJsOiAiaHR0cHM6Ly9jbG91ZC5nb29nbGUuY29tL2JpZ3F1ZXJ5LyIK&gclid=CjwKCAiA5L2tBhBTEiwAdSxJX3WKEBFQ9L3715mJOUzHoTkdBdc0r42dT4_7_94519n1Mbso4TXpBBoCkGYQAvD_BwE&gclsrc=aw.ds&hl=en), [Snowflake](https://www.snowflake.com/en/), [Clickhouse](https://clickhouse.com/), [Databricks (Photon)](https://www.databricks.com/product/photon),…
* OLAP databases that apply:

  + Push-based: [Snowflake](https://www.snowflake.com/en/),…
  + Pull-based: [Databricks (Photon),](https://www.databricks.com/product/photon) [BigQuery](https://cloud.google.com/bigquery/?utm_source=google&utm_medium=cpc&utm_campaign=japac-VN-all-en-dr-BKWS-all-all-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_658171083000-ADGP_Hybrid+%7C+BKWS+-+BRO+%7C+Txt+~+Data+Analytics_BigQuery_bigquery_main-KWID_43700076364598924-aud-1640178259900:kwd-33969409261&userloc_1028581-network_g&utm_term=KW_bigquery&gad_source=1&acs_info=ZmluYWxfdXJsOiAiaHR0cHM6Ly9jbG91ZC5nb29nbGUuY29tL2JpZ3F1ZXJ5LyIK&gclid=CjwKCAiA5L2tBhBTEiwAdSxJX3WKEBFQ9L3715mJOUzHoTkdBdc0r42dT4_7_94519n1Mbso4TXpBBoCkGYQAvD_BwE&gclsrc=aw.ds&hl=en),…

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=140881637)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## File Formats

[![](https://substackcdn.com/image/fetch/$s_!JDar!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48983f0c-dc97-4554-b361-479c06a92c17_794x282.png)](https://substackcdn.com/image/fetch/$s_!JDar!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48983f0c-dc97-4554-b361-479c06a92c17_794x282.png)

DuckDB has advanced support for Parquet.

It also allows you to query Parquet files directly.

([DuckDB will recommend to you in which specific case you should query directly on the Parquet file and in which case you need to load the data to its storage](https://duckdb.org/docs/guides/performance/file-formats#reasons-for-querying-parquet-files))

DuckDB suggests working with Parquet files with row groups of 100K-1M rows each to achieve better parallelized performance.

The reason for this is that DuckDB can only parallelize over row groups, so if a Parquet file has a single giant row group, it can only be processed by a single thread.

DuckDB can also parallelize across multiple rows of groups that belong to various Parquet files.

It’s best practice to have at least as many total row groups across all files as there are CPU threads.

For example, with a computer having 5 threads, in both cases when 5 files with 1 row group or 1 file with 5 row groups will achieve complete parallelism.

When querying many files, performance can be improved by using a Hive-format folder structure to partition the data along the columns used in the filter condition.

The database will only need to read the prefix that meets the filter criteria.

For example:

If the folder/bucket is organized like this:

> `s3://bucket_name/country=us/date=2024-01-01`
>
> `s3://bucket_name/country=us/date=2024-01-02`
>
> `…`

The query which only needs data in 2024-01-02 will only need to load the necessary prefix.

---

## Execution Format

> *This section will talk about how DuckDB represents data in memory for processing.*

(You can think these are similar to Apache Arrow, a standardized column-oriented memory format).

DuckDB has its own standard to store data in memory during execution called `Vector`.

Note: The `Vector` format here and the Vectorized execution engine I mentioned above are two different concepts.

Vectors are logically represented arrays that contain data of a single type.

Internally, DuckDB supports different vector formats, which allow the system to store the same logical data with a different physical representation.

[Here is the list of supported vector formats from DuckDB documentation:](https://duckdb.org/internals/vector.html)

> ### *Flat Vectors*
>
> *Flat vectors are physically stored as a contiguous array; this is the standard uncompressed vector format. For flat vectors, the logical and physical representations are identical.*
>
> [![](https://substackcdn.com/image/fetch/$s_!Xu5P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bff9a47-6bbc-42d3-849d-44fb1145712e_228x384.png)](https://substackcdn.com/image/fetch/$s_!Xu5P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bff9a47-6bbc-42d3-849d-44fb1145712e_228x384.png)
>
> [Drawn based on this original image](https://duckdb.org/internals/vector.html#flat-vectors)
>
> ### *Constant Vectors*
>
> *Constant vectors are physically stored as a single constant value.*
>
> [![](https://substackcdn.com/image/fetch/$s_!UJxo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a499c31-163b-4f91-9ab4-6eb6f724d451_270x432.png)](https://substackcdn.com/image/fetch/$s_!UJxo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a499c31-163b-4f91-9ab4-6eb6f724d451_270x432.png)
>
> [Drawn based on this original image](https://duckdb.org/internals/vector.html#constant-vectors)
>
> *Constant vectors are useful when data elements are repeated - for example, when representing the result of a constant expression in a function call, the constant vector allows us to store the value only once.*
>
> ### *Dictionary Vectors*
>
> *Dictionary vectors are physically stored as a child vector and a selection vector that contains indices into the child vector.*
>
> [![](https://substackcdn.com/image/fetch/$s_!qPmE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F347469da-782a-4073-b9a4-d57008913f8a_335x447.png)](https://substackcdn.com/image/fetch/$s_!qPmE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F347469da-782a-4073-b9a4-d57008913f8a_335x447.png)
>
> [Drawn based on this original image](https://duckdb.org/internals/vector.html#dictionary-vectors)
>
> *Dictionary vectors are emitted by the storage when decompressing from dictionary.*
>
> ### Sequence Vectors
>
> [![](https://substackcdn.com/image/fetch/$s_!jXp7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff75eccfb-86d9-40c0-9a92-b54947e1edd9_286x432.png)](https://substackcdn.com/image/fetch/$s_!jXp7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff75eccfb-86d9-40c0-9a92-b54947e1edd9_286x432.png)
>
> [Drawn based on this original image](https://duckdb.org/internals/vector.html#sequence-vectors)
>
> *Sequence vectors are useful for efficiently storing incremental sequences. They are generally emitted for row identifiers.*

This in-memory format allows for a more compressed representation and potentially allows for compressed execution throughout the system.

---

## ACID

[![](https://substackcdn.com/image/fetch/$s_!QF-d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d60b6e1-2c28-4b4b-9231-77b860db25df_542x682.png)](https://substackcdn.com/image/fetch/$s_!QF-d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d60b6e1-2c28-4b4b-9231-77b860db25df_542x682.png)

When working with databases, you must have to know ACID.

* **Atomicity** guarantees that transactions are either fully completed or not at all – no in-between states, ensuring data integrity.
* **Consistency** ensures the database moves from one valid state to another, preserving the defined rules and constraints.
* **Isolation** prevents interference between concurrent transactions; ensure each transaction can be executed independently.
* **Durability** ensures that committed transactions persist even in the face of system failures, securing the permanence of our valuable data.

Initially, with OLTP databases like PostgreSQL or MySQL, enforcing ACID is a must-have to ensure data integrity.

It’s the same with OLAP databases, where this system now acts like a critical endpoint for business data analytics and usually serves as a shared environment for multiple users (data analysts, data science, data engineers, business users…)

If ACID is unnecessary in the OLAP world, why should open table formats like Delta Lake or Apache Iceberg be developed to make object storage more… ACID?

DuckDB provides transactional guarantees (ACID properties) through our custom, bulk-optimized [Multi-Version Concurrency Control (MVCC)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control).

---

## Outro

There are many other cool things about DuckDB I didn’t mention above because I am afraid it might be too long for this blog.

For example, [the secondary index allows DuckDB](https://duckdb.org/docs/sql/indexes.html) to have traditional indexes like MySQL or PostgreSQL behind the scenes or DuckDB or [DuckDB Wasm](https://duckdb.org/docs/api/wasm/overview.html) (Web Assembly), enabling DuckDB to run right on your browser.

From the user’s point of view, DuckDB is a fascinating tool that can potentially replace libraries like Pandas with very rich SQL with an extensive function library.

In particular, it can be on and running easily without advanced technical knowledge.

From the perspective of those who love to look into the internal world of OLAP databases, DuckDB is a very exciting database that [stands on the shoulders of giants, using components from various open-source projects and drawing inspiration from scientific publications.](https://duckdb.org/why_duckdb#standing-on-the-shoulders-of-giants)

That’s why I chose to make 1+1=0 in DuckDB.

(I mean research about DuckDB).

---

***Reference**: [DuckDB documentation](https://duckdb.org/docs/) and [source code](https://github.com/duckdb/duckdb).*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-made-110-in-duckdb/comments)

It might take 3 minutes to read, but it took me more than three days to prepare, so it will motivate me greatly if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
