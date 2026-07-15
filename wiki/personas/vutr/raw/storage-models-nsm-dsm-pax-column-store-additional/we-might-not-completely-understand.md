---
title: "We might not fully understand the column store!"
channel: vutr
author: "Vu Trinh"
published: 2024-11-30
url: https://vutr.substack.com/p/we-might-not-completely-understand
paid: false
topics: ["Data Engineering", "Snowflake", "BigQuery"]
tags: [column, https, auto, image, page, columns]
---

# We might not fully understand the column store!

*A note on the Row, Column, and Hybrid storage model*

> Source: [Open post](https://vutr.substack.com/p/we-might-not-completely-understand)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]]

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

[![](https://substackcdn.com/image/fetch/$s_!Y_fV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febd034ec-eeb2-4e49-9a38-deb5c3778d76_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Y_fV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febd034ec-eeb2-4e49-9a38-deb5c3778d76_2000x1429.png)

Image created by the author.

---

## Intro

I bet you’ve heard that storing column values close together will improve the performance of the analytics workload in which you only need a few columns in a table with over 20 or 30 columns.

I bet you’ve heard that storing data in a columnar manner helps improve compression significantly because values in the same columns are more likely to have a common pattern than values across columns in the same row.

And…

I bet you used to (or still) think that in the column store, each column will be stored in its own place.

But things might not be 100% like that.

Based on my observation, most of the blogs or documentation say that its product leverages the column store behind the scenes; it actually stores data in a hybrid approach where table data is first divided horizontally into portions, and in each partition, column values are store right next to each other.

Some documentation might be clear about this detail, and some don’t, which I believe makes most of us misunderstand the behavior of column store a little bit ;)

(The only two products I found that say they use column store and store column values completely separately are Redshift and Clickhouse.)

This week, I’ll explore the available storage models: Row, Column, and Hybrid. The article won’t focus solely on column stores; instead, I’ll start by examining row stores and then move on to column stores and the hybrid model to give you a clearer understanding of each's context and characteristics. Most of my insights come from [Andy Pavlo’s lecture](https://www.youtube.com/watch?v=nhlpwmOBEiE&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=8).

---

## Overview

A database is an organized and managed collection of data that models aspects of the real world. It can be as simple as a spreadsheet or a phone contact list.

A database management system (DBMS) is software that stores and analyzes information in a database. It supports the definition, creation, querying, updating, and administration of databases based on a data model.

The model can take various forms—graph, key-value, document, or the most popular one, the relational model, first described by [E.F. Codd in 1969](https://en.wikipedia.org/wiki/Relational_model). This model organizes data into structured tables, also known as relations, consisting of rows and columns.

Each table represents a specific type of entity, such as 'users' or 'orders,' with rows (tuples) representing individual records and columns (attributes) defining properties of those records, like name, age, or order date.

The data model only enforces the logical representation of the data; it does not dictate how the DBMS stores the data physically. Relational DBMSs are free to determine the data layout on disk.

The DBMS cannot allow applications to write data to the database as they would naively read or write to a file. Data on disk is essentially just a series of 0s and 1s, and it is the DBMS's responsibility to organize and manage how this data is written to disk to ensure efficient write and read operations.

However, the efficiency of a data layout must be evaluated differently depending on the workload. Database workloads can generally be categorized into two main types:

* The OLTP workload ingests new information; its data operations mostly read/write/update a small amount of data each time. Typically, the OLTP system is first built in a company to capture information from the real world. Some examples are the database behind web applications or the database that records banking transactions. The workload might be more familiar to those working closely with the company’s product/service, such as the backend developers.
* The OLAP workload has different characteristics from the OLTP workload. Its queries require reading data from many tables (via joins). After getting the data, many aggregations are potentially needed to extract insights or find new patterns. In most cases, OLAP workloads are executed on data collected from OLTP systems. This workload might be more familiar to those in the company’s data analytics functions, such as data engineers or analysts.

The DBMS organizes data in a way that optimally benefits each workload. To achieve this, there are three storage models used for data organization:

* The N-ary Storage Model (NSM): the row store.
* The Decomposition Storage Model (DSM): the column store.
* The Hybrid Storage Model (PAX): When database vendors say they use column store, there is a high chance that they use PAX instead of DSM. You often hear that open file formats like Parquet employ the column store; they also use PAX behind the scenes.

In the following sections, we will explore each model in detail.

---

## NSM - The row store

In this approach, the DBMS continuously stores all the values of all columns for a single row in a page. This is optimal for OLTP workloads where data needs to be written to the system as fast as possible, and the system must also adapt to a potentially large amount of ingested data from many users. Just imagine the database that backs the Amazon website; it might receive an extreme amount of data input when users put items in their carts.

> ***Note**: The term 'page' refers to an atomic data unit; all data within a page is either read or written successfully, or none of the page's data is read or written. In a DBMS, a page can refer to hardware pages, OS pages, or database pages. To align with the underlying hardware, the database page is typically a constant multiple of the 4KB hardware page. (e.g., 32KB). From the rest of the article, I use “page“ to refer to the database page.*

In a page, the row’s data is stored next to each other; after all row column values are written, the new row’s data can be written right next to the previous row. To locate the location of a row on a page, there is a small structure in the page called slot array, in which each entry points to the beginning of the associated row. At the start of the page is the header, then comes the slot array; the first arrived row is written at the end of the page.

When new data arrives, the slot array and the written rows expand in opposite directions: the slot array grows toward the end of the page, while new rows are written toward the page’s beginning. The page is considered full when the slot array and row data meet in the middle. A row can be identified by the page identifier + the slot array entry.

Let's check out the illustration below for a better understanding:

[![](https://substackcdn.com/image/fetch/$s_!JGBc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc01a5e05-5ce3-41a7-8430-a7d413ad6cdb_1450x860.png)](https://substackcdn.com/image/fetch/$s_!JGBc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc01a5e05-5ce3-41a7-8430-a7d413ad6cdb_1450x860.png)

Image created by the author.

Now, let’s come to typical OLTP queries.

[![](https://substackcdn.com/image/fetch/$s_!ly6n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6edcb5f8-5371-410b-b8a4-15f7b395f38b_912x210.png)](https://substackcdn.com/image/fetch/$s_!ly6n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6edcb5f8-5371-410b-b8a4-15f7b395f38b_912x210.png)

Image created by the carbon.now.sh.

Assume we have already located the needed row using the index, page identifier, and slot array. Because all row’s column values are stored close together, the DBMS's task is just to read the data of the whole row and return it to the client without jumping around and finding necessary data.

[![](https://substackcdn.com/image/fetch/$s_!zpD2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18ce60aa-a9e1-4713-a40c-39c6613f79da_618x550.png)](https://substackcdn.com/image/fetch/$s_!zpD2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18ce60aa-a9e1-4713-a40c-39c6613f79da_618x550.png)

Image created by the author.

Stitching column values together can also benefit the insertion, in which row the data only needs to be written on a single page, avoiding scattering the write to multiple places.

However, things got different when it comes to an OLAP query:

[![](https://substackcdn.com/image/fetch/$s_!Ee-s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a55fa14-f411-437b-b567-54a3c53d2c2d_846x292.png)](https://substackcdn.com/image/fetch/$s_!Ee-s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a55fa14-f411-437b-b567-54a3c53d2c2d_846x292.png)

Image created by the carbon.now.sh.

The query only needs to filter the field user\_name following a pattern; because the column’s values are stitched together, the DBMS must load a whole row of data every time to apply the filter only to the field name.

After getting the data, the query only needs to pick out two columns, created\_date and revenue, to do further aggregation; again, the DBMS can’t select the required columns due to the NSM physical organization.

We will explore how these problems are addressed with the next storage model.

But first, let’s summarize the NSM. The model is ideal for workloads requiring fast data insertion and mutation. It is also well-suited for queries that need the entire tuple, which is common in OLTP workloads.

However, it is not optimal for workloads that scan large amounts of table data on a subset of columns. Additionally, it is less effective for compression, as data from different columns often lacks common patterns.

---

## DSM - The column store

In this model, a single column’s value is stored continuously on a page; it maintains separate pages per column with a dedicated header for the column’s metadata.

Let's check out the image below for a better understanding:

[![](https://substackcdn.com/image/fetch/$s_!4hKd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd119a4c8-cfad-44da-a6fd-6755b3fef349_1330x674.png)](https://substackcdn.com/image/fetch/$s_!4hKd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd119a4c8-cfad-44da-a6fd-6755b3fef349_1330x674.png)

Image created by the author.

It’s ideal for OLAP workloads that require heavy-read queries to perform extensive data scans over a subset of table columns. Let's go back to the OLAP query in the NSM section above.

[![](https://substackcdn.com/image/fetch/$s_!ZMJq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e3c97a4-57f6-4e1e-9570-8a35d7df5111_846x292.png)](https://substackcdn.com/image/fetch/$s_!ZMJq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e3c97a4-57f6-4e1e-9570-8a35d7df5111_846x292.png)

Image created by the carbon.now.sh.

When filtering the user\_name column, the DBMS only needs to load the user\_name column’s page and apply the filter, avoiding loading redundant data from other columns. After locating the satisfied rows offset in the user column’s page, the DBMS will apply this offset to the created\_date and revenue column to retrieve data for later aggregation.

[![](https://substackcdn.com/image/fetch/$s_!dwYL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1809e24a-b3f5-4536-8036-32b7897dc712_1184x684.png)](https://substackcdn.com/image/fetch/$s_!dwYL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1809e24a-b3f5-4536-8036-32b7897dc712_1184x684.png)

Image created by the author.

You might be confused about the offset here. Because a row of data is stored in multiple places, there must be a way for the DBMS to know which row a specific column value in a page belongs to. For example, in a page that stores the user column’s values, how did the DBMS know a particular user value belongs to which row?

To address this, the DSM ensures that each value in a column has the same length. This allows the DBMS to easily calculate the offset of specific values using the fixed value size.

It works similarly to how arrays enable random data access using offsets. Since arrays require all elements to be the same size when accessing data at offset *i,*one can calculate the address of the value at this offset by using the formula: first\_element\_address + I \* element\_size.

Values with the same offset from different columns correspond to the same row.

This storage model reduces wasted I/O per query, as the DBMS only reads data from the columns it needs. Additionally, it allows for better data compression, as column values often exhibit patterns. For example, a column might have only a few distinct values repeated throughout the table, such as a mobile device platform column containing only two values: Android and iOS.

However, this model is unsuitable for point queries or frequent data insert operations. For instance, imagine needing to read a single row with 20 columns—the DBMS would have to consolidate data from 20 different pages. Similarly, when writing to a table with 100 columns, the DBMS would need to split the data into 100 separate pages, resulting in significant overhead.

An observation is that OLAP queries rarely access just a single column at a time. This means the DBMS often needs to consolidate data from pages of different columns, which can be physically scattered across the disk, requiring the DBMS to jump around on the disk.

To deal with this, the hybrid table format is introduced.

---

## Pax - The Hybrid Format

In this storage model, table data is horizontally split into row groups, and the columns' data is stored next to each other in the group. The goal is to benefit from fast and efficient data scan on the column store while maintaining the locality of the row store (column values from the same row stay close together, at least in the row group scope).

[![](https://substackcdn.com/image/fetch/$s_!92DI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcaa472db-5866-4fc7-8f42-007c8c0fa17f_478x660.png)](https://substackcdn.com/image/fetch/$s_!92DI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcaa472db-5866-4fc7-8f42-007c8c0fa17f_478x660.png)

Image created by the author

The PAX file has global metadata pointing to row group locations; each row group has metadata about its content.

As mentioned above, most systems say they do column stores; they do the PAX storage model instead of the DSM. I can name a few: BigQuery, Snowflake, DuckDB, Parquet, …

If you want to explore this storage model further, I recommend learning the internals of Parquet. Other systems that use PAX might call the concepts with different names or organize metadata differently, but the idea is still the same:

1. Split data horizontally into portions.
2. In each portion, store the column’s values next to each other. After all values for a given column are written, the system will start writing the values for the following columns.

I wrote a detailed article about Parquet, which you can find here:

---

## Outro

Thank you for reading this far.

In this article, we explored how, despite all relational databases presenting the same logical concepts of tables, rows, and columns to users, the physical data layout can vary depending on the workload the database is designed to serve.

Row stores are ideal for OLTP workloads, while column stores excel in OLAP workloads. Lastly, the hybrid approach combines the strengths of both row and column models, keeping values from the same row close together while still enabling efficient scans of specific columns.

Now it’s time to say goodbye.

P.S.: Next time you hear someone talk about a 'column store' or 'storing data in a columnar fashion,' ask them: 'Is this the PAX or the DSM?

---

## **References**

*[1] Andy Pavlo, CMU Database, [#05 - Row vs. Column Storage + Compression](https://www.youtube.com/watch?v=nhlpwmOBEiE&list=PLSE8ODhjZXjYDBpQnSymaectKjxCy6BYq&index=7)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/we-might-not-completely-understand/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
