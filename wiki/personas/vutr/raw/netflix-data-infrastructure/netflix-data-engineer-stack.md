---
title: "Netflix Data Engineer Stack"
channel: vutr
author: "Vu Trinh"
published: 2024-07-30
url: https://vutr.substack.com/p/netflix-data-engineer-stack
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Data Modeling", "Streaming", "Data Quality"]
tags: [netflix, https, spark, tool, substack, iceberg]
---

# Netflix Data Engineer Stack

*Iceberg, Spark, Flink, and more.*

> Source: [Open post](https://vutr.substack.com/p/netflix-data-engineer-stack)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[data-modeling|Data Modeling]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147091978)

[![](https://substackcdn.com/image/fetch/$s_!Ciw-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e55870d-819b-4917-a50c-f6946ceb6909_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!Ciw-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e55870d-819b-4917-a50c-f6946ceb6909_2000x1429.png)

Image created by the author.

---

## Intro

Towards the end of 2023, Netflix put out a series of tech talks, including one that gave an overview of their data engineering stack. I think many of us are curious about how Netflix manages their data infrastructure, so I decided to write this article. The notes below are my takeaways from watching the talk.

---

## Scope

Netflix offers a wide range of data analytics tools, covering almost every aspect of data engineering. Instead of exploring each tool, the talk focuses on a typical pipeline implementation and highlights some key technologies. In the next section, we will see how Netflix handles batch pipelines at a high level.

## Batch

Netflix's general batch pipeline has four steps: (1) the transform logic implementation, (2) ensuring quality, (3) scheduling jobs, and (4) managing the data.

### The transform

Internally, thousands of [Apache Iceberg](https://iceberg.apache.org/) data tables cover all aspects of Netflix's business. All the batch pipelines are built with [Apache Spark](https://spark.apache.org/), which offers first-class support for SQL, Python, and Scala. Users can choose any language that best suits their use case.

If users choose SQL, there is a tool called Netflix big data query UI that can help make their lives easier. The tool supports cool features like documenting the table involved in the query, auto-completing, and a single entry point for many engines/backends: Spark, Trino, Druid, or Snowflake.

Netflix also allows users to register compute resources when running extensive jobs like backfilling. A UI tool called go/boost serves this purpose.

### Data Quality

Regarding unit tests, Netflix uses native unit test libraries (PyTest or ScalaTest) and the Spark-specific unit test library. For testing purposes, Netflix developed Dataflow Mock Generation — a tool that generates mock data based on the data in the warehouse.

For the data audits, Netflix employs the WAP (Write-Audit-Publish) pattern. They first write the data to a hidden Iceberg snapshot and then audit it using an internal data auditor tool. If the audit passes, this snapshot is exposed to the user. Leveraging Iceberg in this pattern helps Netflix avoid copying data during the audit.

You can read more about the WAP pattern using the Iceberg branch from ’s article

[![](https://substackcdn.com/image/fetch/$s_!q7Ds!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe044cc0d-085a-4edc-b634-7f26d8a5d78c_400x400.png)Ju Data Engineering Newsletter

Write-Audit-Publish (WAP) Pattern

Ensuring safe code releases is a constant challenge in software engineering. One strategy is blue-green deployment, where two identical environments are set up. The blue environment hosts the current application version, while the green one runs the new version…

Read more

2 years ago · 21 likes · 9 comments · Julien Hurault](https://juhache.substack.com/p/write-audit-publish-wap-pattern?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

### Scheduling

Netflix developed a solution called Maestro to serve workflow scheduling. It handles an impressive 70,000 workflows and 500,000 job steps every day. With Maestro, users can set job frequencies using event-based triggers or a time-based scheduler. Workflows can be defined using YAML or Python. Netflix offers many standard steps, similar to Airflow Operators, such as Spark Jobs, Data Audits, and Email Sending. If a custom step is needed, users don't have to dive into the low-level APIs of specific stacks. Instead, Netflix provides a wrapper API that allows access to various engines through a single interface. This design means users don't need deep knowledge of the different APIs and their unique semantics.

### Data Management

Netflix built the Cost Insights Dashboard, which monitors metrics like compute and storage costs. The dashboard can be broken down by team, organization, and platform.

Another tool worth mentioning is the Aggressive Janitor, which supports data management tasks such as cleaning up unused data or enforcing data retention policies.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147091978)

---

## Real-time

### Streaming Application

At Netflix, Apache Flink has become the standard for building real-time pipelines. The real-time data platform offers everything users need to develop their Flink applications. The platform will handle nearly everything, from the observability and alerting to Flink’s job configuration.

### Source and Sink

Netflix engineers built a tool called Keystone that abstracts away stream destination details. Instead of specifying the destination, the application can output the data to Keystone. Behind the scenes of Keystone, there is a Kafka topic that receives the data, and a Flink application will route the data to the configurable destination, such as another Kafka topic, Iceberg table, or Apache Druid.

### Backfilling

Keystone supports using Iceberg tables as Keystone sinks and leveraging that for the backfill source.

### Observability

Netflix developed a tool called Mantis, which can run ad-hoc queries against raw data events. Users can configure a Mantis agent to listen to the raw stream; the agent will receive the user’s query and investigate or debug the stream in real-time.

---

## **Outro**

In this article, I've shared all my insights from watching Netflix's excellent tech talks. We start by looking at how Netflix develops a typical batch pipeline using Iceberg for storage, Spark for transformation logic, the WAP pattern for data auditing, and Maestro for scheduling. Then, we explore their real-time application with Apache Flink, the abstraction of real-time sinks with Keystone, and finally, Mantis for real-time observability.

---

## **References**

*[1] Chris Stephens, Pedro Duarte, [Netflix Data Engineering Tech Talks - The Netflix Data Engineering Stack](https://www.youtube.com/watch?v=QxaOlmv79ls) (2023)*

---

## **📋 The list**

#### ✏️ The Data Quality Conundrum [Part 1](https://thedataecosystem.substack.com/p/issue-15-the-data-quality-conundrum) and [Part 2](https://thedataecosystem.substack.com/p/the-data-quality-conundrum-part-2)

21 minutes, by

> *In part 1, the author will explain the root causes of data quality problems. Then in part 2, Dylan will guide us on how to address these issues.*

#### ✏️ [15 Years of Realtime OLAP (Part 1)](https://materializedview.io/p/15-years-of-realtime-olap-part-1)

6 minutes, by

> *A brief history of Avatara, Apache Pinot, and Apache Druid.*

#### ✏️ [How to review code effectively: A GitHub staff engineer’s philosophy](https://github.blog/developer-skills/github/how-to-review-code-effectively-a-github-staff-engineers-philosophy/)

16 minutes, by Sarah Vessels

> *GitHub Staff Engineer Sarah Vessels discusses her philosophy of code review, what separates good code review from bad, her strategy for finding and reviewing code, and how to get the most from reviews of her own code.*

#### ✏️ [Advanced Data Modelling](https://towardsdatascience.com/advanced-data-modelling-1e496578bc91)

14 minutes, by Mike Shakhomirov

> *Data model layers, environments, tests and data quality explained*

#### ✏️ [Maestro: Data/ML Workflow Orchestrator at Netflix](https://netflixtechblog.com/maestro-netflixs-workflow-orchestrator-ee13a06f9c78)

18 minutes, by Netflix Technology Blog

> *At Netflix, Maestro is a general-purpose, horizontally scalable workflow orchestrator designed to manage large-scale workflows such as data pipelines and machine learning model training pipelines.*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/netflix-data-engineer-stack/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
