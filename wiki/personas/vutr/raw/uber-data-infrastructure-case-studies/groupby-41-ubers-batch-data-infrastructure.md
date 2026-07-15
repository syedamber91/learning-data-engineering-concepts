---
title: "GroupBy #41: Uber’s Batch Data Infrastructure with Google Cloud Platform"
channel: vutr
author: "Vu Trinh"
published: 2024-06-25
url: https://vutr.substack.com/p/groupby-41-ubers-batch-data-infrastructure
paid: false
topics: ["Data Engineering", "Apache Spark", "BigQuery", "Data Lake", "Data Governance"]
tags: [uber, cloud, https, blog, infrastructure, apache]
---

# GroupBy #41: Uber’s Batch Data Infrastructure with Google Cloud Platform

*Plus: Debugging Data Pipelines, How to learn data engineering*

> Source: [Open post](https://vutr.substack.com/p/groupby-41-ubers-batch-data-infrastructure)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[bigquery|BigQuery]] · [[data-lake|Data Lake]] · [[data-governance|Data Governance]]

---

*This is **GroupBy**, the weekly compiled resources for data engineers.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I share my lesson and excellent resources to read in this newsletter.*
>
> *Hope this issue finds you well.*

---

# Uber’s Batch Data Infrastructure with Google Cloud Platform

[![](https://substackcdn.com/image/fetch/$s_!VkQf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff924d7a1-3e20-43d8-9571-fde84fb4557d_1401x1000.png)](https://substackcdn.com/image/fetch/$s_!VkQf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff924d7a1-3e20-43d8-9571-fde84fb4557d_1401x1000.png)

Image created by the author with the help of Canva Image Generator and Draw.io.

## Intro

Uber runs one of the largest Hadoop installations in the world. Their Hadoop ecosystem hosts more than 1 exabyte of data across tens of thousands of servers. A few weeks ago, Uber released an article introducing that they’re working with [Google Cloud Platform](https://cloud.google.com/?hl=en) (GCP) to move their batch data analytics and ML training stack to GCP to keep up with Uber's growing needs. Let’s review some key insights from that article.

> You can find the original blog post here: [Modernizing Uber’s Batch Data Infrastructure with Google Cloud Platform](https://www.uber.com/en-SG/blog/modernizing-ubers-data-infrastructure-with-gcp/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0).

## **Strategy**

* Their initial GCP migration strategy is to use cloud object storage for the data lake and migrate the rest of the data stack to cloud IaaS (Infrastructure as a Service). This ensures a quick, minimally disruptive migration.
* They plan to leverage applicable PaaS (Platform as a Service) offerings, e.g., GCP Dataproc or BigQuery

## Migration Principles

* **Avoid painful migrations for data users:** Uber tries to minimize the change for users (e.g., dashboard owners). They will use a cloud storage connector for HDFS compatibility with Google Cloud Storage, leveraging open standards like [Apache Parquet](https://parquet.apache.org/), [Apache Hudi](https://hudi.apache.org/), [Apache Spark](https://spark.apache.org/), [Apache Hadoop YARN](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html), and [Kubernetes](https://kubernetes.io/). This minimizes migration challenges and allows smooth integration of on-prem HDFS services with GCP storage.
* **Enhance data access proxies:** Uber has developed data access proxies for [Presto](https://prestodb.io/), Spark, and Hive to hide the underlying compute clusters. Once fully migrated, all queries and jobs submitted to these proxies will be routed to the cloud-based stack.
* **Leverage Uber’s container and deployment infrastructure:** The batch data stack sits on top of Uber’s infrastructure building blocks, which are built to be [agnostic between cloud and on-prem](https://www.uber.com/blog/crane-ubers-next-gen-infrastructure-stack/). These platforms allow Uber to expand the batch data ecosystem onto the cloud seamlessly.
* **Forecast potential data governance issues from cloud services:** Uber will enhance data management services to support only approved data services from the cloud vendor, avoiding future data governance complexities.

## **Major Workload**

* **Bucket mapping and cloud resources layout**: Formulating the mapping algorithm for migrating HDFS files and directories from the source cluster to cloud objects.
* **Security integration:** Enable support for all users, groups, and service accounts to continue to be [authenticated](https://www.uber.com/blog/scaling-adoption-of-kerberos-at-uber/) against the object store data lake and any other cloud PaaS. Also, maintain the same levels of authorized access as on-prem.
* **Data replication:** HiveSync is a permissions-aware, bi-directional data replication service built at Uber. The goal of this is to extend HiveSync’s capabilities to replicate the on-prem data lake’s data into the cloud-based data lake and corresponding Hive Metastore.
* **YARN and Presto clusters:** Uber will provision new YARN and Presto clusters on GCP. The existing data access proxies will route traffic to these new cloud-based clusters.

## Challenges and Initiatives

Here are some of the significant categories of challenges of this large migration:

* **Performance**: There are differences in features and performance characteristics between Object Store and HDFS. They will leverage the open-source Hadoop connectors and help evolve them to maximize performance.
* **Usage governance**: Cloud usage costs can be uncontrollable if not carefully managed. Uber will leverage the cloud’s elasticity to control the costs and partner with the internal capacity engineering team to build more advanced cost tracking.
* **Non-analytics/ML-specific usage of HDFS** **by applications**: Uber teams have used HDFS as a generic file store over the years. They migrate these use cases to other internal blob stores while providing a transparent migration path to avoid disruptions.
* **Unknown unknowns**: There will be unanticipated challenges. They hope to detect these issues with early end-to-end integrations.

## Outro

Uber plans to execute the migration plan over the next several quarters and share its progress through a series of blog posts. You can check the [Uber blog](https://www.uber.com/blog/asia/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0) here for upcoming posts on their migration journey.

---

# 📋 The list

────────

[How I built a huge graph database of Netflix's cloud infrastructure](https://blog.dataengineer.io/p/how-i-built-a-huge-graph-database) — 5 mins, by

> *In this article, I’ll be going over:*
>
> * *How a graph database data model would help Netflix manage their cloud security, and what datasets would we need*
> * *How we built a Spring Boot API on top of Postgres to serve most use cases*

────────

[When and Why to Automate: A Data Engineer's Perspective](https://seattledataguy.substack.com/p/when-and-why-to-automate-a-data-engineers) — 8 mins, by

> *The goal of this article is to:*
>
> * *Outline why we automate certain tasks*
> * *Call out some of the reasons not to automate a project*
>
> *Have you, the reader pause and ask, should I really automate this? With that, let’s dive into why you’d look to automate a task.*

[How Uber ensures Apache Cassandra®’s tolerance for single-zone failure](https://www.uber.com/en-SG/blog/single-zone-failure-tolerance/) — 12 mins, by Uber Engineering Blog

> *This blog shows how we ensured the single-zone failure tolerance for Cassandra and, notably, how we converted the large Cassandra fleet in real-time with zero downtime from non-zone-failure-tolerant to single-zone-failure tolerant.*

────────

[Debugging Data Pipelines](https://juhache.substack.com/p/debugging-data-pipelines) — 5 mins, by

> *Julien shares an approach to help your data pipeline bug-fixing process be a little less stressful.*

────────

[Scoping Data Projects: Why Technology Alone Isn’t Enough](https://medium.com/@meskensjan/scoping-data-projects-why-technology-alone-isnt-enough-2f2dafdd1c1c) — 9 mins, by janmeskens

> *This is the first article in a series about data strategy. In this article, I discuss the challenges in defining data projects. Future articles will delve into the topic of data strategy.*

────────

[How to learn data engineering](https://www.blef.fr/learn-data-engineering/) — 6 mins, by Christophe Blefari

> *How to learn data engineering in 2024? This article will help you understand everything related to data engineering.*

---

## 😉 Previously on Dimension

> *Dimension is my sub-newsletter, where I note down things I learn from people smarter than me in the data engineering field. Here is the latest article*

Let me hear your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-41-ubers-batch-data-infrastructure/comments)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
