---
title: "The Data Lake, Warehouse and Lakehouse"
channel: vutr
author: "Vu Trinh"
published: 2024-12-14
url: https://vutr.substack.com/p/the-data-lake-warehouse-and-lakehouse
paid: false
topics: ["Data Engineering", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Data Quality", "ETL"]
tags: [https, auto, warehouse, lake, image, media]
---

# The Data Lake, Warehouse and Lakehouse

*The type of data architecture (not exhaustive)*

> Source: [Open post](https://vutr.substack.com/p/the-data-lake-warehouse-and-lakehouse)

## Topics

[[data-engineering|Data Engineering]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[data-quality|Data Quality]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!5xqZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff31bc437-84d1-4866-b7fd-d1f3f57003ef_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!5xqZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff31bc437-84d1-4866-b7fd-d1f3f57003ef_2000x1429.png)

Image created by the author.

---

## Intro

I started my data engineering journey back in 2019, and the architecture where we first land data in the data lake and then transform it into the data warehouse seemed like the obvious approach.

The order of this data flow made me think that the data lake existed long before the data warehouse.

(Please tell me I’m not the only one who thought this.)

Things only became clearer to me about two years ago when I started researching the Lakehouse concept.

It turns out that data warehouses have been around for a long time, while data lakes were only introduced in the 2010s.

Today, I want to share my notes on data warehouses, data lakes, and the evolution of the Lakehouse as part of my series revisiting the fundamentals of data engineering.

> ***Note:** This is my personal note and may not cover the full picture. Feel free to provide feedback or correct me.*

---

## (Relational) Data Warehouse

Imagine starting a job at a company where you're responsible for creating reports and visualizations for the business team based on the data collected from the company's product.

At first, things are simple.

There's just one database recording transactional data; you extract data directly from it to build shiny reports.

Then, the company starts using a third-party service, and business users request data from this service to be included in their reports. That’s still manageable. You pull data from the database and the third-party API, perform some joins and aggregates, and voilà—you can still provide the reports users need.

But as your company’s product grows rapidly, it develops more services and integrates with additional external tools, each generating its own data. Naturally, your end users want all this data incorporated into their reports.

At this point, you **can't** pull data from every source separately and manually combine it anymore.

[![](https://substackcdn.com/image/fetch/$s_!ih01!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec2eee11-46e6-407e-8854-2eb6b351b32e_752x582.png)](https://substackcdn.com/image/fetch/$s_!ih01!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec2eee11-46e6-407e-8854-2eb6b351b32e_752x582.png)

Image created by the author.

That’s why we need the data warehouse.

[![](https://substackcdn.com/image/fetch/$s_!SNT1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d0d28ef-c759-4b1a-9de5-4cbd232bac11_1410x896.gif)](https://substackcdn.com/image/fetch/$s_!SNT1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d0d28ef-c759-4b1a-9de5-4cbd232bac11_1410x896.gif)

Image created by the author.

It is a repo where we can centralize, store, and manage large amounts of data from multiple data sources to serve the company's analytics workload.

Initially, data is extracted from many sources, transformed into a predefined structure (schema-on-read), and loaded directly into the data warehouse. The data warehouse helps businesses and organizations manage data by providing a centralized repository for data storage and retrieval, enabling more efficient data management and analysis.

But it soon faces challenges.

Data does not only come in tabular format; it can also be video, audio, or text documents. Unstructured data caused massive trouble for the relational data warehouse, which handles structured data.

---

## Data Lake + Data Warehouse

There is a high chance that you have heard the term Big Data once in your career.

Big techs that survived the DotCom bubble in the early 2000s, like Yahoo, Google, and Amazon, pioneered working with Big Data. At first, these companies continued to rely on traditional warehouses for data centralization. However, these systems struggled with data growth in both volumes and formats.

Yahoo developed Apache Hadoop to deal with big data. It includes processing (MapReduce) and storage (HDFS) based on Google's two papers, [MapReduce](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) and [Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf).

Data in this era did not come from the structured format anymore. People realized unstructured data like videos, text, or documents can contribute significantly to business insight. The point is that the relational data warehouse can only manage structured data.

And that’s how the data lake was introduced.

[![](https://substackcdn.com/image/fetch/$s_!ttsE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fbc662b-3350-496a-8550-2789575c258d_1022x476.png)](https://substackcdn.com/image/fetch/$s_!ttsE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fbc662b-3350-496a-8550-2789575c258d_1022x476.png)

Image created by the author.

The data lake is a concept that describes the process of storing a vast amount of data in its format (in HDFS or later in cloud object storage). Unlike traditional data warehouses, the data lake doesn’t require us to define the schema beforehand, so all data, including unstructured ones, can be stored in the lakes without concern about the constraint format.

At first, people tried to replace the traditional data warehouse with the data lake by bringing the processing right on top of the lake. However, the approach had many serious drawbacks; the data lake soon became the data swamp due to lacking proper data management features from the warehouse, such as data discovery, data quality and integrity guarantee, ACID constraints, and data DML support…

Thus, combining the data lake and the data warehouse is the better option.

[![](https://substackcdn.com/image/fetch/$s_!xpxl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e97a8d5-fd23-4db1-9b45-4d24b167ba0b_1430x964.gif)](https://substackcdn.com/image/fetch/$s_!xpxl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e97a8d5-fd23-4db1-9b45-4d24b167ba0b_1430x964.gif)

Image created by the author.

The lake is still where we can ingest raw data in any format without the care of the predefined schema. Later, a subset of data is transformed and loaded into the warehouse system for reporting and analysis. Advanced use cases like machine learning can still access raw data in the data lakes.

---

## Data Lakehouse

However, maintaining the above two-tier data architecture poses some challenges:

* **Data staleness:** The data in the warehouse is stale compared to the lake’s data. This is a step back from the original data warehouse architecture, where new operational data was immediately available for analytics demands.
* **Reliability:** Consolidating the data lake and warehouse is difficult and costly, requiring engineering effort to ETL data between the two systems.
* **Limited support for advanced analytics:** Initially, data warehouses did not support machine learning workloads well, as such tasks require processing large datasets with complex programmatic code. Vendors often recommended exporting data to files, which further increased the complexity of the overall system. Alternatively, users could run these workloads directly on data lake data stored in open formats. However, this approach often came at the cost of rich management features data warehouses provide, such as ACID transactions or data versioning. (This may no longer be the case, as modern data warehouse solutions like BigQuery now offer efficient capabilities for handling machine learning workloads directly within their interfaces.)
* **Total cost of ownership:** Users are billed twice the storage cost for data duplication in the data lake and warehouse.

So, the Lakehouse paradigm was introduced (by Databricks?).

For the namesake, in Lakehouse architecture, people try to bring the data warehouse features right on top of the data lake.

It is an architecture based on low-cost storage (e.g., object storage) that enhances traditional analytical DBMS management and performance features such as ACID transactions, versioning, caching, and query optimization. The Lakehouse combines the best of both worlds.

[![](https://substackcdn.com/image/fetch/$s_!UVMz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2dc04d53-70a1-413a-ad46-bbb95e4440d6_1508x1048.gif)](https://substackcdn.com/image/fetch/$s_!UVMz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2dc04d53-70a1-413a-ad46-bbb95e4440d6_1508x1048.gif)

Image created by the author.

The difference from the past effort, when people also tried to bring processing right on top into the data lake, is that more efficient metadata layers were introduced. Databricks created the Delta Lake, Netflix created the Iceberge to manage analytics data more efficiently on S3, and Uber developed Hudi to bring the capability of data upsert and incremental processing to the data lake.

In Lakhouse, every data-related operation must go through these open table formats to enable data warehouse features like table snapshotting, time traveling, ACID, schema, and partition evolution. These table formats also record statistics that help the query engine prune unnecessary data (e.g., the min/max column values).

For those who want to dive deep into the details of these table formats, you can visit my previous articles here:

---

## Outro

Throughout this article, I’ve tried to present the different types of data architecture and their associated contexts.

In my view, the Lakehouse architecture will continue to grow rapidly, especially with recent advancements in the data infrastructure landscape (such as AWS introducing S3 Tables).

As mentioned, this article may not cover the whole picture, so feel free to leave a comment —I welcome your insights.

Now, it’s time to say goodbye. See you in my next pieces!

---

## **References**

*[1] Databricks, [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.databricks.com/research/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics) (2020).*

*[2] James Serra, [Deciphering Data Architectures: Choosing Between a Modern Data Warehouse, Data Fabric, Data Lakehouse, and Data Mesh](https://www.amazon.com/Deciphering-Data-Architectures-Warehouse-Lakehouse/dp/1098150767) (2024)*

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
