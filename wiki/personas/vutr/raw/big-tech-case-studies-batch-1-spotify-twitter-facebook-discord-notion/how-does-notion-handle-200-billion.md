---
title: "How does Notion handle 200 billion data entities?"
channel: vutr
author: "Vu Trinh"
published: 2024-08-06
url: https://vutr.substack.com/p/how-does-notion-handle-200-billion
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "Data Warehouse", "Data Lake", "Change Data Capture", "Data Quality", "ETL"]
tags: [https, auto, image, notion, good, substackcdn]
---

# How does Notion handle 200 billion data entities?

*From PostgreSQL → Data Lake*

> Source: [Open post](https://vutr.substack.com/p/how-does-notion-handle-200-billion)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147335013)

[![](https://substackcdn.com/image/fetch/$s_!py-h!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b278ad8-b35b-4a27-b713-c070d5095947_1398x1002.png)](https://substackcdn.com/image/fetch/$s_!py-h!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b278ad8-b35b-4a27-b713-c070d5095947_1398x1002.png)

Image created by the author.

---

## Intro

If you've used Notion, you know it lets you do almost everything—note-taking, planning, reading lists, and project management.

Notion isn't rigid; it allows you to customize things until you feel good.

Everything in Notion is a block—text, images, lists, database rows, and even pages.

[![](https://substackcdn.com/image/fetch/$s_!YXHP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a8322c5-a333-446d-a73d-99f61bfbaee7_1857x890.png)](https://substackcdn.com/image/fetch/$s_!YXHP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a8322c5-a333-446d-a73d-99f61bfbaee7_1857x890.png)

Screenshot and decorating by the author ;)

These dynamic units can be transformed into other block types or moved freely within Notion.

Blocks are Notion's LEGOs.

## Postgres ruled them all.

[![](https://substackcdn.com/image/fetch/$s_!MdYl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6140da2c-baee-4574-9fad-18b8066fae15_1355x969.png)](https://substackcdn.com/image/fetch/$s_!MdYl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6140da2c-baee-4574-9fad-18b8066fae15_1355x969.png)

Postgres ruled them all!! Image created by the author.

Initially, Notion stored all the blocks in the Postgres database.

In 2021, they had more than 20 billion blocks.

Now, the blocks have grown to more than two hundred billion entities

Before 2021, they put all the blocks in a single Postgres instance.

Now, they shard the database into 480 logical shards and distribute them over 96 Postgres instances, each responsible for 5 shards.

At Notion, Postgres databases handle everything from online user traffic to offline analytics and machine learning.

Recognizing the explosive demands of analytics use cases, especially their recent Notion AI features, they decided to build a dedicated infrastructure for the offline workload.

## Fivetrans and Snowflake

In 2021, they started the journey with a simple ETL that used Fivetran to ingest data from Postgres to Snowflake, using 480 connectors to write 480 shards to raw Snowflake tables hourly.

[![](https://substackcdn.com/image/fetch/$s_!-nMg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0015d76-b193-491f-8f05-c8d2c2e1fd16_1626x1024.png)](https://substackcdn.com/image/fetch/$s_!-nMg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0015d76-b193-491f-8f05-c8d2c2e1fd16_1626x1024.png)

The first data warehouse design. Image created by the author.

Then, Notion would merge these tables into one big table for analytics and machine learning workload.

But this approach had some problems when the Postgres data grew:

[![](https://substackcdn.com/image/fetch/$s_!7YM_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d9887e-2314-4de6-8d7d-6074d7061521_1430x545.png)](https://substackcdn.com/image/fetch/$s_!7YM_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d9887e-2314-4de6-8d7d-6074d7061521_1430x545.png)

Image created by the author.

* Managing 480 Fivetran connectors is a nightmare.
* Notions users update blocks more often than add new ones. This heavy-updated pattern slows and increases the cost of Snowflake data ingestion.
* The data consumption gets more complex and heavy (AI workloads)

Notion embarked on building their in-house data lake.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147335013)

---

## The Lake

They want to build a solution that provides the following:

* Scalable data repository for storing both raw and processed data.
* Fast and cost-efficient data ingestion and computation for any workload. Especially with their update-heavy block data.

In 2022, they onboarded an in-house data lake architecture that incrementally ingested data from Postgres to Kafka using Debezium, then used Apache Hudi to write from Kafka to S3.

[![](https://substackcdn.com/image/fetch/$s_!NZVB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9818d66-f913-4f9d-a0e1-31026f3b91f5_1645x543.png)](https://substackcdn.com/image/fetch/$s_!NZVB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9818d66-f913-4f9d-a0e1-31026f3b91f5_1645x543.png)

Image created by the author.

The object storage will act as the endpoint for consumed systems, serving analytics, reporting needs, and AI workloads.

They used Spark as their primary data processing engine to handle billions of blocks on the top of the lake.

Offloading data ingestion and computing workload from Snowflake helps them reduce costs significantly.

The changes from Postgres are captured by Kafka Debezium Connector and then written to S3 via Apache Hudi.

Notion chose this table format because it performs well with its update-heavy workload and native integration with Debezium CDC messages.

Here is a brief on how they operate the solutions:

[![](https://substackcdn.com/image/fetch/$s_!bzp1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc03dac73-1144-4f17-87d9-2ac3d5d1a39a_1646x548.png)](https://substackcdn.com/image/fetch/$s_!bzp1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc03dac73-1144-4f17-87d9-2ac3d5d1a39a_1646x548.png)

Image created by the author.

* One Debeizum CDC connector per Postgres host.
* Notion deployed these connectors on managed Kubernetes on AWS (EKS)
* The connector can handle tens of MB/sec of Postgres row changes.
* One Kafka topic per Postgres table.
* All connectors will consume from all 480 shards and write to the same topic for that table.
* They use [Apache Hudi Deltastreamer,](https://hudi.apache.org/docs/0.10.0/hoodie_deltastreamer/) a Spark-based ingestion job, to consume Kafka messages and write data to S3.
* Most data processing jobs were written in PySpark.
* They use Scala Spark for more complex jobs. Notion also leverages multi-threading and parallel processing to speed up the processing of 480 shards.

## The payoff

* Offloading data from Snowflake to S3 saved Notion over a million dollars in 2022, with even more significant savings in 2023 and 2024.
* The overall ingestion time from Postgres to S3 and Snowflake reduced significantly, dropping from over a day to just a few minutes for small tables and a couple of hours for larger ones.
* The new data infrastructure unlocks a more advanced analytics use case and product, enabling the successful rollout of Notion AI features in 2023 and 2024.

---

## **Outro**

Thank you for reading to the end. As I delve deeper into how big tech companies build and manage their data analytics infrastructure, I look forward to sharing valuable lessons from my journey. See you in future posts!

If you enjoy this article, please like and restack it to help more people find it;)

Now it’s time to consume some cool links I found last week ;)

---

## **References**

*[1] XZ Tie, Nathan Louie, Thomas Chow, Darin Im, Abhishek Modi, Wendy Jiao,* **[Building and scaling Notion’s data lake](https://www.notion.so/blog/building-and-scaling-notions-data-lake)** (2024)

---

## **📋 The list**

#### ✏️ [Data products = the future of data engineering](https://blog.dataengineer.io/p/data-products-the-future-of-data)

4 minutes, by

> *In this article we will talk about: (1) The fine line between machine learning and data engineering. (2) What is a data product and how can data engineers up skill to deliver these products*

#### ✏️ [Can You Even \_\_init\_\_.py?](https://towardsdatascience.com/can-you-even-init-py-a682d1adf4e8)

6 minutes, by Louis Chan

> *Whenever you try to import your code from a different folder, you throw in an empty \_\_init\_\_.py. But do we really know \_\_init\_\_.py?*

#### ✏️ [The Top 10 Data Lifecycle Problems that Data Engineering Solves](https://towardsdatascience.com/the-top-10-data-lifecycle-problems-that-data-engineering-solves-7735781959d5)

14 mins, by Mike Shakhomirov

> *In this article, I want to tackle some of the biggest challenges data engineers face when working with pipelines throughout the data lifecycle.*

#### ✏️ [How to implement data quality checks with Great Expectations](https://www.startdataengineering.com/post/implement_data_quality_with_great_expectations/)

8 minutes, by Start Data Engineering

> *By the end of this post, you will have a mental model of how the Great Expectations library works and be able to quickly set up and run your own data quality checks with Great Expectations.*

#### ✏️ [Airbnb |](https://medium.com/airbnb-engineering/apache-flink-on-kubernetes-84425d66ee11) **[Apache Flink® on Kubernetes](https://medium.com/airbnb-engineering/apache-flink-on-kubernetes-84425d66ee11)**

10 minutes, by Airbnb Tech Blog

> *In this blog post, we will delve into the evolution of Flink architecture at Airbnb and compare our prior [Hadoop Yarn](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html) platform with the current [Kubernetes](https://kubernetes.io/)-based architecture.*

#### ✏️ [Delivering Faster Analytics at Pinterest](https://medium.com/pinterest-engineering/delivering-faster-analytics-at-pinterest-a639cdfad374)

6 minutes, by Pinterest Engineering

> *In this blog post, we’ll discuss and share our experience of launching our Analytics app on StarRocks.*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/how-does-notion-handle-200-billion/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
