---
title: "(1/2) I analyzed the pricing models of 5 famous cloud data warehouses so you don't have to."
channel: vutr
author: "Vu Trinh"
published: 2026-03-03
url: https://vutr.substack.com/p/12-i-analyzed-the-pricing-models
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# (1/2) I analyzed the pricing models of 5 famous cloud data warehouses so you don't have to.

*Part 1: Microsoft Fabric, AWS Redshift, and Google BigQuery.*

> Source: [Open post](https://vutr.substack.com/p/12-i-analyzed-the-pricing-models)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=188677941)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!5i16!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcafc79eb-dca0-4c08-89d1-6f251a6d23ae_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!5i16!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcafc79eb-dca0-4c08-89d1-6f251a6d23ae_2000x1429.png)

---

# Intro

Compared to 20 years ago, the ability to store and process large amounts of data to extract insights is far easier to obtain. No more complex MapReduce jobs, no more using OLTP systems for analytical workloads, no more hardware purchase upfront.

Now, you can have a cloud data warehouse solution, such as Snowflake or Databricks, after a few clicks, and they also allow you to try the solutions for free to see if their offering suits your needs.

Everything is abstracted. Most of the time, you write and submit the SQL queries. You need to understand how the pricing models work so you can achieve the desired performance while keeping billing reasonable.

My first intention is to demystify the pricing models of all five cloud data warehouses: Microsoft Fabric, AWS Redshift, Google BigQuery, Databricks, and Snowflake, in an article. After diving into the writing process, I found that it might be too long, so I split it into two parts.

The first part (this article) will cover the pricing models of Microsoft Fabric, AWS Redshift, and Google BigQuery, and the second part will cover the pricing models of Databricks and Snowflake, along with my general best practices for keeping your data warehouse costs under control.

> ***Note 1**: This article won’t debate which solution is cheaper, as costs depend on many factors that vary by your organization's context and requirements. Instead, my purpose is to give you guys a simplified view of the pricing models for cloud data warehouses, which can sometimes be hard to understand at first glance. Also, feel free to correct me if you see anything wrong.*
>
> ***Note 2**: This article focuses on the scenarios when you store your data directly in the cloud data warehouse's proprietary storage. Plus, in each warehouse, I only cover the compute and storage cost.*

---

# Microsoft Fabric

[In 2023, Microsoft introduced Microsoft Fabric](https://azure.microsoft.com/en-us/blog/introducing-microsoft-fabric-data-analytics-for-the-era-of-ai/), a unified analytics platform that brings together many of Microsoft’s analytics tools. Including the Azure Synapse Analytics, the Microsoft data warehouse solution.

[![](https://substackcdn.com/image/fetch/$s_!A75D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa39f3684-d7ea-4cfd-9a1a-0c0358e41cd2_1114x584.png)](https://substackcdn.com/image/fetch/$s_!A75D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa39f3684-d7ea-4cfd-9a1a-0c0358e41cd2_1114x584.png)

With the Microsoft Fabric announcement, there are two existing ways to get data warehouse capabilities in Azure:

* Use Azure Synapse Analytics
* Use the Micro Fabric platform.

However, as I read Microsoft’s documentation, [they recommend using Fabric for now because it will receive ongoing optimizations and features, while Synapse will remain supported but won’t receive new features](https://blog.fabric.microsoft.com/en-us/blog/two-years-on-how-fabric-redefines-the-modernization-path-for-synapse-users). The Fabric also promises to have better performance and lower cost.

I believe many users still use Synapse and have not migrated to Fabric, so I will cover the pricing models for both approaches here.

## Compute

### Synapse

Users can run SQL analytics workloads on Azure Synapse Analytics in two ways.

[![](https://substackcdn.com/image/fetch/$s_!1_4Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089d7e9e-0ca6-4a4b-9640-d95dafc69a12_1040x788.png)](https://substackcdn.com/image/fetch/$s_!1_4Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F089d7e9e-0ca6-4a4b-9640-d95dafc69a12_1040x788.png)

**First, you purchase a Dedicated SQL pool**, which is a set of provisioned resources. The pool’s size is determined by Data Warehousing Units (DWU). The more premium the pool, the more DWU it has and the higher the rate.

[![](https://substackcdn.com/image/fetch/$s_!l8QW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8da27500-a470-41ce-86a6-7cd3263210d7_2302x568.png)](https://substackcdn.com/image/fetch/$s_!l8QW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8da27500-a470-41ce-86a6-7cd3263210d7_2302x568.png)

[Source](https://azure.microsoft.com/en-us/pricing/details/synapse-analytics/).

The pool’s rate also depends on the region: Pool DW100c charges $1.20/hour in East US 2, while in the central US it charges $1.51/hour. The user can purchase reserved capacity for the dedicated SQL pool resource for a 1-year or 3-year period to benefit from the discount.

The user will be billed hourly for the pool usage.

```
SQL pool compute cost = Pool rate per hour * Usage times in hours
```

The user can pause the data warehouse to save cost; however, only if the user pauses the warehouse for the entire hour. If the warehouse was first active but then paused, then the user will be charged for that hour.

[![](https://substackcdn.com/image/fetch/$s_!h4L1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc4e0b78-f45d-47a1-94bf-7afaf8c6177c_1298x276.png)](https://substackcdn.com/image/fetch/$s_!h4L1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc4e0b78-f45d-47a1-94bf-7afaf8c6177c_1298x276.png)

A more important note is that your compute hour billing is calculated based on the highest pool size you used during that hour. For example, if you use DW100c from 1:00 to 1:45 and then DW200C from 1:46 to 1:52, your entire hour’s billing will be calculated at the DW200C rate.

[![](https://substackcdn.com/image/fetch/$s_!y_ZY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34ee7978-8db7-4331-a884-33295b8059cd_1304x368.png)](https://substackcdn.com/image/fetch/$s_!y_ZY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34ee7978-8db7-4331-a884-33295b8059cd_1304x368.png)

**Second, users can run SQL on Azure Synapse using the Serverless approach,** which bills them based on the amount of processed data. The rate is $5/TB, no matter which region you’re in.

[![](https://substackcdn.com/image/fetch/$s_!WqCb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23e15872-ac93-45ed-9b60-84e59bd89189_1740x200.png)](https://substackcdn.com/image/fetch/$s_!WqCb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23e15872-ac93-45ed-9b60-84e59bd89189_1740x200.png)

### Fabric

Microsoft Fabric uses a **capacity-based** pricing model. Unlike the old model, where you have to pay for each service separately, for example, you pay for Synapse for warehousing and Power BI for reporting, in Fabric, you pay for a pool of compute power that all the data tasks, like engineering, science, warehousing, or reporting, share. This simplified the billing.

[![](https://substackcdn.com/image/fetch/$s_!l-1Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8559ed43-7873-4739-b7a5-a92f5bf9a533_994x676.png)](https://substackcdn.com/image/fetch/$s_!l-1Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8559ed43-7873-4739-b7a5-a92f5bf9a533_994x676.png)

A user purchases a specific SKU (e.g., F2 or F64), and each SKU has a different available number of CUs.

[![](https://substackcdn.com/image/fetch/$s_!5KT3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05520d6e-4e23-4453-80f5-3cf924d4727e_930x490.png)](https://substackcdn.com/image/fetch/$s_!5KT3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05520d6e-4e23-4453-80f5-3cf924d4727e_930x490.png)

[Source](https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/)

CUs, or Capacity Unit seconds, are the unit Fabric uses to measure your compute power over time. If the F4 SKU has 4 CU, you will have 4 CUs per second, or 345,600 CUs a day. Whenever you run a task, such as querying the data warehouse or transforming data with Spark, it will consume CUs.

[![](https://substackcdn.com/image/fetch/$s_!Z_Ba!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ed592a6-123a-4fd8-82c5-44dc9d60ba2a_1076x626.png)](https://substackcdn.com/image/fetch/$s_!Z_Ba!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ed592a6-123a-4fd8-82c5-44dc9d60ba2a_1076x626.png)

Users can automatically adjust compute capacity by scaling up or down the SKUs they need. The rate for each SKU can vary by region: the F2 SKU will cost $0.36/hour in East US 2, while the same SKU will cost $0.40/hour in West US.

[![](https://substackcdn.com/image/fetch/$s_!-OTc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90b61eb1-8e42-473c-997f-57b47031ba52_1502x518.png)](https://substackcdn.com/image/fetch/$s_!-OTc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90b61eb1-8e42-473c-997f-57b47031ba52_1502x518.png)

Like Synapse pool, users can commit to a 1-year or 3-year reservation to get the discount.

[Several mechanisms](https://learn.microsoft.com/en-us/fabric/enterprise/throttling) in Fabric allow you to use the CUs more flexibly:

[![](https://substackcdn.com/image/fetch/$s_!rjt1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fbf2377-a738-4c85-a4e8-c3bbc214e6bc_1786x616.png)](https://substackcdn.com/image/fetch/$s_!rjt1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fbf2377-a738-4c85-a4e8-c3bbc214e6bc_1786x616.png)

* **Bursting** is the ability of your capacity to consume more resources than your SKU technically allows for a short period.
* **Smoothing** is the mechanism that balances those “bursts” over time. Fabric spreads (or “smooths”) the burst CU-second consumption over the 24-hour period.
* To some extent, you will run out of capacity if you continuously burst. Fabric will apply **throttling** progressively.

## Strorage

### Synapse

In the Dedicated SQL pool approach, data is stored in Azure Storage, so compute and storage costs are billed separately.

You’re billed for stored data at a rate of $0.01 per TB per month. The stored data includes the data warehouse files, the last 7 days of incremental backups, and a geo-redundant copy (if enabled)

The rate varies across regions: East US is $23/TB/month, while West US is $27.752/TB/month.

[![](https://substackcdn.com/image/fetch/$s_!cKrF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f9c9cae-9431-4de0-893f-b9c82fd6c0f6_974x512.png)](https://substackcdn.com/image/fetch/$s_!cKrF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f9c9cae-9431-4de0-893f-b9c82fd6c0f6_974x512.png)

Fabric will sell you 1TB allocations. If your data volume exceeds 1TB, you will need to allocate an additional 1 TB. The storage cost will be rounded to the nearest TB. If you use the total of 750GB of data, you will be billed for 1 TB.

### Fabric

In Fabric, data is stored in OneLake. Microsoft built the solution on Azure Data Lake Storage Gen2 (ADLS Gen2). The user can store any file, structured or unstructured, in OneLake. Fabric stores your data in a Delta Lake-Parquet format by default.

OneLake costs are categorized into three storage types: regular OneLake storage, Business Continuity and Disaster Recovery (BCDR) OneLake storage, and OneLake cache. Each type will charge you at different rates per GB per month. Those rates vary across regions. In the East US, the OneLake storage rate is $0.026/GB/month.

This storage pricing model is more modern than the one in the dedicated SQL pool, where you’re charged for the data space you don’t use, as Microsoft will round up to the nearest TBs, plus storage is sold as 1TB allocations.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=188677941)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

## AWS Redshift

Amazon Redshift, AWS’s data warehouse service, offers two deployment options: provisioned and serverless.

## Compute

A Redshift warehouse is a cluster of computing resources called nodes. Amazon Redshift offers different node types categorized into two generations: dc2 and RA3

### Provisioned - dc2 generation

dc2 is the legacy generation, in which data is stored directly on the nodes. dc2 offers two node types with different CPU, RAM, and disk capacities. The node usage is billed hourly. The higher the resource type’s capacity, the higher the rate per hour. The rate varies across regions.

[![](https://substackcdn.com/image/fetch/$s_!vq1M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F508a175d-45c7-4d64-a151-3e9aede7ef6b_2360x614.png)](https://substackcdn.com/image/fetch/$s_!vq1M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F508a175d-45c7-4d64-a151-3e9aede7ef6b_2360x614.png)

dc2 pricing in the US East region. [Source](https://aws.amazon.com/redshift/pricing/)

The cost of using dc2 cluster is calculated by:

```
Monthly Redshift cost = Instance Rate * Number of instances * Total usage hours
```

An important note here is that the DC2 cluster cost includes storage, as data is stored directly on the compute nodes’ SSDs.

[![](https://substackcdn.com/image/fetch/$s_!S5wv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e8a0d2f-935f-4ba2-986b-47dfc295c6d7_982x790.png)](https://substackcdn.com/image/fetch/$s_!S5wv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e8a0d2f-935f-4ba2-986b-47dfc295c6d7_982x790.png)

This means that if you need more storage capacity, you must add new instances, which might not be cost-efficient, as you might be charged for the unused CPUs and RAM on those instances.

Users can get discounts when they purchase node reservations, which are commitments to using the instances for a period.

### Provisioned - RA3 generation

RA3 is the current generation, in which data is stored separately in Redshift Managed Storage. RA3 offers four node types with different resource capacities. The compute cost of the RA3 cluster is similar to that of the DC2 instances.

However, unlike the dc2 generation, the cluster’s cost does not include storage, as RA3 instances store data in Redshift Managed Storage. This means the user can scale compute and storage independently.

[![](https://substackcdn.com/image/fetch/$s_!bC0i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73ab998b-02d0-4889-857f-c110600bc41d_1012x598.png)](https://substackcdn.com/image/fetch/$s_!bC0i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73ab998b-02d0-4889-857f-c110600bc41d_1012x598.png)

Users can also get discounts when they purchase node reservations.

### Serverless

In this model, users don’t need to worry about instances, as the Redshift data warehouse automatically scales up or down based on workload. Serverless Redshift usage is measured in Redshift Processing Units (RPUs).

Users will be charged for the workloads they run in RPU-hours, on a per-second basis (with a 60s minimum). The RPU rate varies across regions. The RPU in US East will cost you $0.375 per RPU hour

The user can optionally set the following settings to control the performance and costs of the serverless workload:

* Base: the base capacity.
* Max (Usage Limit): A budget cap (RPU-hours) set over a period (daily, weekly, or monthly)
* MaxRPU (Max Capacity): The absolute upper limit for scaling.

## Storage

### Provisioned - dc2 generation

Storage costs for the dc2 cluster are included in the instance cost.

### Provisioned - RA3 generation

As discussed, the RA3 cluster stores data in Redshift Managed Storage. Each node stores hot data locally on SSDs and long-term data in Amazon S3. If data exceeds the local capacity, it will be automatically offloaded into S3.

[![](https://substackcdn.com/image/fetch/$s_!hH74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3af4e59d-11fb-454e-a9a2-f5a8289dcfcd_706x280.png)](https://substackcdn.com/image/fetch/$s_!hH74!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3af4e59d-11fb-454e-a9a2-f5a8289dcfcd_706x280.png)

The user will pay the same storage rate for Redshift-managed storage, regardless of whether the data lives in SSDs or in Amazon S3.

That said, the total storage cost in Redshift Managed Storage is calculated by:

```
Monthly Redshift Managed Storage cost = Total volume data in GB *  Rate/GB/month
```

The rate varies across different regions. The rate in US East is 0.024$/GB/Month.

### Serverless

Redshift Serverless will store data in Redshift Managed Storage, so please see the section above.

---

# Google BigQuery

## Compute

To understand the BigQuery compute cost, we must understand the concept of a slot.

It is an abstract compute unit used by BigQuery to execute SQL queries or other jobs. BigQuery automatically determines how many slots a query needs. Unlike other warehouses, you don’t need to care about VM instances in BigQuery, as Google designed the warehouse to be serverless.

[![](https://substackcdn.com/image/fetch/$s_!n_BU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad5048f8-85ef-4824-8b0a-926d6d4ee00e_738x454.png)](https://substackcdn.com/image/fetch/$s_!n_BU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad5048f8-85ef-4824-8b0a-926d6d4ee00e_738x454.png)

All you need to know is slots.

There are two pricing models for the compute: on-demand and capacity. Both of them use slots to execute your queries.

### On-demand

In this model, you’re charged based on the amount of processed data multiplied by the rate per TB. The rate varies across different Google Cloud regions. In the US-central-1 region, the rate is $6.25 / 1TB. Your first TB of the month will be free.

[![](https://substackcdn.com/image/fetch/$s_!Y3Da!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd16d1e6-7389-4d02-a2a0-85e94088159e_1244x370.png)](https://substackcdn.com/image/fetch/$s_!Y3Da!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd16d1e6-7389-4d02-a2a0-85e94088159e_1244x370.png)

With the on-demand model, users can access up to 2,000 concurrent slots. BigQuery will temporarily increase this limit to accelerate smaller queries. Users might have fewer available slots due to resource contention in a specific location.

For example, during a period when many users in the Singapore region submit on-demand queries, you will have fewer available slots because the total slots must be shared among all users in Singapore.

### Capacity

In this model, the user is charged by the number of slots used to run queries, which is suitable for organizations that need additional capacity (compared to on-demand) or want greater cost control.

To enable the capacity model, the user must set up a BigQuery reservation. A reservation is how you allocate slots and isolate your workload, so it only competes for resources with other jobs running in the same reservation.

[![](https://substackcdn.com/image/fetch/$s_!KuR0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb17bce9-3be2-423c-bf21-597d3e96b912_1204x548.png)](https://substackcdn.com/image/fetch/$s_!KuR0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb17bce9-3be2-423c-bf21-597d3e96b912_1204x548.png)

For example, an organization can create a reservation for BI, another for daily processing, and a third for ad-hoc workloads. In a reservation, slots are fairly scheduled, which means a long-running query won’t consume all the resources of the following queries.

The total BigQuery compute cost can be estimated by multiplying the total usage slots by the per-slot rate.

For the slot rate, it depends on several factors:

* **BigQuery editions**: Standard, Enterprise, and Enterprise Plus. The higher the edition, the more advanced features BigQuery supports. The edition also determines whether you can set a minimum number of slots per reservation, as the Standard edition can’t. More on this later.
* **Region**: The slot rate varies based on the Google Cloud region.
* **Commitment**: You can pre-purchase slots for 1 or 3-year periods to receive a discount on the slot rate. Commitment does not apply to the Standard edition.

For the total usage slots, we sum across all reservations in the organization. The number of consumed slots in a reservation can be controlled by:

* **Baseline slots (optional)**: You will always have these slots in the reservation, and you will always be charged for them. This ensures that your critical workload will always have an available slot to run, unaffected by the slot-allocation delay. This baseline must be no greater than the reservation’s max slots setting. Only Enterprise and Enterprise Plus users can set this configuration.

  [![](https://substackcdn.com/image/fetch/$s_!jb-4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F372d64b9-37a7-429f-8384-8886ee3f429b_1354x542.png)](https://substackcdn.com/image/fetch/$s_!jb-4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F372d64b9-37a7-429f-8384-8886ee3f429b_1354x542.png)

  + If you purchase commitment, BigQuery uses slot commitments to cover reservations baseline slots.
* **Idle slots**: Slot commitments that are not allocated to any reservation baseline and slots that are allocated to a reservation baseline but aren’t in use are called the idle slots. A reservation can be configured to use idle slots from other reservations or not. If the original reservation needs those idle slots, they will be preempted.

  [![](https://substackcdn.com/image/fetch/$s_!5Gq0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa89dc5-8bd7-40ac-bf4e-e9a4fd0efa51_966x758.png)](https://substackcdn.com/image/fetch/$s_!5Gq0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa89dc5-8bd7-40ac-bf4e-e9a4fd0efa51_966x758.png)
* **Autoscaling slots**: For each reservation, you must set the reservation max slots. The difference between reservation max slots and baseline slots will be filled when queries require slots larger than the baseline. These filled slots can come from two sources: the idle slots or autoscaling slots. BigQuery lets you define the scaling mode, which determines how your reservation’s max slots will be filled: it can be the combination of Baseline + Idle slots, Baseline + Idle + Autoscaling slots, Baseline + Autoscaling slots, Idle + Autoscaling slots, or Idle slots only

  [![](https://substackcdn.com/image/fetch/$s_!hFNG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb709586c-5be1-4591-b134-95200666be1a_710x544.png)](https://substackcdn.com/image/fetch/$s_!hFNG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb709586c-5be1-4591-b134-95200666be1a_710x544.png)

  If your reservation scaling mode is configured to use autoscaling slots, BigQuery will automatically add more slots to handle the query after it ensures your baseline slots or idle slots (if enabled) are used but not enough.

  + For autoscaling slots, scaling up is based on actual usage and rounded up to the nearest 50-slot increment. The important note is that we are charged for the number of scaled slots, not the number of used slots. The commitments don’t apply to autoscaling slots.

Here is an example of BigQuery compute cost:

* Standard edition, no commitment, US-central 1, the slot rate is: 0.04$/hr
* Single reservation with 0 baseline slots and 200 max slots. The average slot usage time a month is 240 hours (8 hours a day)
* The total cost is:

  ```
  1920$ = 0.04 * 200 * 240
  ```

## Storage

The BigQuery storage pricing model is quite complicated, as it has 2 dimensions that can be combined to determine your storage rate.

The first dimension is your data temperature.

If BigQuery data has been modified in the last 90 days, it will be stored in Active storage**.** If the data has not been modified for 90 consecutive days, it will be stored in Long-term Storage; the price of Long-term Storage will be nearly 50% lower than that of Active storage. If you modify the data in Long-term storage, it will be moved back to Active storage and applied to the Active storage rate.

[![](https://substackcdn.com/image/fetch/$s_!W1hl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c03c42b-32e3-4fdb-a98f-d84810631d5c_1400x476.png)](https://substackcdn.com/image/fetch/$s_!W1hl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c03c42b-32e3-4fdb-a98f-d84810631d5c_1400x476.png)

The second dimension is the physical volume of your data. You can choose how Google charges for your data, based on the data volume before (logical model) or after (physical model) compression. The physical rate is more expensive than the logical rate (1,5 to 2 times). You can only benefit from the physical model if the uncompressed-to-compressed data ratio is greater than the physical\_rate/logical\_rate ratio.

[![](https://substackcdn.com/image/fetch/$s_!bx9G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93cb64a9-8918-4191-b515-ab14ec8930b8_1222x572.png)](https://substackcdn.com/image/fetch/$s_!bx9G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93cb64a9-8918-4191-b515-ab14ec8930b8_1222x572.png)

The storage rate is also affected by the Google Cloud region. The Active logical storage rate is 0.023$ in Tokyo and 0.02$ in Singapore.

To calculate the BigQuery storage cost, you must identify:

* The active and long-term data in the physical model
* The active and long-term data in the logical model
* The 4 storage rates in your region: Active physical, Long-term physical, Active logical, and Long-term logical rates
* The total storage cost is calculated by:

  ```
  Total storage cost =   (Active physical volume * Active physical rate)
                       + (Long-term physical volume * Long-term physical rate)
                       + (Active logical volume * Active logical rate)
                       + (Long-term logical volume * Long-term logical rate)
  ```

---

# Outro

In this article, I simplify the pricing models of Microsoft Fabric, AWS Redshift, and Google BigQuery. For each data warehouse, I cover how compute and storage costs are calculated.

I hope my work can help any of you get started with these three cloud data warehouses more quickly, as understanding the pricing model is always one of the most important parts of a production-ready setup.

See you in the second part, where we discuss Databricks and Snowflake pricing models, and my notes on saving cloud data warehouse costs.

---

# Reference

*[1] Bas Land, [Microsoft Fabric Costs Explained: A Complete Guide](https://thatfabricguy.com/microsoft-fabric-costs-explained/), (2025)*

*[2] [Microsoft Fabric pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-fabric/)*

*[3] [Amazon Redshift pricing](https://aws.amazon.com/redshift/pricing/)*

*[4] [Amazon Redshift provisioned clusters](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html)*

*[5] [BigQuery pricing](https://cloud.google.com/bigquery/pricing)*

*[6] BigQuery, [Understand slots](https://docs.cloud.google.com/bigquery/docs/slots)*
