---
title: "Learn the Kimball dimensional modeling with a dbt project"
channel: vutr
author: "Vu Trinh"
published: 2025-09-09
url: https://vutr.substack.com/p/deep-dive-into-the-kimball-dimensional
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "BigQuery", "Data Modeling", "Data Warehouse"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# Learn the Kimball dimensional modeling with a dbt project

*From fundamental knowledge to actual handling of SCD 2 and building facts. Available codes so you can run along.*

> Source: [Open post](https://vutr.substack.com/p/deep-dive-into-the-kimball-dimensional)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=172699790)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!Eb8H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10bca4b5-eb42-49f8-b870-2f411d0e57dc_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!Eb8H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10bca4b5-eb42-49f8-b870-2f411d0e57dc_2000x1428.png)

---

## Intro

In this article, I will attempt to stimulate a (real-life) data modeling project using dbt to manage SQL transformations. We revisit the Kimball data modeling techniques and what dbt is. Then, we start building the fact and dim tables. Especially, we will spend a lot of time dealing with SCD 2, from the hard way (using the dbt’s merge strategy) to using dbt snapshot.

***Note 1**: I used BigQuery (with 300$ free credit) as the warehouse system for this project. Feel free to connect your own data warehouse by adjusting the `profile.yml`.*

***Note 2**: I assumed you have some basic understanding of how to set up a dbt project, so that I won’t dive too much into it.*

***Note 3**: You can follow along by cloning [this repo](https://github.com/vutrinh274/dbt_kimball). Make sure you enter the cloned repo folder so that you can run the commands below. Make sure you set up your preferred data warehouse in the profiles.yml*

## The dimensional modeling

Dimensional modeling was first introduced in Ralph Kimball's 1996 book, The Data Warehouse Toolkit (1st edition). Since then, companies have been widely adopting it to organize analytic data. The approach is popular because it aligns with how business users think.

They naturally think about their operations in terms of measurable metrics and the contexts in which those metrics are observed. For example, a user might want to analyze sales performance by product category, across different regions, over the last 4 weeks. This way of thinking is inherently dimensional: products, regions, and time are all distinct perspectives or dimensions through which performance can be evaluated.

The dimensional modeling data in star schemas. Named for its resemblance to a star, the schema consists of a central fact table surrounded by multiple-dimensional tables.

### Fact

The fact table is the central table in the star schema. It stores the performance measurements resulting from an organization’s business process events. Kimball encourages us to store the low-level measurements to achieve more flexibility.

[![](https://substackcdn.com/image/fetch/$s_!fXEn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0701d9-afa8-416e-8a5c-d617a45adab1_1116x590.png)](https://substackcdn.com/image/fetch/$s_!fXEn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0701d9-afa8-416e-8a5c-d617a45adab1_1116x590.png)

Each row in a fact table corresponds to a real-life measurement event and contains:

* **Foreign Keys**: Links to the related dimension tables.
* **Measures**: Numerical values, such as revenue, quantity sold, or profit.

The data on each row is at a specific level of detail, referred to as the grain; all rows must be at the same grain level.

### Dimension

Dimension tables provide context for the facts. They describe the “who, what, where, when, how, and why.” Each table focuses on a business dimension, such as product, country, or date.

[![](https://substackcdn.com/image/fetch/$s_!6lV-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F504495ea-97bf-4820-876a-8aeb99f8d519_1256x690.png)](https://substackcdn.com/image/fetch/$s_!6lV-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F504495ea-97bf-4820-876a-8aeb99f8d519_1256x690.png)

They play a crucial role in the data warehousing system because they provide a context for measurements. A skyrocketing revenue number alone does not give insight into the business. Each dimension table has a single primary key. This key is “distributed“ to the fact tables as a foreign key.

### The four-step process

There are four steps in the dimensional design process:

* The process begins with **selecting the business process,** in which you identify the key activity or operation to analyze, such as sales or customer interactions.
* Next comes **declaring the grain**, which defines the level of detail for the analysis: “Are you tracking sales by individual transactions, daily summaries, or monthly aggregates?” This ensures consistency and scalability.
* Once we define the grain, we **identify dimensions** that capture the process's descriptive attributes, such as product details, time, or customer demographics.
* Finally, we focus on **building facts and** **the quantitative metrics** tied to the process, such as sales revenue and profit.

Each step builds on the last, ensuring the design supports the bottom-up business's analytical needs while remaining easy to query and understand.

## dbt

dbt is a CLI tool that lets us efficiently transform data with SQL.

[![](https://substackcdn.com/image/fetch/$s_!fLrG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F387c295c-7d92-4013-8e9c-5479715bec03_542x190.png)](https://substackcdn.com/image/fetch/$s_!fLrG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F387c295c-7d92-4013-8e9c-5479715bec03_542x190.png)

It’s not an engine like Spark; it’s not a database like Postgres or Snowflake; it’s a tool that helps you manage your SQL data transformation.

At the heart of dbt is the concept of the **model**. A model is an SQL query saved in a `.sql` file. Each model defines a transformation that transforms data into a desired output inside your data warehouse. When dbt runs, it executes these queries and materializes the transformed data as a table or view. Models give us a tangible form of the SQL transformation logic.

[![](https://substackcdn.com/image/fetch/$s_!V59Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09df9f99-56a4-4e63-beb5-8da710d0be82_556x264.png)](https://substackcdn.com/image/fetch/$s_!V59Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09df9f99-56a4-4e63-beb5-8da710d0be82_556x264.png)

We write dbt models and run some commands in the terminal. It will compile all the model’s code into SQL statements and execute them on the data warehouse. The model’s code combines SQL and Jinja.

[![](https://substackcdn.com/image/fetch/$s_!oG1k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31558400-e5a1-4e39-9e8b-acb2ca51dec6_338x248.png)](https://substackcdn.com/image/fetch/$s_!oG1k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31558400-e5a1-4e39-9e8b-acb2ca51dec6_338x248.png)

In this project, we will use dbt to manage our SQL transformation, from raw data to nicely organized, dimensionally modeled data.

## Don’t mistake this with data modeling.

In this project, I facilitate the data transformation through three stages: raw data is loaded as is to the landing, standardized in staging, and transformed to facts and dimensions in the curated environment. This is similar to the Medallion Architecture, where data is organized into bronze, silver, and gold layers.

Please keep in mind that the bronze, silver, and gold layers, or whatever name you prefer, are not data modeling; they’re just a way for us to facilitate data cleaning and transformation.

## Set up the dbt

### High-level setup

Depending on your data warehouse, you need to input the required information into the `profiles.yaml` so dbt can connect with the warehouse. Please visit the dbt official documentation for your preferred warehouse. In my case, I chose to go with BigQuery. Here is the thing I need to input into the `profiles.yaml`

[![](https://substackcdn.com/image/fetch/$s_!prMK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1be6bafa-2651-4a31-98c9-6fb121aa9608_576x284.png)](https://substackcdn.com/image/fetch/$s_!prMK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1be6bafa-2651-4a31-98c9-6fb121aa9608_576x284.png)

In the `dbt\_project.yml` files, besides basic configuration, I specify the location for the raw data (which is loaded by [dbt seed](https://docs.getdbt.com/reference/commands/seed)) and the processed data in staging and curated:

[![](https://substackcdn.com/image/fetch/$s_!8m0I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a754e2c-b2c5-4784-af43-3a56a5ac3cfd_484x342.png)](https://substackcdn.com/image/fetch/$s_!8m0I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a754e2c-b2c5-4784-af43-3a56a5ac3cfd_484x342.png)

### Loading example data

For the sample data, we used tables from the AdventureWorks sample dataset: product, product\_category, product\_subcategory, sale, and territories. For this project, I cooked (with the help of AI) the data to stimulate the change of the data over time. The name convention will be table\_name\_<date>, for example, product\_20250801 will be the snapshot of the product data at 2025-08-01.

> *[AdventureWorks](https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/home.html) database supports standard online transaction processing scenarios for a fictitious bicycle manufacturer - **Adventure Works Cycles**.*

[![](https://substackcdn.com/image/fetch/$s_!w6qL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f3ab867-3a1c-42ec-ae18-6d2eb7fda3d4_1820x826.png)](https://substackcdn.com/image/fetch/$s_!w6qL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f3ab867-3a1c-42ec-ae18-6d2eb7fda3d4_1820x826.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=172699790)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

With each dataset, I created three files to stimulate the data snapshot from 2025-08-01 to 2025-08-03. You can check out the CSV files in the folder: ./dbt\_bigquery/seeds.

[![](https://substackcdn.com/image/fetch/$s_!3Q8I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc9261df-bb5c-4815-98f8-e6518aaca887_366x488.png)](https://substackcdn.com/image/fetch/$s_!3Q8I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc9261df-bb5c-4815-98f8-e6518aaca887_366x488.png)

These CSV files can be loaded into the data warehouse with the commands:

```
dbt seed --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery
```

After that, we can see the data in the landing dataset on BigQuery:

[![](https://substackcdn.com/image/fetch/$s_!e6F9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7a92670-cb4f-47f6-a107-a730bcfbfb97_340x264.png)](https://substackcdn.com/image/fetch/$s_!e6F9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7a92670-cb4f-47f6-a107-a730bcfbfb97_340x264.png)

In dbt, a model can refer to the tables loaded from seed using the CSV file name, for example, sales\_20250801. However, I want to dynamically refer to the seed table using the input variable when running the dbt command (e.g., process\_date = ‘2025-08-01‘). So, I leveraged the [BigQuery ability to query a wildcard table](https://cloud.google.com/bigquery/docs/querying-wildcard-tables).

In our case, we have three sales tables: sales\_20250801, sales\_20250802, and sales\_20250803. We can read these tables by referring to sales\_\* plus specifying the exact table required by using the \_TABLE\_SUFFIX. For example:

[![](https://substackcdn.com/image/fetch/$s_!bGTU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6aee754-5c16-4b2e-b1f4-0507e9c00e23_608x130.png)](https://substackcdn.com/image/fetch/$s_!bGTU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6aee754-5c16-4b2e-b1f4-0507e9c00e23_608x130.png)

I will tweak the \_TABLE\_SUFFIX a bit so we can later use it as the `snapshot\_date` column. To do this, we first need to [declare the source](https://docs.getdbt.com/docs/build/sources) with the `schema.yaml` file in the `landing` folder, so the model from staging can read the tables loaded from seed as wildcard tables:

[![](https://substackcdn.com/image/fetch/$s_!KOde!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d9a75ef-4f92-49d7-9607-8f2cb38e4a33_1426x392.png)](https://substackcdn.com/image/fetch/$s_!KOde!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d9a75ef-4f92-49d7-9607-8f2cb38e4a33_1426x392.png)

In the staging area, I will select the wildcard table from landing by referring to the source defined in the `schema.yaml`, parse, and expose the \_TABLE\_SUFFIX as the snapshot date, like this:

[![](https://substackcdn.com/image/fetch/$s_!Y7W2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd66689fe-c798-459a-a45d-ca0cc2f82ea0_1410x448.png)](https://substackcdn.com/image/fetch/$s_!Y7W2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd66689fe-c798-459a-a45d-ca0cc2f82ea0_1410x448.png)

In the `staging` folder, there will be a total of 5 stg models associated with five raw datasets. All of them will create a view to expose the raw data as wildcard tables and let us choose which table to consume by filtering on the snapshot\_date column (parsed from \_TABLE\_SUFFIX)

* stg\_product\_categories:

  [![](https://substackcdn.com/image/fetch/$s_!j4Wr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0be72aee-1095-4c23-b1d1-42c9c199ccb7_1016x192.png)](https://substackcdn.com/image/fetch/$s_!j4Wr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0be72aee-1095-4c23-b1d1-42c9c199ccb7_1016x192.png)
* stg\_product\_subcategories

  [![](https://substackcdn.com/image/fetch/$s_!P5Ft!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fffc50f-ee73-4de8-a2d8-ac50484a9dc1_1096x192.png)](https://substackcdn.com/image/fetch/$s_!P5Ft!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fffc50f-ee73-4de8-a2d8-ac50484a9dc1_1096x192.png)
* stg\_products

  [![](https://substackcdn.com/image/fetch/$s_!uHoo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3763ffad-9007-40fb-94a8-4c42d9722d51_968x192.png)](https://substackcdn.com/image/fetch/$s_!uHoo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3763ffad-9007-40fb-94a8-4c42d9722d51_968x192.png)
* stg\_sales

  [![](https://substackcdn.com/image/fetch/$s_!QcWN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c1f3c31-fe17-4a31-aa29-fca91612730c_958x188.png)](https://substackcdn.com/image/fetch/$s_!QcWN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c1f3c31-fe17-4a31-aa29-fca91612730c_958x188.png)
* stg\_territories

  [![](https://substackcdn.com/image/fetch/$s_!8w2x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d334b62-f6b0-481a-91d7-8f9c8e4b0589_948x188.png)](https://substackcdn.com/image/fetch/$s_!8w2x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d334b62-f6b0-481a-91d7-8f9c8e4b0589_948x188.png)

We will use the snapshot\_date heavily later when building the dim and the fact tables.

## Business process and the grain of the fact table

Due to the limitations of the sample data, we have no choice but to focus on the sales process here. In a real project, please make sure you select the business process that your organization needs to observe.

There will be one fact table called `fact\_sale` that records the sales at the order level. This table will have information like order\_date, order\_number, revenue, cost, and profit of each order. Besides that, there will be two foreign keys:

* **product\_surrogate\_key**: link to the `dim\_product`. This allows slicing and dicing the fact\_sale measurement based on product information, such as color or category.
* **sales\_territory\_surrogate\_key**: link to the `dim\_territories`. This allows slicing and dicing the fact\_sale measurement based on territory information, such as country or region.

## Building dims

### SCD 2

Kimball suggests that the dimensions’ primary key should not be the same as the key used in the operational database. This decouples the way our data warehouse manages the primary key compared with how the source system manages it.

In the scope of this project, we will implement SCD 2 and use the dbt macro `dbt\_utils.generate\_surrogate\_key` to create a surrogate key. Behind the scenes, the key will be made by using MD5 to hash a list of input columns.

With type 2, if there is a change in a dimension record, we will insert a new row with the changes. The new record will have a different surrogate key compared to the original record. Fact rows can refer to the other version of the dimension table record by using the desired foreign key.

When applying Type 2, the dimensions record must include two columns: one indicating when the record is effective and one indicating when it expires. I will refer to them as `effective\_date` and `expired\_date` in this article.

[![](https://substackcdn.com/image/fetch/$s_!ToDB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe80c25cc-b2d4-4bd4-abfb-68ca854efb74_1296x588.png)](https://substackcdn.com/image/fetch/$s_!ToDB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe80c25cc-b2d4-4bd4-abfb-68ca854efb74_1296x588.png)

When the new row is added, the previously associated row is marked as “expired”. The previous row’s `end\_date` will be set to the prior date of the new row’s `start\_date` to ensure there will be no gap between them. The latest row will now have the `end\_date` of 9999-12-31.

### Overview of the dimensions we gonna to build

We will build two dimensions, the first is the `dim\_products`, which contains the following fields:

[![](https://substackcdn.com/image/fetch/$s_!7Lbs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7f84e14-62e8-40eb-91c6-728b1d633b8f_1320x832.png)](https://substackcdn.com/image/fetch/$s_!7Lbs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7f84e14-62e8-40eb-91c6-728b1d633b8f_1320x832.png)

Most of the fields can be retrieved from the `stg\_product`. Still, we need to join with `stg\_product\_categories` and `stg\_product\_subcategories` to get the `category\_name` and `subcategory\_name`. To support SCD2, we will generate the `product\_surrogate\_key` by hashing other fields.

The second is the `dim\_territories`, which contain the following fields:

[![](https://substackcdn.com/image/fetch/$s_!Rinp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb416b90-54be-4ff9-a418-e3fe7e3d9876_500x408.png)](https://substackcdn.com/image/fetch/$s_!Rinp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb416b90-54be-4ff9-a418-e3fe7e3d9876_500x408.png)

All of the fields can be retrieved from the `stg\_territories`. To support SCD2, we will generate the `sales\_territory\_surrogate\_key` by hashing other fields.

Now, we will look into the detailed logic.

### SCD 2 implementation in dbt models

To implement the SCD type 2, there are the following steps we need to follow:

* Initiate the dimension table with all records that have `is\_current` is true, effective\_date is the date we process the table (or the date based on your need), and expired date is set to `9999-12-31`

  [![](https://substackcdn.com/image/fetch/$s_!DxaI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e7517a1-7f36-4fb4-8641-88a0ff2dab73_680x278.png)](https://substackcdn.com/image/fetch/$s_!DxaI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e7517a1-7f36-4fb4-8641-88a0ff2dab73_680x278.png)

  + We still need to maintain the business key to detect changes from the source.
  + For the surrogate key, we will hash the columns that are supposed to be changed. This key will be used to track different versions of a record with the same business key.
* When new data comes (complete snapshot or incremental change), we will compare it with the current state of our dimensions (is\_current = true) to extract two types of records:

  [![](https://substackcdn.com/image/fetch/$s_!bDPH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57273068-7513-48c3-b0a3-c08ed38e0d75_772x508.png)](https://substackcdn.com/image/fetch/$s_!bDPH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57273068-7513-48c3-b0a3-c08ed38e0d75_772x508.png)

  + **Type 1**: Records with business keys do not exist in the dimension table. This means these records are new ones. We insert them into the dimension table with the is\_current flag set to True.
  + **Type 2**: Records with business keys exist in the dimension table and have different surrogate keys, which means the existing records have new versions. We also insert them into the dimension table with the is\_current flag set to True.

    > **Note**: Types 1 and 2 are only my personal annotations.

    - However, we still need to do one more action with this type. Old versions in the dimension table must be expired by setting the expired\_date to the prior\_date of the effective\_date of the new version, and the is\_current flag is now set to false.

      [![](https://substackcdn.com/image/fetch/$s_!rtyg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48b1aabd-ed4a-4a61-b87d-b27c34bed3d3_480x324.png)](https://substackcdn.com/image/fetch/$s_!rtyg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48b1aabd-ed4a-4a61-b87d-b27c34bed3d3_480x324.png)
  + For records that have the same business and surrogate keys as existing ones, we don’t need to do anything, as this indicates the records do not change.

To implement the process in dbt, I chose the [merge strategy](https://docs.getdbt.com/docs/build/incremental-strategy#merge). I am aware that dbt suggests using the snapshot feature for SCD 2, but I want to take the harder approach first to ensure I fully understand SCD 2. We’ll go ahead and visit the approach of [using the snapshot later](https://docs.getdbt.com/docs/build/snapshots#what-are-snapshots).

With the merge strategy, dbt requires us to specify the unique keys at least so it can execute the merge statement behind the scenes for us; if the incoming records have keys that exist in the target table, dbt updates them (we can also choose columns to update), if the keys don’t match, dbt inserts those records.

Based on the description at the beginning of this section, we have to give dbt the dataset with the following things so it can update the dimension table:

[![](https://substackcdn.com/image/fetch/$s_!XlzZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f4d56b-f87a-4579-a2f0-120a8c3b163a_526x262.png)](https://substackcdn.com/image/fetch/$s_!XlzZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7f4d56b-f87a-4579-a2f0-120a8c3b163a_526x262.png)

* Complete new records: The merge statement inserts them as new records. (Records with biz keys don’t exist in the dim)
* New version of the existing records: The merge statement inserts them as new records (Records with biz keys exist in the dim but have different surrogate key)
* Existing records with is\_current = false + expired\_date = prior date to the effective date of the new version: The merge statement updates the existing records.

[![](https://substackcdn.com/image/fetch/$s_!5qA9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa102c218-d105-41f5-9071-a2fe000ee5dd_1144x268.png)](https://substackcdn.com/image/fetch/$s_!5qA9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa102c218-d105-41f5-9071-a2fe000ee5dd_1144x268.png)

For the `dim\_product`, I choose: `product\_surrogate\_key`, `product\_key`, `effective\_date` for the unique key. To retrieve all the fields for the `dim\_product`, we need data from three tables: `stg\_products`, ``stg\_product\_subcategories` and `stg\_product\_categories`

[![](https://substackcdn.com/image/fetch/$s_!b5PQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7ec7518-84e1-4921-b656-b8170ca8ecf9_490x806.png)](https://substackcdn.com/image/fetch/$s_!b5PQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7ec7518-84e1-4921-b656-b8170ca8ecf9_490x806.png)

All of them are filtered by the `snapshot\_date`, which is the \_TABLE\_SUFFIX from the wildcard table. (You can scroll up to the `Loading example data` section to revisit it.) The `process\_date` is the input variable that can be specified by using this when running the dbt command:

```
dbt run -s dim_product --vars '{"process_date": "2025-08-03"}'
```

For the initial running of the dbt models, I set the default `process\_date` to be `2025-08-01` in the `dbt\_project.yml` so that the first run will always process the `2025-08-01` snapshot.

[![](https://substackcdn.com/image/fetch/$s_!S8TO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbd32b57-c3a4-4657-93fa-85c2c218d4a9_490x102.png)](https://substackcdn.com/image/fetch/$s_!S8TO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbd32b57-c3a4-4657-93fa-85c2c218d4a9_490x102.png)

After selecting the required staging models, we define the logic to join them and generate the surrogate key:

[![](https://substackcdn.com/image/fetch/$s_!ChQG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40e179b7-4980-41dc-8768-7acd17550462_824x770.png)](https://substackcdn.com/image/fetch/$s_!ChQG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40e179b7-4980-41dc-8768-7acd17550462_824x770.png)

> **Note:** that you only need to hash columns that are supposed to change for the surrogate key. For the `dim\_product`, I assumed all fields can be changed.

Next, we will handle the logic for two scenarios:

* **The first run**: We initiate the dimension table with the first processed snapshot (it will always be the `2025-08-01`), all records will be the latest version (is\_current = true)
* **The incremental run**: We extract the data from the processed snapshot and merge it into the dimension table based on the logic defined at the beginning of this section.

dbt allows us to distinguish between the first run and the incremental run by the `is\_incremental` macro:

[![](https://substackcdn.com/image/fetch/$s_!wwH4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1049e77-6669-4bd1-8f18-7f7ed1da80c8_334x266.png)](https://substackcdn.com/image/fetch/$s_!wwH4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1049e77-6669-4bd1-8f18-7f7ed1da80c8_334x266.png)

To be more precise, dbt distinguishes between the incremental and the full\_refresh run. For the incremental model, the first time the model is run, dbt will full\_refresh it by loading the complete historical data. For example, one can leverage the is\_incremental macro to specify that the filter on the snapshot\_date only applies if it is an incremental run.

[![](https://substackcdn.com/image/fetch/$s_!-RHC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a0f95f-4faf-434a-94f4-5367fe3de2e2_416x154.png)](https://substackcdn.com/image/fetch/$s_!-RHC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96a0f95f-4faf-434a-94f4-5367fe3de2e2_416x154.png)

In this project, I believe that loading the complete historical data when stimulating the SCD 2 is unnecessary. Therefore, I always specify the snapshot\_date filter, regardless of whether the run is incremental or full\_refresh. The first run will always take the default value of the process\_date, indicating that the `dim\_product` table will always be initialized with snapshot `2025-08-01`

[![](https://substackcdn.com/image/fetch/$s_!LzPW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90b91c9a-63a8-4578-bedd-3244cf0b9e6b_656x586.png)](https://substackcdn.com/image/fetch/$s_!LzPW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90b91c9a-63a8-4578-bedd-3244cf0b9e6b_656x586.png)

In our `dim\_product` model, the first run simply selects the data from the `source` CTE:

[![](https://substackcdn.com/image/fetch/$s_!nS4H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6baeea3-7041-4ad4-916a-56072a40efa1_666x826.png)](https://substackcdn.com/image/fetch/$s_!nS4H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6baeea3-7041-4ad4-916a-56072a40efa1_666x826.png)

For the incremental run, we need to do the following things:

* To compare with the current state of the dimension table, we use the [`this` keyword](https://docs.getdbt.com/reference/dbt-jinja-functions/this). The comparison only needs to happen between the latest versions of existing records and the new data, so we filter only records where the flag is\_current is true.

  [![](https://substackcdn.com/image/fetch/$s_!ppWj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edaf563-129f-4f82-8439-705755dce4de_382x256.png)](https://substackcdn.com/image/fetch/$s_!ppWj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edaf563-129f-4f82-8439-705755dce4de_382x256.png)
* We then join this data with the data from the source CTE (using the business key, the `product\_key`) to detect changes:

  [![](https://substackcdn.com/image/fetch/$s_!6AZg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b09d96d-519b-4e72-a4a1-aa7ee89fb00c_540x758.png)](https://substackcdn.com/image/fetch/$s_!6AZg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b09d96d-519b-4e72-a4a1-aa7ee89fb00c_540x758.png)
* We then identified the two types of changes based on the following conditions:

  [![](https://substackcdn.com/image/fetch/$s_!MlLJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed373d16-b3e2-43d7-b07a-925627a448e9_846x482.png)](https://substackcdn.com/image/fetch/$s_!MlLJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed373d16-b3e2-43d7-b07a-925627a448e9_846x482.png)

  + **Type 1**: Records with business keys do not exist in the dimension table. This means these records are new ones. We insert them into the dimension table with the is\_current flag set to True. Used condition is:

  ```
  t_product_key is null
  ```

  + **Type 2**: Records with business keys exist in the dimension table and have different surrogate keys, which means the existing records have new versions. We also insert them into the dimension table with the is\_current flag set to True. Used condition is:

  ```
  t_product_key is not null AND s_product_surrogate_key != t_product_surrogate_key
  ```
* We also need to expire the existing record:

[![](https://substackcdn.com/image/fetch/$s_!Xrcn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e5afec6-f899-430d-a022-a3a862c51100_904x500.png)](https://substackcdn.com/image/fetch/$s_!Xrcn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e5afec6-f899-430d-a022-a3a862c51100_904x500.png)

* The new data and the expired data will be UNIONed and selected like this:

  [![](https://substackcdn.com/image/fetch/$s_!6Oyz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbff09a6-0767-474c-8039-d38e6531a85c_558x438.png)](https://substackcdn.com/image/fetch/$s_!6Oyz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbff09a6-0767-474c-8039-d38e6531a85c_558x438.png)
* This data will then be merged by dbt; changes data will be inserted as new records, and expired data will be updated on existing records.

Next, we will run the `dim\_product` model:

```
dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s dim_product -f
```

For a random check, we see a product with product key 601 has an initial version with an effective date of `2025-01-08`, expired\_date is `9999-12-31`, and the is\_current flag is true:

[![](https://substackcdn.com/image/fetch/$s_!FHaf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73259f8d-bc74-4836-97fd-bb9a50b6c535_1204x424.png)](https://substackcdn.com/image/fetch/$s_!FHaf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73259f8d-bc74-4836-97fd-bb9a50b6c535_1204x424.png)

To stimulate the incremental run of the process of the snapshot `2025-08-02`, we run this command:

```
dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s dim_product --vars '{"process_date": "2025-08-02"}'
```

[![](https://substackcdn.com/image/fetch/$s_!N-TZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d2b9e6b-a781-4ce5-8c4a-f3c7d52260ee_1292x548.png)](https://substackcdn.com/image/fetch/$s_!N-TZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d2b9e6b-a781-4ce5-8c4a-f3c7d52260ee_1292x548.png)

Upon re-checking, we find that product 601 now has a new version with an updated subcategory\_name value. This new record is marked as current and has a different surrogate key. The previous version is marked false for the is\_current flag, and the expired date is now updated to the prior date of the new version’s effective date.

For the `dim\_territories`, the logic is quite the same so that I won’t describe it here.

### dbt snapshot

When researching the “authentic“ way to handle SCD 2 on dbt, numerous resources recommend using a [dbt snapshot](https://docs.getdbt.com/docs/build/snapshots#what-are-snapshots), which implements the SCD 2 behind the scenes to monitor changes for a table. I initially intended to use it, but I decided to switch to the harder approach described above because I believe it would help me better understand the technique.

After experiencing the joy, I’m now back with the snapshot approach.

dbt snapshot monitors a configured table ([using a .yml file in the snapshots folder](https://docs.getdbt.com/reference/resource-configs/snapshots-jinja-legacy)). We specify the source table, the target location of the snapshot monitor result, and the strategy to check changes.

For the `dim\_product`, we need to cheat a bit as the logic requires data from multiple tables. I will create a model called `tmp\_dim\_product\_snapshot`, which is overwritten by data from a specific snapshot:

[![](https://substackcdn.com/image/fetch/$s_!Z18e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fa139d5-f0cd-4b2d-9259-773aed26c0dc_766x640.png)](https://substackcdn.com/image/fetch/$s_!Z18e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fa139d5-f0cd-4b2d-9259-773aed26c0dc_766x640.png)

Next, we register this table as the dbt source so we can refer to it in the snapshot configuration:

[![](https://substackcdn.com/image/fetch/$s_!Dnr8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6f11691-6594-420d-8731-f965bf0d73b7_432x236.png)](https://substackcdn.com/image/fetch/$s_!Dnr8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6f11691-6594-420d-8731-f965bf0d73b7_432x236.png)

We then register this table for snapshot monitoring:

[![](https://substackcdn.com/image/fetch/$s_!3RHo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7533674-4fe2-4b35-ab8b-33d9a81a77ad_904x584.png)](https://substackcdn.com/image/fetch/$s_!3RHo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7533674-4fe2-4b35-ab8b-33d9a81a77ad_904x584.png)

Now we can test whether the snapshot works. The workflow will be like this:

* Run the `tmp\_dim\_product\_snapshot` model with the default snapshot (`2025-08-01`). The table `tmp\_dim\_product\_snapshot` will contain only `2025-08-01` data.

  ```
  dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s tmp_dim_product_snapshot
  ```
* Run `dbt snapshot` to detect change; the result will be written in our configured location.

  ```
  dbt snapshot --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery
  ```
* Randomly check product\_key 601, we get:

  [![](https://substackcdn.com/image/fetch/$s_!M3PG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F002d9219-3de3-4a00-841b-d75b6482a1eb_1682x936.png)](https://substackcdn.com/image/fetch/$s_!M3PG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F002d9219-3de3-4a00-841b-d75b6482a1eb_1682x936.png)
* Ovewriting the `tmp\_dim\_product\_snapshot` model with the snapshot (`2025-08-02`). The table `tmp\_dim\_product\_snapshot` will contain only `2025-08-02` data.

  ```
  dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s tmp_dim_product_snapshot --vars '{"process_date": "2025-08-02"}'
  ```
* Run `dbt snapshot` again and re-check the product\_key 601, we get:

  [![](https://substackcdn.com/image/fetch/$s_!0mAP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5e7e5e9-bf7b-4af1-a4ff-7c2f5a59d62a_1676x814.png)](https://substackcdn.com/image/fetch/$s_!0mAP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5e7e5e9-bf7b-4af1-a4ff-7c2f5a59d62a_1676x814.png)
* Ovewriting the `tmp\_dim\_product\_snapshot` model with the snapshot (`2025-08-03`).

  ```
  dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s tmp_dim_product_snapshot --vars '{"process_date": "2025-08-03"}'
  ```
* Run `dbt snapshot` again and re-check the product\_key 601, we get:

  [![](https://substackcdn.com/image/fetch/$s_!9NGc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63f5fdc1-a31a-431a-bad5-159179f80d45_1676x838.png)](https://substackcdn.com/image/fetch/$s_!9NGc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63f5fdc1-a31a-431a-bad5-159179f80d45_1676x838.png)

It's pretty much the same when we manually write the logic to handle SCD2.

### Quick thoughts

In this project, I manually implemented the SCD 2 logic for learning purposes. For the production environment, the snapshot approach is a better choice, as dbt will handle all aspects of the SCD 2 logic, which I find quite complex to develop and debug.

To use a snapshot, we need a table that is updated in place, and it must be defined as a dbt source. Sometimes, we need to work around a bit, as seen in the example above. This involves creating a tmp table that is updated by overwriting it with data from a specific snapshot\_date, registering it as a dbt source, and then configuring it for dbt snapshot monitoring.

Perhaps I’m not implementing the dbt snapshot according to best practices, which is why I feel that defining a dbt model and then registering its materialization result as a dbt source looking like a workaround. If you have any experience implementing SCD 2 with dbt snapshot, please share your insights by leaving a comment.

## Building facts

For the `fact\_sale` model, I chose the [insert\_overwrite](https://docs.getdbt.com/docs/build/incremental-strategy#insert_overwrite) strategy to load snapshot data. I chose this strategy because it can ensure that running the model for the same snapshot date will be idempotent. The [append](https://docs.getdbt.com/docs/build/incremental-strategy#append) strategy can also do the work, but it will cause duplicate data when running a model multiple times.

[![](https://substackcdn.com/image/fetch/$s_!QJAc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa5fd10e-609a-442d-8e6a-d7d513073590_752x668.png)](https://substackcdn.com/image/fetch/$s_!QJAc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa5fd10e-609a-442d-8e6a-d7d513073590_752x668.png)

To obtain the surrogate key from `dim\_product` and `dim\_territories`, we join them using the business key (product\_key and sales\_territory\_key). We then verify that the snapshot\_date falls within the effective\_date and expired\_date ranges for the valid version.

To stimulate the incremental runs of the `fact\_sale`, we run these commands:

```
dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s fact_sale -f
```

```
dbt run --profiles-dir ./dbt_bigquery --project-dir ./dbt_bigquery -s fact_sale --vars '{"process_date": "2025-08-02"}
```

## Queries to answer biz question

After that, we can run some queries to answer questions, such as the revenue and cost broken down by order date and the category\_name:

[![](https://substackcdn.com/image/fetch/$s_!l9__!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1673c7fe-2fe5-4b5c-94b2-ac9f47222bec_724x620.png)](https://substackcdn.com/image/fetch/$s_!l9__!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1673c7fe-2fe5-4b5c-94b2-ac9f47222bec_724x620.png)

We join the `fact\_sale` with the `dim\_product` (using the `product\_surrogate\_key`) to get the category\_name. For the `dim\_territories`, we can simply join `fact\_sale` with it using the `sale\_territory\_surrogate\_key`

## Outro

In this article, we first revisit the fundamentals of the dbt and Kimball modeling techniques. We then set up the dbt project, load the data source, and spend a significant amount of time building the dim models with SCD 2 with both approaches: manually defining the incremental models vs using dbt snapshot. We later create the fact table by extracting measurements from the sales table and foreign keys from the built dimensions.

Thank you for reading this far. See you in my next article.

## Reference

*[1] [dbt official documentation](https://docs.getdbt.com/docs/introduction)*

*[2] Ralph Kimball, Margy Ross, [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) (3rd Edition)*
