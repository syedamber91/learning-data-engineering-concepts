---
title: "(2/2) I analyzed the pricing models of 5 famous cloud data warehouses so you don't have to."
channel: vutr
author: "Vu Trinh"
published: 2026-03-05
url: https://vutr.substack.com/p/22-i-analyzed-the-pricing-models
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Orchestration"]
tags: [https, auto, databricks, image, cloud, substackcdn]
---

# (2/2) I analyzed the pricing models of 5 famous cloud data warehouses so you don't have to.

*Part 2: Databricks, Snowflake, and the practices for keeping your data warehouse costs under control *

> Source: [Open post](https://vutr.substack.com/p/22-i-analyzed-the-pricing-models)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=189216232)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!Xf4g!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1a3f738-f83f-40c6-96af-c1937495c190_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Xf4g!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1a3f738-f83f-40c6-96af-c1937495c190_2000x1429.png)

---

# Intro

This is the second part of my analysis on the pricing models of the 5 famous cloud data warehouses. You can read the first part, which discusses the pricing models for Microsoft Fabric, AWS Redshift, and Google BigQuery, [here](https://vutr.substack.com/publish/post/188677941?r=2rj6sg&utm_campaign=post&utm_medium=web).

In this article, I will discuss Snowflake or Databricks, along with my general best practices for keeping your data warehouse costs under control.

> ***Note 1**: This article won’t debate which solution is cheaper, as costs depend on many factors that vary by your organization's context and requirements. Instead, my purpose is to give you guys a simplified view of the pricing models for cloud data warehouses, which can sometimes be hard to understand at first glance. Also, feel free to correct me if you see anything wrong.*
>
> ***Note 2**: This article focuses on the scenarios when you store your data directly in the cloud data warehouse's proprietary storage. Plus, in each warehouse, I only cover the compute and storage cost.*

---

# Databricks

## Compute

In Databricks, compute costs are unique in that the vendor bills you on two separate invoices: the first is for software, and the second is for hardware.

[![](https://substackcdn.com/image/fetch/$s_!xW3b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d9023ac-e34d-4961-862a-0fd4792665f4_798x752.png)](https://substackcdn.com/image/fetch/$s_!xW3b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d9023ac-e34d-4961-862a-0fd4792665f4_798x752.png)

For software, Databricks introduces the concept of DBU, the unit of processing power. Your software billing is calculated around this unit:

```
The number of consumed DBUs * The rate of a DBU
```

Each operand varies based on different factors.

First, the number of consumed DBUs depends on:

[![](https://substackcdn.com/image/fetch/$s_!7Fca!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15498c43-157f-4840-a246-dde06c1230ab_1394x576.png)](https://substackcdn.com/image/fetch/$s_!7Fca!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15498c43-157f-4840-a246-dde06c1230ab_1394x576.png)

* **The DBU capacity of an instance:** Each instance has a different limit of DBUs that can run per hour.
* **The number of instances**: for example, 4 or 5 instances

> ***Note**: The organization can configure it to use a spot instance to reduce costs. Cloud providers offer these instances at large discounts (up to 90% off). In return, spot instances can be revoked from cloud providers at any time. This approach is suitable if your use cases can tolerate a few minutes’ lag due to the removal of spot instances (which are later replaced by the on-demand instances)*

* **The time of using DBUs** (billed on a per-second usage, minimum 60 seconds): for example, 8 hours

> ***Note**: the time required to use DBUs might fluctuate depending on the organization's setup.*
>
> * *Cluster termination policy: tearing down your Databricks cluster after some idle time.*
> * *Auto Scaling policy: cluster’s min and max number of workers.*
> * *Number of DBUs quota that a single cluster can consume*

Second, the rate of a DBU depends on:

* **Cloud Provider**: The DBU rate might be different on AWS, GCP, and Azure.

  [![](https://substackcdn.com/image/fetch/$s_!4YLV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8de98598-4ff4-4111-884a-12b7a6ab398f_616x446.png)](https://substackcdn.com/image/fetch/$s_!4YLV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8de98598-4ff4-4111-884a-12b7a6ab398f_616x446.png)
* **Workload**: Different workloads, such as SQL, Lakeflow, or Model service, will have different DBU rates. For some workloads, Databricks offers serverless options in addition to the original one when you need to manage your instances. Serverless offers usually have a higher DBU rate (as Databricks manages everything for you)

  [![](https://substackcdn.com/image/fetch/$s_!NqM2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a380320-a209-4e26-b153-1a7e87c22ddf_1116x942.png)](https://substackcdn.com/image/fetch/$s_!NqM2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a380320-a209-4e26-b153-1a7e87c22ddf_1116x942.png)

  Different workloads have different DBU rates. [Source](https://www.databricks.com/product/pricing/databricks-sql).
* **Plan**: Databricks offers Premium and Enterprise plans (AWS has both, while GCP has only Premium). [Enterprise](https://www.databricks.com/product/pricing/platform-addons) offers stricter governance, compliance, and networking required by highly regulated industries. The Enterprise plan has a higher DBU rate for some workloads.

  [![](https://substackcdn.com/image/fetch/$s_!Damw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefdc1168-6b57-42fa-aeba-b1a1da8ce4d7_1604x728.png)](https://substackcdn.com/image/fetch/$s_!Damw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefdc1168-6b57-42fa-aeba-b1a1da8ce4d7_1604x728.png)

  The same workload with different plans. [Source](https://www.databricks.com/product/pricing/databricks-sql).
* **Region**: Depending on the region of your instances, the DBU rate might differ for the same instance type when it lives in different regions.

  [![](https://substackcdn.com/image/fetch/$s_!J7mj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef275007-6c0a-4644-a6f5-d9bb007f673e_1120x846.png)](https://substackcdn.com/image/fetch/$s_!J7mj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef275007-6c0a-4644-a6f5-d9bb007f673e_1120x846.png)

  The same workload with different regions. [Source](https://www.databricks.com/product/pricing/lakeflow-spark-declarative-pipelines).
* **Commitment**: When you commit to using Databricks at certain levels of usage, you will get a lower DBU rate. The discount increases if you reserve more capacity.

However, the DBU cost does not cover the whole Databricks compute cost. You will need to pay for your cloud provider for the usage of the virtual machines.

[![](https://substackcdn.com/image/fetch/$s_!pEeh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd51383dd-b2bf-460d-846e-ffa9c2f981f5_1316x572.png)](https://substackcdn.com/image/fetch/$s_!pEeh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd51383dd-b2bf-460d-846e-ffa9c2f981f5_1316x572.png)

If you choose the Serverless compute type, you don’t need to pay this extra infrastructure cost to the cloud provider, as Databricks already includes it in the DBU rate for the serverless offering.

Here is an example of the compute cost estimation of a Databricks setup. All the details are retrieved from the [Databricks pricing calculator.](https://www.databricks.com/product/pricing/product-pricing/instance-types) For simplicity, we will skip the auto scaling factor here.

* DBU rate: You subscribe to the Premium Plan, AWS cloud provider, SQL Pro Compute compute type, and US East region. Each DBU will cost you: 0.55$/hr
* Number of consumed DBUs: You choose 3 X-Small instances; each has a capacity of 6 DBU/hour. You use these three instances for 5 hours a day, 30 days a week. The total consumed DBUs are:

  ```
  2700 = 3 (instances) * 6 (instance’s capacity) * 5 (hours a day) * 30 (days a week)
  ```
* The DBUs cost will be:

  ```
  1485$ = 2700 (The number of consumed DBUs) * 0.55 (The rate of a DBU)
  ```
* However, this is not done yet, as you need to include the cloud provider infrastructure cost of your instances:

  ```
  1485$ (DBU cost) + (A * 3) (instanace cost)
  A is the X-Small instance's cost on AWS, as I can't find the exact number online.
  ```

## Storage

For Databricks storage costs, you pay for data stored and for operations executed in the cloud provider's object storage. You can tell Databricks to create a new object storage bucket or use an existing bucket.

The rate varies by cloud provider. For example, AWS S3 standard charges you $0.023 per GB per month. For write-related requests (PUT, COPY, POST, LIST), it is $0.005 per 1000 requests; for read-related requests (GET or SELECT), it is $0.004 per 1000 requests.

In a month, if you store 100 GB of Databricks data in S3, issue 200 PUT requests and 100 GET requests, the total cost will be:

```
3.7$ = 100 * 0.023 + 200 * 0.005 + 100 * 0.004
```

The storage [cost might vary if](https://www.databricks.com/blog/best-practices-cost-management-databricks):

* You offload your data to lower-tier storage after a period of time.
* Additional cost will be added if where you run the compute, and your data is in different zones or different clouds.
* The transfer cost might change if you use advanced network settings such as [VPC endpoints on AWS](https://docs.databricks.com/aws/en/security/network/classic/customer-managed-vpc#configure-regional-endpoints-optional), [Private Link, or Service Endpoints on Azure](https://www.databricks.com/blog/2020/02/28/securely-accessing-azure-data-sources-from-azure-databricks.html), or [Private Google Access (PGA) on GCP](https://docs.databricks.com/gcp/en/security/network/classic/firewall#firewall-configuration-overview).

In 2024, Databricks introduced the [Default Storage feature](https://www.youtube.com/watch?v=sm_hpSv6FzA), which provides configured storage, security policy, and Unity Catalog. Together with serverless compute offerings, Databricks aims to help users get started more quickly without the friction of self-managed infrastructure.

Default Storage usage is measured by a standardized unit called DSU. The DSU rate varies by region, storage type, data volume, or number of transactions. For the AWS cloud provider, the premium plan in the US East Region has a DSU rate of $0.023.

[![](https://substackcdn.com/image/fetch/$s_!hmJ5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefa02acb-a327-43c6-983c-3640dfa43f99_924x612.png)](https://substackcdn.com/image/fetch/$s_!hmJ5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefa02acb-a327-43c6-983c-3640dfa43f99_924x612.png)

[Source](https://www.databricks.com/product/pricing/storage)

When translating the Default Storage usage to DSU usages, we can refer to the official Databricks pricing calculator:

[![](https://substackcdn.com/image/fetch/$s_!h5L9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d17c2b9-06ea-4dee-89e8-259e59427a88_1572x898.png)](https://substackcdn.com/image/fetch/$s_!h5L9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d17c2b9-06ea-4dee-89e8-259e59427a88_1572x898.png)

[Source](https://www.databricks.com/product/pricing/storage)

As you can see, Default Storage billing also charges you based on the stored data volume, the number of requests (write and read), and network transfer costs if you run the compute in a different zone or a different cloud.

---

# Snowflake

## Compute

Snowflake introduces the concept of credit, which is the primary unit of measure for computing resource consumption. Credits are billed per second, with a 60-second minimum.

[![](https://substackcdn.com/image/fetch/$s_!1BIM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64372085-b4da-49fb-8138-7b4922e72aca_1140x828.png)](https://substackcdn.com/image/fetch/$s_!1BIM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64372085-b4da-49fb-8138-7b4922e72aca_1140x828.png)

The compute billing is calculated by:

```
Compute cost = Number of consumed credit * credit rate
```

Unlike Databricks, users only need to pay for Snowflake, not the cloud provider. The Compute cost is broken down into smaller components.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=189216232)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

### Virtual Data Warehouses credits

In Snowflake, most data operations occur in the Virtual Data Warehouses, which hides users from complex worker configurations. Snowflake offers Virtual Warehouses in T-shirt sizes, ranging from X-Small to XX-Large, each with a different credit capacity per hour:

[![](https://substackcdn.com/image/fetch/$s_!wjyQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff35937ca-1d11-4001-b00a-18fc2c8e1cae_1386x166.png)](https://substackcdn.com/image/fetch/$s_!wjyQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff35937ca-1d11-4001-b00a-18fc2c8e1cae_1386x166.png)

In 2025, [Snowflake introduced the Gen 2 warehouse, offering more capacity per warehouse and promising 2x performance.](https://www.snowflake.com/en/engineering-blog/gen2-warehouses-snowflake-multicloud-ga/)

[![](https://substackcdn.com/image/fetch/$s_!AaNv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3700c294-e94e-4dce-b7e9-7ac25553951d_1382x228.png)](https://substackcdn.com/image/fetch/$s_!AaNv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3700c294-e94e-4dce-b7e9-7ac25553951d_1382x228.png)

The total of used warehouse credits is calculated by:

For example, if you’re using the Gen 2 warehouse on AWS

* 1 S warehouse, usage per month is 120 hours
* 1 M warehouse, usage per month is 60 hours

The total warehouse credits per month are:

```
648 = (2.7 * 120) + (5.4 * 60)
```

### Serverless credits

Some features are executed on the Snowflake side rather than in the user’s virtual warehouses.

[![](https://substackcdn.com/image/fetch/$s_!HCmL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F946297c1-7541-4a34-8f02-9318a9450018_1844x596.png)](https://substackcdn.com/image/fetch/$s_!HCmL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F946297c1-7541-4a34-8f02-9318a9450018_1844x596.png)

The billing for these serverless features is based on usage of snowflake-managed resources, measured in compute-hours and billed on a per-second basis. Each feature will have its own number of consumed credits per compute hour.

### Compute pool credits

In addition to SQL, users can use languages such as Python, Java, and Scala to build data applications with Snowpark. This feature translates procedure code into optimized SQL and executes it on Snowflake’s engine.

[![](https://substackcdn.com/image/fetch/$s_!h9nV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd543f1-ce1b-4691-98b4-f33c945daeb6_1130x960.png)](https://substackcdn.com/image/fetch/$s_!h9nV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd543f1-ce1b-4691-98b4-f33c945daeb6_1130x960.png)

To orchestrate the code executions, Snowflake offers Snowpark Container Services, a container orchestration platform. Users package code and dependencies into an Open Container Initiative (OCI) image, which is then deployed as a container in Snowpark Container Services.

The Snowpark Container Services uses compute pools for deployed services. A pool is a set of virtual machine instances. The service’s consumed credits depend on the instance’s quantity and type.

### Cloud service credits

Snowflake’s architecture includes a component called cloud services, which provides services such as access control, query optimizer, and transaction manager. You can think of it as your Snowflake setup’s brain, which orchestrates everything, including streamlining the use of Virtual Warehouses.

[![](https://substackcdn.com/image/fetch/$s_!klI2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c065315-1aac-43c0-a028-b03bde67707e_1006x442.png)](https://substackcdn.com/image/fetch/$s_!klI2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c065315-1aac-43c0-a028-b03bde67707e_1006x442.png)

Like Virtual Data Warehouse, cloud services are also billed using credits. However, the cloud service cost is only charged if the cloud service exceed 10% of the daily usage of virtual warehouses. The cloud service is calculated daily, and monthly billing is the total of the daily charges.

## Calculate the computing cost

To get the total compute credits, we simply:

```
Total credits = Virtual Data Warehouses credits + Serverless credits + Compute pool credits + Total compute credits
```

To calculate the total compute cost, we need another operand: the credit rate.

This rate depends on three factors:

* **Editions:** Snowflake offers Standard, Enterprise, Business Critical, and Virtual Private Snowflake editions. The higher the edition, the more advanced the features and the more focus on security and regulations.
* **Region**: The rate is different if you buy the edition in the US and Tokyo.
* **Cloud vendor**: The rate might vary across AWS, GCP, and Azure, especially when you factor in region.

Here is an example of the edition’s credit rate, on AWS, US East:

[![](https://substackcdn.com/image/fetch/$s_!OI1b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffab6dc6c-0499-40cf-9565-be0d704eaff3_2570x934.png)](https://substackcdn.com/image/fetch/$s_!OI1b!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffab6dc6c-0499-40cf-9565-be0d704eaff3_2570x934.png)

After having the credit rate, the estimated cost is calculated by:

```
Compute cost = Total credits * Credit Rate
```

Compared to Databricks, you only pay for Snowflake and don’t need to worry about cloud provider billing.

## Storage

For storage, it’s quite straightforward: Snowflake charges you based on the average compressed data, at a rate per TB per month. The rate might vary by cloud provider and region.

[![](https://substackcdn.com/image/fetch/$s_!42Vm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0c36c9c-2155-4920-9004-eceb80bed2de_856x650.png)](https://substackcdn.com/image/fetch/$s_!42Vm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0c36c9c-2155-4920-9004-eceb80bed2de_856x650.png)

On AWS, US East, the rate is 23$/TB/month.

Snowflake offers a discount if you pre-purchase the storage capacity. The higher the purchase amount, the greater the discount you will receive.

If you run Snowflake data operations and your data is distributed across different locations, you will incur cross-zone or cross-cloud costs.

---

# How to save cloud costs

I’ve just covered the pricing models of the 5 cloud data warehouses, including ones in the first part. Each will charge you differently; however, I believe there are principles to help control the cost of cloud data warehouses:

* Make sure you understand the pricing model. I have to tell you this: researching the pricing models of those cloud data warehouses has been one of the most time-consuming processes I’ve ever experienced. There are so many things you can be charged for, and what and how you’ll be charged might not be clear at first read. To save costs, you have to understand how costs are incurred.
* Whenever you need to use a function from the cloud data warehouse, check for its pricing, although they might tell you it’s free, double-check again. It might be only free for the trial tier :)
* You will rarely pick the right resource you need for the first time. Continuously monitoring your usage to make sure you pay the reasonable cost for the performance you need.
* Plan how much data you store and figure out whether your data is compressed. An important note is that you’re not only charged for your table data, but there will also be historical data for time-travel query or fail-safe (e.g., if you accidentally delete the data, you can restore from the fail-safe). Read the docs carefully here.
* Plan how long you store the data. Depending on your company's requirements, some data from 2 or 5 years ago might barely bring value and be less frequently accessed. Implement data lifecycle management by removing data or moving it to a lower-tier storage to qualify for a discount.
* Keep your mind on the data transfer costs. If you read through every cloud data warehouse I cover, most charge the transfer fee if your compute and storage are not in the same region. Choose your compute and resource regions wisely, and be careful when moving data to another location.
* Denormalized and normalized data. The denormalization will incur data redundancy (more storage cost). Still, it can help boost query performance, while normalization reduces redundancy and increases data integrity, but it requires more “joins” (which could increase compute cost). Most cloud data warehouses support nested and repeated fields, which can help with data denormalization. Knowing the trade-offs of these techniques and choosing them based on your needs.
* Physical layout is important: most cloud data warehouses support techniques to optimize physical data layouts, such as partitioning (splitting a table into smaller portions), clustering (bringing related column values close together), or compacting small files. Use these options wisely; although they can help you query faster, the system will suffer lower write performance (e.g., appending data will be faster than organizing it). In addition, the system might handle additional metadata (e.g., partition metadata) or require more resources for background optimization tasks (e.g., compaction).
* Actively limiting the selected data. Avoid selecting \*; select only the columns you need, and filter data with the WHERE clause as soon as possible.
* Materializing CTEs or views if they need to be referenced frequently
* If you encounter a slow query. Make sure you optimize it as much as you can before throwing more resources at it.

---

# Outro

In this article, I cover the pricing models of Databricks (the hardest for me to understand) and Snowflake. At the end, I note my personal practices for controlling your cloud data warehouse costs.

I hope it will save time when starting with a cloud data platform.

Thank you for reading this far. See you in my next article.

---

# Reference

*[1] [Databricks Pricing Calculator](https://www.databricks.com/product/pricing/product-pricing/instance-types)*

*[2] Tomasz Bacewicz, Greg Wood, [Best Practices for Cost Management on Databricks](https://www.databricks.com/blog/best-practices-cost-management-databricks) (2022)*

*[3] Snowflake document, [Cost Understanding](https://docs.snowflake.com/en/user-guide/cost-understanding-overall)*

*[4] [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)*
