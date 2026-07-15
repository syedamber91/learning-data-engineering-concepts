---
title: "6 technical skills every data engineer should have"
channel: vutr
author: "Vu Trinh"
published: 2025-07-22
url: https://vutr.substack.com/p/6-technical-skills-every-data-engineer
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Modeling", "Data Warehouse", "Lakehouse", "Orchestration", "Data Quality", "Data Governance"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# 6 technical skills every data engineer should have

*Based on my observations*

> Source: [Open post](https://vutr.substack.com/p/6-technical-skills-every-data-engineer)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]] · [[data-governance|Data Governance]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> *I invite you to join the club with a **50% discount on the yearly package.** Let’s not be suck as data engineering together.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!wAmm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F016c62b6-9378-40f4-9f08-8f0b9b9aa561_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!wAmm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F016c62b6-9378-40f4-9f08-8f0b9b9aa561_2000x1428.png)

---

## Intro

If I were to enter the data engineering field at the moment, I would feel extremely overwhelmed. Tons of tools, tools of skills, and I didn’t even put AI-related stuff on the table.

I read somewhere that the most effective approach to learning in this era is to learn things that would not change. Looking back on my journey as a data engineer, I realized that, indeed, there are a few things like that.

In this article, I shared my six technical skills that I believe every data engineers should equip themself with. They won’t be obsolete anytime soon.

---

## Before we move on

[![](https://substackcdn.com/image/fetch/$s_!HmvC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0eb315c-3bb7-4cc1-923a-92ab2320f8fd_302x286.png)](https://substackcdn.com/image/fetch/$s_!HmvC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0eb315c-3bb7-4cc1-923a-92ab2320f8fd_302x286.png)

For me, the most important aspect of learning something is having a solid feedback loop. Getting someone to provide you with feedback. Your friend, your senior colleague, or the internet community. Asking Gemini or ChatGPT to act like someone who knows what you’re doing (e.g., “imagine you’re a data engineer with 20 years of experience, help me to give feedback on this transform SQL script”) is not a bad option.

The key is to know whether what you’re doing is on the right track or not.

## Data modeling

### Why?

You will soon realize a fact that every subsequent process—every pipeline, every query, every machine learning model—is built upon the structure defined by the data model.

[![](https://substackcdn.com/image/fetch/$s_!Y57s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1629a5d1-e0b4-407b-abf4-06cac1ad2071_706x472.png)](https://substackcdn.com/image/fetch/$s_!Y57s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1629a5d1-e0b4-407b-abf4-06cac1ad2071_706x472.png)

If the data warehouse is a building, data modeling is the blueprint. Without it, we have no clue what to do next. We can survive several months of blindly loading and querying data; however, the nightmare soon comes:

[![](https://substackcdn.com/image/fetch/$s_!hGnc!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4c1feeb-4749-4da2-a2d0-9588a23577b3_1152x450.png)](https://substackcdn.com/image/fetch/$s_!hGnc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4c1feeb-4749-4da2-a2d0-9588a23577b3_1152x450.png)

* **Maintenance Cost**: Without a clear blueprint, we are left with a mess of SQL scripts and tables, making maintenance a costly and frustrating process
* **Inefficient Processing**: Queries against a poorly designed structure are usually slow and resource-intensive
* **Data Integrity Problems**: Without the enforcement of relationships and constraints, it’s hard to ensure data integrity, which could render the information unreliable.
* **Weird Insights**: Without reliable data and standard ways to load and retrieve data, a high chance that analysts and data scientists create bad reports and ML models.
* **No Trust**: Business users then use these weird insights to make decisions, which can lead to costly mistakes. The process soon has one more step: check if the insight is valid.

Let’s imagine a brighter scenario, if we have our nicely designed data modeling sitting there:

* **A Common Language**: With data modeling, we have a shared, unified view of the organization's data, facilitating clear communication between stakeholders.
* **Data Quality and Integrity:** Modeling constraints and relationships gives us a good starting point for ensuring data quality.

[![](https://substackcdn.com/image/fetch/$s_!aFtZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99c1c373-94ba-46c9-8261-5b939890ff82_858x452.png)](https://substackcdn.com/image/fetch/$s_!aFtZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99c1c373-94ba-46c9-8261-5b939890ff82_858x452.png)

* **Reduces Errors:** A data analyst knows exactly how to query a piece of insight. A data engineer knows exactly the location where the data is going to be loaded. Every necessary transformation is performed beforehand, leaving the data nicely organized and ready to be served. A good data model limits errors as much as possible.

### How to learn it?

The first thing we need to know is that data modeling is a process that moves from high-level business concepts to low-level technical implementation:

[![](https://substackcdn.com/image/fetch/$s_!uyEU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96bdbcce-6ff8-463b-bc84-f455d9ea400e_682x270.png)](https://substackcdn.com/image/fetch/$s_!uyEU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96bdbcce-6ff8-463b-bc84-f455d9ea400e_682x270.png)

* **Conceptual Data Model:** This is the highest-level view, focused on capturing business requirements. It identifies the core business entities (e.g., *Customers*, *Products*, *Orders*) and the relationships between them. We don’t care about the underlying technology at this phase. The **conceptual model** is used to align with stakeholders.
* **Logical Data Model:** This layer has more detail than the conceptual model. We add attributes for each entity (e.g., Customer has first\_name, email, customer\_id), identify primary keys, and data types (e.g., string, integer). We also don’t care about the technology here. The logical model acts as a bridge between business concepts and the physical implementation.
* **Physical Data Model:** This is the concrete implementation blueprint for a specific database system. It translates the logical model into tables, columns, constraints, or optimization techniques, such as clustering or partitioning. We use the terminology and features of the chosen technology here (e.g., BigQuery, Snowflake, Databricks).

Next is exploring data modeling methodologies.

The **Kimball Method (Dimensional Modeling)** offers a bottom-up approach optimized for fast and understandable analytics. The method is well documented in the book *[The Data Warehouse Toolkit](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802/ref=sr_1_1?adgrpid=153794607814&dib=eyJ2IjoiMSJ9.Z2UrxOjmDPu17XOHJRUhrBu2O8rZWFdyzMjnCDjw-SaZZw0eMhgawAoCNDpgVxeYZaTrh6wS8rXJKQyOBkw9rWZ1v6VZLAbl-Rt8ZEkTGISy3e7-Ja_V_zSTTa1y_CFiPC4txf8W361YByRmoTRG7AfSSjuO4nmb0oSJhKvhKbWS97iLfdfKGqri5pmdQYSfgRKx_K5xLyJRbdsZ8Bm8eVGXcmbFiDx8bM0iSyfA5KQ.MBUzy3_D5CRHauKL7AvxLezFhQTqU6yvZW_pnXhs9lY&dib_tag=se&hvadid=678882368344&hvdev=c&hvlocphy=9197905&hvnetw=g&hvqmt=e&hvrand=13599264063687650351&hvtargid=kwd-298692373638&hydadcr=14394_13392409&keywords=the+data+warehouse+toolkit&mcid=118ab10bac4d36bfbb4238ac19eab5f5&qid=1752682326&sr=8-1)*, which is the definitive guide to dimensional modeling.

[![](https://substackcdn.com/image/fetch/$s_!zxh9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce0b9b2b-1ac9-4884-bc68-d0fcd0baf599_1118x318.png)](https://substackcdn.com/image/fetch/$s_!zxh9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce0b9b2b-1ac9-4884-bc68-d0fcd0baf599_1118x318.png)

Its core structure is the **star schema**, consisting of a central **fact table** containing quantitative measurements or events surrounded by **dimension tables** that provide descriptive context (e.g., customer details, product information, dates).

In contrast, the **Inmon method**’s approach is top-down, advocating for the creation of a centralized, highly normalized (typically to the Third Normal Form, or 3NF) Enterprise Data Warehouse (EDW). This EDW serves as the single source of truth.

[![](https://substackcdn.com/image/fetch/$s_!pUu6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa4fe328-3a8a-4fa8-ba36-93e9f1f74c63_748x296.png)](https://substackcdn.com/image/fetch/$s_!pUu6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa4fe328-3a8a-4fa8-ba36-93e9f1f74c63_748x296.png)

Departmental data marts are then built from this normalized core to meet specific analytical needs. This method is more complex and less agile, but excels at large-scale data integration and minimizing data redundancy.

I recommend starting with the Kimball method first, as I personally see it’s easier to get started and practice. If I have to learn Kimball again, I will try to grasp its fundamentals from the book, including facts, dimensions, and the 4-step processes. If you don’t want to spend much time on the theory, [a reading guide here](https://www.holistics.io/blog/how-to-read-data-warehouse-toolkit/) is what you need.

After that, we need to practice:

* Select your favorite business domain.
* Begin by defining the business questions. For example, "What are the key performance metrics we need to track?" The answers (e.g., daily sales revenue, number of new subscribers) will form the basis of the fact tables.
* Then, ask "How do we want to slice and dice these metrics?" The answers (e.g., by customer geography, by product category, by time) will define the dimension tables.
* Construct a simple star schema.
* Check if your modeling could help you seamlessly answer your questions.
* Adjust and improve your modeling if needed.
* Get feedback and iterate.

---

## Git

### Why?

We rarely work alone. We rarely work with a single version of the data pipeline, a Python application, or a SQL script. Organizations need a way to version control their work and enable collaboration.

Git is the standard way to do this. It is an [open-source](https://git-scm.com/about/free-and-open-source) distributed version control system developed by the Linux development community in 2005. If you are entirely new to Git, you may find it takes a considerable amount of time. (Why do we need to `git clone` while we can zip and download the repo?).

However, you will soon realize the version control capabilities of Git, saving you a significant amount of time on development and making it easier to share your work. No matter how good your code is, if you don’t know Git, you will find trouble working with others.

Preventing weird things from happening on production, tracing bugs (why the previous version didn’t see this bug), building CI/CD pipelines, isolating your work from teammates, etc

Tons of benefits and practical usage.

### How to learn it?

Among the skills listed in this article, I think Git will be the easiest to learn. A toy project on GitHub, having Git installed on your laptop, and practicing commands.

The key is to understand its fundamentals before practicing.

Git sees the data as snapshots, providing powerful branching capability by leveraging pointers.

[![](https://substackcdn.com/image/fetch/$s_!kOjW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd379e439-f899-48f6-ae23-516284a30cd7_568x202.png)](https://substackcdn.com/image/fetch/$s_!kOjW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd379e439-f899-48f6-ae23-516284a30cd7_568x202.png)

A commit is a snapshot of the entire project at a specific point in time. It's a complete picture of every file and folder in the repository, exactly as they were at the time when the commit was made. A commit will have pointers pointing to its parent commit.

[![](https://substackcdn.com/image/fetch/$s_!OfCf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc27869d-d516-4511-b0e6-56b49519119b_754x312.png)](https://substackcdn.com/image/fetch/$s_!OfCf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc27869d-d516-4511-b0e6-56b49519119b_754x312.png)

A Git branch is simply a movable pointer to a commit.

[![](https://substackcdn.com/image/fetch/$s_!TsB5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F941cdcd5-1fd8-4536-a0ae-c1ceae140564_1364x404.png)](https://substackcdn.com/image/fetch/$s_!TsB5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F941cdcd5-1fd8-4536-a0ae-c1ceae140564_1364x404.png)

For more details, you can check my 15-minute guide on learning Git here:

---

## SQL

### Why?

If you work in the data field, whether you’re a data engineer, a data analyst, or a data scientist, you “speak“ SQL. The language was designed in the 1970s to manipulate and retrieve data from relational databases. Since then, it has gained increasing adoption worldwide as the primary interface for working with these databases.

[![](https://substackcdn.com/image/fetch/$s_!_gCR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e5245c1-df47-4b64-b8eb-e0ec6140da98_418x378.png)](https://substackcdn.com/image/fetch/$s_!_gCR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e5245c1-df47-4b64-b8eb-e0ec6140da98_418x378.png)

The evolution of the OLAP database and the rise of transformation tools, such as DBT or SQLMesh, make SQL an attractive choice for data transformation, which was mainly handled by procedural languages like Java or Python. Some cloud data warehouses, such as BigQuery, even allow users to utilize SQL for machine learning.

Data engineers use SQL for many things.

### How to learn it?

The first is to learn the syntax.

Start simple, working with one table: SELECT, FROM, WHERE, GROUP BY, ORDER BY, HAVING, SUM, COUNT, LIMIT… to retrieve data, and INSERT, UPDATE, DELETE to modify data.

Then, we come to work with more than one table. Learn the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN.

Next, we make it a bit harder when moving to WINDOW FUNCTION. Like GROUP BY, it performs calculations on groups of rows, but there are differences:

* **GROUP BY** collapses rows. It takes multiple rows and aggregates them into a single summary row. For example, `SELECT country, SUM(sales) FROM products GROUP BY country` will return one row for each category, showing the total sales for that category.

  [![](https://substackcdn.com/image/fetch/$s_!wdE0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecd755ca-7b11-414b-a557-33ad08bd2b32_1100x392.png)](https://substackcdn.com/image/fetch/$s_!wdE0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecd755ca-7b11-414b-a557-33ad08bd2b32_1100x392.png)
* **Window functions** operate on a "window" of rows but do not collapse them. They return a value for each row based on the defined window. For example,

  `SELECT country, SUM(sales) OVER (PARTITION BY country) AS category\_total\_sales FROM products` will return all the original product rows. However, it adds a new column (category\_total\_sales) to each row, showing the total sales for the category to which the product belongs.

  [![](https://substackcdn.com/image/fetch/$s_!Vc1G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdcc8cf-3095-4aee-a516-3b187f9a2ea4_892x382.png)](https://substackcdn.com/image/fetch/$s_!Vc1G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2cdcc8cf-3095-4aee-a516-3b187f9a2ea4_892x382.png)

Then, we come to CTEs (Common Table Expressions). They are essential for breaking down complex queries into logical, readable steps, which improves maintainability.

[![](https://substackcdn.com/image/fetch/$s_!oN1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc75f323a-e4d5-4329-bb2e-020195df41ba_332x444.png)](https://substackcdn.com/image/fetch/$s_!oN1K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc75f323a-e4d5-4329-bb2e-020195df41ba_332x444.png)

However, learning syntax alone is not enough. Data engineers must know what happens under the hood, as we not only write SQL queries but also write optimized ones. Understanding the execution order is crucial. A complete query will be executed like this.

[![](https://substackcdn.com/image/fetch/$s_!NWo_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fc98ad8-68a2-464a-b40e-a72ff463c892_918x204.png)](https://substackcdn.com/image/fetch/$s_!NWo_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fc98ad8-68a2-464a-b40e-a72ff463c892_918x204.png)

1. **FROM / JOIN**: The database first identifies the required tables and performs any joins to create the complete dataset.
2. **WHERE**: It then filters this dataset, skipping rows that do not meet the conditions. (e.g., X > 3)
3. **GROUP BY**: The remaining rows are grouped based on the values in one or more columns, preparing them for aggregation (e.g., SUM, COUNT, AVG…)
4. **HAVING**: After the rows are grouped, this clause filters out records that do not meet the aggregate conditions (e.g., SUM(X) > 3)
5. **SELECT**: The engine processes the SELECT list to determine which columns, expressions, and aggregated values to include in the final result. Window functions are also processed here.
6. **DISTINCT**: If specified, duplicate rows are removed from the result set.
7. **ORDER BY**: The final result set is sorted according to the specified columns or expressions.
8. **LIMIT / OFFSET**: The query limits the output to a specific number of rows.

> ***Note**: Some databases, such as BigQuery, also support a very useful clause called [QUALIFY](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#qualify_clause), which filters records based on the value of the window function.*

## Python

### Why?

As I mentioned, data engineers utilize SQL for various purposes, but not for everything. Python can make up for that.

[![](https://substackcdn.com/image/fetch/$s_!kVI7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5def1fce-03ea-4bfa-ba25-cceca7bb8df9_274x222.png)](https://substackcdn.com/image/fetch/$s_!kVI7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5def1fce-03ea-4bfa-ba25-cceca7bb8df9_274x222.png)

You see repetitive tasks and want to automate them. Python can do it.

You face complex transformations that are difficult to express in SQL. Python with PySpark, Pandas, or Polars can help.

Data comes from many systems. Python can help pull them via the REST API.

You need to orchestrate many data pipeline steps. Python can help with tools like Airflow or Dagster.

Or, you want to build a data application. Python can help with Streamlit or a backend framework like FastAPI.

Learning Python is a must.

### How to learn it?

Learning Python is quite easy compared to other languages, as its syntax is much simpler. There are numerous resources available to help us learn how to write a function, an if clause, or a class in Python.

However, learning syntax is never enough. Again, we rarely work alone. Writing code is not hard, but writing readable, maintainable, and extendable code needs time. Many of us start the journey by self-learning Python; thus, writing messy code is understandable.

Over time, we need to care for others who work with us. No matter how good your Python program performs, if your colleagues don’t understand what you’re doing or find it extremely challenging to extend your work, your shiny code is useless.

[![](https://substackcdn.com/image/fetch/$s_!eO5t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddf0bcf7-40a4-4524-b586-9a7cc8993946_610x298.png)](https://substackcdn.com/image/fetch/$s_!eO5t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddf0bcf7-40a4-4524-b586-9a7cc8993946_610x298.png)

Pay attention to writing organized code as soon as possible. Learning design patterns ([Python-general](https://python-patterns.guide/) or [data-pipeline-specific](https://www.startdataengineering.com/post/code-patterns/)), coding principles like [SOLID](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design), or reading the [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) book.

This might be boring at first, as it won’t give you the same feeling as your Python program runs for the first time. But when you add a piece of code without crashing the application, see your colleagues inherit your work seamlessly without pain, or someone takes your work as a reference on how they organize their code, the feeling is even more satisfying.

## OLAP system

### Why?

Oooh, this is my favorite one.

A data warehouse is a logical entity that consolidates data from multiple sources to serve analytics demand. However, the warehouse needs a physical database to store and expose the data. In the past, organizations also used the database that backed their application for this purpose.

Over time, more and more companies have realized they need to extract insights from data to gain business advantages. Database researchers saw an opportunity. Transactional databases (OLTP) cannot serve analytics workloads well because they were not designed to do so.

[![](https://substackcdn.com/image/fetch/$s_!o7nX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22c49ead-b188-4706-93cd-92bf13f2438b_378x250.png)](https://substackcdn.com/image/fetch/$s_!o7nX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22c49ead-b188-4706-93cd-92bf13f2438b_378x250.png)

The boom of OLAP systems began. BigQuery, Databricks, Snowflake, Redshift, or Clickhouse. They were designed to handle TBs or even PBs queries with the most advanced optimization technique.

[![](https://substackcdn.com/image/fetch/$s_!O4oC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe43e340c-97be-45fa-a625-080191434815_548x232.png)](https://substackcdn.com/image/fetch/$s_!O4oC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe43e340c-97be-45fa-a625-080191434815_548x232.png)

Nowadays, an OLAP database is the most important component of the data infrastructure. Most of the data-related tasks occur here: ingesting data, transforming data, serving data, or enforcing data governance.

### How to learn it?

The key to learn any OLAP system is understanding two things: how it processes data and how it stores the data. The good news is that these systems share some commonalities:

* **Overall**: Most of the OLAP systems have a share-nothing architecture; compute and storage layers are separate to achieve high scalability.

  [![](https://substackcdn.com/image/fetch/$s_!fO4G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56898076-af08-4bb5-898e-46aa12c4810d_436x260.png)](https://substackcdn.com/image/fetch/$s_!fO4G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56898076-af08-4bb5-898e-46aa12c4810d_436x260.png)
* **Processing**: Due to the high data volume, data is usually processed by multiple workers. These systems also employ techniques such as [vectorized execution](https://www.youtube.com/watch?v=FrspnYbFSxQ) and/or [code generation](https://www.youtube.com/watch?v=UPQ53hM6AWE) to enhance performance.

  [![](https://substackcdn.com/image/fetch/$s_!CM1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F240b8076-e355-41d8-af84-9570ed0dd725_642x374.png)](https://substackcdn.com/image/fetch/$s_!CM1K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F240b8076-e355-41d8-af84-9570ed0dd725_642x374.png)
* **Storage**:

  + Data in the OLAP system is stored in [column or hybrid format](https://vutr.substack.com/p/we-might-not-completely-understand).

    [![](https://substackcdn.com/image/fetch/$s_!cnWm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F964bd23e-54b0-4bef-b911-f19d8a7617b9_986x634.png)](https://substackcdn.com/image/fetch/$s_!cnWm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F964bd23e-54b0-4bef-b911-f19d8a7617b9_986x634.png)
  + The data also has rich metadata to help the query engine skip as much data as possible when processing a query.

    [![](https://substackcdn.com/image/fetch/$s_!vZRc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bb43630-ab16-42af-8270-4695efd107a1_348x422.png)](https://substackcdn.com/image/fetch/$s_!vZRc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bb43630-ab16-42af-8270-4695efd107a1_348x422.png)
  + To implement version control and support workload isolation (‘I‘ in ACID), these systems don’t allow overwriting data as written data is immutable, and changes result in writing new files.

    [![](https://substackcdn.com/image/fetch/$s_!zDeO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ea26480-fda1-4e27-9f5e-78b977596116_682x258.png)](https://substackcdn.com/image/fetch/$s_!zDeO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ea26480-fda1-4e27-9f5e-78b977596116_682x258.png)
  + To achieve scalability and cost efficiency, most systems use object storage (or storage with shared object storage characteristics).

    [![](https://substackcdn.com/image/fetch/$s_!hYJ-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd340fda-e333-4eed-b061-8f262edfe3de_382x234.png)](https://substackcdn.com/image/fetch/$s_!hYJ-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd340fda-e333-4eed-b061-8f262edfe3de_382x234.png)

Keep these things in mind, and you can explore any OLAP systems you want. For a specific solution, the best approach is to try them. Most cloud data warehouses offer a trial period for their service.

Try it, apply their recommended best practices, see how it helps with data governance, understand its pricing model, and how it can integrate with other systems.

The rise of the lakehouse paradigm means that OLAP systems are no longer the exclusive domain of vendors. A query engine (Spark, Trino) + object storage (GCS, S3) + table format (Delta Lake, Iceberg), and you have your own OLAP systems. The observation above (**Overall, Processing, Storage**) remains applicable here.

Compared to the cloud data warehouse, managing these systems on your own will take more effort, but in return, you have more control over your OLAP system.

## Orchestration

When we're working on a pet project, a single SQL script or a PySpark application is enough. However, things get complicated in production where your team has many dbt models and Python scripts that need to be run.

More importantly, they need to be run in order. A task to load data into a staging table must complete successfully before a transformation task can begin, which in turn must finish before a final reporting table is updated.

Managing this complexity manually is not a solution. Tools, such as Apache Airflow and Dagster, come to the rescue. Besides the OLAP system, a data orchestration tool is an indispensable part of the data infrastructure.

[![](https://substackcdn.com/image/fetch/$s_!ZHGP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc00068a-6df0-49bc-a360-183b1ae98dd2_700x356.png)](https://substackcdn.com/image/fetch/$s_!ZHGP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc00068a-6df0-49bc-a360-183b1ae98dd2_700x356.png)

It automates the scheduling, execution, monitoring, and management of whole data workflows. These workflows are typically represented as Directed Acyclic Graphs (DAGs), where each node in the graph is a task and the directed edges represent dependencies between tasks.

The necessity for these tools arises from key requirements of production-grade data systems:

* **Dependency Management:** Orchestrators ensure that a downstream task only runs after all its upstream dependencies have completed. Exactly what we want when we expect something like pulling an API from two sources, then joining them together.
* **Scheduling:** They provide sophisticated scheduling capabilities beyond simple time-based triggers, allowing for cron-like schedules, event-based triggers (e.g., run when a file arrives in S3), or data-aware schedules (e.g., run when an upstream data asset is available).
* **Error Handling and Retries:** Everything could fail; network issues, API servers down, or SQL error syntax are common. These systems provide built-in mechanisms to automatically retry failed tasks and perform data backfilling.
* **Monitoring and Visibility:** Orchestration tools also offer user interfaces that provide a complete, visual overview of all data pipelines. They allow engineers to monitor the status of DAG runs, inspect logs for individual tasks, and receive alerts on failures, providing critical visibility into the health of the data platform.

### How to learn it?

Keep these in mind.

* **General**:

  + **Task-Based vs. Asset-Based Orchestration:** You will see these two approaches for most orchestration tools out there. The first approach states, "Run this job, then that job" (Airflow was designed with this approach), while the latter asks, "Keep these assets (tables, models…) up-to-date?" (Dagster was designed with this approach).
  + **Idempotency and Backfilling:** These are two critical concepts for a reliable data pipeline.

    - **Idempotency** means that running a task multiple times with the same input produces the same result (e.g., f(x) = x \* 1). An idempotent pipeline can be safely retried after a failure without creating duplicate data or other side effects. A common pattern for achieving idempotency is to design jobs that overwrite a specific data partition(e.g., a specific day's data) rather than appending to it.

      [![](https://substackcdn.com/image/fetch/$s_!mDAR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e7776b3-19ff-4ad1-8020-38891a997c64_792x118.png)](https://substackcdn.com/image/fetch/$s_!mDAR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e7776b3-19ff-4ad1-8020-38891a997c64_792x118.png)
    - **Backfilling** is the process of running a pipeline for historical periods to reprocess data, perhaps to fix a bug in the original logic or incorporate late-arriving data. Idempotent design is a prerequisite for safe and easy backfilling. Orchestration tools provide the mechanisms to trigger and manage these backfill runs across specific date ranges.

      [![](https://substackcdn.com/image/fetch/$s_!hjv_!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdf647de-9616-4df5-a563-a88be201953e_1594x502.png)](https://substackcdn.com/image/fetch/$s_!hjv_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdf647de-9616-4df5-a563-a88be201953e_1594x502.png)
* For a specific tool:

  + Find out how your credentials, such as API tokens or cloud service accounts, are managed.
  + Understand how do these tools isolate tasks?

    - Dependencies: Dagster supports that each data pipeline will have its own set of Python dependencies, while Airflow manages dependencies at the global level.
    - Resource isolation: Each task in Dagster runs in a dedicated Kubernetes pod. Initially, Airflow was designed to have a set of Celery workers, and tasks can run on the same worker. Later, Airflow also supports running tasks as a Kubernetes pod.
    - Understanding these factors will make it easier for you to maintain and monitor a production-grade environment.
  + What other abstractions besides the provided ones can I extend the functionality of the tool? (e.g., Airflow has Hook and Operator concepts to allow users to customize)

    - These tools already have a lot of support for familiar data sources and destinations. However, it’s not comprehensive. Learning how to extend the support for your desired data source/destination, following the tool's best practices, is crucial.

The next step is run these tool on your laptop and write some DAGs. **Apache Airflow** is a great place to start thanks to its massive community and a vast number of integrations.

---

## Outro

Thank you for reading to the end.

In this article, I outlined six technical skills that I think every data engineer should prioritize acquiring. Each skill I shared, why it matters, and my experience in learning and using it effectively, based on my observation and experience.

Of course, there are other things we need to learn, such as data governance, cloud infrastructure, Docker, and bash scripting. However, I believe acquiring data modeling, Git, SQL, Python, OLAP systems, and Orchestration will give us a solid foundation for our careers.

And, don’t forget the feedback loop. It’s the decisive factor on how fast you master a skill.

Now, see you next time.
