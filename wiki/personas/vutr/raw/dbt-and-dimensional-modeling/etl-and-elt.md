---
title: "ETL and ELT"
channel: vutr
author: "Vu Trinh"
published: 2024-12-10
url: https://vutr.substack.com/p/etl-and-elt
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming", "ETL"]
tags: [warehouse, https, auto, storage, image, logic]
---

# ETL and ELT

*It's not just about swapping the 'T' and 'L' positions.*

> Source: [Open post](https://vutr.substack.com/p/etl-and-elt)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!lXnm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdcfdc8f-af23-47d0-8d74-9fec590ee2de_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!lXnm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcdcfdc8f-af23-47d0-8d74-9fec590ee2de_1400x1000.png)

Image created by the author.

---

## Intro

I used to chase shiny technologies when I began my data engineering career.

From open-source…

Docker, Kubernetes, HDFS, Spark, Flink, Airflow, Presto, Elasticsearch, Kafka.

…To the cloud…

Redshift, BigQuery, EMR, Google Dataflow, Pub/Sub.

(The list isn’t exhaustive—I’ve probably forgotten a lot.)

Whenever I stumbled upon a newly discovered data-engineering tool, I’d dive into its documentation, head straight to the “Getting Started” section, copy commands or docker-compose files, tinker a bit in the terminal, and boom—the tool would be up and running.

I even had a GitHub repo filled with docker-compose files (along with other necessary dependencies) capable of running an entire batch or stream processing pipeline with just a single command. (I’m not sure if it still works today.)

For me, learning new tools was like a child discovering ice cream for the first time—wide-eyed and grinning from ear to ear.

But the excitement soon faded.

The question, “Why am I learning this?” started to creep in. That empty feeling was like a balloon full of air, floating aimlessly in the sky.

I realized I needed a foundation—an anchor to keep my balloon grounded.

(It took me two years to reach that realization.)

That’s why I stopped chasing tools and focused on data engineering fundamentals.

As I write this, I believe many people out there feel the same way—wanting to prioritize the fundamentals of data engineering after spending so much time catching up with trendy tools. Sharing bits of my learning journey about these fundamentals feels valuable.

So, here we are, my first article in the back-to-the-fundamentals series.

Writing about ETL and ELT.

---

## ETL

[![](https://substackcdn.com/image/fetch/$s_!Kqyo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7955fea4-ce85-4e83-9ad1-d35609cd132f_1338x700.png)](https://substackcdn.com/image/fetch/$s_!Kqyo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7955fea4-ce85-4e83-9ad1-d35609cd132f_1338x700.png)

Image created by the author.

The process has existed since the 1970s, when the rise of data warehouses began. It involved everything between the data sources (e.g., operational database) and data warehouse system.

1. **Extract**: The process’s first step is extraction. The needed data is gathered from various sources, such as relational databases or third-party APIs
2. **Transform**: Extracted data undergoes many potential transformations, including cleaning, filtering, combining from different sources, and formatting to conform to a target schema.
3. **Load**: The transformed data is loaded into the destination with the predefined schema and constrained.

The important note here is that the transformation happens before loading to the warehouse; the raw data will not be present in the destination, only clean and structured data.

So why ETL in the first place? Why not just dump raw data into the data warehouse?

In the past, data warehouse systems were expensive, both in terms of storage and processing. Companies had to set up their own infrastructure, purchase servers, and buy data warehouse licenses from vendors in the first place. Storage disks weren’t cheap, and networks weren’t as fast as today. Compute and storage were tightly coupled, making system scaling a significant challenge.

Getting everything ready could take months.

Additionally, storing data in a columnar format wasn’t common back then, and the row-oriented databases didn’t perform well for analytics workloads.

All of these factors made ETL a perfect solution; data had to be carefully extracted and transformed so that only a relatively small, curated subset of data was loaded into the warehouse for analysis.

However, ETL had its drawbacks.

Typically, setting up ETL pipelines requires a lot of effort: defining the logic beforehand, setting and managing complex environments (e.g., Apache Spark clusters), coding, testing, and deploying…

All these factors made ETL pipelines inaccessible—only data engineers could understand and manage them. Additionally, the pipeline could become a potential bottleneck if not carefully designed and maintained, especially as data grew in both complexity and volume.

Moreover, ETL lacks flexibility. Data is transformed based on predefined logic, but what if the logic needs to change due to evolving business requirements? Since ETL processes don’t preserve the original source data, data engineers have to adjust the pipeline logic, return to the source system, and go through the entire extract, transform, and load process again.

---

## ELT

[![](https://substackcdn.com/image/fetch/$s_!0XXZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39e65ff3-d626-478f-b117-e4a146cbf5ac_1546x662.png)](https://substackcdn.com/image/fetch/$s_!0XXZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39e65ff3-d626-478f-b117-e4a146cbf5ac_1546x662.png)

Image created by the author.

Things have changed these days.

The emergence of cloud data warehouses has made the solution much more accessible. Pay-as-you-go pricing models, cheaper storage, faster networks, and columnar storage/processing as the standard have commoditized high-performance, cost-efficient data warehouses.

With just a few clicks, your shiny warehouse will be up and running.

People soon realized they didn’t have to transform the data before loading it into the warehouse. They could just dump data straight from the source (maybe some lightweight processing is needed) and let the transformation happen later directly in the warehouse.

The storage cost will surely increase, and the warehouse will have to deal with larger and more complex data. But that’s a reasonable trade-off. The storage cost will increase, but it does not burn your bill like in the past, when you had to pay for the storage (servers) cost beforehand, and disk hardware was not as cheap as it is today. For processing, columnar storage and an engine make handling a large amount of data more efficient than ever.

In return, ELT solves many of the problems associated with ETL.

Most transformation logic can now be handled within the data warehouse using SQL, making it more accessible for users such as data analysts or data scientists. This eliminates the potential performance bottleneck of ETL pipelines. Modern data warehouses also offer powerful processing capabilities for structured and unstructured data. Tools like dbt bring software development practice to writing SQL transformation; we can define, reuse, test, and deploy SQL logic effortlessly.

Most importantly, ELT allows you to keep raw data in the warehouse. (Sure, storage costs may rise, but who cares?) This approach offers several advantages. You don’t need to plan transformation logic in advance; instead, the logic can evolve over time based on analytical needs—an especially valuable benefit in today’s agile software development environment.

Additionally, loading raw data without transformation increases the isolation level between the data warehouse and the source system. In cases of backfilling or logic changes, you can simply revisit the raw data stored in the warehouse without burdening the source system.

---

## Outro

Throughout this article, I don’t mean to suggest that ELT will completely replace the ETL paradigm. Of course, there are cases where ETL is necessary.

My point is that ELT will continue to grow, given the evolution of modern data infrastructure—especially with the emergence of the lakehouse paradigm, which aims to bring data warehouse capabilities directly onto the data lake.

Most cloud platforms now allow users to query data stored in object storage directly from the data warehouse. Open table formats like Hudi, Delta Lake, and Iceberg are evolving rapidly. Take AWS for an example; they recently announced an S3 storage type designed for tabular data, using Apache Iceberg and Parquet as its backbone.

—

Thank you for reading this far. Everything you’ve read represents my personal perspective and might not capture the full picture. So, let’s keep the discussion going! Feel free to share your thoughts on ETL and ELT in the comments. 😉

Now, it’s time to say goodbye. See you on my next piece.

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
