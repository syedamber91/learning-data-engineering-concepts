---
title: "GroupBy #40: Data Infrastructure at Airbnb"
channel: vutr
author: "Vu Trinh"
published: 2024-06-18
url: https://vutr.substack.com/p/groupby-40-data-infrastructure-at
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Databricks", "Streaming", "ETL"]
tags: [https, airbnb, infrastructure, engineering, they, solution]
---

# GroupBy #40: Data Infrastructure at Airbnb

*Plus: How trip.com migrated from Elasticsearch and built a 50PB logging solution with ClickHouse *

> Source: [Open post](https://vutr.substack.com/p/groupby-40-data-infrastructure-at)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[databricks|Databricks]] · [[streaming|Streaming]] · [[etl|ETL]]

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

# 🚀 Data Infrastructure at Airbnb

## Intro

Starting from this issue, I'm introducing a new format to GroupBy. In addition to the usual curated links, I'll be sharing a brief blog/note on my recent learnings and readings in the data/software engineering field. I'll strive to keep it concise, under 7 minutes, to respect your time.

This week is my short note after reading the article about data infrastructure at Airbnb (2016).

> ***Reference**: [Data Infrastructure at Airbnb](https://medium.com/airbnb-engineering/data-infrastructure-at-airbnb-8adfb34f169c) (2016)*

## Airbnb philosophy

The data infrastructure at Airbnb was built up by the following philosophies:

* **Open-source**: trying to adopt the open-source system; if Airbnb builds something that they find helpful, they will contribute back to the community.
* **Prefer standard components and methods:** Having intuition about when to build a unique solution and when to adopt an existing solution is essential.
* **Scalability:** Airbnb had to ensure its infrastructure could scale with the growth of the data.
* **Solve real problems by listening to your colleagues:** Empathizing with internal data users is essential.

## **Infrastructure Overview**

[![](https://substackcdn.com/image/fetch/$s_!ATxg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bcb0b91-4380-4f6d-8556-e390203d9940_1344x960.gif)](https://substackcdn.com/image/fetch/$s_!ATxg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bcb0b91-4380-4f6d-8556-e390203d9940_1344x960.gif)

Image created by the author. [Reference](https://medium.com/airbnb-engineering/data-infrastructure-at-airbnb-8adfb34f169c)

* Data came from two sources: events from Kafka and MySQL database dumps.
* This source data contains user activity event data and dimensional snapshots.
* There are two Hadoop clusters: Gold and Silver. Critical jobs ran in the Gold environment, and more “relaxed” jobs ran in the Silver one.
* Data in Gold is treated as a single source of truth; data can ONLY be copied from Gold to Silver.
* Despite the isolation, separating into two clusters comes at the cost of data replication and keeping data in sync.
* Treating Hive-managed tables as their central source and sink for data.
* Using Presto for almost all ad hoc queries on Hive-managed tables.
* They built a web-based query engine called [Airpal](https://airbnb.io/airpal/) backed by Presto. This is Airbnb's primary interface for users to run SQL.
* They use Airflow for job scheduling.
* Engineers and data scientists working on machine learning will work with Spark.
* Airbnb also leverages Spark for stream processing.

## **Detailed Look at The Hadoop Cluster**

Airbnb made a significant migration for their Hadoop Cluster. Two years before the article writing time, two sets of poorly architected clusters called Pinky and Brain were run on a set of EC2 instances running HDFS with 300 terabytes.

At the time of writing, Airbnb had two separate HDFS clusters (Gold and Silver) with 11 petabytes of data, and they also stored multiple petabytes of data in S3. Here are some problems they have overcome during the migration:

* **Running Hadoop on Mesos**

  + Lacking visibility into logs and cluster health
  + Hadoop on Mesos could only run MapReduce version 1.
  + Cluster underutilization
  + High operational load and difficulty reasoning about the system
  + **Solution**: moving away from Mesos.

* **Remote reads and writes**

  + By storing all the HDFS data in mounted [EBS](https://aws.amazon.com/ebs/) volumes, Airbnb sent large amounts of data over the public [Amazon EC2](https://aws.amazon.com/ec2/?gclid=CjwKCAjwmrqzBhAoEiwAXVpgosv6h8mDc8mt2gA7-K5_cf91Ng2u73ymFfVMME8Ix7S-c37LuWSvtRoCH7wQAvD_BwE&trk=04e4a6fd-7779-47a2-87a1-3becd8d90d5b&sc_channel=ps&ef_id=CjwKCAjwmrqzBhAoEiwAXVpgosv6h8mDc8mt2gA7-K5_cf91Ng2u73ymFfVMME8Ix7S-c37LuWSvtRoCH7wQAvD_BwE:G:s&s_kwcid=AL!4422!3!589846461771!e!!g!!amazon%20ec2!16178327434!136912441367) network for queries. → Agains the Hadoop design of local reads and writes on disks.
  + Moreover, they mistakenly split the data storage across three separate availability zones within a single AWS region. Each zone was designated as its own rack, causing remote reads and writes for the three replicas. → More remote data transfer → Slow performance.
  + **Solution**: having dedicated instances using local storage and running in a single availability zone.
* **Heterogeneous Workload on Homogeneous Machines:**

  + There were distinct requirements for the architectural components.
  + Hive/Hadoop/HDFS machines required a lot of storage but didn’t need much RAM or CPU.
  + Presto and Spark required RAM and CPU but didn’t need much storage.
  + **Solution**: Leveraging the flexibility of EC2 instance types supported by Amazon for each component to save cost and increase resource utilization.
* **System Monitoring**

  + One major issue was creating custom monitoring and alerting for the cluster. Hadoop, Hive, and HDFS are complex systems with many potential failure points. Anticipating all failure states and setting reasonable alert thresholds felt like reinventing the wheel for Airbnb.
  + **Solutions:** They signed a support contract with [Cloudera](https://www.cloudera.com/) to gain from their expertise in architecting and operating these large systems and to reduce the maintenance burden by using the Cloudera Manager tool.

After the migration, they were able to cut costs dramatically and, at the same time, increase awesome performance. Here are a few numbers:

> * *Disk read/write improved from 70–150MB/sec to 400+ MB/sec*
> * *Read throughput is ~3X better*
> * *Write throughput is ~2X better*
> * *Cost is reduced by 70%*

## Outro

That’s all for my note this week. I decided to write a note like this to share more about things I’ve learned with you guys.

Through this week's note, I hope to help you look closely into the internal infrastructure of Airbnb. Now it’s time for some cool links I found last week.

---

# 📋 The list

────────

**[Databricks - Open Sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog)** — 12 mins, by Databricks blog

> *We are excited to announce that we are open-sourcing Unity Catalog, the industry’s first open source catalog for data and AI governance across clouds, data formats, and data platforms.*

────────

**[Build Data Engineering Projects with Free Template](https://www.startdataengineering.com/post/data-engineering-projects-with-free-template/) —** 6 mins, by Start Data Engineering

> *This post will cover the critical concepts of setting up data infrastructure, development workflow, and a few sample data projects that follow this pattern.*

────────

**[Walmart - Reliably Processing Trillions of Kafka Messages Per Day](https://medium.com/walmartglobaltech/reliably-processing-trillions-of-kafka-messages-per-day-23494f553ef9) —** 8 mins, by Ravinder Matte

> *In this article we highlight how Apache Kafka messages are reliably processed at a scale of trillions of messages per day with low cost and elasticity.*

────────

**[How trip.com migrated from Elasticsearch and built a 50PB logging solution with ClickHouse](https://clickhouse.com/blog/how-trip.com-migrated-from-elasticsearch-and-built-a-50pb-logging-solution-with-clickhouse?)** — 20 mins, by Dongyu Lin

> *This blog article will explain the story of our logging platform, why we initially built it, the technology we used, and finally, our plan for its future on top of ClickHouse leveraging some of the features like SharedMergeTree.*

────────

**[Building an ETL pipeline with Apache Airflow and Visualizing AWS Redshift data using Microsoft Power BI](https://github.com/Wittline/uber-expenses-tracking) —** by Ramses Alexander Coraspe Valdez

> *The goal of this project is to track the expenses of [Uber Rides](https://www.uber.com/) and [Uber Eats](https://www.ubereats.com/) through data Engineering processes using technologies such as Apache Airflow, AWS Redshift, and [Power BI](https://powerbi.microsoft.com/es-es/).*

────────

**[Reducing Data Questions Deluge](https://sqlpatterns.com/p/reducing-data-questions-deluge)** *—* 5 mins, by Ergest Xheblati

> *How properly done self-service analytics can reduce requests on data teams.*

────────

**[Senior Engineer Fatigue](https://luminousmen.com/post/senior-engineer-fatigue)** — 4 mins, by luminousmen

> *Senior fatigue is, perhaps paradoxically, a sign of maturity in engineering. It's an indicator that you’re transitioning from doing everything to ensuring that everything that needs to be done gets done in the most effective way.*

---

## 😉 Previously on Dimension

> *Dimension is my sub-newsletter, where I note down things I learn from people smarter than me in the data engineering field. Here is the latest article*

Let me hear your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-40-data-infrastructure-at/comments)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
