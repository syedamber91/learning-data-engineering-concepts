---
title: "How to start learning Cloud as a data engineer?"
channel: vutr
author: "Vu Trinh"
published: 2026-03-31
url: https://vutr.substack.com/p/how-to-start-learning-cloud-as-a
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "BigQuery", "Data Warehouse", "Data Lake", "Orchestration"]
tags: [https, auto, cloud, good, substackcdn, image]
---

# How to start learning Cloud as a data engineer?

*The skill that is demanded in the most job descriptions*

> Source: [Open post](https://vutr.substack.com/p/how-to-start-learning-cloud-as-a)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[orchestration|Orchestration]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=191841638)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!EoNt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb66d7708-7530-4455-9d00-b7908be200d8_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!EoNt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb66d7708-7530-4455-9d00-b7908be200d8_2000x1429.png)

---

# Intro

In the [last survey](https://open.substack.com/pub/vutr/p/tell-me-what-youd-like-to-read-as?utm_campaign=post-expanded-share&utm_medium=web), I was asked to write about Cloud computing (AWS, GCP, or Azure) a lot.

My opinion about learning Cloud is that, although most JDs ask you to have Cloud experience, it should be one of the last things you should learn when you start the data engineer journey. Knowing how to use Cloud services but lacking the fundamental skills only makes you a Cloud user, not a data engineer.

I planned to skip discussing Cloud before the survey, as the cloud vendors are doing a great job of guiding new users who are trying their platforms.

But I was wrong.

Although there are many tutorials, a completely new user would still be overwhelmed by the diversity of cloud services (which vary depending on the cloud vendor). And if you’re a data engineer who is already overwhelmed by all the things you should learn, entering the Cloud without prior experience would leave you 2x as overwhelmed.

Another obstacle is that people often think learning Cloud is expensive because it requires a credit card.

—

In this article, I will imagine that I have to learn Cloud from scratch; what should I do? My notes here are vendor-agnostic, which means users can use them with AWS, GCP, or Azure.

---

# tl;dr

* Cloud experience in data engineer JDs means you know how to rent cloud services to build and manage your company’s data infrastructure efficiently.
* Choose one Cloud and stick with it. Don’t learn more than one Cloud at once. Your learning can scale to other clouds.
* Most clouds can be interacted with via three methods: UI, CLI, SDK/API.
* Your service could be network-isolated using VPC. (Not all services can be placed in VPC)
* Access Control will determine whether you’re a mature data engineer or not. So learn it as soon as possible.
* Learning how your service costs, how can you control and restrict the cost.
* Learning observability, what happens (logging), the service’s health (metric), and anomaly notification (alert)
* After that, you can learn specific services. Apply your learning of access control, cost control, and observability for every service.
* Always start with object storage first. Then go with virtual machines.
* Then, replace your local stack gradually with the data analytics-related service, such as the orchestration, the data processing, and the data warehouse services.
* The rule of thumb: start all services with the minimum setup at first.
* **Optionally**, learning Infrastructure as Code (IaC) to have more consistency and reproducibility in cloud service provisioning.

  ---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=191841638)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

# What is Cloud?

Let’s imagine you live in a time when no cloud vendors existed.

You’re building an application and want to deploy it. You need a server. You tell your company to buy one. If you need more resources, you might ask your company to buy more servers.

Now, back in today, you can open your browser, log in to your favorite Cloud console, and rent a VM instance, paying only for the usage hours.

We don't maintain physical servers.

—

The cloud is simply a network of powerful computers owned by companies like Amazon, Google, and Microsoft, that you can rent over the internet instead of buying your own.

[![](https://substackcdn.com/image/fetch/$s_!wtSK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa944c6-cb63-4d16-8e1a-a6411173827f_1122x1020.png)](https://substackcdn.com/image/fetch/$s_!wtSK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa944c6-cb63-4d16-8e1a-a6411173827f_1122x1020.png)

The vendor abstracts the physical resource and offers you services on top of it. You can rent a wide range of services on a cloud platform right now, from a VM instance, object storage, to a complete data warehouse solution.

—

Thus, you might know why every company you apply to will ask you for cloud experience. Unless the companies demand complete control over their infrastructure, the Cloud is the inevitable choice. It’s convenient, and it has a great ecosystem of services.

[![](https://substackcdn.com/image/fetch/$s_!p3gc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb07a50e8-4d64-4a1b-aeff-501b970cdc44_838x700.png)](https://substackcdn.com/image/fetch/$s_!p3gc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb07a50e8-4d64-4a1b-aeff-501b970cdc44_838x700.png)

As most infrastructure is managed in the Cloud, the company’s entire data stack will also live there. As data engineers, we have to plan, interact with, optimize, monitor, and secure the cloud services that underpin the company’s data life cycles, from ingestion, storage, and processing to serving.

## Region

When learning Cloud, it's important to know about regions.

[![](https://substackcdn.com/image/fetch/$s_!tpQI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5adfd41f-13da-49fe-ae48-e8626b27e35e_994x572.png)](https://substackcdn.com/image/fetch/$s_!tpQI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5adfd41f-13da-49fe-ae48-e8626b27e35e_994x572.png)

A region is a physical cluster of data centers in a specific geographic location. AWS has regions such as us-east-1 (Virginia), ap-southeast-1 (Singapore), and eu-west-1 (Ireland). GCP and Azure have equivalent setups. Each region is completely independent.

[![](https://substackcdn.com/image/fetch/$s_!Wn4p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99182bad-4082-4a4f-9703-5de0f0b7bfe2_642x934.png)](https://substackcdn.com/image/fetch/$s_!Wn4p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99182bad-4082-4a4f-9703-5de0f0b7bfe2_642x934.png)

In a region, there are **availability zones (AZs)**, separate physical facilities. Each zone has separate infrastructure, from independent power to networking, to isolate a zone failure from affecting other zones.

Region choice really matters:

* **Latency.** If your application servers are in Singapore and your data warehouse is in the US, every query crosses the Pacific. That adds tens to hundreds of milliseconds per round trip.
* **Service availability.** Not every service is available in every region. Some newer managed services launch in, for example, `us-east-1` first, and take months to reach other regions.
* **Cross-region cost:** Data transfer within the same region and same AZ is free or nearly free. The moment data crosses a region or zone boundary, you start paying for egress traffic. This cost is often overlooked, but it can significantly increase your billing.

Here is the the rule of thumb for choosing a region for your services: Every service you provision, your storage, compute, and database should always live in the same region.

There are cases where your company place services in different regions (e.g., different business teams have their services distributed across regions based on their geographic locations). Then, you must be aware of the cross-region transfer cost when moving data between services (e.g., pulling historical data from their service to a centralized warehouse)

Choose a Cloud and stick to it. Your learning can scale to other clouds. Below are my priority orders of things you should learn when you start learning Cloud.

# Interacting with the Cloud

First things first, you have to learn how to interact with your Cloud vendor.

There are three main ways.

First is using the web UI. It is straightforward (and fun).

[![](https://substackcdn.com/image/fetch/$s_!uCyV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d54b49f-12db-4e2e-bd79-8c3d1a9a2b4e_1072x728.png)](https://substackcdn.com/image/fetch/$s_!uCyV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d54b49f-12db-4e2e-bd79-8c3d1a9a2b4e_1072x728.png)

Second, you can use the CLI to interact with Cloud services from the terminal. You can package multiple commands into a bash script to execute multi-step actions, such as starting the VM, running commands inside the instance, and stopping the VM.

[![](https://substackcdn.com/image/fetch/$s_!BL2f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F822f8945-f16a-45f5-85db-952f30767c87_362x270.png)](https://substackcdn.com/image/fetch/$s_!BL2f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F822f8945-f16a-45f5-85db-952f30767c87_362x270.png)

One use case that requires a data engineer to use the CLI to interact with the Cloud is building a CI/CD pipeline.

Third, you can interact via SDK/API. This allows your Python script to write data to S3, warm up the Spark clusters, or submit queries to the Cloud data warehouse service.

[![](https://substackcdn.com/image/fetch/$s_!2tsG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7df9351d-8d76-4128-9ca2-4c1a5b82cc8a_926x484.png)](https://substackcdn.com/image/fetch/$s_!2tsG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7df9351d-8d76-4128-9ca2-4c1a5b82cc8a_926x484.png)

---

# Access Control

You don’t want your Cloud services to be accessed by anyone.

Make sure you understand how to restrict access to a cloud service. Most cloud providers use **IAM (Identity and Access Management)** to control who can do what.

[![](https://substackcdn.com/image/fetch/$s_!awqZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc053a600-9f24-43c9-b414-c99fc3476b2e_1424x516.png)](https://substackcdn.com/image/fetch/$s_!awqZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc053a600-9f24-43c9-b414-c99fc3476b2e_1424x516.png)

A user will be granted a set of permissions to access the service. You won’t feel this when you’re learning, as you will be the admin of your account, and you have permissions to nearly everything.

However, things will be stricter in production (if your company does things right). A application should have “just enough“ permissions to interact with a. This is called the principle of least privilege.

Your pipeline that reads from S3 shouldn’t also have permission to delete databases.

You can invite a friend (or your dummy email) and play with IAM. This may seem annoying and time-wasting at first, but knowing how to restrict access to a cloud resource will make you a more mature data engineer.

---

# Networking

When you rent resources in the cloud, they don’t live in the air; they live on real physical servers inside a data center, connected through real network infrastructure.

Cloud networking is how you control that infrastructure: who can reach what, through which paths, and with what restrictions. This is a lower level of access control, as the restriction is applied on the physical resource (e.g., blocks traffic from host abc) instead of logical rules (permissions)

[![](https://substackcdn.com/image/fetch/$s_!nG_U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e211cfe-5685-4a59-8e9b-fb8d25df3e87_1054x570.png)](https://substackcdn.com/image/fetch/$s_!nG_U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e211cfe-5685-4a59-8e9b-fb8d25df3e87_1054x570.png)

A common way to do this is to put your service into the **VPC (Virtual Private Cloud)**.

> *A note: not every service can be placed in a VPC.*

It’s a (logically) isolated network that you own inside the cloud provider’s infrastructure. The VPC can have multiple subnets to divide the network into smaller segments further. For services within the VPC, users can control which traffic can go in and out.

—

For me, knowing that a cloud service could be placed inside a VPC and protected by a set of traffic rules is enough for a data engineer in most cases. Diving into the network won’t be a data engineer’s top priority, as we can consult (or request) the infrastructure team for network settings, configuration adjustments, debugging to understand why we can’t access service A, or guidance on how to protect service B properly.

[![](https://substackcdn.com/image/fetch/$s_!wusu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9daab73b-3794-43dc-906e-e7772406bf8f_890x382.png)](https://substackcdn.com/image/fetch/$s_!wusu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9daab73b-3794-43dc-906e-e7772406bf8f_890x382.png)

Suppose your (target) company expects you to have more network knowledge, to, for example, manage a whole data stack with strict restrictions access, feel free to dive more into it. I believe the documentation from the Cloud vendor (with the help of AI) is sufficient. Creating a simple VPC, adding a service to it, and experimenting with how traffic could be restricted.

---

# Cost

“Learning cloud is expensive.”

These are the impressions from most new learners. You must indeed provide your credit card information to finish the cloud account setup. Here's the catch: all cloud providers offer free trial credits, and some services include free-tier usage.

To protect you from overusing the free credit:

* Always set billing alerts so you get notified before costs spike. All cloud providers allow you to do this, for example, by setting alerts when your usage passes $50.

  [![](https://substackcdn.com/image/fetch/$s_!dE62!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe16507e5-f333-4521-ba05-3a71c9109ec4_502x290.png)](https://substackcdn.com/image/fetch/$s_!dE62!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe16507e5-f333-4521-ba05-3a71c9109ec4_502x290.png)
* Most cloud services are pay-as-you-go. The vendor doesn’t charge for services that are stopped. Remember to stop or delete anything you don’t use. If we do it correctly, 12-core, 36 GB of RAM VM instances won’t cost you more than $10 (covered by the free credits) for 5 hours of usage.

  [![](https://substackcdn.com/image/fetch/$s_!e0WM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbdbb32f-595d-439a-abaa-a7feb6d2d80e_520x510.png)](https://substackcdn.com/image/fetch/$s_!e0WM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbdbb32f-595d-439a-abaa-a7feb6d2d80e_520x510.png)
* Before touching any service, make sure you read the pricing model, what you will be charged for, and how you will be charged. Understanding the pricing model is very important not only for tracking costs during your learning but also for planning resource usage for production workloads.

  [![](https://substackcdn.com/image/fetch/$s_!E9kw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe8f4552-f7a9-4520-a445-cfbc9908373d_528x398.png)](https://substackcdn.com/image/fetch/$s_!E9kw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe8f4552-f7a9-4520-a445-cfbc9908373d_528x398.png)

---

# Observability

The next thing you have to get familiar with is observing how your service performs:

* L**ogs**: what happened inside your services.

  [![](https://substackcdn.com/image/fetch/$s_!758O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f3125ba-21ac-489f-b592-e4f38adce88c_456x408.png)](https://substackcdn.com/image/fetch/$s_!758O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f3125ba-21ac-489f-b592-e4f38adce88c_456x408.png)
* **Metrics**: The health of your services, how many resources your service uses, or how much your service usage costs.

  [![](https://substackcdn.com/image/fetch/$s_!Q5of!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9f5675e-db86-4fcc-b50e-c78b0368068c_792x604.png)](https://substackcdn.com/image/fetch/$s_!Q5of!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9f5675e-db86-4fcc-b50e-c78b0368068c_792x604.png)
* **Alerts**: Configuration to notify you of service anomalies

  [![](https://substackcdn.com/image/fetch/$s_!_3NF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F834f5c24-3311-44d1-bbba-4104eee32adc_810x272.png)](https://substackcdn.com/image/fetch/$s_!_3NF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F834f5c24-3311-44d1-bbba-4104eee32adc_810x272.png)

After gaining a basic understanding of the cloud, interaction methods, access control, networking basics, cost, and observability, we can begin learning about data engineering services. For any service, let’s apply your understanding of those topics to manage it, from choosing the region to monitoring the service.

If you’re totally new to the Cloud platform, basic knowledge of those topics is enough; you can gain more experience when you're working with Cloud on a real project later. Just keep in mind why those topics are needed.

# Object Storage

Object storage (S3 on AWS, GCS on GCP, Blob Storage on Azure) is the backbone of every modern data architecture.

[![](https://substackcdn.com/image/fetch/$s_!iTbG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc0c8a6-7363-44d5-8d3c-4c4282a97650_354x410.png)](https://substackcdn.com/image/fetch/$s_!iTbG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc0c8a6-7363-44d5-8d3c-4c4282a97650_354x410.png)

It is a technology that manages data as units called **objects**. Unlike a file hierarchy on a computer, this storage organizes objects in a **flat structure** within containers called **buckets**. Thanks to its ability to “store anything,” object storage is widely adopted as a data lake, where raw data is first centralized and later consumed by other services.

To learn object storage:

* Learn about different storage classes: vendors offer multiple storage classes designed to optimize costs and performance based on data access patterns. The higher the storage class, the higher the storage cost, and the lower the request cost. This implies that you need to keep hot data in high class (e.g, S3 standard) and keep cold data in low class (e.g., S3 Glacier Deep Archive)

  [![](https://substackcdn.com/image/fetch/$s_!ypST!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ca5f8a-0b13-4857-86fd-2c02b891c7ee_494x278.png)](https://substackcdn.com/image/fetch/$s_!ypST!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ca5f8a-0b13-4857-86fd-2c02b891c7ee_494x278.png)
* Learn about life cycle management: You can configure your object to be moved to a different storage class or expire the objects or their old versions using the lifecycle management feature.
* Read and Write: For a large object, consider how your vendor can help you optimize the object's reading and writing performance. For example, S3 and GCS support multipart uploading, in which the object’s parts can be uploaded simultaneously to improve performance. Or, they supported reading a byte range of an object to save bandwidth.

  [![](https://substackcdn.com/image/fetch/$s_!rWM9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c8858c4-5f66-4ec8-9931-5fce0a40dfa0_468x402.png)](https://substackcdn.com/image/fetch/$s_!rWM9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c8858c4-5f66-4ec8-9931-5fce0a40dfa0_468x402.png)

Object storage is one of the friendliest services for new learners, as most vendors charge only $25 for 1 TB of data in the standard class. A few MBs or GBs of your side data project will cost you no more than 5$ per month; the free credit also covers this cost.

Creating an object storage’s bucket is quite simple; the default setup is sufficient in most cases (e.g., cloud vendors prevent your bucket from being exposed to the public by default). Interacting with this service is also straightforward, as those actions will center around LIST, PUT, or GET.

So if you haven’t used any Cloud service before, object storage is a good starting point. Create a cloud account and an object storage bucket, and slightly adjust your Python script to read and write data to object storage (with proper credentials set up) instead of the local file system.

---

# Compute Options

Physical servers back every single cloud service. The difference between services is the user’s level of control over the underlying server.

The ones with the most control are the virtual machines (e.g., AWS EC2). You literally rent a server where you can customize nearly everything, from RAM, CPUs, and disks to the OS.

[![](https://substackcdn.com/image/fetch/$s_!70Bs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53c83985-f184-45a8-b96c-7a330e0996f5_658x576.png)](https://substackcdn.com/image/fetch/$s_!70Bs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53c83985-f184-45a8-b96c-7a330e0996f5_658x576.png)

In the middle, there are services with higher-level abstractions to help you deploy your application faster; some examples include Kubernetes services (all clouds have this) or Spark YARN cluster. All are backed by a set of virtual machines. You still see the virtual machine cost in your billing.

[![](https://substackcdn.com/image/fetch/$s_!yWPO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25f39411-cbf0-493f-849b-747f16e7662a_1156x514.png)](https://substackcdn.com/image/fetch/$s_!yWPO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25f39411-cbf0-493f-849b-747f16e7662a_1156x514.png)

Above this, you will see serverless services where you can use them as if the virtual machines behind them were visible.

[![](https://substackcdn.com/image/fetch/$s_!eMa5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5d5f413-fa65-4f35-be35-224d1c4f589b_994x522.png)](https://substackcdn.com/image/fetch/$s_!eMa5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5d5f413-fa65-4f35-be35-224d1c4f589b_994x522.png)

—

For a data engineer, learning virtual machines, a serverless option (e.g, AWS Lambda), and, to some extent, Kubernetes services is enough.

Like Object storage, virtual machines are also beginner-friendly. The default networking and security settings are sufficient; you only need to choose the region, the number of CPUs, RAM, Disk, and OS (e.g., Ubuntu, Debian).

If you no longer need the VM, you can stop and restart it. Vendors don’t charge you for the stopped instance.

> ***Note**: Most cloud vendors don’t allow new accounts to provision overly expensive machines with tons of CPU.*

Instead of running “docker-compose” on your laptop, run it on the VM. That’s how you get familiar with the VM.

---

# Data lifecycle-related services

Then, we come to the services specific to the data lifecycle. There are three main services you need to keep an eye on:

[![](https://substackcdn.com/image/fetch/$s_!VS5t!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddb73191-7346-4d78-be79-6cb2785d9ae1_800x586.png)](https://substackcdn.com/image/fetch/$s_!VS5t!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fddb73191-7346-4d78-be79-6cb2785d9ae1_800x586.png)

* Orchestration services (e.g., cloud-managed Airflow or AWS StepFunction)
* Distributed Data processing services (e.g., AWS EMR, Google Dataproc)
* Data Warehouse service (e.g., AWS Redshift, Google BigQuery, Snowflake…)

If you have fundamental data engineering knowledge, you’d already know what those services are used for.

You only need to learn how to use them in the Cloud. Just like object storage or compute, you have to create an instance of the service you want to learn and start swapping your local instance to the one in the Cloud. For example, you now submit your Spark application to the YARN cluster on AWS instead of to the local Standalone cluster.

The pricing model for these services might not be as straightforward as that for virtual machines or object storage. So here is the rule of thumb: always choose the minimal setup. You will have your service running to play with, and we'll keep the cost low. Most of these services won’t charge you for stopping time, so don’t forget to stop them when you’re done.

Once you gain confidence, you can experiment with a higher setting (which costs you more).

---

# (Optional)Infrastructure as code (IaC)

Normally, when you set up cloud resources, you click around in the console, create a bucket, spin up a VM, and attach a role.

It works, but it’s manual. Three months later, you don’t remember what you built or why.

IaC is the practice of defining your infrastructure in code. Text files that describe exactly what resources you want, what their configurations are, and how they connect.

[![](https://substackcdn.com/image/fetch/$s_!-LlL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc459a1b5-38b1-4d48-a3b2-23014e022855_1468x622.png)](https://substackcdn.com/image/fetch/$s_!-LlL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc459a1b5-38b1-4d48-a3b2-23014e022855_1468x622.png)

You write a file that says, “I want an S3 bucket in us-east-1, with versioning enabled, private access only, and this lifecycle policy.” Then you run a command, and the tool builds it for you. The dominant tool is **Terraform**, cloud-agnostic and compatible with AWS, GCP, and Azure.

—

IaC is crucial because it helps you consistently reproduce the environment with the required services. As data engineers, we use IaC to spin up CI environments or replicate environments for dev/staging/prod.

It’s power. But it won’t be one of the first things you need to learn. Learn if after you feel comfortable with using cloud services. As for me, you can consult or request the infrastructure team for the IaC setup.

---

# Outro

In this article, I share my notes in case I have to start learning Cloud from scratch. First, we need to understand what the Cloud is, why it is divided into regions, how to interact with the Cloud, how access control works, how the VPC works, how to control costs, and how to monitor service health.

After covering those fundamentals, we jump into services, starting with object storage and virtual machines, then moving on to other data analytics services such as orchestration, data processing, and data warehouse.

Then, you can optionally learn the IaC to automate cloud resource provisioning.

Thank you for reading this far. See you in my next articles.
