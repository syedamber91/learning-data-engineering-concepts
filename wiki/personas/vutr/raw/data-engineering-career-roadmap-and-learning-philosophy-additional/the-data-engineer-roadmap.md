---
title: "The Data Engineer Roadmap"
channel: vutr
author: "Vu Trinh"
published: 2026-02-17
url: https://vutr.substack.com/p/the-data-engineer-roadmap
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Modeling", "Data Warehouse", "Lakehouse", "Orchestration", "Streaming", "Batch Processing", "Data Quality", "ETL"]
tags: [https, auto, good, image, substackcdn, fetch]
---

# The Data Engineer Roadmap

*The right way to become a useful data engineer*

> Source: [Open post](https://vutr.substack.com/p/the-data-engineer-roadmap)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=187397614)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!3oQW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff40e7718-2faf-4e20-a1b7-dbf0c0bb38e7_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!3oQW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff40e7718-2faf-4e20-a1b7-dbf0c0bb38e7_2000x1429.png)

---

# Intro

After 6 years of being a data engineer, I’ve realized that data engineering is not an easy field. Moving data from A to B seems like a simple flow at a high level. However, extracting insights from raw data is not easy; reliably ingesting, transforming, storing, and serving it at scale requires significant time and expertise. This is especially true today, when data is generated faster and in more diverse formats than ever before. And data consumers are no longer just humans; AI models and agents are just as hungry as business users.

The challenge of becoming a valuable data engineer does not stop there. Compared to software engineering, data engineering is a relatively new field. The unique characteristics of data products make it extremely hard to provide templates and guidelines for data projects, as each project has different requirements for reliability, scalability, performance, and usability.

In this article, I share my personal roadmap for learning to become a data engineer in 2026. You will see a mix of skills, tools, and my personal experience/sharing.

This article will definitely help you if:

* You want to learn data engineering from scratch.
* You aim to switch your career from software engineering, data analyst, data science,…
* Or you want to grow more as a data engineer.

Some notes before we begin:

* First, I assume that you’re aware of a data engineer’s responsibility. This factor is not part of the roadmap, but it drives you to follow it. Make sure you understand it before moving on. You can find my note [here](https://vutr.substack.com/i/164727703/1-aware-of-the-data-engineers-responsibilities).
* You shouldn’t be demotivated, as someone on the internet says that AI will do everything for us, from coding to building a pipeline. Given the complexity of data engineering, AI needs our intervention and auditing to work well. And, to guide an AI agent, you must first know how to do things right
* This article only focuses on the technical skills/tools. This does not mean that technical skills are everything a data engineer needs. Problem-solving, communication, and a user-oriented mindset are other key factors, but I won’t mention them here to keep the article concise.

---

# TL;DR

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=187397614)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

Things a data engineer should learn in order, based on my experience:

* Data Modeling
* SQL
* Python
* OLAP systems: cloud data warehouses, DuckDB, open table formats
* dbt
* Data formats: CSV, JSON, Avro, Parquet (disk), Arrow (memory)
* Processing engine: Spark and Polars
* Data orchestration: Airflow
* Software engineering: Git, CI/CD, Testing, Docker, k8s (optional)
* Message system: Kafka
* Stream processing: Flink
* AI-related: Basic LLM, Agent, Vector database, and how to guide AI do things for us.

---

# Data Modeling

From raw to insight, you must answer these two questions:

* How do I transform the data?
* How do I organize the data so it can be served and used efficiently?

You can go case by case at first. For example, a user A needs this kind of table, so you build a pipeline for it. Then user B needs another table, so you build another pipeline for it. Things work. However, as the use case expands, the number of sources increases, and the way data is served changes, we will have trouble.

[![](https://substackcdn.com/image/fetch/$s_!hGnc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4c1feeb-4749-4da2-a2d0-9588a23577b3_1152x450.png)](https://substackcdn.com/image/fetch/$s_!hGnc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4c1feeb-4749-4da2-a2d0-9588a23577b3_1152x450.png)

Ambiguous terms (finance “customer” vs sale “customer”?), silo data, adding a new source requires at least 2 weeks, different results on the same metric, slow queries, and no trust from business users.

All because we lack a bigger picture.

Based on [Joe Reis](https://joereis.substack.com/p/my-definition-of-data-modeling-for), the author of the famous [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/) book:

> *A data model is a structured representation that organizes and standardizes data to enable and guide human and machine behavior, inform decision-making, and facilitate actions. — [Joe Reis](https://joereis.substack.com/p/my-definition-of-data-modeling-for)*

With data modeling, we will have:

* **A Common Language**: With data modeling, we have a shared, unified view of the organization’s data, facilitating clear communication between stakeholders.
* **Data Quality and Integrity:** Modeling constraints and relationships gives us a good starting point for ensuring data quality.
* **Reduces Errors:** A data analyst knows exactly how to query a piece of insight. A data engineer knows exactly where the data will be loaded. All necessary transformations are performed beforehand, leaving the data well-organized and ready to serve. A good data model minimizes errors.

—

If I read a data engineering roadmap online and it doesn't include learning data modeling as one of the first steps, I will skip it right away.

The rise of “Putting more resources into the cloud data warehouse“ and “AI can do everything “ usually makes people think data modeling is not needed anymore. However, I think that’s not true; if we want AI to plug in and answer analytics questions, it must first understand the semantics of the data.

[![](https://substackcdn.com/image/fetch/$s_!i5Kl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99abe47a-ac78-4e55-843c-6053a588326f_1262x834.png)](https://substackcdn.com/image/fetch/$s_!i5Kl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99abe47a-ac78-4e55-843c-6053a588326f_1262x834.png)

Some say we can put the semantic layer right on top of raw data, and the problem is solved. I don’t agree with that. For me, data modeling is the core of any analytical data foundation, while the semantic layer sits on top, providing context and meaning. There are two typical processes in the semantic layer:

[![](https://substackcdn.com/image/fetch/$s_!4tCr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b410b39-6800-4856-8b6d-34ea70cd86b1_762x490.png)](https://substackcdn.com/image/fetch/$s_!4tCr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b410b39-6800-4856-8b6d-34ea70cd86b1_762x490.png)

* **Declaration**: You onboard data assets along with their relationships, define calculations, and might perform lightweight transformations.
* **Consumption**: Users navigate and select the desired metrics and dimensions exposed by the semantic layer (with more user-friendly names). The input is then converted into an SQL query that leverages the information from the Declaration stage.

The performance and usability of the consumption stage depend on the declaration stage. The declaration stage, in turn, depends on how your company stores and organizes data. And **data modeling** controls those processes. If you don’t have data modeling at all, your semantic layer will also be a mess.

[![](https://substackcdn.com/image/fetch/$s_!Ua5C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb478b609-20ae-465f-a0c2-76eebe71eac6_1198x882.png)](https://substackcdn.com/image/fetch/$s_!Ua5C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb478b609-20ae-465f-a0c2-76eebe71eac6_1198x882.png)

In short, learn data modeling, or more precisely, the mindset of “data must be organized in a way that it can support and reflect the company's business.”

Get started with dimensional modeling. Read the first 3,4 chapters of the book [The Data Warehouse Toolkit](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) and build some simple models. Dimensional modeling is easy to get started with and is adopted by many companies. You might need to learn other modeling techniques later, but dimensional modeling should be your first.

[![](https://substackcdn.com/image/fetch/$s_!zxh9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce0b9b2b-1ac9-4884-bc68-d0fcd0baf599_1118x318.png)](https://substackcdn.com/image/fetch/$s_!zxh9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce0b9b2b-1ac9-4884-bc68-d0fcd0baf599_1118x318.png)

Biz proccess → Data modeling; the bottom-up approach of Kimball modeling.

Here are my previous articles to help you get started with Kimball:

---

# SQL

If you work in the data field, you “speak“ SQL. The language was designed in the 1970s to manipulate and retrieve data from relational databases. Since then, it has gained increasing adoption worldwide as the primary interface for working with these databases.

The evolution of OLAP databases and the rise of transformation tools, such as dbt, make SQL an attractive choice for data transformation, which was previously handled by procedural languages like Java or Python. Some cloud data warehouses, such as BigQuery, even allow users to use SQL for machine learning.

If you can write SQL, you can turn raw data into insights when the data is already in the database.

[![](https://substackcdn.com/image/fetch/$s_!tnSa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91ff0fe6-7c67-4d78-aa70-25714c51db6e_554x542.png)](https://substackcdn.com/image/fetch/$s_!tnSa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91ff0fe6-7c67-4d78-aa70-25714c51db6e_554x542.png)

The order of SQL execution.

So, make sure you learn SQL at the start of the journey. You can learn it alongside data modeling so you can practice both simultaneously (e.g., use SQL to transform raw data into predefined models). Make yourself familiar with grouping, aggregation, ordering, different types of joins, CTEs, and window functions.

Then, take a closer look at how things are carried out behind a SQL query. As data engineers, we must write scalable, readable, and runnable queries. Understanding the internal allows you to debug and optimize the query.

Also, when you practice the SQL question, please make sure your first step is to fully understand the question and the provided data schema.

Here is my article to help you get started with SQL:

---

# Python

Data practitioners utilize SQL for many purposes, but not for everything. Python can make up for that.

You see repetitive tasks and want to automate them. Python can do it.

You face complex transformations that are difficult to express in SQL. Python with PySpark, Pandas, or Polars can help.

Data comes from many systems. Python can help pull them via the REST API.

You need to orchestrate many data pipeline steps. Python can help with tools like Airflow or Dagster.

Or, you want to build a data application. Python can help with Streamlit or a backend framework like FastAPI.

[![](https://substackcdn.com/image/fetch/$s_!kVI7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5def1fce-03ea-4bfa-ba25-cceca7bb8df9_274x222.png)](https://substackcdn.com/image/fetch/$s_!kVI7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5def1fce-03ea-4bfa-ba25-cceca7bb8df9_274x222.png)

You must learn Python.

Learning Python is easier than other languages because its syntax is simpler. There are numerous resources available to help us learn how to write a function, an if clause, or a class in Python.

However, learning syntax is never enough. Writing code is not hard, but writing readable, maintainable, and extendable code needs time. We need to care for others. No matter how good your Python program performs, if your colleagues don’t understand what you’re doing or find it extremely challenging to extend your work, your shiny code is useless.

[![](https://substackcdn.com/image/fetch/$s_!eO5t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddf0bcf7-40a4-4524-b586-9a7cc8993946_610x298.png)](https://substackcdn.com/image/fetch/$s_!eO5t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddf0bcf7-40a4-4524-b586-9a7cc8993946_610x298.png)

You can first start by learning the syntax, getting familiar with data processing with NumPy/Pandas, and making API calls. If you could, write a simple class to manage API requests, including making requests, handling responses, and paginating. Don’t rush to use Python directly in PySpark or Airflow; the goal is to master the syntax and understand how well the code is written in Python (idiomatic Python).

Pay attention to writing organized code as soon as possible. Learning design patterns ([Python-general](https://python-patterns.guide/) or [data-pipeline-specific](https://www.startdataengineering.com/post/code-patterns/)), coding principles like [SOLID](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design), or reading the [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) book.

---

# OLAP

Your transformed data must be stored somewhere to serve end users, and an OLAP database is the most common destination of a data pipeline. It’s the physical implementation of your data warehouse.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=187397614)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

## OLTP vs OLAP

When learning about OLAP systems, you must first know what they actually are. They are data management systems (DBMS) that implement techniques and mechanisms for storing, processing, and retrieving data for analytical workloads.

Compared to the OLAP databases, an OLTP database is designed for a different kind of workload:

[![](https://substackcdn.com/image/fetch/$s_!o7nX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22c49ead-b188-4706-93cd-92bf13f2438b_378x250.png)](https://substackcdn.com/image/fetch/$s_!o7nX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22c49ead-b188-4706-93cd-92bf13f2438b_378x250.png)

* OLTP databases such as PostgreSQL or MySQL were designed for the data operations that mostly read/write/update a small amount of data each time. These databases were optimized to locate a single piece of data as fast as possible. Data is typically organized in row format, where the values in the same row are stored together.
* OLAP databases such as BigQuery and Snowflake were designed for loading massive historical data for aggregation and joins. Those systems were optimized to prune data as much as possible by leveraging columnar format and column’s value statistics.

As data engineers, our main focus is on OLAP databases, since the backend teams usually manage OLTP databases.

So how do we learn it? First, you can read my previous article to have general knowledge of any OLAP systems:

## Cloud data warehouse

[![](https://substackcdn.com/image/fetch/$s_!O4oC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe43e340c-97be-45fa-a625-080191434815_548x232.png)](https://substackcdn.com/image/fetch/$s_!O4oC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe43e340c-97be-45fa-a625-080191434815_548x232.png)

Then sign up for free trials of cloud data warehouses such as Snowflake, Databricks, and BigQuery. There are several levels of learning:

* Loading some data and getting used to the UI/UX, the way the data is organized (e.g., database, schema), and how to monitor and debug a query.
* Understanding and applying the best practice to optimize the cost and performance: e.g., clustering, partitioning.
* Knowing how things work internally via an academic paper or a vendor’s material.

## DuckDB

[![](https://substackcdn.com/image/fetch/$s_!FjpN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638c089d-c330-4c56-ad08-db78ce3333c5_178x266.png)](https://substackcdn.com/image/fetch/$s_!FjpN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F638c089d-c330-4c56-ad08-db78ce3333c5_178x266.png)

Over the last 5 years, DuckDB has been widely adopted thanks to its robustness and simplicity. Unlike cloud data warehouses, DuckDB is an OLAP system that runs directly on your laptop with minimal setup. So, it's also a good choice for learning.

## Open table format

In the 2020s, the emergence of the lakehouse model gives companies more options beyond cloud data warehouses. One disadvantage of a cloud data warehouse is that the vendors manage the your data; the ability of new query engines to run on top of it depends on how well the vendor supports them.

Lakehouse architecture suggests that companies store data in object storage using open table formats such as Iceberg, Hudi, or Delta Lake to provide data warehousing capabilities for various query engines.

[![](https://substackcdn.com/image/fetch/$s_!xl9E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd8daff5-84bb-48f8-81a7-2f368e87165d_884x900.png)](https://substackcdn.com/image/fetch/$s_!xl9E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd8daff5-84bb-48f8-81a7-2f368e87165d_884x900.png)

There are two main selling points of Lakehouse:

* You have 100% control over the storage layer.
* You can bring any query engine (in theory) on top of the data.

With that power, more and more companies want to implement lakehouse architecture, so I believe learning open table formats is necessary.

After developing a mental model of an OLAP system (from playing with a cloud data warehouse or DuckDB), move on to learn one table format. Choose one and ensure you understand how it works internally (my choice would be Iceberg, given its openness and adoption), especially how it manages metadata and data. If you want to have a feel of what a table format is, I have written several articles about this topic:

---

# dbt

In the past, data warehouse systems were expensive, and companies had to purchase servers and licenses from vendors. Storage disks were also expensive, and networks weren’t as fast as they are today. Tightly-coupled compute and storage made scaling difficult. Also, the row-oriented databases didn’t perform well for analytics workloads.

All made ETL a perfect solution. Data had to be extracted and transformed to load only a curated subset into the warehouse.

But things have changed.

The rise of cloud data warehouses and other OLAP systems, such as DuckDB, has commoditized analytical capabilities: pay-as-you-go pricing models, cheaper storage, faster networks, and columnar storage/processing as the standard.

People soon realized they could dump data directly from the source and let the SQL transformation happen in the warehouse later. SQL queries are increasingly used for data transformation, whereas in the past this was mainly done in Python, Java, or Scala.

In that context, people need a way to manage SQL queries. That's where dbt fits the picture. It is a CLI tool that lets us efficiently transform data with SQL. It’s not an engine like Spark or a database like Postgres or Snowflake; it’s a tool that helps you manage your SQL data transformation.

[![](https://substackcdn.com/image/fetch/$s_!fLrG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F387c295c-7d92-4013-8e9c-5479715bec03_542x190.png)](https://substackcdn.com/image/fetch/$s_!fLrG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F387c295c-7d92-4013-8e9c-5479715bec03_542x190.png)

At the heart of dbt is the model concept. A model is an SQL query saved in a `.sql` file. The model’s code is not solely SQL; it combines SQL and Jinja.

[![](https://substackcdn.com/image/fetch/$s_!oG1k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31558400-e5a1-4e39-9e8b-acb2ca51dec6_338x248.png)](https://substackcdn.com/image/fetch/$s_!oG1k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31558400-e5a1-4e39-9e8b-acb2ca51dec6_338x248.png)

dbt’s Jinja has special functions called source() and ref(), which let us reference a physical table in the data warehouse and other dbt models, respectively. Together, dbt can form a complete data transformation lineage in which the leftmost model points to the physical table (using source) and subsequent models (using ref) reference the previous models.

[![](https://substackcdn.com/image/fetch/$s_!ZUEW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17f5b8e4-1da2-466d-8f80-8a167d1300a5_1156x432.png)](https://substackcdn.com/image/fetch/$s_!ZUEW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17f5b8e4-1da2-466d-8f80-8a167d1300a5_1156x432.png)

A dbt model is purely code at its core, making it naturally compatible with Git for version control. Teams can track changes, collaborate via pull requests, roll back to previous versions, and implement CI/CD pipelines to test, build, and deploy—just like software engineers do with application code. dbt also automatically generates documentation that provides a clear overview of your data transformations and lineage.

—

You can learn dbt when practicing SQL, OLAP systems, and data modeling. Technically, with only these 4 components, you can build a complete data pipeline using SQL to transform data based on the data model and store it in an OLAP system. At the same time, the entire development, testing, and deployment can be handled with dbt and Git.

---

# Data formats

## On disk

Throughout the data engineering lifecycle, data must pass through many “stations” before reaching its final destination. All the stations are basically physical servers where data is stored on disk and is read and written via the abstraction called a file format.

However, all formats are not created the same, as each is designed to suit a specific need. As a data engineer, you must understand the difference to decide on which format to use in a specific situation. There are at least 4 file formats you need to focus on:

[![](https://substackcdn.com/image/fetch/$s_!MrzU!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F756a1c46-386d-41d0-834f-5a0b13235bb1_1540x558.png)](https://substackcdn.com/image/fetch/$s_!MrzU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F756a1c46-386d-41d0-834f-5a0b13235bb1_1540x558.png)

* **Comma-Separated Values (CSV)** is a plain-text format designed to store data in a structured manner.
* **JSON** emerged from web development as a lightweight, text-based data interchange format.
* **Apache Avro** is a data serialization framework that originated within the Apache Hadoop ecosystem. It is a row-oriented format with language-independent schema definition.
* **Parquet** stores data in a hybrid format, where data is first horizontally partitioned into units called “row groups.” Within each group, column data is stored close together. This allows the query engine to read only the required row groups and columns, significantly reducing I/O

I also wrote an article on this topic to help you get started:

## In-memory

Besides being stored on disk, data is also processed and persisted in-memory. In the past, each OLAP processing/query engine has had its own way of representing data in memory. However, ten years ago, an evolution began with the introduction of the Apache Arrow project, which standardized memory representation for analytical workloads.

It promise for a standard in-memory columnar format. In addition to performance, Arrow aims to enable interoperability among OLAP engines, allowing them to exchange data directly via the Arrow format without the overhead of serialization/deserialization.

You can learn more about Arrow by reading this article:

---

# Processing engines

Sometimes SQL is not enough, and you might feel that other abstractions, such as the DataFrame, are more intuitive to work with. In this case, your transformation must occur outside the OLAP systems.

## Spark

When it comes to processing, Apache Spark is always the strong candidate given its ecosystem, performance, and reliability. It was introduced in hopes of providing a better alternative to MapReduce. Unlike its predecessor, Spark relies heavily on in-memory processing via the RDD abstraction, an **immutable**, **partitioned collection** of records in memory that can be operated on in parallel.

Processing logic is expressed as a series of transformations (e.g., filtering, aggregation) that are later triggered by an action (e.g., show). This lazy approach allows Spark to delay the execution so the system can plan for a more optimal plan.

[![](https://substackcdn.com/image/fetch/$s_!rgQI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68745d94-f1cd-400d-9f9a-de7d709ff2e0_976x760.png)](https://substackcdn.com/image/fetch/$s_!rgQI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68745d94-f1cd-400d-9f9a-de7d709ff2e0_976x760.png)

In Spark, the driver handles planning and coordination, while the executor handles the physical data processing.

Since its introduction, Spark has been the king of distributed processing engines. A really high chance that you will work with Spark at least once during your data engineer career. Thus, learning Spark definitely is one of your next steps.

Start with the fundamentals, start a Spark cluster locally, increase the processed data gradually, and tune your cluster little by little to ensure you understand the mechanism and get used to the process of tuning your Spark setup (which is the most time-consuming process of operating Spark in real life)

I also wrote a Spark article that covers every aspect of Spark fundamentals:

## Pandas/Numpy/Polars

Because Spark is a cluster-based processing engine, it comes with complexity and overhead. It requires a deep understanding to make it work for your needs, such as how to set up the cluster with sufficient resources or how to debug when your application runs on the cluster remotely.

Small datasets can be handled with Pandas or Numpy, the go-to libraries for data manipulation in Python. However, these two can only handle small datasets due to Python’s global interpreter limit.

Pandas or NumPy can only process small datasets, whereas Spark can handle big data but adds complexity. So, how do we handle medium-sized datasets?

[![](https://substackcdn.com/image/fetch/$s_!fUIB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ff563ed-0e82-48b7-9606-03ccdff3134b_1868x764.png)](https://substackcdn.com/image/fetch/$s_!fUIB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ff563ed-0e82-48b7-9606-03ccdff3134b_1868x764.png)

Polars is your choice here.

> ***Note**: DuckDB can also be used for medium-sized datasets; however, I list it as an OLAP system in the section above. In this section, I emphasize the processing engine that primarily operates through other abstractions rather than SQL.*

Written in Rust and exposed via Python, the library still provides the DataFrame abstraction (like Pandas), but performance is no longer limited because data is processed in parallel on your laptop, with the entire process handled in Rust.

---

# Orchestrate the data pipeline.

> ## Airflow

After learning the tools/skills above, you can build an end-to-end data pipeline in Python to pull data from the API, land it in object storage in Parquet format, and process it based on the data model using SQL + dbt or Spark/Polars.

However, they are separate tasks and must be run manually. In production, we need a “glue“ layer to stick everything together, harmonize the end-to-end pipeline, as well as the ability to observe, monitor, debug, and ensure the fault-tolerance (e.g., what if a task fails)

That layer is called data orchestration.

Apache Airflow is the most commonly chosen option. Although there are many alternatives, such as Dagster or Prefetch, Airflow has its own standing thanks to its simplicity, strong community, and wide adoption. Thus, if I had to recommend an orchestration tool for anyone learning data engineering, I wouldn’t hesitate to say Airflow.

[![](https://substackcdn.com/image/fetch/$s_!b8-B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe73baaa6-8c3d-46f0-ae1e-6c60fb3ba21d_708x324.png)](https://substackcdn.com/image/fetch/$s_!b8-B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe73baaa6-8c3d-46f0-ae1e-6c60fb3ba21d_708x324.png)

Airflow operates on the concept of **Directed Acyclic Graphs (DAGs)** to model workflows.

Apache Airflow was created in 2014 at Airbnb, when the company was dealing with massive, increasingly complex data workflows. At the time, existing orchestration tools were either too rigid or lacked scalability, or couldn’t accommodate the dynamic nature of data pipelines.

[![](https://substackcdn.com/image/fetch/$s_!-xgl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde4b0932-6c5e-4c08-b028-9232cb66c5bb_666x448.png)](https://substackcdn.com/image/fetch/$s_!-xgl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde4b0932-6c5e-4c08-b028-9232cb66c5bb_666x448.png)

Essentials Airflow’s components: DAG folder, Scheduler, Web Server, Workers and Metadata database

The guiding principle was simple: make workflow orchestration flexible, programmable, and maintainable by writing workflows as code. By leveraging Python, Airflow gave data engineers a familiar, intuitive way to define workflows while integrating seamlessly into modern software engineering practices.

To learn Airflow, there is no better way than to learn some basic concepts, set up a local Airflow environment, and build some DAGs. You can combine what you have learned: Airflow orchestrates the whole process, from pulling data using Python to processing it using SQL + dbt or Spark/Polars.

[![](https://substackcdn.com/image/fetch/$s_!T7SH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42d2609-ed0c-45c1-96da-b02ca6e188c0_1084x718.png)](https://substackcdn.com/image/fetch/$s_!T7SH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc42d2609-ed0c-45c1-96da-b02ca6e188c0_1084x718.png)

Also, during the learning process, pay attention to how you spot and handle task failures, how to run the data backfill, the resource and dependencies isolation support (e.g., does one heavy task affect others, or can I run one task in Python 3.11 and another in 3.12), and how to manage credentials and secrets.

---

# Software engineering

People are applying software engineering best practices to data engineering to control product output quality.

## Git

[![](https://substackcdn.com/image/fetch/$s_!qdve!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0841ca72-fe6f-43bd-88ea-de0307a7de3e_1294x400.png)](https://substackcdn.com/image/fetch/$s_!qdve!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0841ca72-fe6f-43bd-88ea-de0307a7de3e_1294x400.png)

Just don’t share code with your teammates via Google Drive. There are three inevitable things:

* You rarely work alone.
* You don’t write your code and forget it; you need to track its change history to fix bugs or add new features.

Thus, you need a tool to:

* Facilitate collaboration
* Version control your work

And Git was designed for that purpose. Learn Git. It is non-negotiable. You need to understand how to use the basic commands and how they affect your work history. I wrote a Git article not long ago:

## Testing

When you write a piece of code, no matter whether it is Python, SQL, or anything else, learn how to test what you produce, unit test, integration test, data quality test, and other kinds of tests (if needed) to make sure your work doesn’t corrupt anything.

## Docker

Docker is the famous container platform that allows you to create, build, and orchestrate containers. The container is similar to a Virtual Machine (VM), but it is lighter because containers do not require a dedicated OS.

[![](https://substackcdn.com/image/fetch/$s_!Bcz_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf5bed4d-d658-44be-a630-b9e337463dd9_814x638.png)](https://substackcdn.com/image/fetch/$s_!Bcz_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf5bed4d-d658-44be-a630-b9e337463dd9_814x638.png)

Containers are the most common practice to deploy your software application on multiple environments, thanks to their interoperability. Equip yourself with some basic knowledge of Docker containers, how to write a Dockerfile, how to build it, and how to run a container from that image, and how to orchestrate a bunch of containers via Docker Compose.

That will allow you to be more proactive in future work when you need to control the whole local-dev-prod deployment process of a data/backend application.

## CI/CD

Testing your changes, building a Docker image, and deploying it somewhere when a new branch is merged into your develop or master branch cannot be handled manually.

[![](https://substackcdn.com/image/fetch/$s_!wWjF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb49fccde-812d-45bd-8efd-860dbc944765_1232x358.png)](https://substackcdn.com/image/fetch/$s_!wWjF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb49fccde-812d-45bd-8efd-860dbc944765_1232x358.png)

You need the CI/CD pipeline for that.

Learn to build a simple pipeline in your GitHub personal repo to get a sense of the process, and actively learn from others at your job to ensure it aligns with your company's practices and standards.

## Kubernetes (optional)

Kubernetes is an open-source platform that automates the deployment, scaling, and operation of containerized applications. It is the most widely adopted container orchestration platform (e.g., how many containers you want to run for your application, what if a container fails, etc.)

[![](https://substackcdn.com/image/fetch/$s_!UZ1b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F966b980a-b019-43b6-8970-0f01e80a9f7a_1350x664.png)](https://substackcdn.com/image/fetch/$s_!UZ1b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F966b980a-b019-43b6-8970-0f01e80a9f7a_1350x664.png)

The overview architecture of Kubernetes.

Knowing how to work with Kubernetes will give you a greater advantage; however, if I had to start the data engineer role over again, I wouldn’t prioritize it over other skills, as I believe you will get help with Kubernetes from other teams, such as the DevOps department.

However, if you aim to work on a more platform-building role (e.g., building a platform for others to build a data pipeline), learning Kubernetes is a must.

---

# Message system

> ## Kafka

If you want to become a data engineer, you must prepare to work with many data sources with different interfaces to extract the data. From an OLTP database, pulling/pushing from an API, or consuming from a message system.

Kafka is a widely used messaging system in many companies’ infrastructure to facilitate data movement between services.

[![](https://substackcdn.com/image/fetch/$s_!ibNn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3209f8b-20ac-40b0-b837-0a25512d5200_1500x522.png)](https://substackcdn.com/image/fetch/$s_!ibNn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3209f8b-20ac-40b0-b837-0a25512d5200_1500x522.png)

Thus, data engineers must prepare for situations where the pipeline needs to consume data from a message system, such as Kafka. First, learn how to write to Kafka, store and serve data, and understand data retention. Then learn about how to publish and, especially, consume messages from Kafka, for example, how do we scale consumption if the volume of data increases?

I also wrote an article about Kafka:

Your future company might work with other alternative systems like Google PubSub or Amazon Kenesis; however, I believe learning the fundamentals of Kafka will also help you do well with other systems, as they provide pretty much the same interface (e.g., publisher-consumer model)

---

# Stream processing

> ## Flink

Spark is famous for batch processing. It also supports stream processing with a micro-batching feature; however, it was not designed for true stream processing due to batch-processing overhead that affects performance and the lack of robust watermark and state management mechanisms.

That’s where Flink fits.

[![](https://substackcdn.com/image/fetch/$s_!kXBD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F097473a6-f6ca-4068-a14b-abe48a27771b_1240x918.png)](https://substackcdn.com/image/fetch/$s_!kXBD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F097473a6-f6ca-4068-a14b-abe48a27771b_1240x918.png)

Flink’s cluster architecture

Designed to deliver sub-millisecond performance through advanced watermark configuration and state management, Flink is a strong choice if your use case requires extremely low-latency data processing.

However, I won’t prioritize learning this framework as much as Spark because I personally observe that you will deal with batch processing 90% of the time; for the remaining 10%, Spark Structured Streaming will also cover 60-70% of it. Recently, Spark Structured Streaming introduced a new mode called real-time mode, which promises to provide competitive performance compared to Flink.

Thus, when learning a processing engine, I will always strive to learning Spark first. However, if you aim for a career that deals with stream processing all the time (e.g., Uber, Netflix, or any companies that need to make decisions based on real-time data), feel free to move up this framework on the list.

---

# AI related

We live in a time when we hardly ignore AI. There are two purposes of learning AI as a data engineer:

* First is to help the AI engineers or data scientists deploy AI applications (e.g., the chatbot). Here, you might need to understand the basics of machine learning, LLMs, Agents, or vector databases. The goal is not to build or tune models, but to help prepare data and infrastructure.

  [![](https://substackcdn.com/image/fetch/$s_!17an!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85b48eaa-5c56-4bc7-aaec-9cdf8196403c_878x480.png)](https://substackcdn.com/image/fetch/$s_!17an!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85b48eaa-5c56-4bc7-aaec-9cdf8196403c_878x480.png)
* Second is to use AI to augment your work (e.g., asking Claude to build your pipeline). I’m not against using AI to ease your burden; however, I’m against using it without knowing what the final output will look like. For example, ask AI to generate a SQL script, but it is unreadable and slow, and you can’t point that out. That’s why I always recommend learning the fundamentals first, so you're aware of what you’re doing before handing over to a chatbot or IDE.

  [![](https://substackcdn.com/image/fetch/$s_!Ig5M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41927cb5-d5f2-4ea0-b7e9-c7ad10b29b15_842x514.png)](https://substackcdn.com/image/fetch/$s_!Ig5M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41927cb5-d5f2-4ea0-b7e9-c7ad10b29b15_842x514.png)

# Others

There are other tools I didn't mention, such as NoSQL databases, because I believe they aren’t as critical as the ones I listed here. However, you might need them when working for a specific company, and feel free to put them into your list.

---

# Outro

In this article, I outlined my own data engineer roadmap to help anyone who wants to become a data engineer have direction on what they're going to learn. We begin with data modeling, SQL, Python, OLAP systems, processing engines, file formats, and a data orchestration tool. By learning and mastering these skills, you can already build a complete data application.

To ensure your work is robust enough for production, you must develop software engineering skills such as Git, CI/CD, Testing, and Docker. Then you can focus on Kafka and Flink to expand your ability to work with message-based data sources and the stream processing paradigm.

Finally, we come to AI. Someone might say I'm conservative when putting AI last, but I always believe in the “know what you’re doing before letting AI do it“.

Thank you for reading this far. See you in my next articles.
